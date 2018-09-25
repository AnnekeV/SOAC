#databases
import numpy as np
import netCDF4 as netcdf

# import data 
path = '/Users/niekcollotdescury/Desktop/UU/Meteo/project 2/Databases/'

sst  = 'sst_retrieved_4_12.txt'
ice  = "N_09_extent_v3.0_sie.txt"
geop = 'geop_retrieved_16_1.txt'

prestest1 = 'mslp.mon.mean.nc'
fh1 = netcdf.Dataset(path + prestest1)    #mlsp


sst = np.loadtxt(path + sst) 
ice = np.loadtxt( path + ice, skiprows = 1) 
geop = np.loadtxt(path + geop)

#constants
index = -1
index1 = np.linspace(0 , 30, 31)


#get geop
geop = geop[:, 1]
geop = np.delete(geop , index1)
geop = np.delete(geop , index)

geop *= 10


# 

#get right information out of datafiles
#sea surface temperatures
sst = sst[:, 1]
sst = np.delete(sst, index1)

# ice extent
ice = ice[:, 1]
ice = np.delete(ice, index) 

#get the mean pressure from the file
mean_pres = fh1['mslp'][:]                     # mean pressure for the world 
mean_pres = (mean_pres[: , 2:11 , 112:136])   # mean pressure for Greenland

# prs = fh1['mlsp'][:]
# prs = prs
ave_summer_1979 = np.zeros((9,24))
ave_summer_1990 = np.zeros((9,24))
ave_summer_2000 = np.zeros((9,24))
ave_summer_2014 = np.zeros((9,24))
for i in range(9):
    for j in range(24):
        ave_summer_1979[i,j] = np.mean(mean_pres[5:8,i,j])
        ave_summer_1990[i,j] = np.mean(mean_pres[137:140,i,j])
        ave_summer_2000[i,j] = np.mean(mean_pres[257:260,i,j])
        ave_summer_2014[i,j] = np.mean(mean_pres[425:428,i,j])


# chosen lat and lon 
lat = fh1['lat'][0:24]
lon = fh1['lon'][112:136]


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


time = np.zeros(len(years))
yearly_average = np.zeros(len(years))
for j in range(len(years)):
    mr = years[j]                   # pick the months for every year 
    
    time[j] = (1979 + j)          # list with the years
    # add the dates and calculate the means for every years

    yearly_average[j] = ((np.mean(mean_pres[mr[0]:mr[1], :,:])))

     
time = np.delete(time, index)        
yearly_average = np.delete(yearly_average, index)


