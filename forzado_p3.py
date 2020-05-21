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
    w0, gamma, X, w = params
    Fm = X * (np.cos(w*t))
    dxdt = v
    dvdt = (Fm) + (-w0**2 * np.sin(x)) - (gamma*v)
    drdt = vr
    dvrdt = 0
    return dxdt, drdt, dvdt, dvrdt, 1.0

def punto(t, params):
    w0, gamma, X, w = params
    Fm = X * (np.cos(w*t))
    Theta = (Fm)/(np.sqrt(((w0**2 - w**2)**2)+((gamma*w)**2))) #(Fm)/(np.sqrt(((w0**2 - t**2)**2)+((gamma*t)**2)))
    return Theta

def punto_2(t, params):
    w0, gamma, X, w = params
    Fm = X * (np.cos(w*t))
    fase = np.arctan((gamma*w)/((w0**2) - (w**2))) #np.arctan((gamma*t)/((w0**2) - (t**2)))
    return fase

def energy(v, x):
    ek = (1/2) * m * (l**2) * (v**2)
    ep = m * g * l * (1 - np.cos(x))
    et = ek + ep
    return et, ek, ep

def integrate(obj, params):
    xpos, vpos, tpos, fpos, fapos, Thpos = [], [], [], [], [], []
    # xpos, vpos, tpos, Thpos = [], [], [], []
    _, _, _, _, tc = obj.objs.get_state()
    while tc < 30:  #9.55:
        xc, _, vc, _, tc = obj.objs.get_state()
        # fa, Theta = punto(tc, params) #This
        Theta = punto(tc, params)
        fa = punto_2(tc, params)
        xo = Theta * np.cos(w*tc + fa) #This
        fpos.append(xo) #This
        fapos.append(fa) #This
        Thpos.append(Theta)
        xpos.append(xc)
        vpos.append(vc)
        tpos.append(tc)
        obj.do_step()
    return tpos, xpos, vpos, fpos, fapos, Thpos
    # return tpos, xpos, vpos, Thpos

def provisional_integrate(params, W):
    fapos, Thpos = [], []
    for q in range(len(W)):  #9.55:
        Theta = punto(W[q], params) #This
        #fapos.append(fa) #This
        Thpos.append(Theta)
    return Thpos

def provisional_integrate_2(params, W):
    fapos, Thpos = [], []
    for q in range(len(W)):  #9.55:
        fa = punto_2(W[q], params) #This
        fapos.append(fa) #This
        # Thpos.append(Theta)
    return fapos

def energies(tpos, xpos, vpos):
    ek, ep, em= [], [], []
    for i in range(len(tpos)):
        ener_to, ener_ci, ener_po = energy(vpos[i], xpos[i])
        ek.append(ener_ci)
        ep.append(ener_po)
        em.append(ener_to)
    return ek, ep, em

def periodo(x, t):
    pos = []
    count = 0
    for i in range(len(x)):
        if x[i] <= x[i+1] and x[i+1] >= x[i+2]:
            count += 1
            pos.append(i)
            if count == 2:
                break
    return t[pos[1]] - t[pos[0]]


gamma, X, w = 0.5, 4, 4.0
x0, v0, w0, t0 = 0., 0., 3., 0
sim_params = w0, gamma, X, w
deltat = 0.01
# W = [0, 1, 2, 2.2, 2.4, 2.6, 2.8, 3, 3.2, 3.4, 4]
# AW = [0, 1, 2, 2.2, 2.4, 2.6, 2.8, 3.2, 3.4, 4]
# A, AP = [], []
# for i in range(len(W)):
#     poop = W[i]/w0
#     A.append(poop)
# for i in range(len(AW)):
#     poopo = AW[i]/w0
#     AP.append(poopo)


m1 = "Euler"
m2 = "Euler-Cromer"
m3 = "Midpoint"

num_method = m2

pendulo = os.Oscillator(x0, v0, w0, t0, "P1")
pendulo_force = fr.Forces(restoring_force, sim_params)
pendulo.set_force(pendulo_force)
euler = sol.Solver(pendulo, num_method, deltat)
tvac, xvac, vac, fvac, favac, Thvac = integrate(euler, sim_params)
# tvac, xvac, vac, Thvace = integrate(euler, sim_params)
# Thvac = provisional_integrate(sim_params, W)
# favac = provisional_integrate_2(sim_params, AW)
en_ci, en_po, en_to = energies(tvac, xvac, vac)


delta_e = en_to[-1] - en_to[0]
print("Theta: ", x0, ", v: ", v0, ", dt: ", deltat, ", de: ", delta_e)
print("Energia In: ", en_to[0], ", Energia Fin: ", en_to[-1])
print("Periodo: ", periodo(xvac, tvac))

deltae = []
for i in range(len(en_to)):
    deltae.append(en_to[i] - en_to[0])

# fig, ax = plt.subplots()
# ax.plot(tvac, xvac, ls='--', c ='royalblue', label='Angle')
# ax.plot(tvac, vac, ls='--', c = 'deeppink', label='Velocity')
# ax.set(xlabel='time (AU)', ylabel='State (AU)')
# ax.grid()

# fig, ax = plt.subplots()
# ax.plot(tvac, xvac, ls='--', c ='royalblue', label='Angle')
# ax.plot(tvac, fvac, ls='--', c = 'deeppink', label='Velocity')
# ax.set(xlabel='time (AU)', ylabel='State (AU)')
# ax.grid()

fig, ax = plt.subplots()
ax.plot(tvac, Thvac, ls='--', c ='royalblue', label='Theta')
ax.plot(tvac, xvac, ls='--', c = 'deeppink', label='Angle')
ax.set(xlabel='time (AU)', ylabel='State (AU)', title='$\omega$ = 4.0')
ax.grid()

# fig, ax = plt.subplots()
# ax.plot(A, Thvac, ls='--', c ='royalblue', label='Theta')
# ax.plot(AP, favac, ls='--', c = 'deeppink', label='Fase')
# # ax.plot(W, A, ls='--', c = 'blueviolet', label='$\omega$/$\omega_0$')
# ax.set(xlabel='$\omega$/$\omega_0$ (AU)', ylabel='State (AU)')
# ax.grid()

# fig, ax = plt.subplots()
# ax.plot(tvac, en_to, ls='--', c = 'blueviolet', label='Total Energy')
# ax.plot(tvac, en_ci, ls='--', c ='royalblue', label='Cinetic Energy')
# ax.plot(tvac, en_po, ls='--', c = 'deeppink', label='Potecial Energy')
# ax.set(xlabel='time (AU)', ylabel='Energy (J)')
# ax.grid()

# fig, ax = plt.subplots()
# ax.plot(tvac, deltae, 'm--', label='Delta E')
# ax.set(xlabel='time (AU)', ylabel='Energy (J)')
# ax.grid()


plt.legend()
plt.show()
