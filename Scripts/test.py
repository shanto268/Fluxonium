import numpy as np

print "First: calculate C_shunt"
Cj = 5e-15
L =100e-9
w = 6.138e9*2*np.pi
Cs = 1.0/(w**2*L)
e = 1.6e-19
Ec = e**2/(2*(Cs+Cj))*1.5e24
print "C_shunt="+str(Cs*1e15)+"fF"
print "E_c="+str(Ec)
print "Second: calculate Lj to give resonant coupling"
w=10.4821e9*2*np.pi
C_sum = Cs+Cj
Lj = 1.0/(w**2*C_sum)
print "Lj="+str(Lj*1e9)+"nH"
print "Third: Check for resonance"
f1 = 10.3228
f2 = 10.4038
print (f1+f2)/2.0
print "Fourth: Calculate coupling"
g = (f2-f1)/2.0
print "g="+str(g*1e3)+"MHz"