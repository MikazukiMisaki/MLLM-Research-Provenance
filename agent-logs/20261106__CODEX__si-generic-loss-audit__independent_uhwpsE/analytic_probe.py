"""Independent, invented CPU-only weighted cross-entropy checks."""
import math
import torch
from loss_fixture import Example, dataset_weights, window_terms

torch.set_num_threads(1)
targets = [True, False, False]
for arm in ('C1', 'C4'):
    x1 = torch.tensor([[0., 0.], [0., 0.], [8., -8.]], dtype=torch.float64, requires_grad=True)
    x2 = torch.tensor([[0., 0.], [9., -9.], [7., -7.]], dtype=torch.float64, requires_grad=True)
    x3 = torch.tensor([[math.log(3), 0.], [6., -6.]], dtype=torch.float64, requires_grad=True)
    e1 = Example(x1, torch.tensor([-100, 1, 0]), 0)
    e2 = Example(x2, torch.tensor([-100, 1, -100]), 1)
    e3 = Example(x3, torch.tensor([-100, 0]), 2)
    out = sum(window_terms([e1, e2], targets, arm))
    grad = torch.autograd.grad(out, (x1, x2))
    z = 1 if arm == 'C1' else 2
    expected1 = torch.tensor([[z/6, -z/6], [-z/6, z/6], [0, 0]], dtype=torch.float64)
    v = 1/6 if arm == 'C1' else 1/12
    expected2 = torch.tensor([[v, -v], [0, 0], [0, 0]], dtype=torch.float64)
    torch.testing.assert_close(out, torch.tensor(math.log(2)*(1 if arm == 'C1' else 1.5), dtype=torch.float64), rtol=0, atol=1e-12)
    torch.testing.assert_close(grad[0], expected1, rtol=0, atol=1e-12)
    torch.testing.assert_close(grad[1], expected2, rtol=0, atol=1e-12)
    out3 = sum(window_terms([e3], targets, arm))
    grad3 = torch.autograd.grad(out3, x3)[0]
    factor = 1 if arm == 'C1' else .5
    torch.testing.assert_close(out3, torch.tensor(math.log(4/3)*factor, dtype=torch.float64), rtol=0, atol=1e-12)
    torch.testing.assert_close(grad3, torch.tensor([[-.25*factor, .25*factor], [0., 0.]], dtype=torch.float64), rtol=0, atol=1e-12)
    print(f'{arm}: mixed={out.item():.15f}; partial={out3.item():.15f}; all analytic gradients PASS')
for group in ([False], [True], [False, False], [True, True]):
    for arm in ('C1', 'C4'):
        try:
            dataset_weights(group, arm)
        except ValueError:
            pass
        else:
            raise AssertionError((group, arm))
print('8 endpoint variants rejected PASS')
# Contrast the already-audited Qwen source's float32 upcast. This is not a Qwen forward.
x = torch.tensor([[0.3, -0.2], [0., 0.]], dtype=torch.bfloat16, requires_grad=True)
y = torch.tensor([-100, 0])
observed = window_terms([Example(x, y, 0)], [True, False], 'C1')[0]
float32_ce = torch.nn.functional.cross_entropy(x[:-1].float(), y[1:])
assert observed.item() != float32_ce.item()
print(f'bfloat16 fixture={observed.item():.12f}; float32-upcast CE={float32_ce.item():.12f}; equality={observed.item()==float32_ce.item()}')
