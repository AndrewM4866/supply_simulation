import simpy
import numpy as np
#import matplotlib.pyplot as plt

#Variables
cycles = 100
ERR = 0.05
ALLOWED_ERR = 25
PROC_TIME = 0.5 #Seconds irl
simulation_time = cycles * PROC_TIME

#Proccess outputs
rng = np.random.default_rng() #Initializing the rng

target = 50
USL = target + ALLOWED_ERR
LSL = target - ALLOWED_ERR
#UCL
#LCL

#Runs x cycles of manufacturing process a
def manuf_proc_a(env):
    print('Target: {target}')
    print('USL: {USL}')
    print('LSL: {LSL}')

    print('Running cycles starting at %f' % env.now)
    
    #Run x cycles
    for i in range(cycles):
        #Randomly generate 1-100 for outputs
        output = rng.integers(low=(target - ALLOWED_ERR), high=(target + ALLOWED_ERR))
        
        #Wait 0.5ms for cycle
        yield env.timeout(PROC_TIME)

        #Print Process Outputs
        print('Cycle: %i' % (i+1))
        print('Current output: %i' % output)
        print('Current time: %f \n' % env.now)

env = simpy.Environment()
#Assigns the process as manuf_proc_a
env.process(manuf_proc_a(env))
env.run(until=(simulation_time + PROC_TIME))
