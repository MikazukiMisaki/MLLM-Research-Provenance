"""Three-arm paired binary Monte Carlo; synthetic outcomes, standard library only."""
import json
import math
import random

REPLICATIONS = 20_000
SEED = 20261118


def thresholds(n):
    # The observed effect criterion implies w > k/2. For exact two-sided
    # McNemar, p = 2 * sum(comb(k,i), i=w..k) / 2**k.
    effect = (n+9)//10
    result = {}
    for k in range(n+1):
        tail = 0
        for w in range(k,-1,-1):
            tail += math.comb(k,w)
            if 2*w-k >= effect:
                result[k,w] = (40*tail <= 2**k, 80*tail <= 2**k)
    return result


def simulation(n, coupling):
    rng = random.Random(SEED)
    table = thresholds(n)
    accepted = [0,0,0]
    wins = [0,0]
    losses = [0,0]
    for _ in range(REPLICATIONS):
        w1=l1=w2=l2=0
        for _ in range(n):
            c = rng.random() < 0.5
            pa = 0.45 if c else 0.15
            r1, r2 = rng.random(), rng.random()
            d1 = r1 < pa
            d2 = (r2 if coupling == 'conditional_independence' else r1) < pa
            if c:
                w1 += d1; w2 += d2
            else:
                l1 += d1; l2 += d2
        a05,a025 = table.get((w1+l1,w1),(False,False))
        b05,b025 = table.get((w2+l2,w2),(False,False))
        accepted[0] += a025
        accepted[1] += b025
        accepted[2] += a05 and b05 and (a025 or b025)
        wins[0] += w1; wins[1] += w2
        losses[0] += l1; losses[1] += l2
    phat = accepted[2] / REPLICATIONS
    se = math.sqrt(phat*(1-phat)/REPLICATIONS)
    return {'n':n, 'coupling':coupling, 'replications':REPLICATIONS,
            'seed':SEED, 'joint_passes':accepted[2], 'joint_pass_rate':phat,
            'monte_carlo_se':se, 'approx_mc_95_interval':[phat-1.96*se,phat+1.96*se],
            'single_a_pass_alpha_025':accepted[0]/REPLICATIONS,
            'single_b_pass_alpha_025':accepted[1]/REPLICATIONS,
            'observed_mean_win_probabilities':[x/(REPLICATIONS*n) for x in wins],
            'observed_mean_loss_probabilities':[x/(REPLICATIONS*n) for x in losses]}

if __name__ == '__main__':
    for n in (82,200):
        for coupling in ('conditional_independence','conditional_identical'):
            print(json.dumps(simulation(n,coupling),sort_keys=True))
