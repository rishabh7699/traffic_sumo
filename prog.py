#!/usr/bin/env python

import os
import sys
import optparse

# we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


from sumolib import checkBinary  # Checks for the binary in environ vars
import traci

def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options


# contains TraCI control loop
def run():
    step = 0
    waiting_time = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        if step%100 == 0:
            traci.trafficlight.setRedYellowGreenState("n0","ggggggrrrrrrrrrrrrrrrrrr")
        elif step%100 == 25:
            traci.trafficlight.setRedYellowGreenState("n0","rrrrrrggggggrrrrrrrrrrrr")
        elif step%100 == 50:
            traci.trafficlight.setRedYellowGreenState("n0","rrrrrrrrrrrrggggggrrrrrr")
        elif step%100 == 75:
            traci.trafficlight.setRedYellowGreenState("n0","rrrrrrrrrrrrrrrrrrgggggg")
        step += 1
        waiting_time = traci.edge.getWaitingTime("e10")
        if step%100 == 0:
            print(waiting_time, traci.edge.getLastStepMeanSpeed("e10"))
            
        traci.simulationStep()
    traci.close()
    sys.stdout.flush()


# main entry point
if __name__ == "__main__":
    options = get_options()

    # check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # traci starts sumo as a subprocess and then this script connects and runs
    traci.start([sumoBinary, "-c", "sumo.sumocfg"])
    run()