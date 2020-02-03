#!/usr/bin/env python

import os
import sys
import set_route
from neuralNetwork import NeuralNetwork

tools = os.path.join('/usr/share/sumo', 'tools')
sys.path.append(tools)

from sumolib import checkBinary  # Checks for the binary in environ vars
import traci

# contains TraCI control loop
def predict(p, t, i, nn):
    x = p+t+[i]
    tt = int(nn.feed_forward(x))
    time = max(t)+10+tt
    return time

def run(p, nn, file):
    step = 0
    waiting_time = 0
    t = [0, 25, 50, 75]
    T = [25, 25, 25]
    time = 75
    G = ["ggggggrrrrrrrrrrrrrrrrrr", "rrrrrrggggggrrrrrrrrrrrr", "rrrrrrrrrrrrggggggrrrrrr", "rrrrrrrrrrrrrrrrrrgggggg"]
    Y = ["rrrrrrrrrrrrrrrrrryyyyyy", "yyyyyyrrrrrrrrrrrrrrrrrr", "rrrrrryyyyyyrrrrrrrrrrrr", "rrrrrrrrrrrryyyyyyrrrrrr"]
    while traci.simulation.getMinExpectedNumber() > 0 and step < 3600:
        for i in range(4):
            if step == t[i]:
                traci.trafficlight.setRedYellowGreenState("n0",G[i])    
                t[i] = predict(p,t,i,nn)
                T += [t[i] - time]
                time = t[i]
            elif step == t[i]-4:
                traci.trafficlight.setRedYellowGreenState("n0",Y[i])
        step += 1
        for i in ["e10", "e20", "e30", "e40"]:
            waiting_time += traci.edge.getWaitingTime(i) 
        traci.simulationStep()
    file.write(str(T)+"\n")
    traci.close()
    sys.stdout.flush()
    return waiting_time


# main entry point
def simulation(p, nn, file):
    set_route.set(p[0],p[1],p[2],p[3])
    # sumoBinary = checkBinary('sumo-gui')
    sumoBinary = checkBinary('sumo')
    # traci starts sumo as a subprocess and then this script connects and runs
    traci.start([sumoBinary, "-c", "sumo.sumocfg"])
    waiting_time = run(p, nn, file)
    #print(waiting_time)
    return waiting_time

