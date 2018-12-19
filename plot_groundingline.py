""" Always on"""
import numpy as np
import importlib as im
import plotting_functions as pf
import matplotlib.pyplot as plt
im.reload(pf)

directory = pf.directory 

A       =  5e-23
RHOI    =  912              # kg/m3
W       =  40000


flux_in = np.array([1000, 600.0, 400.0, 300, 200, 150, 100, 80,60,  40, 20, 10], dtype = 'float')
flux_in *= 1e-3
eq_ground = []
t_plot    = []

for i in range(len(flux_in)): 
    fn = np.loadtxt(directory + 
                    "output/output_gf_SOAC_A_{}_As_130_DT_0.5_T_20000.0_DX_1000_fluxin_{}_BNL_high.txt"
                    .format(A, flux_in[i]))  
    flow_dif       = fn[0,:]
    grounding_line = fn[1,:]
    eq_ground.append(grounding_line[-1])
    
fig, ax =  plt.subplots()
ax = fig.add_axes([0,0,1,1])    # add axis for position textbox   
plt.plot(flux_in*W*24*365*3600*RHOI / (10e12), eq_ground,marker = '*', markersize = 13,   label = "high to low")

    
flux_in_low = np.array([10, 20, 40, 60, 80, 100, 150, 200, 300, 400] , dtype = 'float')
flux_in_low *= 1e-3
eq_ground = []
t_plot    = []
    
for i in range(len(flux_in_low)): 
    fn = np.loadtxt(directory + 
                    "output/output_gf_SOAC_A_{}_As_130_DT_0.5_T_8000.0_DX_1000_fluxin_{}_BNL_low.txt"
                    .format(A, flux_in_low[i]))  
    flow_dif       = fn[0,:]
    grounding_line = fn[1,:]
    eq_ground.append(grounding_line[-1])
    
plt.plot(flux_in_low*W*24*365*3600*RHOI / (10e12), eq_ground,marker = 'o', label = "low to high")


plt.title("Response grounding line to flux of ice ")
plt.xlabel("Flux (Gt/yr)")
plt.legend(loc = 4)
plt.ylabel("Grounding line (km)")
pf.box(("Ice flow parameter = {} ".format(A)), x=0.6, y=0.5, ax=ax, color = "grey")
plt.savefig(directory + "figures/grounding_line_vs_flux_A_{}.png".format(A))
plt.show()

