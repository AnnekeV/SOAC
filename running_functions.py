#plotting and stuff
# -*- coding: utf-8 -*-
''' SOAC project glacier
Niek collot d'escury & Anneke Vries
'''

import numpy as np

RHOI    =  912              # kg/m3
RHOW    =  1030             # kg/m3
G       =  9.8              # m/s2
N       =  3                # glens flow law exponent


def eps(u , n , DX):
    """Calculate epsilon for eta with given:
    u, n (matrix size) , DX """
    epsilon     = np.zeros(n-1)     # define eps at i+1/2
    for i in range (0 , n-1):
        epsilon[i] = 0.5 * ((u[i+1] - u[i]) / (DX))**2
        if epsilon[i]<1e-50: epsilon[i] =  1e-50    # set minimum value for epsilon
    return epsilon
    
def func_eta(u , A , n , DX):
    """Calculate eta with epsilon with given:
    u , A (stiffness shelf) , n (matrix size) , DX """
    X = eps(u , n , DX)
    eta = 0.5 * A**(-1 /N)* X**((1-N) / (2*N))      # eta i+0.5
    return eta


def u_constants(u, h , n , BETA , DX , A):
    """Calculate the constants for the sparce matrix with given 
    u, h , n (matrix size) BETA (friction) , DX , A (stiffness shelf)"""
    eta =    func_eta(u , A , n , DX)
    
    c1 =np.zeros(n)
    c2 =np.zeros(n)
    c3 =np.zeros(n)
    
    for i in range(1, n-1):
        
        ''' The average of h[i] + h[i+1]/[i-1] as h[i+/ - 1/2] '''
        h_plus      = (h[i] + h[i+1]) / 2
        h_min       = (h[i-1] + h[i]) / 2
        
        ''' calculate the constants'''
        c1[i]       = 4  * (eta[i] * h_plus) / DX**2
        c2[i]       = - 4 * ((eta[i] * h_plus) + (eta[i-1] * h_min)) / DX**2 - ( BETA[i])
        c3[i]       = 4  * (eta[i-1] * h_min) / DX**2
    

    ''' Dynamic boundary condtion '''
    c3[-1] = -eta[-1] 
    c2[-1] = eta[-1]

    c2[0]  = h[0]          # Kinematic boundary conditions (incomming flux)

    return c1 ,c2, c3
    
def spar(u,  h , BETA , n , DX , A):
    """Fill the sparce matrix with given:
    u, h ,BETA , n (matrix size) , DX , A """

    c1,c2,c3 =u_constants(u,h , n , BETA , DX , A)
    matrix = np.zeros([n, n])

    for i in range(0,n-1):  # i is number of rows
        
        matrix[i+1 , i]    = c3[i+1]
        matrix[i , i  ]    = c2[i]  
        matrix[i , i+1]    = c1[i]
    matrix[-1,-1] = c2[-1]
    
    sparse = np.linalg.inv(matrix) # use np to inverse the matrix 
    return sparse
  
 
def u_func(u , h, flux_in , bedrock ,As , DX , n , A):
    """Calculate the u velocity from the the height above 
    sea level and the matrix given:
    u,h , incomming flux, bedrock ,As (sliding parameter)
    DX, n (matrix size) , A stiffness glacier
    new = l+1, old = l"""   
    
    ''' Calculate weight of ice, grounding line and height above water '''
    s_water = (1-(RHOI / RHOW))* h        # calculate height of shelf above water when floating
    
    s = np.zeros(len(s_water))            # array for height above water         
    float_cons = np.zeros(len(s_water))   # factor to calculate bouyancy/BETA
    floating = []                         # list with all indices with floating ice
    for i in range(len(s)):
        
        # check max between floating fraction and height above bedrock:
        s[i] = max((h[i] + bedrock[i]) , s_water[i])  
        
        
        if (h[i] + bedrock[i] - s_water[i]) < 0:  # check if ice is floating
            floating.append(i)                    # append all indices for floating ice
        else:
            float_cons[i] = min(1 , s[i]/h[i])    # if grounded ice calculate fraction above water
        
    ''' Bottom friction dependend on weight of ICE'''
    BETA = As * RHOI * G*h - RHOW*(1-float_cons)*G 
    BETA[floating] = 0              # friction is zero when floating
    
    ''' Calculate forcing '''
    s_cons = np.zeros(n)                 # Driving force 
    s_cons[0]  = flux_in                 # initial driving force derived from incoming flux
    
    # driving force for left/dynamic boundary
    h_min =  (h[-1] + h[-2]) / 2
    s_cons[-1] = (h[-1]**2 * DX *RHOI * G / (8 * h_min)) *(1 - (RHOI / RHOW))
    
    # driving force for all non boundary positions
    for i in range(1 , n-1):
        s_cons[i] = RHOI * G * h[i] *((s[i+1] - s[i-1])/ (2* DX))       # use central difference scheme

    u_old = u              # choose old/given value as gues u value to be iterated
    u_new = np.zeros(n)    # determine length new u velocity
    

    
    check = 1              # check difference (du/u) next iteration for 1% difference
    count= 0               # counter to check if while loop is stuck stop >100
    while check>0.01 and count < 100:  
        
        ''' define u_new '''
        sparse = spar(u_old, h , BETA , n , DX , A) # call sparcs matrix function with u_old, h, BETA
        u_new  = sparse.dot(s_cons)    # calculate new velocity from sparse matrix and driving force
        
        check = np.max(abs((u_new - u_old) / u_old))   # du/u for the check
        count +=1                                      # counter raise
        u_old = u_new                                  # update u_old

    return u_new , s , floating[0]
    

def euler(u_old , h_old , gamma , n , DX , DT ):
    """Apply the euler forward scheme given:
    u, h, gamma (inertia), n (matrix size) , DX , DT
    new = t+1, old = t""" 

    h_new    = np.zeros(n)                    # h[t+1, :]
    ''' continuity equation to calc h[t+1, :] '''
    for i in range(1 , n-1):
        h_new[i] = h_old[i] + DT * ((u_old[i-1] * h_old[i-1] 
                   - u_old[i+1] * h_old[i+1]) / (2*DX))     # apply central difference scheme
    
    ''' fill the first and final value for h[t+1, 0/-1] 
        with given equation (WJ) ''' 
    h_new[0]  = gamma*h_old[0] +  (1- gamma)*(2*h_new[1] - h_new[2])              
    h_new[-1] = gamma*h_old[-1] + (1- gamma)*(2*h_new[-2] - h_new[-3])
    

    ''' remove negative height values '''
    zero_values = np.argwhere(h_new<0)
    for i in zero_values:
        h_new[i] = 0
    
    return h_new
    
    
def calc_h(u_old , h_old , DT_frac , n , DT , DX , gamma):
    """Apply the RK4 forward scheme given:
    u, h , DT_frac (size forward step) , n (matrix size) 
    , DT , DX , gamma (inertia)
    new = t+1, old = t""" 

    h_new    = np.zeros(n)                    # h[t+1, :]
    dh = np.zeros(n)
    
    ''' continuity equation to calc h[t+1, :] '''
    for i in range(1 , n-1):
        dh[i] =  DT * ((u_old[i-1] * h_old[i-1] 
                   - u_old[i+1] * h_old[i+1]) / (2*DX))     # apply central difference scheme
    
    h_new[1:-1] = h_old[1:-1] + dh[1:-1] * DT_frac
    
    ''' fill the first and final value for h[t+1, 0/-1] 
        with given equation (WJ) ''' 
    h_new[0]  = gamma*h_old[0] +  (1- gamma)*(2*h_new[1] - h_new[2])              
    h_new[-1] = gamma*h_old[-1] + (1- gamma)*(2*h_new[-2] - h_new[-3])
    

    ''' check for negative height values '''
    assert (min(h_new) >= 0)
   
    dh[0]  = (h_new[0] - h_old[0]) /DT_frac
    dh[-1] = (h_new[-1] - h_old[-1]) /DT_frac
    
    
    return h_new, dh
    
def runt(u , h , flux_in, bedrock ,As , DX , n , A , DT , gamma):
    
    
    h_R1,dh1 = calc_h(u , h , 0.5  , n , DT , DX , gamma)
    u1 , _ , _ = u_func(u , h_R1 , flux_in , bedrock ,As , DX , n , A)
    
    h_R2 , dh2 = calc_h(u1 , h , 0.5  , n , DT , DX , gamma)
    u2 , _ , _ = u_func(u1 , h_R2 , flux_in , bedrock ,As , DX , n , A) 
    
    h_R3 , dh3 = calc_h(u2 , h , 1 , n , DT , DX , gamma)
    u3 , _ , _ = u_func(u2 , h_R3 , flux_in , bedrock ,As , DX , n , A)
    
    h_R4, dh4 = calc_h(u3 , h , 1 , n , DT , DX , gamma)

    h_new = h + (1/6)*(dh1+ (2*dh2) + (2*dh3)+ dh4)

    return h_new
    
