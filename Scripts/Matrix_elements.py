from Fluxonium_hamiltonians.Single_small_junction import charge_matrix_element as nem
from Fluxonium_hamiltonians.Single_small_junction import phase_matrix_element as pem
from Fluxonium_hamiltonians.Single_small_junction import qp_matrix_element as qpem
import numpy as np
from matplotlib import pyplot as plt

N = 50
E_l = 0.5
E_c = 2.5
E_j = 10
iState = 1
fState = 2

phi_ext = np.linspace(0,0.5,100)
element = np.zeros(len(phi_ext))
for idx, phi in enumerate(phi_ext):
    element[idx]=abs(qpem(N, E_l, E_c, E_j, phi*2*np.pi, iState, fState))
fig1 = plt.figure(1)
plt.plot(phi_ext, element)

iState = 1
fState = 3

phi_ext = np.linspace(0,0.5,100)
element = np.zeros(len(phi_ext))
for idx, phi in enumerate(phi_ext):
    element[idx]=abs(qpem(N, E_l, E_c, E_j, phi*2*np.pi, iState, fState))
fig1 = plt.figure(1)
plt.plot(phi_ext, element)

iState = 1
fState = 4

phi_ext = np.linspace(0,0.5,100)
element = np.zeros(len(phi_ext))
for idx, phi in enumerate(phi_ext):
    element[idx]=abs(qpem(N, E_l, E_c, E_j, phi*2*np.pi, iState, fState))
fig1 = plt.figure(1)
plt.plot(phi_ext, element)

iState = 1
fState = 5

phi_ext = np.linspace(0,0.5,100)
element = np.zeros(len(phi_ext))
for idx, phi in enumerate(phi_ext):
    element[idx]=abs(qpem(N, E_l, E_c, E_j, phi*2*np.pi, iState, fState))
fig1 = plt.figure(1)
plt.plot(phi_ext, element)

plt.show()
