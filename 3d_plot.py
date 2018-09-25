'''
======================
3D surface (color map)
======================

Demonstrates plotting a 3D surface colored with the coolwarm color map.
The surface is made opaque by using antialiased=False.

Also demonstrates using the LinearLocator and custom formatting for the
z axis tick labels.
'''

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

from matplotlib import animation


import numpy as np

import importlib 
#import modules
import databases as db
import polyfit as pl
# 
# #reload modules because of possible adjustments to the modules
# 
# 
# import databases as db
importlib.reload (db)
importlib.reload (pl)




# fig = plt.figure()
# ax = fig.gca(projection='3d')
# 
# def rotate(angle):
#     ax.view_init(azim = angle)
# 
# # Make data.
# X = db.lat
# Y = db.lon
# # X, Y = np.meshgrid(X, Y)
# R = np.sqrt(X**2 + Y**2)
# Z = db.ave_summer
# 
# 
# 
# # Plot the surface.
# surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
#                         linewidth=0, antialiased=False)
# 
# 
# 
# # Customize the z axis.
# ax.set_zlim(90000,  100100)
# ax.zaxis.set_major_locator(LinearLocator(10))
# ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
# 
# # Add a color bar which maps values to colors.
# fig.colorbar(surf, shrink=0.5, aspect=5)
# 
# 
# rot_animation = animation.FuncAnimation(fig, rotate, frames = np.arange(0, 362, 2), interval = 100)
# 
# 
# fig.set_figheight(10)
# fig.set_figwidth(10)
# fig.savefig('/Users/niekcollotdescury/Desktop/sdfwg')
# 
# rot_animation.save('/Users/niekcollotdescury/Desktop/wfwvwrvrv.gif', dpi=80,writer = 'imagemagick')
# plt.show()






x = np.linspace(280, 340 , 24)
y = np.linspace(65, 85 , 9)
X, Y = np.meshgrid(x, y)
plt.contourf(X, Y, db.ave_summer_1979 , cmap = plt.get_cmap('coolwarm'), vmin = 100560, vmax=102000)
plt.colorbar()
plt.xlabel('Longtitude')
plt.ylabel('Latitude')
plt.title('Contour plot pressure over Greenland 1979')

plt.savefig('/Users/niekcollotdescury/Desktop/UU/Meteo/project 2/plots/countourplot1979')
plt.show()

X, Y = np.meshgrid(x, y)
plt.contourf(X, Y, db.ave_summer_1990 , cmap = plt.get_cmap('coolwarm'), vmin = 100560, vmax=102000)
plt.colorbar()
plt.xlabel('Longtitude')
plt.ylabel('Latitude')
plt.title('Contour plot pressure over Greenland (1990)')

plt.savefig('/Users/niekcollotdescury/Desktop/UU/Meteo/project 2/plots/countourplot1990')
plt.show()

X, Y = np.meshgrid(x, y)
plt.contourf(X, Y, db.ave_summer_2000 , cmap = plt.get_cmap('coolwarm'), vmin = 100560, vmax=102000)
plt.colorbar()
plt.xlabel('Longtitude')
plt.ylabel('Latitude')
plt.title('Contour plot pressure over Greenland (2000)')

plt.savefig('/Users/niekcollotdescury/Desktop/UU/Meteo/project 2/plots/countourplot2000')
plt.show()

X, Y = np.meshgrid(x, y)
plt.contourf(X, Y, db.ave_summer_2014 , cmap = plt.get_cmap('coolwarm'), vmin = 100560, vmax=102000)
plt.colorbar()
plt.xlabel('Longtitude')
plt.ylabel('Latitude')
plt.title('Contour plot pressure over Greenland (2014)')

plt.savefig('/Users/niekcollotdescury/Desktop/UU/Meteo/project 2/plots/countourplot2014')
plt.show()





# plt.contourf(o_potential)
# plt.show()
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
