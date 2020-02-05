#!/usr/bin/env python

import os
import sys
import set_route
from neuralNetwork import NeuralNetwork
from numpy import random

sys.path.append('/usr/share/sumo/tools')

from sumolib import checkBinary  # Checks for the binary in environ vars
import traci

# contains TraCI control loop
def predict(p, queue, i, nn):
    x = p+queue+[i]
    tt = int(nn.feed_forward(x))
    time = 10+tt
    return time

def run(p, nn):
    step = 0
    waiting_time = 0
    turn = 3
    time = 0
    T = []
    G = ["rrrrrrrrrrrrrrrrrrgggggg", "ggggggrrrrrrrrrrrrrrrrrr", "rrrrrrggggggrrrrrrrrrrrr", "rrrrrrrrrrrrggggggrrrrrr"]
    Y = ["rrrrrrrrrrrrrrrrrryyyyyy", "yyyyyyrrrrrrrrrrrrrrrrrr", "rrrrrryyyyyyrrrrrrrrrrrr", "rrrrrrrrrrrryyyyyyrrrrrr"]
    while traci.simulation.getMinExpectedNumber() > 0 and step < 3600:
        if time == 0:
            turn += 1
            turn %= 4
            traci.trafficlight.setRedYellowGreenState("n0",G[turn])
            queue = []
            for edge in ["e10", "e20", "e30", "e40"]:
                queue += [traci.edge.getLastStepVehicleNumber(edge)]
            time = predict(p, queue, turn, nn)
            T += [time]
        if time == 4:
            traci.trafficlight.setRedYellowGreenState("n0",Y[turn])
        step += 1
        time -= 1
        for i in ["e10", "e20", "e30", "e40"]:
            waiting_time += traci.edge.getLastStepHaltingNumber(i) 
        traci.simulationStep()
    with open("./results/res.txt", "a") as file:
        file.write(str(T)+"\n")
    traci.close()
    sys.stdout.flush()
    return waiting_time


# main entry point
def simulation(nn, mode = 0, traffic = 0.5):

    p = [random.rand(), random.rand(), random.rand(), random.rand()]
    s = sum(p)
    s = traffic/s
    for i in range(4):
        p[i] = p[i]*s
    with open("./results/res.txt", "a") as file:
        file.write(str(p)+"\n")
    set_route.set(p[0],p[1],p[2],p[3])
    if mode:
        sumoBinary = checkBinary('sumo-gui')
    else:
        sumoBinary = checkBinary('sumo')
    # traci starts sumo as a subprocess and then this script connects and runs
    traci.start([sumoBinary, "-c", "./sumo/sumo.sumocfg"])
    waiting_time = run(p, nn)
    total_cars = 3600*sum(p)
    avg_waiting_time = waiting_time/total_cars
    #print(waiting_time)
    return -avg_waiting_time

