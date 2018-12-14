#plotting and stuff
# -*- coding: utf-8 -*-
''' SOAC project glacier
Niek collot d'escury & Anneke Vries
'''
""" Import modules """
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import gc
import imageio
import importlib as im

###############################################################
# Import module with plotting parameters
###############################################################

import sys
sys.path.insert(0,"/Users/niekcollotdescury/Documents/code/")
import plotting_parameters as pm
im.reload(pm)

directory = "/Users/niekcollotdescury/Desktop/SOAC/project"

###############################################################
# Functions
###############################################################
def box(text , x , y , ax , color):
    props = dict(boxstyle='round', facecolor=color, alpha=0.5)
    plt.text( x, y  , text 
    , transform = ax.transAxes,
    bbox = props ,size = 14 , style = "italic" , weight = "bold")    


''' lists for file names to be used in the GIF function '''
files_h = []
files_v = []
def plot(X , ylabel, title ,s , bolean , grounding , run_time , DT_days , n, DX , bedrock):
    """Plot function with given 
    variable, ylabel and title, surface height, 
    boolean for bedrock, position grounding line,
    timesteps, DT_days , n (size matrix) , DX , bedrock"""
    

    ''' color schemes for velocity and ice '''
    colors_v = mpl.cm.gist_rainbow(np.linspace(0, 1 , int(run_time)))    # colors velocity
    colors_i = mpl.cm.gist_rainbow(np.linspace(0, 1 , int(run_time)))        # colors ice bottom and surface
    
    ''' sinus wave for wave for water level '''
    n_list = np.arange(0 , n ,1)
    sea_level = 10 * np.cos(2 * np.pi *n_list /10)
    
    ''' Plot all time evolutions in one figure '''
    fig, ax =  plt.subplots()
    ax = fig.add_axes([0,0,1,1])    # add axis for position textbox
    
    ''' x array and y array for the filling of the figure '''
    fill_x = np.linspace(0 , n*DX , n)/1000
    fill_bottom_bedrock = np.linspace(bedrock[-1] , bedrock[-1] , n)
    x_grid = np.linspace(0 , n*DX , n)/1000
    
    for i in range(0 , run_time , (run_time // 5)-1):# max(1 , time//5 -1)) :
        if bolean == True:
            # fig , ax = plt.subplots()
            # ax = fig.add_axes([0,0,1,1])
            ''' plot water between sea surface and bedrock and plot sea level'''
            ax.fill_between(fill_x , sea_level , bedrock , color = 'blue')
            # ax.plot(np.linspace(0, n , n) , sea_level , color = 'cornflowerblue' , linewidth = 1)  

            ''' filled plot bedrock and ice'''
            ax.fill_between(fill_x ,bedrock , fill_bottom_bedrock, color = 'peru')                  
            ax.fill_between(fill_x , s[i,:] , (s[i,:]-X[i,:]) , color = 'deepskyblue')
            
            ''' plot ice surface line and bottom ice line '''
            ax.plot(x_grid , s[i, :] , color = colors_i[i] , label = "Thickness: t = {}".format(i)) 
            ax.plot(x_grid , (s[i,:]-X[i,:]) , color = colors_i[i] ) 
            plt.yticks(np.arange(-600 ,400 , 100 ))
            
            ''' Show position grounding line with arrow to text box '''
            # ax.plot([floating , floating] , [(s[i,floating]-X[i,floating]) , s[i , floating]], linestyle = '--' , linewidth = 3 , color = 'black')
            # plt.arrow(floating-10 , s[i , floating]+300 , +9 , -270 , head_width = 4 , head_length = 25)
            
            ''' Create textbox just outisde figure for starting date and finishing date '''
            # box("Bedrock" , 0.2 , 0.2 , ax , "peru")
            # box("Ice" , 0.3 , 0.6 , ax , "deepskyblue")
            # box("Water" , 0.9 , 0.1 ,ax , "blue")
            # box("Grounding line" , 0.7 , 0.8 , ax , "white")
            
            plt.legend(bbox_to_anchor=(1.1, 1))
            
            
            filename_h = "fig_{}".format(i)
            files_h.append(filename_h)
            # plt.savefig(directory + "/gif/figures/{}.png" .format(filename_h))
        

        
        else:
            # fig , ax = plt.subplots()
            # ax = fig.add_axes([0,0,1,1])            
            
            ax.plot(np.arange(0 , n*DX , DX)/1000 , X[i, :] , label = "t={}" .format(i) , color = colors_v[i])
            plt.legend()            
                                    
            filename_v = "fig_{}".format(i)
            files_v.append(filename_v)
            # plt.savefig(directory + "/gif/figures/{}.png" .format(filename_v))

            
    ''' figure settings '''
    plt.title(title)
    plt.xlabel("Length (km)" .format(DX))
    plt.ylabel(ylabel)
    
    plt.savefig(directory +"/figures/{}".format(title))
    plt.show()
    
def make_gif(files , name):
    images = []
    for filename in files:
        images.append(imageio.imread(directory + "/gif/figures/{}.png" .format(filename)))
    imageio.mimsave(directory + '/gif/gif_name.gif', images , duration = 0.00001)
    gc.collect() 

def plot_simpel(x , y , title , ylabel , xlabel ,boolean, tekst , color):
    """ Simpel plot function with x, y, title, ylabel, xlabel, boolean for tekst box, tekst, color """
    fig , ax = plt.subplots()
    ax = fig.add_axes([0,0,1,1])
    
    plt.plot(x, y , color = color)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if boolean == True:
        box(tekst , 0.5 , 0.2 , ax , color = 'black')
    plt.show()

 