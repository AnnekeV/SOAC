# Exercise 1.14 Atmospheric Dynamics 2018 (page 96): 
# http://www.staff.science.uu.nl/~delde102/AtmosphericDynamics[2018]Ch1.pdf

# https://docs.python.org/2.7/
# IMPORT MODULES
import numpy as N  # http://www.numpy.org
import matplotlib.pyplot as P   # http://matplotlib.org
import math as M  # https://docs.python.org/2/library/math.html
import matplotlib as mpl


path = "C:\\Users\\annek\\Documents\\2018-2019\\SOAC\\"

mpl.rcParams["figure.figsize"]   = 8.4, 5.8   # figure size in inches


# PARAMETER VALUES
dt = 1800.0 # time step in s  original 360 en 480
tmax = 96 # max. number of time steps in an integration 1440/60; 360/240
omega = 0.000072792  # angular velocity Earth [s^-1]
lat = 52 # latitude of IJmuiden in degrees
pi = 3.14159
phi = 0.0 # phase of the pressure gradient 
ro = 1.25 # density
A = 0.001 # Pa/m
phase = 0.0 # phase of surface pressure gradient in time
fcor = 2 * omega *  M.sin(lat * pi/180)  # Coriolis parameter
C1= - (A/(fcor*ro)) * ( (M.pow(omega,2) /(M.pow(fcor,2) - M.pow(omega,2))) + 1)
C3 = A * omega /(ro*(M.pow(fcor,2) - M.pow(omega,2)))

#  DEFINE time, u, v and the analytical solution, u_ana as arrays and fill them with zero's 
time = N.zeros((tmax))
time_axis = N.zeros((tmax))
u = N.zeros((tmax))# x-component velocity
v = N.zeros((tmax))# y-component velocity
u_ana = N.zeros((tmax))# analytical solution x-component velocity

# INITIAL CONDITION (t=0) : atmosphere in rest
t = 0
time[t] = 0
time_axis[t] = 0
u[t] = 0
v[t] = 0
u_ana[t] = 0

# TIME LOOP EULER FORWARD SCHEME
for t in range(len(time)-1): 
 du = dt * ((fcor*v[t]) - ((A/ro)* M.cos((omega*time[t])+phase)))
 dv = -dt * fcor * u[t]
 time[t+1] = time[t]+dt 
 u[t+1] = u[t] + du
 v[t+1] = v[t] + dv	
 u_ana[t+1] = (C1 * M.sin(fcor * time[t+1])) + ( C3* M.sin((omega * time[t+1]) + phase) )

for t in range(len(time)):
 time_axis[t] = time[t] / 3600.
 
# MAKE PLOT of evolution in time of u and u_ana
P.plot(time_axis, u_ana, color='black')
P.plot(time_axis, u, color='red')
P.axis([0,time_axis[tmax-1],-25.0,25.0])  # define axes 
P.xticks(N.arange(0,time_axis[tmax-1],6), fontsize=12) 
P.yticks(N.arange(-25.0,25.0,5), fontsize=12) 
P.xlabel('time [hours]', fontsize=14) # label along x-axes
P.ylabel('u [m/s]', fontsize=14) # label along x-axes
P.title('Exercise 1.14 DYME') # Title at top of plot
P.text(1, 23, 'u (analytical solution): black line', fontsize=10, color='black')
P.text(1, 21, 'u (numerical solution): red line (forward time difference scheme)', fontsize=10, color='red')
P.grid(True)
P.tight_layout()
P.savefig(path + "SeabreezeSimulation_dt_tmax.png") # save plot as png-file
P.show() # show plot on screen
