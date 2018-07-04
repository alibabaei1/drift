import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
from scipy import optimize
import scipy.optimize 

def find_corr_number( array1, array2, element):
    i= np.where(array1== element)
    return array2[i]
def f_prim(x,a0,a1,a2,a3,a4):
    if (x<= 0):
        return 0
    else:
        return np.exp(a0+a1*np.log(x)+a2*np.log(x)**2+a3*np.log(x)**3+a4*np.log(x)**4)
def f_Sec(x,a0,a1,a2,a3,a4):
    return np.exp(a0+a1*np.log(x)+a2*np.log(x)**2+a3*np.log(x)**3+a4*np.log(x)**4)
def Stopping_Power_Al(Energy):
    return f(Energy,7.10324628e+00,  -1.94662466e-01,  -1.46767221e-01,   1.20252433e-03, 1.79847844e-03)
def Stopping_Power(Energy):    #dE/dx
    return f(Energy,7.51161379e+00, -1.95417699e-01, -1.94390614e-01, -1.24903581e-04,2.79996333e-03)
def New_Stopping_power(Energy,length,dichte):
     Stopping_Power(Energy)*length*dichte

dichte_luft = 1.20479E-03
dichte_Al = 2.69890E+00
dichte_Mylar=1.40000E+00

dry_air = 'drayair.pl'
Al = 'Aldata.pl'
Mylar = 'Mylar.pl'
dary_air_data = np.loadtxt(dry_air, comments='#')
Al_data = np.loadtxt(Al, comments='#')
Mylar_data = np.loadtxt(Mylar, comments='#')

Energy_dry_air = dary_air_data[:,0] #kanal
Stopping_Power_dry_air = dary_air_data[:,1] #Energie
Range_CSDA_dry_air = dary_air_data[:,2]

Energy_Al = Al_data[:,0] #kanal
Stopping_Power_Al = Al_data[:,1] #Energie
Range_CSDA_Al = Al_data[:,2]

Energy_Mylar = Mylar_data[:,0] #kanal
Stopping_Power_Mylar = Mylar_data[:,1] #Energie
Range_CSDA_Mylar = Mylar_data[:,2]

popt_air, pcov_air = curve_fit(f_Sec, Energy_dry_air, Stopping_Power_dry_air,p0=[-2.4,7.6,-0.3,-0.02,0.02])
popt_Al, pcov_Al = curve_fit(f_Sec, Energy_Al, Stopping_Power_Al,p0=[-2.4,7.6,-0.3,-0.02,0.02])
popt_Mylar, pcov_Mylar = curve_fit(f_Sec, Energy_Mylar, Stopping_Power_Mylar,p0=[-2.4,7.6,-0.3,-0.02,0.02])

def Stopping_Power_Air(Energy):
    return f_prim(Energy,*popt_air)
def Stopping_Power_Al(Energy):
    return f_prim(Energy,*popt_Al)
def Stopping_Power_Mylar(Energy):
    return f_prim(Energy,*popt_Mylar)
def Stopping_Power_step_Air(Energy , length, n):
    multiplicator = dichte_luft * length
    for i in range(n):
        Energy = Energy - Stopping_Power_Air(Energy)*multiplicator
    return Energy
def Stopping_Power_step_Al(Energy , length, n):
    multiplicator = dichte_Al * length
    for i in range(n):
        Energy = Energy - Stopping_Power_Al(Energy)*multiplicator
    return Energy
def Stopping_Power_step_Mylar(Energy, length, n):
    multiplicator = dichte_Mylar * length
    for i in range(n):
        Energy = Energy - Stopping_Power_Mylar(Energy)*multiplicator
    return Energy
def E_loss( E_in, d, Stopping_Power_von_Material):
    if Stopping_Power_von_Material == 'Air':
        return Stopping_Power_step_Air(E_in, 3e-2, int(d/3e-2))
    elif Stopping_Power_von_Material == 'Al':
        return Stopping_Power_step_Al(E_in, 1e-5, int(d/1e-5)) 
    elif Stopping_Power_von_Material == 'Mylar':
        return Stopping_Power_step_Mylar(E_in, 1e-5, int(d/1e-5)) 
    else:
        print('Not defined')
def Orange_direct(E_in):
    E_1= E_loss( E_in, 0.43, 'Air') #3.3mm + 0.1mm luft
    E_2= E_loss( E_1, 1e-4, 'Al' ) #1u Al
    E_3= E_loss( E_2, 6e-4, 'Mylar') # 6um Mylar
    E_4= E_loss( E_3, 0.15, 'Air' ) # 1.5 mm luft
    return E_4
def Orange(E_in, theta):
    E_1= E_loss( E_in, 0.43/np.cos(theta*np.pi/180), 'Air') #3.3mm + 0.1mm luft
    E_2= E_loss( E_1, 1e-4/np.cos(theta*np.pi/180), 'Al' ) #1u Al
    E_3= E_loss( E_2, 6e-4/np.cos(theta*np.pi/180), 'Mylar') # 6um Mylar
    E_4= E_loss( E_3, 0.15/np.cos(theta*np.pi/180), 'Air' ) # 1.5 mm luft
    return E_4
def limit_theta(Energy):
    n= 0
    while(Orange(Energy,n)>=0.1):
#        print(Orange(Energy,n))
        n=n+.1
    return n-.1
#limit_theta(3)
def random_theta(Energy, Anzahl):
    return np.random.uniform(0,limit_theta(Energy),Anzahl)
def random_End_Energy(Energy,Anzahl):
    a = []
    for i in range(Anzahl):
        result= Orange(Energy,random_theta(Energy,1))
        a.append(result)
    return np.asarray(a)

def histo1(Energy):
    plt.xlabel('Energie[MeV]')
    plt.ylabel('Anzahl')
    plt.title('#= 50000, bins= 30, Energy= 5.4 MeV')
    plt.grid(True)
    n, bins, patches = plt.hist(random_End_Energy(Energy,50000), 30, density=False, facecolor='g', alpha=1)
    plt.savefig('5-4MeV_01.png')
def histo2(Energy):
    plt.xlabel('Energie[MeV]')
    plt.ylabel('Anzahl')
    plt.title('#= 50000, bins= 30, Energy= 5.4 MeV')
    plt.grid(True)
    n, bins, patches = plt.hist(random_End_Energy(Energy,50000), 30, density=False, facecolor='g', alpha=1)
    plt.savefig('5-4MeV_02.png')
def histo3(Energy):
    plt.xlabel('Energie[MeV]')
    plt.ylabel('Anzahl')
    plt.title('#= 50000, bins= 30, Energy= 5.4 MeV')
    plt.grid(True)
    n, bins, patches = plt.hist(random_End_Energy(Energy,50000), 30, density=False, facecolor='g', alpha=1)
    plt.savefig('5-4MeV_03.png')
def histo4(Energy):
    plt.xlabel('Energie[MeV]')
    plt.ylabel('Anzahl')
    plt.title('#= 50000, bins= 30, Energy= 5.4 MeV')
    plt.grid(True)
    n, bins, patches = plt.hist(random_End_Energy(Energy,50000), 30, density=False, facecolor='g', alpha=1)
    plt.savefig('5-4MeV_04.png')
#def histo2(Energy):
#    plt.xlabel('Energie[MeV]')
#    plt.ylabel('Anzahl')
#    plt.title('#= 50000, bins= 30, Energy= 4 MeV')
#    plt.grid(True)
#    n, bins, patches = plt.hist(random_End_Energy(Energy,50000), 30, density=False, facecolor='g', alpha=1)
#    plt.savefig('4MeV_2.png')
#def histo3(Energy):
#    plt.xlabel('Energie[MeV]')
#    plt.ylabel('Anzahl')
#    plt.title('#= 100000, bins= 30, Energy= 3 MeV')
#    plt.grid(True)
#    n, bins, patches = plt.hist(random_End_Energy(Energy,100000), 30, density=False, facecolor='g', alpha=1)
#    plt.savefig('3MeV_2.png')
#def histo4(Energy):
#    plt.xlabel('Energie[MeV]')
#    plt.ylabel('Anzahl')
#    plt.title('#= 100000, bins= 30, Energy= 2.9 MeV')
#    plt.grid(True)
#    n, bins, patches = plt.hist(random_End_Energy(Energy,100000), 30, density=False, facecolor='g', alpha=1)
#    plt.savefig('2_9MeV_2.png')
    
    
from multiprocessing import Process


def Main():
    Energy1 = 5.4
    Energy2 = 5.4
    Energy3 = 5.4
    Energy4 = 5.4
    
    p1 = Process(target=histo1,args=(Energy1,))
    p2 = Process(target=histo2,args=(Energy2,))
    p3 = Process(target=histo3,args=(Energy3,))
    p4 = Process(target=histo4,args=(Energy4,))
    
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    
    p1.join()
    p2.join()
    p3.join()
    p4.join()
if __name__ == '__Main__':
    Main()
import time
start_time = time.time()
Main()
print("--- %s seconds ---" % (time.time() - start_time))
