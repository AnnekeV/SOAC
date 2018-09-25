#project 2 dynamical metereology
#import packages

import importlib 
#import modules
import databases as db
import polyfit as pl

#reload modules because of possible adjustments to the modules
importlib.reload (db)
importlib.reload (pl)

sst = db.sst
ice = db.ice
pres = db.yearly_average
time = db.time
geop = db.geop


# plot pca
pl.pca(sst , ice , 'Sea surface temperature ($^oC$)' , 'Ice extent ($10^6 km^2$)' , 'Correlation between sea surface temperature\nand ice extent' )
# pl.pca(sst , pres, 'Sea surface temperature ($^oC$)', 'J.J.A. average pressure (Pa)' , 'Correlation between sea surface temperature\nand pressure ' )
# pl.pca(ice , pres, 'Ice extent ($10^6 km^2$)' , 'J.J.A. average pressure (Pa)', 'Correlation between ice extent and pressure' )
# with geop
pl.pca(sst , geop, 'Sea surface temperature ($^oC$)', 'Geopential height\n200mb (m)', 'Correlation between sea surface temperature\nand geopotential height')
# pl.pca(pres , geop, 'J.J.A. average pressure (Pa)', 'Geopential height\n200mb (m)', 'Correlation between pressure and\ngeopotential height')
pl.pca(ice , geop, 'Ice extent ($10^6 km^2$)', 'Geopential height\n200mb (m)', 'Correlation between ice extent\nand geopotential height')
# 
#  # plot time series
# pl.time_plot(time, pres, 'Time (yr)', 'J.J.A. average pressure (Pa)', "Pressure time series")
# pl.time_plot(time, ice, 'Time (yr)', 'Ice extent ($10^6 km^2$)', "Ice extent time series")
# pl.time_plot(time, sst, 'Time (yr)', 'Sea surface temperature ($^oC$)', "Sea surface temperatures time series")
# pl.time_plot(time , geop, 'Time (yr)', 'Geopential height 200mb (m)', 'Geopontetial height time series')

