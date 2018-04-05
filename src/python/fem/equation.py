from sympy import *
from IPython.display import display

# переменные
x1, x2, t = symbols('x1 x2 t', real=True)

# константы
Ak, Al = symbols('A_k, A_l')
Bk, Bl = symbols('B_k, B_l')
Ck, Cl = symbols('C_k, C_l')

# базисные функции
N_k = Ak * x1 + Bk * x2 + Ck
N_l = Al * x1 + Bl * x2 + Cl

# коэффициенты
a_k, a_mk, a_2mk = symbols('a_k, a_{m+k}, a_{2m+k}')

# выражения
N_11, N_22, N_12, N_p = symbols('N_11 N_22 N_12 N_p')

# константы
rho, rho_a, gamma, theta = symbols('rho rho_a gamma theta')
f, W, g, c, Pa, h = symbols('f W g c Pa h')

# misc
k = Symbol("k")
M = Symbol("M")

# функции
#H, q1, q2 = symbols('H q1 q2')

q1 = Sum(a_k(t) * N_k, (k, 1, M))
q2 = Sum(a_mk(t) * N_k, (k, 1, M))
H = Sum(a_2mk(t) * N_k, (k, 1, M))

# уравнения
eq1 = diff(q1, x1) + diff(q2, x2) + diff(rho * H, t)
eq2 = diff(q1, t) + diff((q1**2 / H), x1) + diff(((q1 * q2) / H), x2) - diff((N_11 - N_p), x1) - diff(N_12, x2) - f * q2 - (gamma**2 * rho_a * W**2 * cos(theta)) + (g/c**2) * (1/rho) * (q1 * sqrt(q1**2 + q2**2) / H**2) - Pa * diff(H, x1) - (rho * g * H) * diff(h, x1)
eq3 = diff(q2, t) + diff(((q1 * q2) / H), x1) + diff((q2**2 / H), x2) - diff((N_22 - N_p), x2) - diff(N_12, x2) + f * q1 - (gamma**2 * rho_a * W**2 * sin(theta)) + (g/c**2) * (1/rho) * (q2 * sqrt(q1**2 + q2**2) / H**2) - Pa * diff(H, x2) - (rho * g * H) * diff(h, x2)


eq1 = integrate(Mul(eq1, N_l), x1, x2)
eq2 = integrate(Mul(eq2, N_l), x1, x2)
eq3 = integrate(Mul(eq3, N_l), x1, x2)

print(eq2)

#print(latex(S(eq1, evaluate=True)))
#print(latex(S(eq2, evaluate=True)))
#print(latex(S(eq3, evaluate=True)))
