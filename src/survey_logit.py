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

References: Binder (1983) and Lumley (n.d., R package "survey") for the
linearization; Rubin (1987) for combining imputations.
"""

import numpy as np
import pandas as pd


def fit_logit(X, y, w, iterations=50, tolerance=1e-10):
    """Weighted logistic regression. X: (n, k) array, y: 0/1 array, w: weights.

    Returns the coefficient vector.
    """
    beta = np.zeros(X.shape[1])
    for _ in range(iterations):
        p = 1 / (1 + np.exp(-X @ beta))
        gradient = X.T @ (w * (y - p))
        hessian = (X * (w * p * (1 - p))[:, None]).T @ X
        step = np.linalg.solve(hessian, gradient)
        beta = beta + step
        if np.max(np.abs(step)) < tolerance:
            return beta
    raise RuntimeError("Logistic regression did not converge")


def coefficient_influence(X, y, w, beta):
    """Each record's linearized contribution to beta: A^-1 x_i w_i (y_i - p_i).

    A is the weighted information matrix. The variance of the coefficients is
    design_covariance() of these rows (the "sandwich" estimator).
    """
    p = 1 / (1 + np.exp(-X @ beta))
    information = (X * (w * p * (1 - p))[:, None]).T @ X
    scores = X * (w * (y - p))[:, None]
    return scores @ np.linalg.inv(information)


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
    return np.linalg.solve(weighted_X.T @ X, weighted_X.T @ y)


def linear_influence(X, y, w, beta):
    """Each record's linearized contribution to a weighted least-squares beta."""
    information = (X * w[:, None]).T @ X
    scores = X * (w * (y - X @ beta))[:, None]
    return scores @ np.linalg.inv(information)


def rubin(estimates, variances):
    """Combine m estimates of one quantity (and their variances) with Rubin's rules.

    Returns (estimate, standard_error).
    """
    estimates = np.asarray(estimates, dtype=float)
    variances = np.asarray(variances, dtype=float)
    m = len(estimates)
    within = variances.mean()
    between = estimates.var(ddof=1)
    total = within + (1 + 1 / m) * between
    return estimates.mean(), float(np.sqrt(total))
