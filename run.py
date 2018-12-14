# -*- coding: utf-8 -*-
''' SOAC project glacier
Niek collot d'escury & Anneke Vries
'''
from timeit import default_timer as timer
start = timer()

import numpy as np
import importlib as im

import running_functions as rf
import plotting_functions as pf

im.reload(pf)
im.reload(rf)

directory = pf.directory 

###############################################################
# Constants
###############################################################

RHOI    =  912              # kg/m3
RHOW    =  1030             # kg/m3
G       =  9.8              # m/s2
N       =  3                # glens flow law exponent
DX      =  200              # m
L       =  50000            # m
W       =  40000
DT_days = 0.5
DT      =  24*3600*DT_days  # s
A       =  1e-24            # ice flow parameter
As      =  130
n       =  L//DX            # length shelf

###############################################################
# Initial conditions
###############################################################
u_rand_left   = 3.5e-5     # initial velocity  m/s (±1km/yr)
u_rand_right  = 3e-5       # final velocity    m/s (1km/yr)
h_left        = 600        # initial height    m 
h_right       = 200
bedrock_l     = -400
bedrock_r     = -800

h_initial      = np.linspace(h_left , h_right, n)            # initial gues for the velocity
u_initial      = np.linspace(u_rand_left , u_rand_right , n) # initial gues for the height

''' Linear bedprofile '''
bedrock        = np.linspace(bedrock_l , bedrock_r , n)


''' Non linear bedprofile '''
# x = np.arange(0 , n , 1)
# bedrock = y = y = 200 - 2.449093*x + 0.3359508*x**2 - 0.009628521*x**3 + 0.00007636045*x**4 - 1.837399e-7*x**5

###############################################################
# Variables
###############################################################
time          = int(1500 / DT_days)      # timesteps
gamma         = 0.3        # inertia


''' Constant influx '''
flux_cons = 50e-3 
flux_in = np.linspace(flux_cons , flux_cons , time)


###############################################################
# function
###############################################################
def run_code(flux_in):
    u = np.zeros([time , n])        # create matrix with time rows and length collumns
    h = np.zeros([time , n])        # create matrix with time rows and length collumns
    s = np.zeros([time , n])
    grounding_line = np.zeros(time)
    flow_dif       = np.zeros(time) 
    
    
    h[0,:] = h_initial              # intial values determined by intial flow 
    u[0,:] ,s[0,:] , grounding_line[0] = rf.u_func(u_initial , h[0, :] , 
                                        flux_in[0], bedrock ,As , DX , n , A) 
    
    flow_dif[0] = h[0 ,-1]*u[0 , -1]*W - (flux_in[-1]*W) 
    ''' loop for number of timesteps '''
    t=0
    t_plot = 0
    stability_count = 0
    
    while t < time-1:   

        h[t+1, :]  = rf.runt(u[t, :], h[t, :] , flux_in[t] , 
                      bedrock ,As , DX , n , A , DT , gamma)
        # h[t+1, :]  = euler(u[t, :], h[t, :])
        
        u[t+1, :] , s[t+1 ,:] , grounding_line[t+1] = rf.u_func(u_initial , h[0, :] , 
                                                        flux_in[0], bedrock ,As , DX , n , A)
        
        

        t        += 1
        t_plot   += 1
        
        outflow = h[t ,-1]*u[t , -1]*W
        flow_dif[t] = outflow - (flux_in[-1]*W) 
        if abs(flow_dif[t]) <= 0.02:
            
            stability_count +=1
            if stability_count == (int(10/DT_days)):
                t +=1e7

                print ("stability")
        
        
        percentage = t / time * 100
    
        if t%1000 ==0:
            run_duration = timer()
            print (" {} steps :{:.2f}".format(t,  run_duration - start))
        
       
        
    return u , h , s , grounding_line , flow_dif , t_plot

u , h , s , grounding_line , flow_dif , t_plot = run_code(flux_in)


# fn = np.loadtxt(directory + 
#                 "/output_SOAC_A_1e-{}_As_{}_DT_0.5_T_100000.0_DX_200_fluxin_{}.txt"
#                 .format(24,130,0.05))
# 
# flow_dif       = fn[0,:]
# grounding_line = fn[1,:]
# 
# t_plot = len(grounding_line)
    
    
time_axis = np.linspace(0 , t_plot*DT_days , t_plot)                       # time axis for plots 
###############################################################
# Plot u, h, flow difference and grounding line
##############################################################
pf.plot(h[0:t_plot] , "Height (m)" , "Elevation shelf" ,s[0:t_plot] 
        , True , grounding_line , t_plot,DT_days, n , DX ,bedrock )
pf.plot(3600*24*365*u[0:t_plot] ,"speed (m/yr)" , "Velocity" ,s[0:t_plot] 
        , False , grounding_line  , t_plot,DT_days, n , DX ,bedrock )



pf.plot_simpel(time_axis, flow_dif[0:t_plot] *24*365*3600*RHOI / (10e12), 
            "Evolution flux balance" , r"$\Delta$ flux (GT/yr)"
            ,"Time days (days)" , False , "nothin" , "darkgreen")

pf.plot_simpel(time_axis ,grounding_line[0:t_plot] * (DX/1000), "Evolution grounding line" , 
            "Distance to influx (km)", "Time (days)" , True , 
            "Initial flux: {:.2f} in GT/yr"
            .format(flux_in[0]*W*24*365*3600*RHOI / (10e12)) , "darkblue")


###############################################################
# make gif
###############################################################
# always first adjust plot code to save individual figures!!!!!!!!!!!!
# pf.make_gif(files_h , height)
# pf.make_gif(files_v , velocity) 
 
 
 
###############################################################
# savetxt for gemini run
###############################################################
# directory = "/home/students/6256481/"
# np.savetxt( directory + "output_gf_SOAC_A_{}_As_{}_DT_{}_T_{}_DX_{}_fluxin_{}.txt" .format(A ,
#             As , DT_days , time * DT_days , DX , flux_cons),        
#             (flow_dif[0:t_plot] , grounding_line[0:t_plot]))
# np.savetxt( directory + "output_h_SOAC_A_{}_As_{}_DT_{}_T_{}_DX_{}_fluxin_{}.txt" .format(A ,
#             As , DT_days , time * DT_days , DX , flux_cons),        
#             (h[0,:] , h[t])) 
 

end = timer()
print ("Time elapsed: {}".format(end-start)) 