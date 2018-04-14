import numpy as np
from scipy.integrate import odeint, ode
import matplotlib.pyplot as plt


def function(y, t):
    a1, a2 = y
    #print(y[0])

    return [a2,
            a1-a1**3]


t = np.linspace(0, 10)
y0 = [-0.1, 0.7]
fig = plt.figure(facecolor='white')

[y1, y2] = odeint(function, y0, t, args=(), full_output=False).T


solution = ode(function).set_integrator('dopri5', method = 'adams')
solution.set_initial_value(y0, t)
solution.integrate(solution.t + 0.1)


#print(solution)
#plt.plot(t, solution)#should graph the data

#plt.plot(t, y1, '-o', t, y2, '-o', linewidth=2)
#plt.plot(y1, y2, linewidth=2, label='')
#plt.xlim(-10, 10)
#plt.ylim(-10, 10)
#plt.grid(True)
#plt.show()
