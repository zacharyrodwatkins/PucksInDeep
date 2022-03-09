from operator import pos
from pickle import TRUE
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
    motor_dfs = []
    for line in lines:
        data = json.loads(line)
        # print(data)
        if 'MALLET' in data.keys():
            data = data['MALLET']
            data['path_index'] = path_index
            # print(data)
            new_df = pd.DataFrame(data,index = [0])
            dfs.append(new_df)
            # positions.append(data, ignore_index = True)
            
        # elif 'PATH' in data.keys():
        #     last_position_data = dfs[-1]
        #     if path_index == 0:
        #         dummy_path = {}
        #         dummy_path['x'] = last_position_data['x']
        #         dummy_path['y'] = last_position_data['y']
        #         for key in ['vx','vy','ax','ay','t','logger_time']:
        #             dummy_path[key]=0

        #         paths.append(pd.DataFrame(dummy_path))
        #         functions.append((lambda t : dummy_path['x']), (lambda t : dummy_path['y']))

        #         path_index += 1
        #         paths.append(pd.DataFrame(data['PATH'], index=[0]))

        if 'PUCK' in data.keys():
            data = data['PUCK']
            data['path_index'] = path_index
            # print(data)
            new_df = pd.DataFrame(data,index = [0])
            puck_status_dfs.append(new_df)
            
        if 'MOTOR' in data.keys():
            data = data['MOTOR']
            data['path_index'] = path_index
            new_df = pd.DataFrame(data, index= [0])
            motor_dfs.append(new_df)


    motor_info = pd.concat(motor_dfs).reset_index(drop=True)
    positions = pd.concat(dfs).reset_index(drop=True)

    time_on_path_list =  motor_info['time_on_path'].values.tolist()
    start_index =time_on_path_list.index(min(time_on_path_list))

    motor_info =  motor_info[start_index+1:].reset_index(drop=True)
    positions = positions[start_index+1:].reset_index(drop=True)
    print(positions)
    # paths = pd.concat(paths).reset_index(drop=True)
    # puck_status = pd.concat(puck_status_dfs).reset_index(drop=True)

    # plt.plot(puck_status["logger_time"], puck_status["vy"])
    # plt.plot(positions["logger_time"], positions["y"])
    # plt.xlabel("time (s)")
    # plt.ylabel("y velocity (cm/s)")
    # plt.legend(["puck position", "mallet position"])
    # plt.title("Using Mallet Position Readout to Validate Puck Velocity Readings")

    plt.plot(np.array(positions['time_on_path']), np.array(positions['y']))
    plt.plot(np.array(positions['time_on_path']), np.array(positions['x']))
    plt.plot(np.array(motor_info['time_on_path']), np.array(motor_info['m1']))
    plt.plot(np.array(motor_info['time_on_path']), np.array(motor_info['m2'])*-1)

    plt.show()

if __name__ == "__main__":
    # /home/fizzer/PucksInDeep/RPi/rosHockey/data_logger/data/2022-03-08 17:35:49.063425.csv
    data_file = '../data/2022-03-08 17:35:49.063425.csv'
    plot_paths(data_file)


    # paths.append({"x" : 0, 'y' : 0, ''})
