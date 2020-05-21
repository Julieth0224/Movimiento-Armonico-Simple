import sys
import numpy as np
import matplotlib.pyplot as plt
# sys.path.insert(0, '../')

import oscillator.oscillator as os
import forces.forces as fr
import solver.solver as sol
import animator.animator as ani


def restoring_force(state, params):
    x, L, v, vr, t = state
    w0 = params
    dxdt = v
    dvdt = -w0**2 * np.sin(np.radians(x))
    drdt = vr
    dvrdt = 0
    return dxdt, drdt, dvdt, dvrdt, 1.0

def integrate(obj):
    xpos, vpos, tpos = [], [], []
    tc = 0
    while tc < 20:  #9.55:
        xc, _, vc, _, tc = obj.objs.get_state()
        xpos.append(xc)
        vpos.append(vc)
        tpos.append(tc)
        obj.do_step()
    return tpos, xpos, vpos

x0, v0, w0, t0 = 0, 10., 5, 0
sim_params = w0
deltat = 0.0001

m1 = "Euler"
m2 = "Euler-Cromer"
m3 = "Midpoint"

num_method = m2

pendulo = os.Oscillator(x0, v0, w0, t0, "P1")
pendulo_force = fr.Forces(restoring_force, sim_params)
pendulo.set_force(pendulo_force)
euler = sol.Solver(pendulo, num_method, deltat)
tvac, xvac, vac = integrate(euler)


fig, ax = plt.subplots()
ax.plot(tvac, xvac, c = 'purple', label='Pendulo')
# ax.plot(t0, x0, 'o-', c='purple')

ax.set(xlabel='t (a.u.)', ylabel='x (a.u.)',
       title='')
ax.grid()

plt.legend()
plt.show()

# pendulo = (tvac, xvac)
#
# anime = ani.Animator(pendulo)
# anime.setup_anime()
# anime.run_anime()
