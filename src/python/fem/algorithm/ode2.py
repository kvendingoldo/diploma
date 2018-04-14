from scipy import *
from scipy.integrate import ode
from pylab import *

"""Example using ode integrator, Lorenz equations"""


def foo(t, y, p):  # system of 1st order ode
    sigma = p[0];
    beta = p[1];
    rho = p[2]
    dy = zeros([3])
    dy[0] = sigma * (y[1] - y[0])
    dy[1] = y[0] * (rho - y[2]) - y[1]
    dy[2] = y[0] * y[1] - beta * y[2]
    print(dy)
    return dy


t0 = 0;
tEnd = 100.0;
dt = 0.01
y0 = [0, 0, 1]  # Initial conditions
Y = [];
T = []  # create empty lists
p = [10.0, 8.0 / 3.0, 28.0]  # parameters for odes

# Set up integrator 'vode'.  Non-stiff use Adams, stiff use bdf
r = ode(foo).set_integrator('vode', method='adams')
# r = ode(foo).set_integrator('vode',method='bdf')

# Maybe future version of scipy will have Runge-Kutta methods dopri5 and dop853
# r = ode(foo).set_integrator('dopri5')

r.set_f_params(p).set_initial_value(y0, t0)

while r.successful() and r.t + dt < tEnd:
    r.integrate(r.t + dt)
    Y.append(r.y)  # makes a list of 1d arrays
    T.append(r.t)

Y = array(Y)  # convert from list to 2d array

subplot(2, 1, 1)
plot(T, Y)
subplot(2, 1, 2)
plot(Y[:, 0], Y[:, 2])
show()
