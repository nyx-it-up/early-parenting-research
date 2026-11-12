"""Survey-weighted logistic regression with design-based (Taylor linearization) standard errors.

statsmodels has no survey-design regression, and its ordinary weighted fit
treats the weights as frequency counts, which makes standard errors too small.
This module fits the model with the weights and computes standard errors from
each record's linearized contribution ("influence"), using the same design as
the rest of the NSCH analysis: strata DESIGN_STRATUM and each household as its
own primary sampling unit (NSCH samples one child per household).

Domain estimation: the model is fitted to the domain (e.g. mothers with
complete data), but the variance is computed over ALL records of the file,
with zero contributions outside the domain, so stratum sizes are not distorted.

Functions
  fit_logit            weighted maximum likelihood (Newton-Raphson)
  coefficient_influence  each record's contribution to the coefficients
  design_covariance    stratified variance of any set of contributions
  predictive_margin    adjusted percentage when everyone is set to one group
  rubin                combine estimates across multiply imputed data sets
  t_interval           95% interval from an estimate, its SE and degrees of freedom
  d1_test              multivariate Wald F test for multiply imputed data

A model that cannot be estimated (singular information matrix, or no
convergence, e.g. too few cases with the outcome) raises NotEstimable.

References: Binder (1983) and Lumley (n.d., R package "survey") for the
linearization; Rubin (1987) for combining imputations; Barnard and Rubin
(1999) for the small-sample degrees of freedom; Li, Raghunathan and Rubin
(1991) for the D1 test.
"""

import numpy as np
import pandas as pd
from scipy import stats


class NotEstimable(RuntimeError):
    """The model cannot be estimated on this sample."""


def fit_logit(X, y, w, iterations=50, tolerance=1e-10):
    """Weighted logistic regression. X: (n, k) array, y: 0/1 array, w: weights.

    Returns the coefficient vector.
    """
    beta = np.zeros(X.shape[1])
    for _ in range(iterations):
        p = 1 / (1 + np.exp(-X @ beta))
        gradient = X.T @ (w * (y - p))
        hessian = (X * (w * p * (1 - p))[:, None]).T @ X
        try:
            step = np.linalg.solve(hessian, gradient)
        except np.linalg.LinAlgError:
            raise NotEstimable("singular information matrix")
        beta = beta + step
        if not np.all(np.isfinite(beta)):
            raise NotEstimable("coefficients are not finite")
        if np.max(np.abs(step)) < tolerance:
            return beta
    raise NotEstimable("logistic regression did not converge")


def solve_or_not_estimable(matrix, right_side):
    try:
        return np.linalg.solve(matrix, right_side)
    except np.linalg.LinAlgError:
        raise NotEstimable("singular information matrix")


def coefficient_influence(X, y, w, beta):
    """Each record's linearized contribution to beta: A^-1 x_i w_i (y_i - p_i).

    A is the weighted information matrix. The variance of the coefficients is
    design_covariance() of these rows (the "sandwich" estimator).
    """
    p = 1 / (1 + np.exp(-X @ beta))
    information = (X * (w * p * (1 - p))[:, None]).T @ X
    scores = X * (w * (y - p))[:, None]
    return solve_or_not_estimable(information, scores.T).T


def design_covariance(contributions, strata):
    """Covariance matrix from per-record contributions (n x k), stratified, PSU = record.

    contributions must cover every record in the file (zeros outside the domain).
    Var = sum over strata of n_h / (n_h - 1) * sum of squared deviations from the stratum mean.
    """
    frame = pd.DataFrame(contributions)
    centered = frame - frame.groupby(strata.values).transform("mean")
    n_h = strata.map(strata.value_counts()).values
    scale = np.sqrt(n_h / (n_h - 1))
    scaled = centered.values * scale[:, None]
    return scaled.T @ scaled


def predictive_margin(X_domain, w_domain, beta, coefficient_if, domain_rows, n_total):
    """Adjusted share (a "predictive margin") and its per-record contributions.

    X_domain is the domain's design matrix with the exposure columns already
    set to the group of interest for everyone, so the result answers: "what
    share would have the outcome if everyone in the domain were in this group,
    keeping their other characteristics?"

    The contribution combines (1) variation in the covariates across records
    and (2) uncertainty in beta, as Stata's svy margins does by default.
    Returns (margin, contributions over all n_total records).
    """
    p = 1 / (1 + np.exp(-X_domain @ beta))
    total_weight = w_domain.sum()
    margin = (w_domain * p).sum() / total_weight
    gradient = (X_domain * (w_domain * p * (1 - p))[:, None]).sum(axis=0) / total_weight

    contributions = coefficient_if @ gradient
    contributions[domain_rows] += w_domain * (p - margin) / total_weight
    return margin, contributions


def cluster_variance(contributions, clusters):
    """Variance of one estimate with clusters (e.g. states) as the only sampling units.

    Used when the comparison involves a cluster-level variable such as a state
    policy: records in the same state share the policy, so states, not
    households, are the independent units. contributions covers every record.
    """
    totals = pd.Series(contributions).groupby(clusters.values).sum()
    g = len(totals)
    return float(g / (g - 1) * ((totals - totals.mean()) ** 2).sum())


def fit_linear(X, y, w):
    """Weighted least squares (for a mean score). Returns the coefficient vector."""
    weighted_X = X * w[:, None]
    return solve_or_not_estimable(weighted_X.T @ X, weighted_X.T @ y)


def linear_influence(X, y, w, beta):
    """Each record's linearized contribution to a weighted least-squares beta."""
    information = (X * w[:, None]).T @ X
    scores = X * (w * (y - X @ beta))[:, None]
    return solve_or_not_estimable(information, scores.T).T


def design_df(strata):
    """Complete-data degrees of freedom of the design: PSUs (households) minus strata."""
    return len(strata) - strata.nunique()


def rubin(estimates, variances, complete_df):
    """Combine m estimates of one quantity (and their variances) with Rubin's rules.

    Degrees of freedom follow Barnard and Rubin (1999), which stay below the
    complete-data degrees of freedom (complete_df) of the design.
    Returns (estimate, standard_error, degrees_of_freedom).
    """
    estimates = np.asarray(estimates, dtype=float)
    variances = np.asarray(variances, dtype=float)
    m = len(estimates)
    within = variances.mean()
    between = estimates.var(ddof=1)
    total = within + (1 + 1 / m) * between
    missing_share = (1 + 1 / m) * between / total
    observed_df = (complete_df + 1) / (complete_df + 3) * complete_df * (1 - missing_share)
    if missing_share == 0:
        df = observed_df
    else:
        df = 1 / (missing_share ** 2 / (m - 1) + 1 / observed_df)
    return estimates.mean(), float(np.sqrt(total)), float(df)


def t_interval(estimate, se, df):
    """95% confidence interval using the t distribution."""
    critical = stats.t.ppf(0.975, df)
    return estimate - critical * se, estimate + critical * se


def d1_test(betas, covariances):
    """D1 multivariate Wald test that all k coefficients are zero, for m imputations.

    betas: (m, k) estimates; covariances: m (k, k) covariance matrices.
    Li, Raghunathan and Rubin (1991). Returns (F, numerator df k, denominator df, p).
    """
    betas = np.asarray(betas, dtype=float)
    m, k = betas.shape
    mean = betas.mean(axis=0)
    within = np.mean(covariances, axis=0)
    between = np.atleast_2d(np.cov(betas, rowvar=False, ddof=1))
    increase = (1 + 1 / m) * np.trace(between @ np.linalg.inv(within)) / k
    f_statistic = float(mean @ np.linalg.solve(within, mean)) / (k * (1 + increase))
    t = k * (m - 1)
    if t > 4:
        denominator_df = 4 + (t - 4) * (1 + (1 - 2 / t) / increase) ** 2
    else:
        denominator_df = t * (1 + 1 / k) * (1 + increase) ** 2 / 2
    return f_statistic, k, float(denominator_df), float(stats.f.sf(f_statistic, k, denominator_df))
