import simpy
import numpy as np
#import matplotlib.pyplot as plt

#--------------------------------------------------------
#                       Configs
#--------------------------------------------------------
rng = np.random.default_rng() #Initializing the rng

#Variables
ERR = 0.05
ALLOWED_ERR = 10
MAX_ERR = 25
PROC_TIME = 1 #Hours
PROC_A_STOCK_REQ = 1

#Proccess outputs
TARGET = 50
USL = TARGET + ALLOWED_ERR
LSL = TARGET - ALLOWED_ERR
UCL = TARGET + MAX_ERR
LCL = TARGET - MAX_ERR

#Sourcing inputs
INBOUND_CAPACITY = 100
DAILY_SOURCE = 10

MAX_CYCLES = 100
SIMULATION_TIME = MAX_CYCLES * PROC_TIME

cycle = 0

#--------------------------------------------------------
#                       Functions
#--------------------------------------------------------
#Sourcing function
def sourcing(env, stock_inbound):
    #Keep sourcing moving until end of simulation
    while True:
        yield env.timeout(24)

        if stock_inbound.level <= stock_inbound.capacity and (stock_inbound.level + DAILY_SOURCE) < stock_inbound.capacity:
            yield stock_inbound.put(DAILY_SOURCE)
            print(f'Added {DAILY_SOURCE} to stock_inbound')
        else:
            print(f'No stock added')

        print(f'Current stock: {stock_inbound.level} out of {stock_inbound.capacity}\n')

#Runs x cycles of manufacturing process a
def manuf_proc_a(env, stock_inbound):
    global cycle

    while True:
        if stock_inbound.level >= 1:
            print(f'Taking {PROC_A_STOCK_REQ} from stock - current stock: {stock_inbound.level}') 
            stock_inbound.get(1) #Get 1 unit from stock

            #Randomly generate 1-100 for outputs
            output = rng.integers(low=(LCL), high=(UCL))

            #Wait 0.5 for cycle
            yield env.timeout(PROC_TIME)
            cycle += 1
            #print(f'Cycle: {cycle}')
            print(f'Output: {output}')

            #Decision making for proc outputs
            #If above USL parts get reworked
            #If below LSL parts get thrown out
            if output >= LSL and output <= USL:
                print(f'Cycle {cycle} succeeded')
                #Add logic moving stock forward
            elif output > USL:
                print(f'Cycle {cycle} underworked, returning to stock')
                stock_inbound.put(1) #Return to stock to be reworked
                print(f'New stock level {stock_inbound.level}')
            elif output < LSL:
                print(f'Cycle {cycle} overworked, throwing out')
                #Add logic for throwing out stock
            else:
                print(f'Unkown output for Cycle {cycle}')

            #Print Process Outputs
            print(f'Current time: {env.now} \n')
        else:
            yield env.timeout(PROC_TIME)
            print(f'No stock, waiting for more')

#--------------------------------------------------------
#               Starting the simulation
#--------------------------------------------------------
env = simpy.Environment()

#Resources
stock_inbound = simpy.Container(env, capacity=INBOUND_CAPACITY, init=50)

print(f'--------------------------------------------')
print(f'                    Configs                 ')
print(f'--------------------------------------------')
print(f'Max space: {stock_inbound.capacity}')
print(f'Current stock {stock_inbound.level}')
print(f'Daily source: {DAILY_SOURCE}\n')
print(f'TARGET: {TARGET}')
print(f'USL: {USL}')
print(f'LSL: {LSL}')
print(f'Running cycles starting at {env.now}')
print(f'--------------------------------------------\n')

#Starting processes
env.process(sourcing(env, stock_inbound))
env.process(manuf_proc_a(env, stock_inbound))
env.run(until=(SIMULATION_TIME + PROC_TIME))