#!/usr/bin/env python

import os
import sys
import set_route
from neuralNetwork import NeuralNetwork
from numpy import random

sys.path.append('/usr/share/sumo/tools')

from sumolib import checkBinary
import traci

def predict(p, queue, i, nn):
    # return 30
    x = [0,0,0,0]
    x[i] = 1
    # x = p+queue+x
    x = queue + x
    tt = abs(nn.feed_forward(x))
    tt = int(tt)
    time = 6+tt
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
    traci.close()
    return waiting_time, T


# main entry point
def simulation(nn, mode = 0, traffic = 1.0):

    p = [random.rand(), random.rand(), random.rand(), random.rand()]
    s = sum(p)
    s = traffic/s
    for i in range(4):
        p[i] = p[i]*s
    set_route.set(p)
    if mode:
        sumoBinary = checkBinary('sumo-gui')
    else:
        sumoBinary = checkBinary('sumo')
    traci.start([sumoBinary, "-c", "./sumo/sumo.sumocfg"])
    waiting_time, T = run(p, nn)
    total_cars = 3600*traffic
    avg_waiting_time = waiting_time/total_cars
    return -avg_waiting_time, p, T

