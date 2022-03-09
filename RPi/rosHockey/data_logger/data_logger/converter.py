# from click import pass_obj
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
from solve_for_coefs import *
from pathlib import Path  



def plot_paths(log_file, n_paths = -1):
    with open(log_file, "r") as f:
        lines = f.readlines()

    if n_paths >= 0:
        pass
        # only take most recent n paths
        # new_pat_indicies = 
        
    paths = []
    functions = []
    # cols = {"x", 'y','vx','vy','ax','ay','time_on_path', 'logger_time', 'path_index'}
    path_index = 0
    # positions = pd.DataFrame(columns=cols)

    dfs = []
    puck_status_dfs = []
    radius = 100*0.07115/2
    first = True
    x0 = 0
    y0 = 0
    for line in lines:
        data = json.loads(line)
        if 'MALLET' in data.keys():

            matlab_fit_data = {}
            data = data['MALLET']

            matlab_fit_data['theta1'] = 180*((data['x'] - x0) + (data['y'] - y0))/(2*radius*np.pi)
            matlab_fit_data['theta2'] = 180*((data['x'] - x0) - (data['y'] - y0))/(2*radius*np.pi)
            matlab_fit_data['x'] = data['x'] - x0
            matlab_fit_data['y'] = data['y'] - y0
            matlab_fit_data['I'] = 0.0
            matlab_fit_data['time'] = data['time_on_path']

            if (matlab_fit_data['time'] < 2):

                if first:
                    x0 = data['x']
                    y0 = data['y']
                    matlab_fit_data['theta1'] = 180*((data['x'] - x0) + (data['y'] - y0))/(radius*np.pi)
                    matlab_fit_data['theta2'] = 180*((data['x'] - x0) - (data['y'] - y0))/(radius*np.pi)
                    matlab_fit_data['x'] = data['x'] - x0
                    matlab_fit_data['y'] = data['y'] - y0
                    first = False
                    print(matlab_fit_data)

                new_df = pd.DataFrame(matlab_fit_data,index = [0])
                dfs.append(new_df)
            
    positions = pd.concat(dfs).reset_index(drop=True)
    
    # print(positions)
    file = Path("C:\\Users\\epham\\Documents\\airhockey\\PucksInDeep\\RPi\\rosHockey\\data_logger\\data\\d_step_speed_10.txt")
    file.parent.mkdir(parents=True, exist_ok=True)  
    positions.to_csv(file, index=False)

if __name__ == "__main__":
    data_file = "C:\\Users\\epham\\Documents\\airhockey\\PucksInDeep\\RPi\\rosHockey\\data_logger\\data\\d_step_slow_2022-03-08 14_24_24.578303.csv"
    plot_paths(data_file)

