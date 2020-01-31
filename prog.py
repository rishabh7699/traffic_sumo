#!/usr/bin/env python

import os
import sys
import set_route

tools = os.path.join('/usr/share/sumo', 'tools')
sys.path.append(tools)

from sumolib import checkBinary  # Checks for the binary in environ vars
import traci


# contains TraCI control loop
def run():
    step = 0
    waiting_time = 0
    while traci.simulation.getMinExpectedNumber() > 0 and step < 7000:
        if step%100 == 0:
            traci.trafficlight.setRedYellowGreenState("n0","ggggggrrrrrrrrrrrrrrrrrr")
        elif step%100 == 25:
            traci.trafficlight.setRedYellowGreenState("n0","rrrrrrggggggrrrrrrrrrrrr")
        elif step%100 == 50:
            traci.trafficlight.setRedYellowGreenState("n0","rrrrrrrrrrrrggggggrrrrrr")
        elif step%100 == 75:
            traci.trafficlight.setRedYellowGreenState("n0","rrrrrrrrrrrrrrrrrrgggggg")
        elif step%100 == 96:
            traci.trafficlight.setRedYellowGreenState("n0","rrrrrrrrrrrrrrrrrryyyyyy")
        elif step%100 == 21:
            traci.trafficlight.setRedYellowGreenState("n0","yyyyyyrrrrrrrrrrrrrrrrrr")
        elif step%100 == 46:
            traci.trafficlight.setRedYellowGreenState("n0","rrrrrryyyyyyrrrrrrrrrrrr")
        elif step%100 == 71:
            traci.trafficlight.setRedYellowGreenState("n0","rrrrrrrrrrrryyyyyyrrrrrr")
        step += 1
        waiting_time += traci.edge.getWaitingTime("e10") 
        waiting_time += traci.edge.getWaitingTime("e20") 
        waiting_time += traci.edge.getWaitingTime("e30") 
        waiting_time += traci.edge.getWaitingTime("e40") 
    
        traci.simulationStep()
    print(waiting_time)
    traci.close()
    sys.stdout.flush()
    return waiting_time


# main entry point
def main():
    set_route.set(0.1,0.5,0.1,0.1)
    sumoBinary = checkBinary('sumo-gui')
    sumoBinary = checkBinary('sumo')
    # traci starts sumo as a subprocess and then this script connects and runs
    traci.start([sumoBinary, "-c", "sumo.sumocfg"])
    waiting_time = run()
    print(waiting_time)

main()