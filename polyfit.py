# This document should make a polyfit 
# import packages
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as sc
# import modules
import databases as db

# import data
# ice = db.ice
# sst = db.sst
# pres = db.yearly_average
# time = db.time

linewidth = 3
figwidth = 15
figheight = 6
left = 0.16
right = 0.7


# make a function to make beautiful?!?!?!?!?! graphs
def pca(x_var,y_var, x_axis, y_axis, title) :
    
    # calculate trend
    z = np.polyfit(x_var, y_var, 1)
    T = np.poly1d(z)

    # Slope and R-value
    slope, intercept, r_val, p_val, stderr = sc.linregress(x_var, y_var)
    
    # location textbox in plot
    x = 0.71
    y = 0.3
    
    # make plot
    fig, x1 = plt.subplots()
    x1.scatter(x_var,y_var, color = 'darkblue')
    x1.plot(x_var,T(x_var), "red", linewidth = linewidth)
    
    # set grid
    x1.grid()
    
    # set graph parameters
    plt.subplots_adjust(right= right)      #create space to the right of the graph 
    plt.subplots_adjust(left= left)      # create space to the left of the graph
    fig.set_figwidth(figwidth)                # set figure width
    fig.set_figheight(figheight)                # set figure heigth
    
    #plot text in a box next to the graph
    plt.gcf().text(x , y, "Slope = {0: .2f}".format(slope), fontsize = 18, bbox=dict(facecolor='black', edgecolor = 'black', boxstyle = 'round', alpha=0.2))

    #plot labels and title
    plt.xlabel(x_axis, fontsize = 22 , style = 'italic')
    plt.ylabel(y_axis, fontsize = 22, style = 'italic')
    plt.title(title, fontsize = 22, fontweight = 'bold', style= 'italic')
    
    plt.tick_params(labelsize=20)
    
    #save figure in correct file
    path = '/Users/niekcollotdescury/Desktop/Meteo/project 2/plots/pca_correlation/'
    fig_name = '{}' .format(title)
    plt.savefig(path + fig_name)
    
    plt.show()
    # end function
    
def time_plot(time,y_var, x_axis, y_axis, title) :
    
    # calculate trend
    z = np.polyfit(time, y_var, 1)
    T = np.poly1d(z)
    
    # # create standard deviation, average, variance 
    std = np.std(y_var)
    ave = np.mean(y_var)
    var = np.var(y_var)
    
    # Slope, intercept, R_value
    slope, intercept, r_val, p_val, stderr = sc.linregress(time, y_var)
    
    # location textbox in plot
    x = 0.71
    y = 0.3
     
    # make plot
    fig, x1 = plt.subplots()
    x1.scatter(time,y_var, color = 'darkblue')
    x1.plot(time,T(time), "red", linewidth = linewidth)
    # set grid
    x1.grid()

    # set graph parameters
    plt.subplots_adjust(right=right)      #create space to the right of the graph 
    plt.subplots_adjust(left= left)      # create space to the left of the graph
    fig.set_figwidth(figwidth)                # set figure width
    fig.set_figheight(figheight)                # set figure heigth  
    
    #plot text in a box next to the graph
    plt.gcf().text(x , y,     "Standard deviation  = {0: .2f}\nMean  = {1: .2f}\n"
    "Variance = {2: .2f}\nSlope = {3: .2f}\nR-value = {4: .2f}" 
    .format(std, ave, var, slope, r_val), fontsize = 14, bbox=dict(facecolor='black', edgecolor = 'black', boxstyle = 'round', alpha=0.2))

    # plot the axis labels and title
    plt.xlabel(x_axis, fontsize = 16 , style = 'italic')
    plt.ylabel(y_axis, fontsize = 16, style = 'italic')
    plt.title(title, fontsize = 18, fontweight = 'bold', style= 'italic')
    
    # save figure
    path = '/Users/niekcollotdescury/Desktop/Meteo/project 2/plots/Time_series/'
    fig_name = '{}' .format(title)
    plt.savefig(path + fig_name)
    
    plt.show()

    # end function

    
def r_val(x_var ,y_var) :
    
    # calculate trend
    z = np.polyfit(x_var , y_var, 1)
    T = np.poly1d(z)
    
    std = np.std(y_var)
    ave = np.mean(y_var)
    var = np.var(y_var)
    
    # R value 
    slope, intercept, r_val, p_val, stderr = sc.linregress(x_var, y_var)
    
    return r_val, std, ave, var
    
    


    
    
    
