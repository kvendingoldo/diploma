from numpy import pi, cos
from scipy.integrate import solve_ivp


def fun(t, N1):
    print(t)
    input = 1-cos(t) if 0<t<2*pi else 0
    return -100*N1 + input


N0=0

sol = solve_ivp(fun=fun, t_span=[0, 2], y0=[N0], t_eval=[0,2])
