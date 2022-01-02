# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 12:38:09 2021

@author: snc001
"""



#2, Number of pipes, Npipes, Calling all pipes information from SWMM 

#3, Number of events available,

#4, Extract pipes ids, Expipes, this function uses Number of pipes as source of data I.e. function 2 


import matplotlib.pyplot as plt
from pyswmm import Simulation, Subcatchments, Links, Nodes, RainGages

# to simulate the model
sim = Simulation ('./model_weir_setting.inp')

#1, Area of the network, NArea, Calling areas from SWMM
#1, Area of a subcatchment
def Sub_area():
    subcatch_object = Subcatchments(sim)
    total_area = 0
    for subcatchmt in subcatch_object:
        total_area += subcatchmt.area
    return total_area
    
#2, number of pipes: filtering out pumps
def Npipes():
    link_objects = Links(sim)
    n=0
    for link in link_objects:
        if not link.is_pump():
            n= n+1
    return n


    
#3, Number of events available Nevents, calling all events loaded in SWMM      #number of rain events
# todo: i assume those are rain events? this looks wrong in the input there are many
def Nevents():
    return len(RainGages(sim))

#4, Extract pipes ids:
def Expipes():
    pipeIds = []
    for link in Links(sim):
        if link.is_pump():
            print("skip {}".format(link.nodeid))
            continue
        pipeIds.append(link.linkid)
    return pipeIds

#5, Extract pipes in a location,ExpipeLoc, this function extracts only one pipe location  lat and lon



#6, Extract pipe locations, ExAllLoc, this function extract all location


#7, Extract time series of depth in a pipe, ExTsD, Take from an event all time steps of the water depth in a pipe
# to do: time series for other pipes
def ExTsD (pipe_name):
    pipe = Links(sim)[pipe_name]
    wdepth = []
    sim.step_advance(15*60)  # to limit the time interval to 15 mins instead of every minute
    for step in sim:
        wdepth.append((sim.current_time, pipe.depth)) # to show the time at which the flow occurs
    return wdepth


#8, Extract time series of velocity in a pipeExTsV, Take from an event all time steps of the Vel in a pipeprint("pipe flow = ", ExTsD())
def ExTsV ():

    sim2 = Simulation ('./model_weir_setting.inp')
    c1c2 = Links(sim2)["C1:C2"]
    pipe_velocity = []
    sim2.step_advance(15*60)  # to limit the time interval to 15 mins instead of every minute
    for step in sim2:
        pipe_velocity.append((sim2.current_time, c1c2.flow))       # to show the time at which the velocity occurs
    return pipe_velocity

#9, Extract time series of a location with a flood, ExFL, Take from an event all time steps of Flood location
def ExFl ():
    sim2 = Simulation('./model_weir_setting.inp')
    j1 = Nodes(sim2)["J1"]
    fl_j1= []
    sim2.step_advance(15 * 60)
    for step in sim2:
        fl_j1.append((sim2.current_time, j1.flooding))
    return fl_j1
#surcharge depth
def ExSurch():
    sim2 = Simulation('./model_weir_setting.inp')
    j1 = Nodes(sim2)["J1"]
    surch_j1 = []
    sim2.step_advance(15 * 60)
    for step in sim2:
        surch_j1.append((sim2.current_time, j1.surcharge_depth))
    return surch_j1
    #j1 = Nodes(sim)["J1"]
    #print  j1.surcharge_depth

#10, Extract time series of a flood volume, ExFV, Take from an event all time steps of Flood location


print("\n") # pyswmm library prints something on it's own, just do a newline so we know where our output starts
print("area = ", Sub_area())
print("number of pipes = ", Npipes())
print("pipes = ", Expipes())
print("number of events = ", Nevents())
print("water depth = ", ExTsD("C1:C2"))
print("velocity of flow = ", ExTsV())
print("flooding in manhole j1= ", ExFl())
print("surcharge depth= ", ExSurch())
j1 = Nodes(sim)["J1"]
print(j1.statistics)

#plt.plot(ExTsF()) # redo this plotting naming the axis
#plt.show()
#sim.execute() #when the simulation is executed, we can't get subcatchments anymore? it fails with SIGSEGV. todo: figure out why

