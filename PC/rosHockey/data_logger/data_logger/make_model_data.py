import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
from solve_for_coefs import *
import pickle as pkl
R = 3.5306

def get_end_index(m1,m2):
    for i in reversed(range(len(m1))):
        if not ((abs(m1[i]) <= 0.01) and (abs(m2[i]) <= 0.01)):
            return i
    return None


def make_data(positions, motor_efforts, show=True):
    end_index = get_end_index(motor_efforts['m1'], motor_efforts['m2'])

    if end_index is None:
        return

    positions = positions[:end_index+1]
    motor_efforts = motor_efforts[:end_index+1]
    
    if (len(positions)<=6):
        return


    x = np.array(positions['x'])
    y = np.array(positions['y'])

    m1 = np.array(motor_efforts['m1'])*24/128
    m2 = np.array(motor_efforts['m2'])*24/128
    t = np.array(positions['time_on_path'])

    fit_x = np.polyfit(t,x, deg=5)
    fit_y = np.polyfit(t,y, deg=5)
    fit_m1 = np.polyfit(t,m1, deg=5)
    fit_m2 = np.polyfit(t,m2, deg=5)


    if show == True:

        fig, ax1 = plt.subplots()
        ax1.plot(t,x,color = 'b', label='x')
        ax1.plot(t,y,color = 'r',label = 'y')

        ax2 = ax1.twinx()
        ax2.plot(t,m1,color = 'g', label = 'm1')
        ax2.plot(t,m2,color = 'c', label = 'm2')
        ax1.legend(loc = 'upper left')
        ax2.legend(loc = 'upper right')
        ax1.set_xlabel("Time (s)")
        ax2.set_ylabel("Volts")
        ax1.set_ylabel("Position (cm)")




        for p,c,ax in zip([fit_x,fit_y,fit_m1,fit_m2],['b','r','g','c'],[ax1,ax1,ax2,ax2]):
            test_t = np.linspace(t[0],t[-1])
            vals = np.polyval(p,test_t)
            ax.plot(test_t,vals,color = c, linestyle='dashed')
            
    plt.show()

    theta_1_coeffs = (fit_x + fit_y)/(R)
    theta_2_coeffs = (fit_x - fit_y)/(R)

    return np.concatenate((theta_1_coeffs, theta_2_coeffs)), np.concatenate((fit_m1, fit_m2, np.array([t[-1]])))



def get_all_paths(log_file):
    with open(log_file, "r") as f:
        lines = f.readlines()

    pos_dfs = []
    motor_dfs = []
    paths_theta = []
    paths_motor = []

    for line in lines:
        data = json.loads(line)
        if 'MALLET' in data.keys():
            data = data['MALLET']
            new_df = pd.DataFrame(data,index = [0])
            pos_dfs.append(new_df)


        elif 'MOTOR' in data.keys():
            data = data['MOTOR']
            motor_df = pd.DataFrame(data,index = [0])
            if len(motor_dfs)>0 and data['time_on_path'] < np.array(motor_dfs[-1]['time_on_path'])[-1]:
                positions = pd.concat(pos_dfs[:-1]).reset_index(drop=True)
                motor_efforts = pd.concat(motor_dfs).reset_index(drop=True)
                motor_dfs = [motor_df]
                pos_dfs = [pos_dfs[-1]]
                path = make_data(positions, motor_efforts)
                if path is not None:
                    pt, pm = path
                    paths_theta.append(pt)
                    paths_motor.append(pm)
            else:
                motor_dfs.append(motor_df)

    return np.stack(paths_theta), np.stack(paths_motor)


if __name__ == "__main__":
    data_file = 'data/2022-03-16 20:54:22.237820.json'
    out_file = os.path.splitext(data_file)[0] + '_nn_data_with_time.pkl'
    paths=get_all_paths(data_file)
    with open(out_file, 'wb') as f:
        pkl.dump(paths,f)
        print("Wrote {} lines to {}".format(len(paths[0]),out_file))

    # paths.append({"x" : 0, 'y' : 0, ''})
