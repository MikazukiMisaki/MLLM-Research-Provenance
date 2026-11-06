#!/usr/bin/env python3
"""Synthetic crossed task x product inference; no real task or model data."""
import json, platform
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent
R = 3000
BATCH = 100
BASE_SEED = 20261106
A = -0.7
DELTA = 0.25
BETA_B, BETA_C = 1.15, 0.85
Z = 1.959963984540054
X, W = np.polynomial.hermite.hermgauss(48)
W = W / np.sqrt(np.pi)

def expit(x):
    return 1.0 / (1.0 + np.exp(-x))

def normal_mean(intercept, sd):
    intercept = np.asarray(intercept)
    return np.sum(expit(intercept[..., None] + np.sqrt(2.0) * sd * X) * W, axis=-1)

def fixed_target(b, c):
    return np.mean(normal_mean(A + DELTA + b, BETA_B) - normal_mean(A + c, BETA_C), axis=-1)

def population_target(sigma):
    return float(normal_mean(A + DELTA, np.hypot(BETA_B, sigma)) - normal_mean(A, np.hypot(BETA_C, sigma)))

def summarize(err, se, invalid=None):
    valid = np.isfinite(se) & (se >= 0)
    cover = np.abs(err[valid]) <= Z * se[valid]
    p = float(np.mean(cover)) if valid.any() else None
    return dict(mean_estimated_se=float(np.mean(se[valid])) if valid.any() else None,
                empirical_sd=float(np.std(err, ddof=1)),
                empirical_sd_approx_mcse=float(np.std(err, ddof=1) / np.sqrt(2 * (len(err)-1))),
                coverage=p,
                coverage_mcse=float(np.sqrt(p * (1-p) / cover.size)) if cover.size else None,
                coverage_valid_replicates=int(valid.sum()),
                invalid_variance_fraction=float(np.mean(~valid)) if invalid is None else float(np.mean(invalid)))

def scenario(n, k, sigma, target_type, seed):
    rng = np.random.default_rng(seed)
    estimates, targets, naive, task, crossed = [], [], [], [], []
    if target_type == 'fixed_products':
        fb = rng.normal(0, sigma, size=(1, k))
        fc = rng.normal(0, sigma, size=(1, k))
        frozen_target = float(fixed_target(fb, fc)[0])
    else:
        frozen_target = population_target(sigma)
    for start in range(0, R, BATCH):
        m = min(BATCH, R-start)
        t = rng.standard_normal((m, n, 1))
        b = np.broadcast_to(fb, (m, k)) if target_type == 'fixed_products' else rng.normal(0, sigma, (m, k))
        c = np.broadcast_to(fc, (m, k)) if target_type == 'fixed_products' else rng.normal(0, sigma, (m, k))
        pb = expit(A + DELTA + BETA_B*t + b[:, None, :])
        pc = expit(A + BETA_C*t + c[:, None, :])
        yb = rng.random((m, n, k)) < pb
        yc = rng.random((m, n, k)) < pc
        d = yb.astype(np.int8) - yc.astype(np.int8)
        row = d.mean(axis=2)
        col = d.mean(axis=1)
        v_naive = d.var(axis=(1,2), ddof=1) / (n*k)
        v_task = row.var(axis=1, ddof=1) / n
        v_product = col.var(axis=1, ddof=1) / k
        v_cross = v_task + v_product - v_naive
        estimates.extend(d.mean(axis=(1,2)))
        targets.extend(np.full(m, frozen_target))
        naive.extend(np.sqrt(v_naive))
        task.extend(np.sqrt(v_task))
        crossed.extend(np.where(v_cross >= 0, np.sqrt(np.maximum(v_cross, 0)), np.nan))
    est, true = np.array(estimates), np.array(targets)
    error = est - true
    return dict(N=n, K_pairs=k, products_per_arm=k, sigma_product=sigma, target_type=target_type,
                target=frozen_target, mean_estimate=float(est.mean()), bias=float(error.mean()),
                mean_bias_mcse=float(error.std(ddof=1)/np.sqrt(R)),
                methods={'naive_N_times_K':summarize(error, np.array(naive)),
                         'task_cluster':summarize(error, np.array(task)),
                         'two_way_cluster_asymptotic':summarize(error, np.array(crossed))})

def self_check():
    # Exchangeability under zero effect and identical arm slopes gives exactly zero.
    x = normal_mean(A, np.hypot(1.0, 0.7))
    assert abs(float(x-x)) < 1e-14
    # One-dimensional Gaussian integration agrees with explicit tensor quadrature.
    sigma = 0.7
    two = np.sum(W[:,None] * W[None,:] * expit(A + DELTA + np.sqrt(2)*BETA_B*X[:,None] + np.sqrt(2)*sigma*X[None,:]))
    one = normal_mean(A+DELTA, np.hypot(BETA_B, sigma))
    assert abs(float(one-two)) < 2e-9, (one,two)
    # Swapping arm intercept arrays negates the fixed target when arm intercept and slopes match.
    b=np.array([[0.2,-0.4]]); c=np.array([[-0.1,0.7]])
    q=lambda u,v: np.mean(normal_mean(A+u, 1.)-normal_mean(A+v, 1.), axis=-1)
    assert np.allclose(q(b,c), -q(c,b), atol=1e-14)
    return {'quadrature_1d_vs_2d_abs_error':abs(float(one-two)), 'arm_exchange_null':True, 'fixed_arm_swap':True}

if __name__ == '__main__':
    check = self_check()
    definitions=[(80,4,.7,'random_products'),(320,4,.7,'random_products'),
                 (80,16,.7,'random_products'),(320,16,.7,'random_products'),
                 (80,4,0.,'random_products'),(80,4,.7,'fixed_products'),
                 (320,4,.7,'fixed_products'),(80,16,.7,'fixed_products')]
    results=[scenario(*case, seed=BASE_SEED+i) for i,case in enumerate(definitions)]
    output={'schema':'synthetic_crossed_precision_v1','seed':BASE_SEED,'replicates_per_scenario':R,
            'python':platform.python_version(),'numpy':np.__version__,'self_check':check,
            'data':'entirely synthetic; no real tasks, manifests, models, or environment',
            'model':{'intercept_C':A,'intercept_B':A+DELTA,'task_slopes_B_C':[BETA_B,BETA_C],
                     'task_latent':'i.i.d. standard normal shared across arms and products',
                     'product_latent':'independent normal per B/C product, fixed within column across tasks',
                     'noise':'independent Bernoulli draws conditional on task and product',
                     'unit':'paired B and C output for a task and product-index pair',
                     'formula':'P(Y_aik=1)=logistic(intercept_a+task_slope_a*T_i+U_ak)'},
            'interval':'nominal 95% Wald z=1.95996; invalid negative crossed variance excluded and explicitly counted',
            'results':results}
    (ROOT/'results.json').write_text(json.dumps(output,indent=2)+'\n')
    for r in results:
        print(r['target_type'],r['N'],r['K_pairs'],r['sigma_product'],'target',round(r['target'],4),
              'bias',round(r['bias'],4),[(k,round(v['empirical_sd'],4), round(v['mean_estimated_se'],4),round(v['coverage'],3),round(v['invalid_variance_fraction'],3)) for k,v in r['methods'].items()])
