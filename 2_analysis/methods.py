"""Statistical methods used by wastewater_analysis.py.

Everything here is plain NumPy/SciPy so each step can be read and checked.

Model (requirement R07, research question RQ2)
    outcome[c, t] = a + b * spending[c, t] + company effect[c] + year effect[t] + error
    - company effects absorb permanent differences between companies (size, geography, network age);
    - year effects absorb shocks shared by every company in a year (weather, rule changes);
    - b is therefore estimated only from changes *within* each company over time.

Uncertainty with only nine companies (R07, RQ3; MacKinnon, Nielsen and Webb, 2023)
    - CV3 cluster jackknife: refit leaving out one company at a time;
    - restricted wild-cluster bootstrap (WCR): every one of the 2**9 = 512 sign patterns.

Author: Dinka Christabel Samuel. Methods adapted from the project's 16 Nov 2026 review
pipeline; written with AI assistance (see the AI-use disclosure in Appendix A).
"""
from itertools import product

import numpy as np
import pandas as pd
from scipy import stats

LOG_10_PERCENT = np.log(1.10)   # converts a log-spending slope to "per 10% more spending"


# --------------------------------------------------------------------------- core fit
def design_matrix(data, predictors):
    """Intercept + predictors + company dummies + year dummies (first of each dropped)."""
    dummies = pd.get_dummies(data[["company_code", "year_start"]].astype(str),
                             drop_first=True, dtype=float)
    return np.column_stack([np.ones(len(data)), data[predictors].to_numpy(float), dummies.to_numpy()])


def fit(data, outcome, predictors):
    """Ordinary least squares with company and year effects.

    Returns the coefficient vector, the design matrix and the residuals. The slope of the
    first predictor is also recomputed by the Frisch-Waugh-Lovell route (partialling out
    every other column) as a built-in correctness check.
    """
    X = design_matrix(data, predictors)
    y = data[outcome].to_numpy(float)
    if np.linalg.matrix_rank(X) < X.shape[1] or len(y) <= X.shape[1]:
        raise ValueError("Design is rank-deficient or has no residual degrees of freedom")
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    others = np.delete(X, 1, axis=1)
    x_resid = X[:, 1] - others @ np.linalg.lstsq(others, X[:, 1], rcond=None)[0]
    y_resid = y - others @ np.linalg.lstsq(others, y, rcond=None)[0]
    if not np.isclose(beta[1], x_resid @ y_resid / (x_resid @ x_resid), rtol=1e-7, atol=1e-9):
        raise AssertionError("Frisch-Waugh-Lovell check failed")
    return beta, X, y - X @ beta, x_resid


# --------------------------------------------------------------------- uncertainty
def cv3_jackknife(data, outcome, predictors, slope):
    """Leave-one-company-out slopes and the CV3 standard error.

    SE^2 = (G-1)/G * sum_g (slope_without_g - slope)^2 , with G companies.
    """
    companies = sorted(data.company_code.unique())
    deleted = np.array([fit(data[data.company_code != c], outcome, predictors)[0][1] for c in companies])
    g = len(companies)
    se = np.sqrt((g - 1) / g * np.sum((deleted - slope) ** 2))
    return se, dict(zip(companies, deleted))


def wild_cluster_bootstrap_p(X, y, groups):
    """Restricted wild-cluster bootstrap p-value for H0: slope = 0 (CV1 t-statistic).

    1. Fit the model *without* the spending column (the null) and keep its residuals.
    2. For each of the 2**G sign patterns, flip every company's residuals by +1 or -1,
       rebuild y, refit the full model and record the t-statistic.
    3. p = share of bootstrap |t| at least as large as the observed |t|.
    Enumerating every pattern (no random seed) makes the result exactly reproducible.
    """
    n, k = X.shape
    labels, idx = np.unique(groups, return_inverse=True)
    g = len(labels)
    xtx_inv = np.linalg.inv(X.T @ X)
    solve = xtx_inv @ X.T
    small_sample = g / (g - 1) * (n - 1) / (n - k)

    def t_stat(y_vec):
        b = solve @ y_vec
        e = y_vec - X @ b
        scores = np.array([X[idx == j].T @ e[idx == j] for j in range(g)])
        return b[1] / np.sqrt(small_sample * np.sum((scores @ xtx_inv[:, 1]) ** 2))

    others = np.delete(X, 1, axis=1)
    fitted0 = others @ np.linalg.lstsq(others, y, rcond=None)[0]
    resid0 = y - fitted0
    observed = t_stat(y)
    draws = np.array([t_stat(fitted0 + resid0 * np.array(s)[idx]) for s in product([-1.0, 1.0], repeat=g)])
    return float(np.mean(np.abs(draws) >= abs(observed) - 1e-10)), len(draws), float(observed)


def minimum_detectable_effect(se, g, alpha=0.05, power=0.80):
    """Smallest true slope the design detects with the given power (two-sided t, G-1 df).

    MDE = (t_{1-alpha/2} + t_{power}) * SE. Returned per 10% higher spending.
    """
    df = g - 1
    return (stats.t.ppf(1 - alpha / 2, df) + stats.t.ppf(power, df)) * se * LOG_10_PERCENT


def holm(p_values):
    """Holm step-down adjustment for a small family of tests."""
    p = np.asarray(p_values, float)
    order = np.argsort(p)
    adjusted = np.empty_like(p)
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, (len(p) - rank) * p[i])
        adjusted[i] = min(1.0, running)
    return adjusted


# ------------------------------------------------------------------ one full model
def run_model(data, outcome, predictors, label, outcome_source, spending_measure):
    """Fit one specification and return a results row plus leave-one-out slopes."""
    data = data.sort_values(["company_code", "year_start"]).reset_index(drop=True)
    beta, X, resid, x_resid = fit(data, outcome, predictors)
    slope = beta[1]
    se, deleted = cv3_jackknife(data, outcome, predictors, slope)
    g = data.company_code.nunique()
    t_crit = stats.t.ppf(0.975, g - 1)
    p_boot, n_draws, t_obs = wild_cluster_bootstrap_p(X, data[outcome].to_numpy(float),
                                                      data.company_code.to_numpy())
    leverage = pd.Series(x_resid ** 2).groupby(data.company_code).sum() / np.sum(x_resid ** 2)
    row = {
        "model_id": f"{outcome}|{label}",
        "outcome": outcome, "specification": label,
        "spending_measure": spending_measure, "outcome_source": outcome_source,
        "first_year": int(data.year_start.min()), "last_year": int(data.year_start.max()),
        "n": len(data), "companies": g,
        "slope_log": slope, "cv3_se_log": se,
        "diff_per_10pct": slope * LOG_10_PERCENT,
        "ci_low_10pct": (slope - t_crit * se) * LOG_10_PERCENT,
        "ci_high_10pct": (slope + t_crit * se) * LOG_10_PERCENT,
        "p_cv3": 2 * stats.t.sf(abs(slope / se), g - 1),
        "p_wild_bootstrap": p_boot, "bootstrap_draws": n_draws, "t_cv1": t_obs,
        "mde_10pct_80power": minimum_detectable_effect(se, g),
        "outcome_mean": data[outcome].mean(),
        "omit_one_min_10pct": min(deleted.values()) * LOG_10_PERCENT,
        "omit_one_max_10pct": max(deleted.values()) * LOG_10_PERCENT,
        "max_company_leverage_share": leverage.max(),
        "residual_df": len(data) - X.shape[1],
        "condition_number": np.linalg.cond(X),
    }
    omissions = [{"model_id": row["model_id"], "omitted_company": c,
                  "diff_per_10pct": b * LOG_10_PERCENT} for c, b in deleted.items()]
    return row, omissions


# ------------------------------------------------------------------ self-tests
def self_tests():
    """Method checks on artificial data (R11). Raise AssertionError on any failure."""
    rng = np.random.default_rng(20261118)
    companies = [f"C{i}" for i in range(9)]
    grid = pd.DataFrame([(c, y) for c in companies for y in range(2017, 2024)],
                        columns=["company_code", "year_start"])
    grid["x"] = rng.normal(size=len(grid))
    grid["y"] = (2.5 * grid.x + pd.factorize(grid.company_code)[0] + 0.4 * grid.year_start)
    # 1. A known slope is recovered exactly when there is no noise.
    assert np.isclose(fit(grid, "y", ["x"])[0][1], 2.5, atol=1e-9), "known slope not recovered"
    # 2. Balanced two-way demeaning gives the same slope as the dummy-variable fit.
    grid["y"] = grid.y + rng.normal(scale=0.5, size=len(grid))
    def demean(col):
        a = grid.pivot(index="company_code", columns="year_start", values=col).to_numpy()
        return a - a.mean(0) - a.mean(1)[:, None] + a.mean()
    xd, yd = demean("x"), demean("y")
    assert np.isclose(np.sum(xd * yd) / np.sum(xd * xd), fit(grid, "y", ["x"])[0][1], atol=1e-9), \
        "demeaning check failed"
    # 3. The bootstrap enumerates all 512 patterns and returns a valid p-value.
    _, X, _, _ = fit(grid, "y", ["x"])
    p, draws, _ = wild_cluster_bootstrap_p(X, grid.y.to_numpy(), grid.company_code.to_numpy())
    assert draws == 512 and 0 <= p <= 1, "bootstrap enumeration failed"
    # 4. Holm: smallest p doubled, then monotone.
    assert np.allclose(holm([0.01, 0.04]), [0.02, 0.04]), "Holm adjustment failed"
    return True
