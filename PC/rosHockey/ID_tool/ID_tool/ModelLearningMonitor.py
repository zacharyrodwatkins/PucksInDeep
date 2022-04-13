from cProfile import label
from os import read
import serial
import numpy as np
import matplotlib.pyplot as plt


ser = serial.Serial('/dev/ttyUSB0',460800, timeout=1)
ser.flush()

last = [0,0,0]
last_V1 = []
last_V2 = []
V1 = []
V2 = []
er1 = []
er2 = []
t = []
path_steps = 500
path_time = 0.5
done = False
first = 0
prev_t =None
while True:
    while not done:
        line = ser.readline()
        line = line.decode()
        if not (len(line) == 0):
            last = line.split(" ")
            print(last)
            last[-1] = last[-1].strip("\n")
            last[-1] = last[-1].strip("\r")
            last = [float(x) for x in last]
            V1.append(last[0])
            V2.append(last[1])
            er1.append(last[2])
            er2.append(last[3])
            t.append(last[4])
            # print(t[-1])
            
            if last[4] == path_steps-1:
                done = True

    
    t = [time/1E3 for time in t]

    fig, ax1 = plt.subplots()

    effort_x = np.array(V1)+np.array(V2)
    effort_y = np.array(V1)-np.array(V2)

    ax2 = ax1.twinx()
    # ax1.plot(t, V1)
    # ax1.plot(t, V2)

    ax1.plot(t, effort_x, label='effort x')
    ax1.plot(t,effort_y, label='effort y')


    V1_poly = np.polyfit(t, V1, 4)
    V2_poly = np.polyfit(t, V2, 4)
    
    # ax1.plot(t, np.polyval(V1_poly, t))
    # ax1.plot(t, np.polyval(V2_poly, t))
    if (len(last_V1) > 0):
        # try:
        print(prev_t)
        effort_x_last = np.array(last_V1)+np.array(last_V2)
        effort_y_last= np.array(last_V1)-np.array(last_V2)

        # ax1.plot(t, last_V1)
        # ax1.plot(t, last_V2)
        ax1.plot(prev_t, effort_x_last, label='previous x effort')
        ax1.plot(prev_t, effort_y_last, label='previous y effort')
        # except:
        #     print("missed smthn")
    # ax2.plot(t, er1, "black")
    # ax2.plot(t, er2, "gray")

    # err_x = np.array(er1)+np.array(er2)
    # err_y = np.array(er1)-np.array(er2)

    ax2.plot(t, er1, "black",label = 'x error')
    ax2.plot(t, er2, "gray", label = 'y error')

    # ax1.legend(["next V1", "next V2", "V1 last", "V2 last"])
    ax1.legend()
    # ax2.legend(["theta 1 error", "theta 2 error"])
    ax2.legend()
    plt.show()
    
    print("V1 Poly: {}".format(V1_poly))
    print("V2 Poly: {}".format(V2_poly))

    if not (input("RUN PATH? (Y/n)") == "n"):
        ser.write("a".encode())
        done = False

    prev_t = True
    if prev_t is not None:
        prev_t = t
    last_V1 = V1
    last_V2 = V2
    V1 = []
    V2 = []
    er1 = []
    er2 = []
    t = []
