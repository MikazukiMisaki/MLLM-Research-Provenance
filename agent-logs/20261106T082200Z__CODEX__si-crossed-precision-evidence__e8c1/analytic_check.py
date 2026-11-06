#!/usr/bin/env python3
"""Independent quadrature of exact crossed-design variance for random products."""
import json
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent
source=json.loads((P/'results.json').read_text())
x,w=np.polynomial.hermite.hermgauss(64)
w=w/np.sqrt(np.pi)
x=x*np.sqrt(2)
f=lambda z: 1/(1+np.exp(-z))
def expect(z): return np.sum(w*z)
def gauss_matrix(mu,sigma): return (f(mu[:,None]+sigma*x[None,:])*w[None,:]).sum(axis=1)
out=[]
for r in source['results']:
 if r['target_type']!='random_products': continue
 n,k,s=r['N'],r['K_pairs'],r['sigma_product']
 pb=gauss_matrix(-.45+1.15*x,s); pc=gauss_matrix(-.7+.85*x,s)
 mu=expect(pb-pc)
 covtask=expect((pb-pc)**2)-mu**2
 # conditional product effects integrated over shared task for each arm.
 ub=(f(-.45+s*x[:,None]+1.15*x[None,:])*w[None,:]).sum(axis=1)
 uc=(f(-.7+s*x[:,None]+.85*x[None,:])*w[None,:]).sum(axis=1)
 covprod=(expect(ub**2)-expect(ub)**2)+(expect(uc**2)-expect(uc)**2)
 vard=expect(pb+pc-2*pb*pc)-mu**2
 sd=np.sqrt((vard+(k-1)*covtask+(n-1)*covprod)/(n*k))
 sim=r['methods']['naive_N_times_K']['empirical_sd']
 mc=r['methods']['naive_N_times_K']['empirical_sd_approx_mcse']
 assert abs(mu-r['target'])<1e-8
 assert abs(sim-sd)<5*mc, (r,sd,sim,mc)
 out.append({'N':n,'K':k,'sigma_product':s,'mean_quadrature':mu,'variance_components':{'single_paired_cell':vard,'shared_task_covariance':covtask,'shared_product_pair_covariance':covprod},'analytic_sd':sd,'simulated_sd':sim,'sim_sd_approx_mcse':mc,'difference_in_approx_mcse':(sim-sd)/mc})
(P/'analytic_check.json').write_text(json.dumps({'status':'PASS','method':'64-point Gauss-Hermite exact crossed variance decomposition; compares simulation to analytical SD within 5 approximate Monte Carlo SD errors','checks':out},indent=2)+'\n')
for a in out: print(a['N'],a['K'],a['sigma_product'],'analytic SD',round(a['analytic_sd'],5),'simulation',round(a['simulated_sd'],5),'difference_MCSE',round(a['difference_in_approx_mcse'],2))
