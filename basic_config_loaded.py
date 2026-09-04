import simpy
import numpy as np
import yaml
import sys
#import matplotlib.pyplot as plt

#Opening and assigning configurations from the config.yaml
#Try is to catch errors when opening
def load_config(config_file):
    try:
        with open(config_file, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print("Error: config.yaml file not found.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        sys.exit(1)

#Runs x cycles of manufacturing process a
def manuf_proc_a(env):
    print(f'Target: {target}')
    print(f'USL: {USL}')
    print(f'LSL: {LSL}')

    print('Running cycles starting at %f' % env.now)
    
    #Run x cycles
    for i in range(cycles):
        #Randomly generate output between target+- allowed error
        output = rng.integers(low=(target - ALLOWED_ERR), high=(target + ALLOWED_ERR))
        
        #Wait 0.5ms for cycle
        yield env.timeout(PROC_TIME)

        #Print Process Outputs
        print('Cycle: %i' % (i+1))
        print('Current output: %i' % output)
        print('Current time: %f \n' % env.now)

        #Collect data
        manuf_proc_a_outputs[env.now] = { 
            "Cycle": i+1, 
            "Output": int(output)
        }

config = load_config('config.yaml')
print(f'Configs: {config}')

#nest the config.get to avoid having to do 2 .get to access data
proc_a_config = config.get('machine_proc_a', {})

#Variables
cycles = proc_a_config.get('cycles')
ERR = proc_a_config.get('error')
ALLOWED_ERR = proc_a_config.get('max_deviation')
PROC_TIME = proc_a_config.get('cycle_time')

simulation_time = cycles * PROC_TIME

#Proccess outputs
rng = np.random.default_rng() #Initializing the rng

#Target variables for manufacturing processes
target = proc_a_config.get('target')
USL = target + ALLOWED_ERR
LSL = target - ALLOWED_ERR
#UCL
#LCL

#Create dictionary for data
manuf_proc_a_outputs = {}

env = simpy.Environment()
#Assigns the process as manuf_proc_a
env.process(manuf_proc_a(env))
env.run(until=(simulation_time + PROC_TIME))

#Print Data Dictionary:
#print("Simulation run data")
#print(manuf_proc_a_outputs)