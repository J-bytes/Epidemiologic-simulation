# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 13:06:46 2020

@author: jonathan beaulieu-emond

Small World V 3.0. This code will attempt to simulate a small world version of a pandemic spread through a population
with an object-oriented approch to pythonic code
"""
import math

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from prerequisite import small_world_power_law, watts_strogatz,personne

#---------------------------------------------------------------------------
#global variables of the system
#global N,M,L,k,C,max_iter,n_sick,n_dead,n_healthy,maps


#======================================================================


#maps,G=watts_strogatz(N,C,P)
#maps,G=small_world_power_law(N,C,lambd)
#%%
"""
Initialisation of the grid and the walkers
"""

def grid_init(M,N,n_sick,L,P_infection,P_mortality,df,columns,advanced_feature,adherence) :
    """
    

    Parameters
    ----------
    M : integer
        Number of walkers in the network.
    N : integer
        Number of nodes in the network.
    n_sick : integer
        the number of sick indiviual at iteration 0
    L : integer
        The number of iteration once infected during which the person is contagious.
    P_infection : float
            The probability of getting infected if meeting a sick person
    P_mortality : float
            The probability of dying after "lifespan" iteration once sick.
    df : pandas dataframe
        A dataframe containing the values for the paramters defined by age groups
     columns : Array
        An array of dictionnary containing the column name for the pandas dataframe from the datatable
    advanced_feature : array
        an arry containing the keywords ["confine","restrict","masks","lockdown"] depending if the checkboxes are checked
    adherence : float
        The probability of a random individual in the population to respect the measures as defined in advanced_feture

    Returns
    -------
    grid : array
        An array giving the number of infected people in each node.
    rgrid : array
        An array contining the number of the first individual to "infect" a node. Used to estimate R
    walkers : array of class personne
        An arrray containing all of the walkers inside the newtork as object of class personne as defined in prerequisite.py.

    """
    grid=np.zeros(N)
    rgrid=np.zeros(N)
    walkers=[]
    if 'empty' in df :
        for i in range(0,M) :
            rx=np.random.randint(0,N-1)
            walkers.append(personne(rx,L,i+1,P_infection,P_mortality))
            
    else : #if advanced features has been activated
       numero=0
       for index, row in df.iterrows():
           nombre=int(int(row['proportion of population'])/100*M)
           infectiosite=float(row['infectiosity'])
           mortalite=float(row['mortality'])
           movements=float(row['movements'])
           age=row['Age']
           for i in range(0,nombre) :
               rx=np.random.randint(0,N-1)
               random_adherence=np.random.random()
               if random_adherence<adherence :
                   walkers.append(personne(rx,L,numero+1,infectiosite,mortalite,'healthy',age,movements,advanced_feature))
               
               else :
                   walkers.append(personne(rx,L,numero+1,infectiosite,mortalite,'healthy',age,movements))
               numero+=1
        
        
    while len(walkers)<M :
        walkers.append(personne(rx,L,numero+1,infectiosite,mortalite,'healthy',age,movements))
        
        
    #a patient zero(s) is randomly selected 
    jj=np.random.randint(0,M-1,size=n_sick)
    for i in jj :
        walkers[i].status="sick"
        grid[walkers[i].x]+=1
        rgrid[walkers[i].x]=walkers[i].number
    return grid,rgrid,walkers



"""

Loop that simulate the passage of time. At each iteration a loop on every walkers is made to ensure they are 
all moving.
"""
#@jit(parallel=True)
def epidemic(M,N,n_sick_original,max_iter,duree,maps,repetition, liste_sick,liste_health,liste_dead,P_infection,P_mortality,df=['empty'],columns=[],advanced_feature=[],adherence=0) :
    """
    this function takes empty lists ( liste_sick,liste_health,liste_dead) and fills them with the values of the simulation
    without explicitly returning them.

    Parameters
    ----------
   M : integer
        Number of walkers in the network.
    N : integer
        Number of nodes in the network.
    n_sick_original : integer
        the number of sick indiviual at iteration 0
    max_iter : integer
        The maximum number of iteration the simulation can run before shutting down
        to avoids running forever.
    duree : integer
        The number of iteration once infected during which the person is contagious.
    maps : dictionnary
        A dictionnary with all the nodes as key and the edges as values
    repetition : integer
       the number of repetition of the simulation for statistical analysis
    liste_sick : array of integers
        The number of sick individuals at each iterations
    liste_health :  array of integers
        The number of healthy individuals at each iterations
    liste_dead :  array of integers
        The number of dead individuals at each iterations
    P_infection : float
            The probability of getting infected if meeting a sick person
    P_mortality : float
            The probability of dying after "lifespan" iteration once sick.
    df : pandas dataframe
        A dataframe containing the values for the paramters defined by age groups. The default is ['empty'].
     columns : Array
        An array of dictionnary containing the column name for the pandas dataframe from the datatable. The default is [].
    advanced_feature : array
        an arry containing the keywords ["confine","restrict","masks","lockdown"] depending if the checkboxes are checked. The default is [].
    adherence : float
        The probability of a random individual in the population to respect the measures as defined in advanced_feture. The default is 0.
  
    Returns
    -------
    r0 : float
        The average number of person a sick individuals infects


    
    """
    r0=[]
    
    for i in range(0,repetition) :
        n_sick=n_sick_original
        n_dead=0
        n_healthy=M-n_sick
        grid,rgrid,walkers=grid_init(M,N,n_sick,duree,P_infection,P_mortality,df,columns,advanced_feature,adherence)
       
        iterate=0
       
        while (n_sick >=1) and (iterate < max_iter):
            for j in range(0,M) :
                walkers[j].update_pos(maps, grid,rgrid)
                n_healthy,n_sick,n_dead=walkers[j].update_status(maps,grid,rgrid,n_healthy,n_sick,n_dead)
            liste_health[i,iterate]=n_healthy
            liste_sick[i,iterate]=n_sick
            liste_dead[i,iterate]=n_dead
            iterate+=1
            #print("iteration {0}, sick {1}, dead {2}.".format(iterate,n_sick,n_dead))
            
            
         
        liste_infected_by=[]
        for w in walkers :
            liste_infected_by.append(w.infected_by)
            
        liste_infected_by=np.array(liste_infected_by)
        liste_infected_by=liste_infected_by[np.where(liste_infected_by!=0)]
        
        rliste=[]
        for j in range(0,M) :
            rliste.append(len(np.where(liste_infected_by==j)[0]))
        
        rliste=np.array(rliste)
        r0.append(np.mean(rliste[np.where(rliste!=0)]))
  
    return r0




n_iterate=2
N =15000 # lattice size
M =3800 # number of random walkers
L =20 # lifetime parameter
#k=L/2 #temps avant hospitalisation/apparition des symptômes
C=int(N/100) #Environ nombre de connection maximale
P=0.4
b=0.1 # interconnectivity parameters of small world. bigger means less connections
lambd=0.5
max_iter=100000 # maximum number of iterations
P_infection=0.8
P_mortality=0.8

if __name__ == '__main__': 
   
    
  
        n_sick_original=1
        n_repetition=2
        maps=nx.to_dict_of_lists(nx.Graph(nx.connected_watts_strogatz_graph(N,C,P)))

        liste_sick,liste_health,liste_dead=np.zeros((n_repetition,max_iter)),np.zeros((n_repetition,max_iter)),np.zeros((n_repetition,max_iter))
    
        r0=epidemic(M,N,n_sick_original,max_iter,L,maps,n_iterate, liste_sick,liste_health,liste_dead,P_infection,P_mortality)
       
        print(r0)
            
        #=====================Graphisme===============================
        limite=np.where(np.logical_or(liste_sick.mean(axis=0)==0,liste_dead.mean(axis=0)==M))[0][0]
        liste_sick,liste_health,liste_dead=liste_sick[:,0:limite],liste_health[:,0:limite],liste_dead[:,0:limite]
        x=np.arange(0,max_iter)[0:limite]
        y=np.mean(liste_sick,axis=0)
        
        yerr=np.std(liste_sick,axis=0)
        markers,caps,bars=plt.errorbar(x,y,yerr=yerr,fmt='.')
        [bar.set_alpha(0.2) for bar in bars]
        [cap.set_alpha(0) for cap in caps]
        
          
        
        y=np.mean(liste_health,axis=0)
        yerr=np.std(liste_health,axis=0)
        markers,caps,bars=plt.errorbar(x,y,yerr=yerr,fmt='.')
        [bar.set_alpha(0.2) for bar in bars]
        [cap.set_alpha(0) for cap in caps]
        
          
        
        y=np.mean(liste_dead,axis=0)
        yerr=np.std(liste_dead,axis=0)
        markers,caps,bars=plt.errorbar(x,y,yerr=yerr,fmt='.')
        [bar.set_alpha(0.2) for bar in bars]
        [cap.set_alpha(0) for cap in caps]
        plt.xlabel('Densité de population (marcheur par noeuds)')
        plt.ylabel('Durée moyenne de \'épidémie')
        #plt.ylabel("Nombre total de personne infectées")
        #End of the code 
