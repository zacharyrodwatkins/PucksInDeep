from click import pass_obj
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
from solve_for_coefs import *



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
    for line in lines:
        data = json.loads(line)
        if 'MALLET' in data.keys():
            data = data['MALLET']
            data['path_index'] = path_index
            # print(data)
            new_df = pd.DataFrame(data,index = [0])
            dfs.append(new_df)
            # positions.append(data, ignore_index = True)
            
        elif 'PATH' in data.keys():
            last_position_data = dfs[-1]
            if path_index == 0:
                dummy_path = {}
                dummy_path['x'] = last_position_data['x']
                dummy_path['y'] = last_position_data['y']
                for key in ['vx','vy','ax','ay','t','logger_time']:
                    dummy_path[key]=0

                paths.append(pd.DataFrame(dummy_path))
                functions.append((lambda t : dummy_path['x']), (lambda t : dummy_path['y']))

                path_index += 1
                paths.append(pd.DataFrame(data['PATH'], index=[0]))

        elif 'PUCK' in data.keys():
            data = data['PUCK']
            data['path_index'] = path_index
            # print(data)
            new_df = pd.DataFrame(data,index = [0])
            puck_status_dfs.append(new_df)
            
    positions = pd.concat(dfs).reset_index(drop=True)
    paths = pd.concat(paths).reset_index(drop=True)
    puck_status = pd.concat(puck_status_dfs).reset_index(drop=True)
    print(paths)

    plt.plot(puck_status["logger time"], puck_status["vy"])
    plt.plot(positions["logger time"], positions["vy"])

if __name__ == "__main__":
    data_file = '/home/fizzer/PucksInDeep/RPi/rosHockey/data_logger/data/2022-02-14 19:06:37.937629.csv'
    plot_paths(data_file)


    # paths.append({"x" : 0, 'y' : 0, ''})
