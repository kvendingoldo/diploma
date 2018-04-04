from sympy import *

# базисные функции
N_k, N_l = symbols('N_k, N_l')

# переменные
x1, x2, t = symbols('x1 x2 t', real=True)

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

q1 = Sum(a_k(t) * N_k(x1, x2), (k, 1, M))
q2 = Sum(a_mk(t) * N_k(x1, x2), (k, 1, M))
H = Sum(a_2mk(t) * N_k(x1, x2), (k, 1, M))

# уравнения
eq1 = Derivative(q1, x1) + Derivative(q2, x2) + Derivative(rho * H, t)
eq2 = Derivative(q1, t) + Derivative((q1**2 / H), x1) + Derivative(((q1 * q2) / H), x2) - Derivative((N_11 - N_p), x1) - Derivative(N_12, x2) - f * q2 - (gamma**2 * rho_a * W**2 * cos(theta)) + (g/c**2) * (1/rho) * (q1 * sqrt(q1**2 + q2**2) / H**2) - Pa * Derivative(H, x1) - (rho * g * H) * Derivative(h, x1)
eq3 = Derivative(q2, t) + Derivative(((q1 * q2) / H), x1) + Derivative((q2**2 / H), x2) - Derivative((N_22 - N_p), x2) - Derivative(N_12, x2) + f * q1 - (gamma**2 * rho_a * W**2 * sin(theta)) + (g/c**2) * (1/rho) * (q2 * sqrt(q1**2 + q2**2) / H**2) - Pa * Derivative(H, x2) - (rho * g * H) * Derivative(h, x2)


eq1 = Integral(Mul(eq1, N_l(x1, x2)), x1, x2)
eq2 = Integral(Mul(eq2, N_l(x1, x2)), x1, x2)
eq3 = Integral(Mul(eq3, N_l(x1, x2)), x1, x2)


print(latex(S(eq1, evaluate=False)))
print(latex(S(eq2, evaluate=False)))
print(latex(S(eq3, evaluate=False)))
