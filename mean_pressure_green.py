#project 2 dynamical metereology

# from pylab import *
# import datetime
# import time

from scipy import stats
import numpy as np

import netCDF4 as netcdf
import matplotlib.pyplot as plt


fh = netcdf.Dataset('/Users/niekcollotdescury/Desktop/Meteo/project 2/Databases/pres_mean_greenland')

mean_pres = fh['pres'][:]                     # mean pressure for the world 
mean_pres = (mean_pres[: , 0:24 , 112:136])   # mean pressure for Greenland

# chosen months
min_month = 5         # from june
max_month = 8         # to august

#create a list with the number of years in the databases
years = [] 
num_years = 2017-1979                # number of years         
for i in range(num_years + 1):
    month_1 = min_month + 12 * i     # add 12 months for every year
    month_2 = max_month + 12 * i     # add 12 months for every year
    years.append([month_1, month_2])

# create a list with the years and the yearly 
# averaged pressures for the chosen months
dates = []
yearly_average = []
for j in range(len(years)):
    mr = years[j]                   # pick the months for every year 
    
    dates.append(1979 + j)          # list with the years
    # add the dates and calculate the means for every years
    yearly_average.append([(np.mean(mean_pres[mr[0]:mr[1], :,:]))])

# start = 1970
# end = 2020
# L = (end - start) + 1
# 
fit = np.polyfit(dates, yearly_average, 1)
# p = np.poly1d(fit)
# x = np.linspace(start, end, L)



slope, intercept = np.polyfit(np.log(dates), np.log(yearly_average), 1)
slope1 = 0.0631
x = dates
y = yearly_average
#slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)

# To get coefficient of determination (r_squared)

# print ("r-squared:", r_value**2)

fig, (ax1,ax2) = plt.subplots(2,1, sharex= True)
ax1.plot(dates, yearly_average)
ax1.set_xlabel("Time(yr)")
ax1.set_ylabel("Sea level pressure (pa)")

ax2.plot(dates, fit[0] * dates + fit[1], color = 'red')
ax2.scatter(dates, yearly_average)
ax2.set_xlabel("Time(yr)")
ax2.set_ylabel("Sea level pressure (pa)")
ax2.text(2012, 96800, "s = {:.3f}" .format(slope1))

ax1.axes.grid()
ax2.axes.grid()
# plt.savefig('/Users/niekcollotdescury/Desktop/Meteo/project 2/plots/meansurfacepresa00')
fig.set_figheight(5)
fig.set_figwidth(6)
plt.tight_layout()
plt.show()


     


