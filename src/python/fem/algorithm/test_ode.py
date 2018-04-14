import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


def f(y, t):
    a1, a2 = y
    print(y[0])

    return [a2,
            a1-a1**3]


t = np.linspace(0, 10, 70)
y0 = [-0.1, 0.7]
fig = plt.figure(facecolor='white')

[y1, y2] = odeint(f, y0, t, args=(), full_output=False).T
#plt.plot(t, y1, '-o', t, y2, '-o', linewidth=2)
plt.plot(y1, y2, linewidth=2, label='')
plt.xlim(-10, 10)
plt.ylim(-10, 10)
plt.grid(True)
plt.show()
