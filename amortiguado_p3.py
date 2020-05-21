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
    w0, gamma = params
    dxdt = v
    dvdt = (-w0**2 * np.sin(x)) - (gamma*v)
    drdt = vr
    dvrdt = 0
    return dxdt, drdt, dvdt, dvrdt, 1.0

def energy(v, x):
    ek = (1/2) * m * (l**2) * (v**2)
    ep = m * g * l * (1 - np.cos(x))
    et = ek + ep
    return et, ek, ep

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

def energies(tpos, xpos, vpos):
    ek, ep, em= [], [], []
    for i in range(len(tpos)):
        ener_to, ener_ci, ener_po = energy(vpos[i], xpos[i])
        ek.append(ener_ci)
        ep.append(ener_po)
        em.append(ener_to)
    return ek, ep, em


x0, v0, w0, gamma, t0 = 0.2, 0., 3., 4., 0
sim_params = w0, gamma
deltat = 0.01

m1 = "Euler"
m2 = "Euler-Cromer"
m3 = "Midpoint"

num_method = m2

pendulo = os.Oscillator(x0, v0, w0, t0, "P1")
pendulo_force = fr.Forces(restoring_force, sim_params)
pendulo.set_force(pendulo_force)
euler = sol.Solver(pendulo, num_method, deltat)
tvac, xvac, vac= integrate(euler)
en_ci, en_po, en_to = energies(tvac, xvac, vac)

delta_e = en_to[-1] - en_to[0]
print("Theta: ", x0, ", v: ", v0, ", dt: ", deltat, ", de: ", delta_e)
print("Energia In: ", en_to[0], ", Energia Fin: ", en_to[-1])

deltae = []
for i in range(len(en_to)):
    deltae.append(en_to[i] - en_to[0])
#
# fig, ax = plt.subplots()
# ax.plot(tvac, xvac, ls='--', c ='royalblue', label='Angle')
# ax.plot(tvac, vac, ls='--', c = 'deeppink', label='Velocity')
# ax.set(xlabel='time (AU)', ylabel='State (AU)')
# ax.grid()


fig, ax = plt.subplots()
# ax.plot(tvac, en_to, ls='--', c = 'blueviolet', label='Total Energy')
ax.plot(tvac, en_ci, ls='--', c ='royalblue', label='Kinetic Energy')
ax.plot(tvac, en_po, ls='--', c = 'deeppink', label='Potecial Energy')
ax.set(xlabel='time (AU)', ylabel='Energy (J)')
ax.grid()

# fig, ax = plt.subplots()
# ax.plot(tvac, deltae, 'm--', label='Delta E')
# ax.set(xlabel='time (AU)', ylabel='Energy (J)')
# ax.grid()


plt.legend()
plt.show()
