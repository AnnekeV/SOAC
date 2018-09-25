#eigenvectors en shit

import importlib 

import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt
#import modules
import databases as db
import polyfit as pl

#reload modules because of possible adjustments to the modules
importlib.reload (db)
importlib.reload (pl)
#load data
sst = db.sst
ice = db.ice
pres = db.yearly_average
time = db.time
geop = db.geop

sst_r_val, sst_std, sst_ave, sst_var  =  pl.r_val(time, sst)
sst_norm = (sst- sst_ave)/ sst_std
sstnorm_r_val, sstnorm_std, sstnorm_ave, sstnorm_var  =  pl.r_val(time, sst_norm)

ice_r_val, ice_std, ice_ave, ice_var  =  pl.r_val(time, ice)
ice_norm = (ice - ice_ave) / ice_std
icenorm_r_val, icenorm_std, icenorm_ave, icenorm_var  =  pl.r_val(time, ice_norm)

pres_r_val, pres_std, pres_ave, pres_var  =  pl.r_val(time, pres)
pres_norm = (pres - pres_ave) / pres_std
presnorm_r_val, presnorm_std, presnorm_ave, presnorm_var  =  pl.r_val(time, pres_norm)

geop_r_val, geop_std, geop_ave, geop_var  =  pl.r_val(time, geop)
geop_norm = (geop - geop_ave) / geop_std
geopnorm_r_val, geopnorm_std, geopnorm_ave, geopnorm_var  =  pl.r_val(time, geop_norm)


# r_values (correlation values) for eigenvectors and eigenvalues
sst_sst, df ,df ,dg = pl.r_val(sst_norm, sst_norm)
ice_ice, df ,df ,dg = pl.r_val(ice_norm, ice_norm)
pres_pres, df ,df ,dg = pl.r_val(pres_norm, pres_norm)

geop_geop, df ,df ,dg = pl.r_val(geop_norm, geop_norm)
sst_geop, df ,df ,dg = pl.r_val(sst_norm, geop_norm)
ice_geop, df ,df ,dg = pl.r_val(ice_norm, geop_norm)

sst_ice, df ,df ,dg = pl.r_val(sst_norm, ice_norm)
sst_pres, df ,df ,dg = pl.r_val(sst_norm, pres_norm)
ice_pres, df ,df ,dg = pl.r_val(ice_norm, pres_norm)

# # matrix of r-values
matrix = [[sst_sst, sst_pres, sst_ice], [ sst_pres, pres_pres, ice_pres],[ sst_ice, ice_pres, ice_ice]]

matrix1 = [[sst_sst, sst_geop, sst_ice], [ sst_geop, geop_geop, ice_geop],[ sst_ice, ice_geop, ice_ice]]

# w = eigen values (not per se in right order)
# v = eigen vectors such that the column v[:,i] is the eigenvector corresponding to the eigenvalue w[i]
w, v  = LA.eig(matrix1)       
w_perc = w/sum(w)*100     # relative contributions to total variance
v1 = v[:, 0]               # first eigenvector  (54% of variance)    3 numbers represent the three variables              
v2 = v[:, 1]

print (w)
print (v)

# matrix time_series data
matrix_data = np.array([sst_norm, pres_norm, ice_norm])
matrix_data = matrix_data.transpose(1, 0 )

matrix_data1 = np.array([sst_norm, geop_norm, ice_norm])
matrix_data1 = matrix_data1.transpose(1, 0 )



#projection eigenvectors on data
proj =np.dot(matrix_data1, v[:, 0:2])
pca1 = proj[:,0]



# polyfit and plot of pca 1
pl.pca(pca1, sst, 'First principal component', 'Sea surface temperature ($^oC$)', 'Correlation between first principal component \n and sea surface temperature ')
pl.pca(pca1, ice, 'First principal component', 'Ice extent ($10^6 km^2$)', 'Correlation between first principal component \n and ice extent')
pl.pca(pca1, pres, 'First principal component', 'J.J.A. pressure (Pa)', 'Correlation between first principal component \n and pressure')
pl.pca(pca1, geop, 'First principal component', 'Geopotential height 200mb (m)', 'Correlation between first principal component \n and geopotential height')


# plot of the first principal component analyses in time
fig, ax1 = plt.subplots()
ax1.scatter(time, pca1, color = 'darkblue')

ax1.set_xlabel('Time (yr)', fontsize = 14 , style = 'italic')
ax1.set_ylabel('Amplitude of the first\nprincipal component', fontsize = 14 , style = 'italic')
plt.subplots_adjust(left=0.16)      # create space to the left of the graph
plt.title('Projection of the First\nprincipal component', fontsize = 14, fontweight = 'bold', style= 'italic')

ax1.annotate(("{:.2f} $10^6$ km$^2$" .format(ice[10])), xy = (time[10] , pca1[10]) , xytext = ((time[5]) , 2), arrowprops=dict(color='red',  arrowstyle = '->') )
ax1.annotate(("{:.2f} $10^6$ km$^2$" .format(ice[-2])), xy = (time[-2] , pca1[-2]) , xytext = ((time[-17]) , 2.7), arrowprops=dict(color='red',  arrowstyle = '->') )
plt.grid()
plt.savefig('/Users/niekcollotdescury/Desktop/Meteo/project 2/plots/Projection of the First principale component')
plt.show()





