# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 13:27:43 2020

@author: joeda
"""
import numpy as np
import networkx as nx
class personne:

    def __init__(self, x, lifespan,number,P_infection,P_mortality,status="healthy"):
        """
        This function defines the property of the object personne such as position(x), etc.

        Parameters
        ----------
        x : TYPE
            DESCRIPTION.
        status : TYPE, optional
            DESCRIPTION. The default is "healthy".
        lifespan : TYPE, optional
            DESCRIPTION. The default is L.
        walk_speed : TYPE, optional
            DESCRIPTION. The default is 1.
        age : TYPE, optional
            DESCRIPTION. The default is '10-24'.

        Returns
        -------
        None.

        """
  
        self.x = x # position
        self.number=number
        self.status = status # health status ("healthy","sick", "dead",")
       
        self.P_infection = P_infection 
        self.P_mortality = P_mortality 
        self.lifespan=lifespan
        self.infected_by=0
    
    def change_status(self, s):
        self.status = s

    @property
    def get_pos(self):
        return self.x
    @property
    def get_status(self):
        return self.status

    

    def update_pos(self,maps,grid,rgrid):
        """
        Update the position of the person based on the available destination as given by the map

        Parameters
        ----------
        maps : dictionnary of all the connection of each point in the type of the graph theory
        grid : array giving the number of infected people in each node

        Returns
        -------
        None.

        """
        
        if  self.get_status != "dead" and   self.get_status != "immune":
           
            connection=maps[self.x]
            a=np.random.randint(0,len(connection))
           
            
            if self.get_status=='sick' :
                grid[int(connection[a])] += 1
                grid[int(self.x)]        -= 1
                rgrid[int(connection[a])] += self.number
                rgrid[int(self.x)]        = 0
                
            self.x = connection[a]
            
            
       
            

    def update_status(self,maps,grid,rgrid,n_healthy,n_sick,n_dead):
            """
            This function verify the status of our person. If a sick person is present on the node at the same time, 
            the person will get sick too.
    
            Parameters
            ----------
            maps : dictionnary of all the connection of each point in the type of the graph theory.
            grid : array giving the number of infected people in each node.
    
            Returns
            -------
            None.
    
            """
         
            
            if self.status == "healthy" :
                
                if grid[int(self.x)]>0 : 
                    proba=np.random.random()
                    if proba<self.P_infection :
                        self.status="sick"
                        self.infected_by=rgrid[int(self.x)]
                        n_healthy-=1
                        n_sick+=1
                        
                
                
            if self.status == "sick" :
                
                self.lifespan-=1
                
                if self.lifespan<=0 :
                    
                    proba=np.random.random()
                    if proba<self.P_mortality :
                        self.status="dead"
                        grid[int(self.x)]-=1
                        
                        n_dead += 1
                        n_sick -= 1
                    else :
                        self.status="immune"
                        grid[int(self.x)]-=1
                        n_sick-=1
                        
                    
            return n_healthy,n_sick,n_dead
              
def watts_strogatz(N,C,P):
    sigma=0
    tries=0
    ngraph=0
    while (sigma==0 or ngraph!=1) and tries<100 :
        maps = {}
        for i in range(0,N) :
            maps.update([(i/1,np.delete(np.arange(i-C/2,i+C/2+1,dtype=np.int32)%N,int(C/2)))])
        
        
        for i in range(0,N) :
           #print(i)
           for (ex,j) in enumerate(maps[i/1]) :
               prob=np.random.random()
               if prob<P :
                   #step 1 : change the edge for the ex node
                   new_edge=np.random.randint(0,N)/1
                   old_node=(maps[i/1][ex])
                   maps[i/1][ex]=new_edge
                   
                   #step 2 : remove the edge from the old connected node
                   
                   old_edge=np.where(maps[old_node]==ex)[0]
                   maps[old_node]=np.delete(maps[old_node],old_edge)
                  
                  
                  
                 
                   #step 3 : add the new edge to the new node
                   maps[new_edge]=np.append(maps[new_edge],ex)
                
                   
        #print('testing')
        G=nx.Graph(maps)
        #nx.draw_circular(G,dim=5,scale=0.1,node_size=5,linewidths=0.1)
        #sigma=nx.algorithms.smallworld.sigma(G,niter=5)
        sigma=1
        ngraph=0
        sub_graphs=(G.subgraph(c) for c in nx.connected_components(G))
        for i, sg in enumerate(sub_graphs):
            print(i,sg)
            #print ("subgraph {} has {} nodes".format(i, sg.number_of_nodes()))
            ## print ("\tNodes:", sg.nodes(data=True))
            # print ("\tEdges:", sg.edges())
            ngraph+=1
        tries+=1
        
        return maps,G
    


def small_world_power_law(N,C,lambd):
    ngraph=0
    while ngraph!=1 :
        maps = {}
        for i in range(0,N) :
            maps.update([(i,[])])
        
        for i in range(0,N) :
            
           
           
            #b=(lambd-1)*m**(lambd-1)
            
            nombre=int(int((C)*(i+1)**(-lambd)))
        
            #print(nombre)
            if nombre<1 : nombre=1
            if nombre>=N : nombre=N-1
            rx=np.random.randint(0,N-1,size=(nombre)) 
            while i in rx :
                rx=np.random.randint(0,N-1,size=(nombre))
      
            connect2=rx
            connect1=maps[i]
            connect1=np.append(connect1,connect2)#!!!! certain connections may repeat themselves
            maps.update([(i , connect1)])
            
            for j in range(0,nombre) :
                connect1=maps[j]
                np.append(connect1,i)
                maps.update([(j , connect1)])
                
        G=nx.Graph(maps)
        ngraph=0
        sub_graphs=(G.subgraph(c) for c in nx.connected_components(G))
        for i, sg in enumerate(sub_graphs):
            ngraph+=1
            
    return maps,G

