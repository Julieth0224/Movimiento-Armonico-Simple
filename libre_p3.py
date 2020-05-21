import sys
import numpy as np
import matplotlib.pyplot as plt
# sys.path.insert(0, '../')

import oscillator.oscillator as os
import forces.forces as fr
import solver.solver as sol

g = 9.8
l = 1
m = 1

def restoring_force(state, params):
    x, L, v, vr, t = state
    w0 = params
    dxdt = v
    dvdt = -w0**2 * np.sin(x)
    drdt = vr
    dvrdt = 0
    return dxdt, drdt, dvdt, dvrdt, 1.0

def integrate(obj):
    xpos, vpos, tpos= [], [], []
    _, _, _, _, tc = obj.objs.get_state()
    while tc < 10:  #9.55:
        xc, _, vc, _, tc = obj.objs.get_state()
        xpos.append(xc)
        vpos.append(vc)
        tpos.append(tc)
        obj.do_step()
    return tpos, xpos, vpos


x0, v0, w0, t0 = 0.2, 0., 3., 0
sim_params = w0
deltat = 0.1

m1 = "Euler"
m2 = "Euler-Cromer"
m3 = "Midpoint"

num_method = m2

pendulo = os.Oscillator(x0, v0, w0, t0, "P1")
pendulo_force = fr.Forces(restoring_force, sim_params)
pendulo.set_force(pendulo_force)
euler = sol.Solver(pendulo, num_method, deltat)
tvac, xvac, vac= integrate(euler)


print("dt: ", deltat)

fig, ax = plt.subplots()
ax.plot(tvac, xvac, ls='--', c ='royalblue', label='Angle')
ax.plot(tvac, vac, ls='--', c = 'deeppink', label='Velocity')
ax.set(xlabel='time (AU)', ylabel='State (AU)')
ax.grid()




plt.legend()
plt.show()
