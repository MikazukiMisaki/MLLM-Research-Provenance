"""Reference-only paired analysis. No experimental inputs are read by default.

Population inference needs a prospectively frozen schedule and justified sampling
assumptions. Partial outcomes must never be silently omitted.
"""
from math import comb


def _binomial_tail(n, k, p):
    if k <= 0:
        return 1.0
    if k > n:
        return 0.0
    return sum(comb(n, j) * p**j * (1-p)**(n-j) for j in range(k, n+1))


def clopper_pearson(k, n, alpha=.0125):
    if not (type(k) is int and type(n) is int and 0 <= k <= n and n > 0 and 0 < alpha < 1):
        raise ValueError('invalid binomial counts or alpha')
    tail = alpha / 2
    def solve_increasing(target, count):
        lo, hi = 0.0, 1.0
        for _ in range(100):
            mid = (lo + hi) / 2
            if _binomial_tail(n, count, mid) < target:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2
    lower = 0.0 if k == 0 else solve_increasing(tail, k)
    upper = 1.0 if k == n else solve_increasing(1-tail, k+1)
    return lower, upper


def mcnemar_two_sided(wins, losses):
    if not all(type(x) is int and x >= 0 for x in (wins, losses)):
        raise ValueError('invalid discordances')
    d = wins + losses
    if d == 0:
        return 1.0
    return min(1.0, 2.0 * sum(comb(d, k) for k in range(min(wins, losses)+1)) / (2**d))


def analyze(records, *, expected_tasks):
    if not isinstance(records, list) or not isinstance(expected_tasks, dict) or not expected_tasks or any(not isinstance(k, str) or not k or not isinstance(v, str) or not v for k, v in expected_tasks.items()):
        raise ValueError('invalid prespecified task list')
    if len(records) != len(expected_tasks):
        raise ValueError('incomplete paired data')
    by_task = {}
    for row in records:
        if (set(row) != {'task_id', 'family', 'A', 'B', 'C'} or row['task_id'] in by_task
            or not isinstance(row['family'], str) or any(type(row[arm]) is not bool for arm in 'ABC')):
            raise ValueError('invalid, missing or duplicate outcomes')
        by_task[row['task_id']] = row
    if set(by_task) != set(expected_tasks):
        raise ValueError('task set does not match frozen schedule')
    if any(row['family'] != expected_tasks[task_id] for task_id, row in by_task.items()):
        raise ValueError('task family differs from frozen schedule')
    contrasts = {}
    n = len(records)
    for arm in ('A', 'B'):
        wins = sum(row['C'] and not row[arm] for row in records)
        losses = sum(row[arm] and not row['C'] for row in records)
        win_lower, win_upper = clopper_pearson(wins, n)
        loss_lower, loss_upper = clopper_pearson(losses, n)
        contrasts[f'C-{arm}'] = {
            'n': n, 'wins': wins, 'losses': losses, 'ties': n-wins-losses,
            'delta': (wins-losses)/n,
            'simultaneous_95pct_conservative_ci': [win_lower-loss_upper, win_upper-loss_lower],
            'mcnemar_two_sided_p': mcnemar_two_sided(wins, losses),
        }
    ordered = sorted(contrasts, key=lambda k: contrasts[k]['mcnemar_two_sided_p'])
    small = min(1., 2*contrasts[ordered[0]]['mcnemar_two_sided_p'])
    large = min(1., max(small, contrasts[ordered[1]]['mcnemar_two_sided_p']))
    for key, p in zip(ordered, (small, large)):
        contrasts[key]['holm_adjusted_p'] = p
    families = {}
    for row in records:
        family = row['family']
        if family not in families:
            families[family] = {'n': 0, 'A_success': 0, 'B_success': 0, 'C_success': 0}
        entry = families[family]
        entry['n'] += 1
        for arm in 'ABC':
            entry[arm+'_success'] += int(row[arm])
    for value in families.values():
        value['C_minus_A'] = (value['C_success'] - value['A_success']) / value['n']
    primary_warning = any(10*(c['wins']-c['losses']) <= -n for c in contrasts.values())
    family_warning = any(10*(f['C_success']-f['A_success']) <= -f['n'] for f in families.values())
    positive = all(c['holm_adjusted_p'] <= .05 and 10*(c['wins']-c['losses']) >= n for c in contrasts.values())
    decision = 'UNFAVORABLE_WARNING' if primary_warning or family_warning else ('LARGE_EFFECT_SIGNAL' if positive else 'INCONCLUSIVE')
    nonharm = contrasts['C-A']['simultaneous_95pct_conservative_ci'][0] > -.05
    return {'scope': 'reference only; finite schedule descriptive; population inference requires assumptions',
            'n': n, 'contrasts': contrasts, 'families': families, 'decision': decision,
            'five_pp_nonharm_supported_under_inference_assumptions': nonharm,
            'not_a_claim_of_true_effect_over_ten_pp_or_subgroup_significance': True}
