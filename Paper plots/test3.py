# Analyze T1 data from 2.5-3.5GHz
import numpy as np
from matplotlib import pyplot as plt

from Fluxonium_hamiltonians.Squid_small_junctions import bare_hamiltonian
from Fluxonium_hamiltonians.Squid_small_junctions import charge_matrix_element as nem
from Fluxonium_hamiltonians.Squid_small_junctions import phase_matrix_element as pem
from Fluxonium_hamiltonians.Squid_small_junctions import qp_matrix_element as qpem

# Define file directory
directory = "C:\Data\Fluxonium #10 simulations"
simulation = "Relaxation_wSquid"
path = directory + "\\" + simulation
plt.figure(figsize=(10, 10))
plt.rc('font', family='serif')

# Define constants
e = 1.602e-19  # Fundamental charge
h = 6.62e-34  # Placnk's constant
phi_o = h / (2 * e)  # Flux quantum

T1_array = []
flux_array = []
# T1 data for 02 transition
directory = "G:\Projects\Fluxonium\Data\Summary of T1_T2_vs flux_Fluxonium#10\Corrected flux"

simulation = "T1 avg_T2_qubit f(0to2) vs flux_38p76 to 38p26mA.csv"
path = directory + "\\" + simulation
data = np.genfromtxt(path, delimiter=',', dtype=float)
flux = data[1::, 0]
freq = data[1::, 1]
T1 = data[1::, 2]
for idx in range(len(T1)):
    if freq[idx] > 5:
        T1_array = np.append(T1_array, T1[idx])
        flux_array = np.append(flux_array, flux[idx])

simulation = "T1 avg_T2_qubit f(0to2) vs flux_39p37 to 39p78mA.csv"
path = directory + "\\" + simulation
data = np.genfromtxt(path, delimiter=',', dtype=float)
flux = data[1::, 0]
freq = data[1::, 1]
T1 = data[1::, 2]
for idx in range(len(T1)):
    if freq[idx] > 4.5:
        T1_array = np.append(T1_array, T1[idx])
        flux_array = np.append(flux_array, flux[idx])

simulation = "T1 avg_T2_qubit f(0to2) vs flux_41p5 to 42mA.csv"
path = directory + "\\" + simulation
data = np.genfromtxt(path, delimiter=',', dtype=float)
flux = data[1::, 0]
freq = data[1::, 1]
T1 = data[1::, 2]
for idx in range(len(T1)):
    if freq[idx] > 4:
        T1_array = np.append(T1_array, T1[idx])
        flux_array = np.append(flux_array, flux[idx])

# Get matrix elements
current = flux_array * 1e-3
N = 50
E_l = 0.746959655208
E_c = 0.547943694372
E_j_sum = 21.9627179709
level_num = 10
B_coeff = 60
A_j = 3.80888914574e-12
A_c = 1.49982268962e-10
beta_squid = 0.00378012644185
beta_ext = 0.341308382441
d = 0.0996032153487
energies = np.zeros((len(current), level_num))
qp_element = np.zeros((len(current), 2))
n_element = np.zeros(len(current))
p_element = np.zeros(len(current))

iState = 1
fState = 2
for idx, curr in enumerate(current):
    flux_squid = curr * B_coeff * A_j * 1e-4
    flux_ext = curr * B_coeff * A_c * 1e-4
    H = bare_hamiltonian(N, E_l, E_c, E_j_sum, d, 2 * np.pi * (flux_squid / phi_o - beta_squid),
                         2 * np.pi * (flux_ext / phi_o - beta_ext))
    for idy in range(level_num):
        energies[idx, idy] = H.eigenenergies()[idy]
    n_element[idx] = nem(N, E_l, E_c, E_j_sum, d, 2 * np.pi * (flux_squid / phi_o - beta_squid),
                         2 * np.pi * (flux_ext / phi_o - beta_ext), iState, fState)
    p_element[idx] = pem(N, E_l, E_c, E_j_sum, d, 2 * np.pi * (flux_squid / phi_o - beta_squid),
                         2 * np.pi * (flux_ext / phi_o - beta_ext), iState, fState)
    qp_element[idx, :] = qpem(N, E_l, E_c, E_j_sum, d, 2 * np.pi * (flux_squid / phi_o - beta_squid),
                              2 * np.pi * (flux_ext / phi_o - beta_ext), iState, fState)
freq_02 = energies[:, 2] - energies[:, 0]
freq_12 = energies[:, 2] - energies[:, 1]
T1_final = []
flux_final = []
freq_final = []
qpem_final_1 = []
qpem_final_2 = []
pem_final = []
for idx in range(len(T1_array)):
    if freq_12[idx] > 2.5 and freq_12[idx] < 3.5:
        T1_final = np.append(T1_final, T1_array[idx])
        pem_final = np.append(pem_final, p_element[idx])
        qpem_final_1 = np.append(qpem_final_1, qp_element[idx, 0])
        qpem_final_2 = np.append(qpem_final_2, qp_element[idx, 1])

# plt.plot(freq_12, T1_array, 'bo')
plt.loglog(qpem_final_1 ** 2 + qpem_final_2 ** 2, T1_final, 'D', mfc='none', mew='2', mec='red')
# plt.loglog(pem_final, T1_final, 'D', mfc='none', mew='2', mec='red')

#######################Simulation#######################
hbar = h / (2 * np.pi)
kB = 1.38064852e-23
T = 1e-2
E_c = E_c / 1.509190311677e+24  # convert GHz to J
E_l = E_l / 1.509190311677e+24  # convert to J
E_j_sum = E_j_sum / 1.509190311677e+24  # convert to J
E_j1 = 0.5 * E_j_sum * (1 + d)
E_j2 = 0.5 * E_j_sum * (1 - d)
delta_alum = 5.447400321e-23  # J
# current = flux_final * 1e-3
##########Upper limit
Q_cap = 2.1e6
Q_ind = 0.8e6
Q_qp = 3.5e6

cap = e ** 2 / (2.0 * E_c)
ind = hbar ** 2 / (4.0 * e ** 2 * E_l)
gk = e ** 2.0 / h
g1 = 8.0 * E_j1 * gk / delta_alum
g2 = 8.0 * E_j2 * gk / delta_alum
pem_sim = np.array([1e-2, 1.5e0])
qpem_sim = np.array([5e-5, 10])
trans_energy = energies[:, fState] - energies[:, iState]
# w = trans_energy*1e9*2*np.pi
w = 3e9 * 2 * np.pi
Y_cap = w * cap / Q_cap
Y_ind = 1.0 / (w * ind * Q_ind)
Y_qp1 = (g1 / (2 * Q_qp)) * (2 * delta_alum / (hbar * w)) ** (1.5)
Y_qp2 = (g2 / (2 * Q_qp)) * (2 * delta_alum / (hbar * w)) ** (1.5)

gamma_cap = np.zeros(len(pem_sim))
gamma_qp = np.zeros((len(qpem_sim), 2))

for idx in range(len(qpem_sim)):
    gamma_cap[idx] = (phi_o * pem_sim[idx] / hbar / (2 * np.pi)) ** 2 * hbar * w * Y_cap * (
    1 + 1.0 / np.tanh(hbar * w / (2 * kB * T)))
    # gamma_ind[idx] = (phi_o * pem_sim[idx] / hbar / (2 * np.pi)) ** 2 * hbar * w * Y_ind * (1 + 1.0 / np.tanh(hbar * w / (2 * kB * T)))
    gamma_qp[idx, 0] = (qpem_sim[idx]) ** 2 * (w / np.pi / gk) * Y_qp1
    gamma_qp[idx, 1] = (qpem_sim[idx]) ** 2 * (w / np.pi / gk) * Y_qp2
# T1_sim = 1/gamma_cap
# plt.loglog(pem_sim**2, T1_sim*1e6,linewidth = '1', color = 'g', linestyle ='-')
# T1_sim = 1/(gamma_qp[:,0] + gamma_qp[:,1])
# plt.loglog(2*qpem_sim**2, T1_sim*1e6,linewidth = '1', color = 'g', linestyle ='-')
##########Lower limit
Q_cap = 0.37e6
Q_ind = 0.8e6
Q_qp = 0.6e6

cap = e ** 2 / (2.0 * E_c)
ind = hbar ** 2 / (4.0 * e ** 2 * E_l)
gk = e ** 2.0 / h
g1 = 8.0 * E_j1 * gk / delta_alum
g2 = 8.0 * E_j2 * gk / delta_alum
pem_sim = np.array([1e-2, 1.5e0])
qpem_sim = np.array([5e-5, 10])
trans_energy = energies[:, fState] - energies[:, iState]
# w = trans_energy*1e9*2*np.pi
w = 3e9 * 2 * np.pi
Y_cap = w * cap / Q_cap
Y_ind = 1.0 / (w * ind * Q_ind)
Y_qp1 = (g1 / (2 * Q_qp)) * (2 * delta_alum / (hbar * w)) ** (1.5)
Y_qp2 = (g2 / (2 * Q_qp)) * (2 * delta_alum / (hbar * w)) ** (1.5)

gamma_cap = np.zeros(len(pem_sim))
gamma_qp = np.zeros((len(qpem_sim), 2))

for idx in range(len(qpem_sim)):
    gamma_cap[idx] = (phi_o * pem_sim[idx] / hbar / (2 * np.pi)) ** 2 * hbar * w * Y_cap * (
    1 + 1.0 / np.tanh(hbar * w / (2 * kB * T)))
    # gamma_ind[idx] = (phi_o * pem_sim[idx] / hbar / (2 * np.pi)) ** 2 * hbar * w * Y_ind * (1 + 1.0 / np.tanh(hbar * w / (2 * kB * T)))
    gamma_qp[idx, 0] = (qpem_sim[idx]) ** 2 * (w / np.pi / gk) * Y_qp1
    gamma_qp[idx, 1] = (qpem_sim[idx]) ** 2 * (w / np.pi / gk) * Y_qp2
# T1_sim = 1/gamma_cap
# plt.loglog(pem_sim**2, T1_sim*1e6,linewidth = '1', color = 'g', linestyle ='-')
# T1_sim = 1/(gamma_qp[:,0] + gamma_qp[:,1])
# plt.loglog(2*qpem_sim**2, T1_sim*1e6,linewidth = '1', color = 'g', linestyle ='-')

##########################################################################################################################
# T for 01 transition
T1_array = []
freq_array = []
flux_array = []
# T1 data for 01 transition
directory = "G:\Projects\Fluxonium\Data\Summary of T1_T2_vs flux_Fluxonium#10\Corrected flux"

simulation = "T1avg(0to1)vs flux 41p52 to 42p0mA.csv"
path = directory + "\\" + simulation
data = np.genfromtxt(path, delimiter=',', dtype=float)
flux = data[1::, 0]
freq = data[1::, 1]
T1 = data[1::, 2]
T1_array = np.append(T1_array, T1)
flux_array = np.append(flux_array, flux)
freq_array = np.append(freq_array, freq)

simulation = "T1_T2_qubit f(0to1)vs flux 43p65_45p4mA.csv"
path = directory + "\\" + simulation
data = np.genfromtxt(path, delimiter=',', dtype=float)
flux = data[1::, 0]
freq = data[1::, 1]
T1 = data[1::, 2]
T1_array = np.append(T1_array, T1)
flux_array = np.append(flux_array, flux)
freq_array = np.append(freq_array, freq)

simulation = "T1 avg_T2_qubit f(0to1) vs flux_39p46 to 39p39mA.csv"
path = directory + "\\" + simulation
data = np.genfromtxt(path, delimiter=',', dtype=float)
flux = data[1::, 0]
freq = data[1::, 1]
T1 = data[1::, 2]
T1_array = np.append(T1_array, T1)
flux_array = np.append(flux_array, flux)
freq_array = np.append(freq_array, freq)

simulation = "T1 avg_T2_qubit f(0to1) vs flux_38p5 to 38p76mA.csv"
path = directory + "\\" + simulation
data = np.genfromtxt(path, delimiter=',', dtype=float)
flux = data[1::, 0]
freq = data[1::, 1]
T1 = data[1::, 2]
T1_array = np.append(T1_array, T1)
flux_array = np.append(flux_array, flux)
freq_array = np.append(freq_array, freq)
#
# #########################################################################################
directory = "G:\Projects\Fluxonium\Data\Summary of T1_T2_vs flux_Fluxonium#10\Automation code"
simulation = "T1_auto_41to41p05mA.csv"
path = directory + "\\" + simulation
data = np.genfromtxt(path)
flux = data[:, 0] - 0.04
freq = data[:, 1]
T1 = data[:, 2]
T1_array = np.append(T1_array, T1)
flux_array = np.append(flux_array, flux)
freq_array = np.append(freq_array, freq)

simulation = "T1_auto_41p55to41p6mA.csv"
path = directory + "\\" + simulation
data = np.genfromtxt(path)
flux = data[:, 0] - 0.04
freq = data[:, 1]
T1 = data[:, 2]
T1_array = np.append(T1_array, T1)
flux_array = np.append(flux_array, flux)
freq_array = np.append(freq_array, freq)

simulation = "T1_auto_37p2to38p5mA_1.csv"
path = directory + "\\" + simulation
data = np.genfromtxt(path)
flux = data[:, 0] - 0.04
freq = data[:, 1]
T1 = data[:, 2]
T1_array = np.append(T1_array, T1)
flux_array = np.append(flux_array, flux)
freq_array = np.append(freq_array, freq)

simulation = "T1_auto_38p5to38p6mA.csv"
path = directory + "\\" + simulation
data = np.genfromtxt(path)
flux = data[:, 0] - 0.04
freq = data[:, 1]
T1 = data[:, 2]
T1_array = np.append(T1_array, T1)
flux_array = np.append(flux_array, flux)
freq_array = np.append(freq_array, freq)

simulation = "T1_auto_38p58to38p62mA.csv"
path = directory + "\\" + simulation
data = np.genfromtxt(path)
flux = data[:, 0] - 0.04
freq = data[:, 1]
T1 = data[:, 2]
T1_array = np.append(T1_array, T1)
flux_array = np.append(flux_array, flux)
freq_array = np.append(freq_array, freq)

simulation = "T1_auto_38p62to38p68mA.csv"
path = directory + "\\" + simulation
data = np.genfromtxt(path)
flux = data[:, 0] - 0.04
freq = data[:, 1]
T1 = data[:, 2]
T1_array = np.append(T1_array, T1)
flux_array = np.append(flux_array, flux)
freq_array = np.append(freq_array, freq)

# Slice through the arrays
T1_final = []
flux_final = []
freq_final = []
for idx in range(len(T1_array)):
    if freq_array[idx] > 2.5 and freq_array[idx] < 3.5:
        T1_final = np.append(T1_final, T1_array[idx])
        flux_final = np.append(flux_final, flux_array[idx])
        freq_final = np.append(freq_final, freq_array[idx])
# Get matrix elements
current = flux_final * 1e-3
N = 50
E_l = 0.746959655208
E_c = 0.547943694372
E_j_sum = 21.9627179709
level_num = 10
B_coeff = 60
A_j = 3.80888914574e-12
A_c = 1.49982268962e-10
beta_squid = 0.00378012644185
beta_ext = 0.341308382441
d = 0.0996032153487
energies = np.zeros((len(current), level_num))
qp_element = np.zeros((len(current), 2))
n_element = np.zeros(len(current))
p_element = np.zeros(len(current))

iState = 0
fState = 1
for idx, curr in enumerate(current):
    flux_squid = curr * B_coeff * A_j * 1e-4
    flux_ext = curr * B_coeff * A_c * 1e-4
    H = bare_hamiltonian(N, E_l, E_c, E_j_sum, d, 2 * np.pi * (flux_squid / phi_o - beta_squid),
                         2 * np.pi * (flux_ext / phi_o - beta_ext))
    for idy in range(level_num):
        energies[idx, idy] = H.eigenenergies()[idy]
    n_element[idx] = nem(N, E_l, E_c, E_j_sum, d, 2 * np.pi * (flux_squid / phi_o - beta_squid),
                         2 * np.pi * (flux_ext / phi_o - beta_ext), iState, fState)
    p_element[idx] = pem(N, E_l, E_c, E_j_sum, d, 2 * np.pi * (flux_squid / phi_o - beta_squid),
                         2 * np.pi * (flux_ext / phi_o - beta_ext), iState, fState)
    qp_element[idx, :] = qpem(N, E_l, E_c, E_j_sum, d, 2 * np.pi * (flux_squid / phi_o - beta_squid),
                              2 * np.pi * (flux_ext / phi_o - beta_ext), iState, fState)

plt.loglog(qp_element[:, 0] ** 2 + qp_element[:, 1] ** 2, T1_final, 's', mfc='none', mew='2', mec='blue')
# plt.loglog(p_element ** 2, T1_final, 's', mfc='none', mew='2', mec='blue')
#######################Simulation#######################
hbar = h / (2 * np.pi)
kB = 1.38064852e-23
T = 1e-2
E_c = E_c / 1.509190311677e+24  # convert GHz to J
E_l = E_l / 1.509190311677e+24  # convert to J
E_j_sum = E_j_sum / 1.509190311677e+24  # convert to J
E_j1 = 0.5 * E_j_sum * (1 + d)
E_j2 = 0.5 * E_j_sum * (1 - d)
delta_alum = 5.447400321e-23  # J
current = flux_final * 1e-3
##########Upper limit
Q_cap = 1.05e6
Q_ind = 0.8e6
Q_qp = 10e6

cap = e ** 2 / (2.0 * E_c)
ind = hbar ** 2 / (4.0 * e ** 2 * E_l)
gk = e ** 2.0 / h
g1 = 8.0 * E_j1 * gk / delta_alum
g2 = 8.0 * E_j2 * gk / delta_alum
pem_sim = np.array([1e-2, 1.5e0])
qpem_sim = np.array([5e-5, 10])
trans_energy = energies[:, fState] - energies[:, iState]
# w = trans_energy*1e9*2*np.pi
w = 3e9 * 2 * np.pi
Y_cap = w * cap / Q_cap
Y_ind = 1.0 / (w * ind * Q_ind)
Y_qp1 = (g1 / (2 * Q_qp)) * (2 * delta_alum / (hbar * w)) ** (1.5)
Y_qp2 = (g2 / (2 * Q_qp)) * (2 * delta_alum / (hbar * w)) ** (1.5)

gamma_cap = np.zeros(len(pem_sim))
gamma_qp = np.zeros((len(qpem_sim), 2))

for idx in range(len(qpem_sim)):
    gamma_cap[idx] = (phi_o * pem_sim[idx] / hbar / (2 * np.pi)) ** 2 * hbar * w * Y_cap * (
    1 + 1.0 / np.tanh(hbar * w / (2 * kB * T)))
    # gamma_ind[idx] = (phi_o * pem_sim[idx] / hbar / (2 * np.pi)) ** 2 * hbar * w * Y_ind * (1 + 1.0 / np.tanh(hbar * w / (2 * kB * T)))
    gamma_qp[idx, 0] = (qpem_sim[idx]) ** 2 * (w / np.pi / gk) * Y_qp1
    gamma_qp[idx, 1] = (qpem_sim[idx]) ** 2 * (w / np.pi / gk) * Y_qp2
# T1_sim = 1/gamma_cap
# plt.loglog(pem_sim**2, T1_sim*1e6,linewidth = '2', color = 'k', linestyle ='--')
T1_sim = 1 / (gamma_qp[:, 0] + gamma_qp[:, 1])
plt.loglog(2 * qpem_sim ** 2, T1_sim * 1e6, linewidth='2', color='k', linestyle='--')
##########Lower limit
Q_cap = 0.26e5
Q_ind = 0.8e6
Q_qp = 0.25e6

cap = e ** 2 / (2.0 * E_c)
ind = hbar ** 2 / (4.0 * e ** 2 * E_l)
gk = e ** 2.0 / h
g1 = 8.0 * E_j1 * gk / delta_alum
g2 = 8.0 * E_j2 * gk / delta_alum
pem_sim = np.array([1e-2, 1.5e0])
qpem_sim = np.array([5e-5, 10])
trans_energy = energies[:, fState] - energies[:, iState]
# w = trans_energy*1e9*2*np.pi
w = 3e9 * 2 * np.pi
Y_cap = w * cap / Q_cap
Y_ind = 1.0 / (w * ind * Q_ind)
Y_qp1 = (g1 / (2 * Q_qp)) * (2 * delta_alum / (hbar * w)) ** (1.5)
Y_qp2 = (g2 / (2 * Q_qp)) * (2 * delta_alum / (hbar * w)) ** (1.5)

gamma_cap = np.zeros(len(pem_sim))
gamma_qp = np.zeros((len(qpem_sim), 2))

for idx in range(len(qpem_sim)):
    gamma_cap[idx] = (phi_o * pem_sim[idx] / hbar / (2 * np.pi)) ** 2 * hbar * w * Y_cap * (
    1 + 1.0 / np.tanh(hbar * w / (2 * kB * T)))
    # gamma_ind[idx] = (phi_o * pem_sim[idx] / hbar / (2 * np.pi)) ** 2 * hbar * w * Y_ind * (1 + 1.0 / np.tanh(hbar * w / (2 * kB * T)))
    gamma_qp[idx, 0] = (qpem_sim[idx]) ** 2 * (w / np.pi / gk) * Y_qp1
    gamma_qp[idx, 1] = (qpem_sim[idx]) ** 2 * (w / np.pi / gk) * Y_qp2
# T1_sim = 1/gamma_cap
# plt.loglog(pem_sim**2, T1_sim*1e6,linewidth = '2', color = 'k', linestyle ='--')
T1_sim = 1 / (gamma_qp[:, 0] + gamma_qp[:, 1])
plt.loglog(2 * qpem_sim ** 2, T1_sim * 1e6, linewidth='2', color='k', linestyle='--')

##############################
# fac = 6e3
plt.ylim([1e1, 8e3])
# plt.xlim([1e1/fac,8e3/fac])
fac = 5e4
plt.xlim([1e1 / fac, 8e3 / fac])
plt.tick_params(labelsize=18)
plt.show()
