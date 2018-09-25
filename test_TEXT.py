# option to annotate text to points in the figure with possible arrow for indication

# This document should make a polyfit 
# import packages
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as sc
# import modules
import databases as db

# import data
ice = db.ice
sst = db.sst
pres = db.yearly_average
time = db.time


# make a function to make beautiful?!?!?!?!?! graphs
def pca(x_var,y_var, x_axis, y_axis, title) :
    
    # calculate trend
    z = np.polyfit(x_var, y_var, 1)
    T = np.poly1d(z)

    # Slope and R-value
    slope, intercept, r_val, p_val, stderr = sc.linregress(x_var, y_var)
    
    # location text in plot
    x = 0.71
    y = 0.3
    
    # plt.text(x, y+3*dy,"Slope  = {: .2f}" .format(slp))
    # plt.text(x, y+4*dy,"R  = {: .2f}" .format(r_val))
    
    # plt.gcf().text(0.4, 0.1, "Slope  = {: .2f}" .format(slp), fontsize=14)


    # make plot
    fig, x1 = plt.subplots()
    x1.scatter(x_var,y_var, color = 'darkblue')
    x1.plot(x_var,T(x_var), "red")
    # set grid
    x1.grid()
    
    # set graph parameters
    plt.subplots_adjust(right=0.7)      #create space to the right of the graph 
    plt.subplots_adjust(left=0.16)      # create space to the left of the graph
    fig.set_figwidth(10)                # set figure width
    fig.set_figheight(4)                # set figure heigth
    
    #plot text in a box next to the graph
    plt.gcf().text(x , y, "Slope = {0: .2f}\nR-value = {1: .2f}".format(slope, r_val), fontsize = 13, bbox=dict(facecolor='black', edgecolor = 'black', boxstyle = 'round', alpha=0.2))

    #plot labels and title
    plt.xlabel(x_axis, fontsize = 12 , style = 'italic')
    plt.ylabel(y_axis, fontsize = 12, style = 'italic')
    plt.title(title, fontsize = 14, fontweight = 'bold', style= 'italic')
    
    dx = (max(x_var) - min(x_var)) /  len(x_var)
    
    for i in range(5, 11):
        x1.annotate(("{:.2f}, {:.2f}" .format(x_var[i], y_var[i])), xy = (x_var[i] , y_var[i]) , xytext = (((x_var[i]) + dx) , y_var[i]) )
    
    x1.annotate(("{:.2f}, {:.2f}" .format(x_var[-1], y_var[-1])), xy = (x_var[-1] , y_var[-1]) , xytext = (((x_var[-1]) + (10*dx)) , y_var[-1]), arrowprops=dict(facecolor='black', shrink=0.07) )
    
    
    path = '/Users/niekcollotdescury/Desktop/'
    fig_name = '{}' .format(title)
    plt.savefig(path + fig_name)
    
    plt.show()
    

    
    # end function

# pca(sst, pres, 'Time (yr)', 'J.J.A. average pressure (Pa)', "pressure time series")

plt.plot([1,2,3,4,5,6], [2,3,4])
plt.show()
