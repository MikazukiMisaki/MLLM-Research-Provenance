"""Count unlabeled pairs of partitions; no task instances or seeds."""
from itertools import permutations, product
import json

def canonical_labels(seq):
    seen = {}
    return tuple(seen.setdefault(x, len(seen)) for x in seq)

def partitions(n):
    return {canonical_labels(x) for x in product(range(n), repeat=n)}

def pair_orbit(a, b):
    return min((canonical_labels(tuple(a[i] for i in p)),
                canonical_labels(tuple(b[i] for i in p)))
               for p in permutations(range(len(a))))

result=[]
for n in range(1, 6):
    p=partitions(n)
    classes={pair_orbit(a,b) for a in p for b in p}
    result.append({'targets':n,'partitions':len(p),'paired_partition_orbits':len(classes),
                   'predicted_script_steps':6*n-1})
print(json.dumps(result,indent=2,sort_keys=True))
