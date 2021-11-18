import matplotlib.pyplot as plt
from tkinter import * 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from PIL import ImageTk, Image
import path_generator
import numpy as np
from numpy.lib.twodim_base import vander
import BP_Coms

class Liveplot:
    def __init__(self, master):
        self.master = master
        # Create a container
        self.frame = Frame(master)

        # Make plot with background image of half table
        playspace_width = 760
        playspace_height = 1120
        self.fig, self.ax = plt.subplots()
        self.half_table = Image.open('HalfTable.png')
        self.half_table = self.half_table.resize((playspace_width, playspace_height), Image.ANTIALIAS).transpose(Image.FLIP_TOP_BOTTOM)
        self.canvas = FigureCanvasTkAgg(self.fig,master=master)
        plt.imshow(self.half_table)
        plt.xlim(0, playspace_width)
        plt.ylim(0, playspace_height)

        # Initialize mallet position and draw plot
        self.x = 0  # Positions for desired final state, update by clicking plot
        self.y = 0
        self.current_pos = self.ax.plot([self.x], [self.y], 'o', color='black', markersize=10)[0]
        self.final_pos = self.ax.plot([self.x], [self.y], 'o', color='blue', markersize=10)[0]
        self.canvas.draw()
        self.x_path = [0]
        self.y_path = [0]
        self.path = self.ax.plot(self.x_path, self.y_path)
        self.x_stop = [0,0,0]
        self.y_stop = [0,0,0]
        self.time_to_complete = 1

        # Create Click/Drag callbacks
        self.clicked = False
        self.click_clb = self.canvas.mpl_connect('button_press_event', self.on_click)
        self.release_clb = self.canvas.mpl_connect('button_release_event', self.on_release)
        self.move_clb = self.canvas.mpl_connect('motion_notify_event', self.on_move)
        
        # Create button and entry widgets
        vcmd = (master.register(self.validate),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.final_vel_label = Label(text="Final Velocity (x, y)", font=("Arial", 10))
        self.final_vel_label.grid(row=2, column=0, sticky=NW, padx=(100,0))
        self.final_x_vel = Entry(self.frame, validate = 'key', validatecommand = vcmd, 
                               width = 4, bg = "#AAAAAA", font=("Arial", 10))
        self.final_x_vel.insert(-1, '0')
        self.final_x_vel.grid(row=2, column=2, sticky=E, pady=(185,0))
        self.final_y_vel = Entry(self.frame, validate = 'key', validatecommand = vcmd, 
                               width = 4, bg = "#AAAAAA", font=("Arial", 10))
        self.final_y_vel.grid(row=2, column=3, sticky=W, pady=(185,0))
        self.final_y_vel.insert(-1, '0')

        self.final_acc_label = Label(text="Final Acceleration (x, y)", font=("Arial", 10))
        self.final_acc_label.grid(row=3, column=0, sticky=NW, padx=(100,0))
        self.final_x_acc = Entry(self.frame, validate = 'key', validatecommand = vcmd,
                               width = 4, bg = "#AAAAAA", font=("Arial", 10))
        self.final_x_acc.grid(row=3, column=2, sticky=E, pady=(50,0))
        self.final_x_acc.insert(-1, '0')
        self.final_y_acc = Entry(self.frame, validate = 'key', validatecommand = vcmd,
                               width = 4, bg = "#AAAAAA", font=("Arial", 10))
        self.final_y_acc.grid(row=3, column=3, sticky=W, pady=(50,0))
        self.final_y_acc.insert(-1, '0')

        self.time_label = Label(text="Time to Complete", font=("Arial", 10))
        self.time_label.grid(row=4, column=0, sticky=NW, padx=(100,0))
        self.time = Entry(self.frame, validate = 'key', validatecommand = vcmd,
                          width = 4, bg = "#AAAAAA", font=("Arial", 10))
        self.time.grid(row=4, column=3, sticky=W, pady=(50,0))
        self.time.insert(-1, '1')

        self.gen_path = Button(self.frame, text = "Generate Path", bg = "#BBBBBB",
                               command = self.generate_path, font=("Arial", 10))
        self.gen_path.grid(row=5, column=0, sticky=E, padx=(100,0), pady=(40,0))
        self.send_path = Button(self.frame, text = "Send Path", bg = "#BBBBBB",
                                command = self.send_path, font=("Arial", 10))
        self.send_path.grid(row=5, column=2, sticky=W, pady=(40,0))

        self.frame.rowconfigure(0, minsize=400)
       
        self.canvas.get_tk_widget().grid(row=0, column=0, rowspan=1, columnspan=3)
        self.frame.grid(row=0, column=0, rowspan=5)

        self.remaining = 0
        self.mallet_update_period = 100  # ms
        self.countdown(10)

    # Timer for updating current mallet pos
    def countdown(self, remaining = None):
        # if remaining is not None:
        #     self.remaining = remaining

        # if self.remaining%2 == 0:
        #     self.time.config(bg="#000000")
        # else:
        #     self.time.config(bg="#AAAAAA")

        # self.remaining -= 1
        # if (self.remaining <= 0):
        #     self.remaining = 10
        #     print("didone")
        cur_mallet_stat = BP_Coms.get_mallet_stat()
        print(cur_mallet_stat)
        self.current_pos.set_data(cur_mallet_stat[0:2])
        self.master.after(self.mallet_update_period, self.countdown)
        self.canvas.draw()

    def generate_path(self):
        x_start = [self.current_pos.get_data()[0], 0, 0]
        self.x_stop = [self.x, float(self.final_x_vel.get()), float(self.final_x_acc.get())]
        y_start = [self.current_pos.get_data()[1], 0, 0]
        self.y_stop = [self.y, float(self.final_y_vel.get()), float(self.final_y_acc.get())]
        self.time_to_complete = float(self.time.get())
        (self.x_path, self.y_path, self.t_path) = path_generator.gen_path(x_start, y_start, self.x_stop, self.y_stop, self.time_to_complete)
        self.path = self.ax.plot(self.x_path, self.y_path, color='red')
        self.ax.lines.pop(3)
        self.canvas.draw()

    def send_path(self):
        send_x = self.x_stop.append(self.time_to_complete)
        send_y = self.y_stop.append(self.time_to_complete)
        BP_Coms.send_path(send_x, send_y)

    def validate(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        if value_if_allowed:
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False

    def on_click(self, event):
        if event.inaxes is not None:
            self.x = event.xdata
            self.y = event.ydata
            print(self.x, self.y)
            self.final_pos.set(xdata = self.x, ydata = self.y)
            self.canvas.draw()
        else:
            print('Clicked ouside axes bounds but inside plot window')
        self.clicked = True

    def on_release(self, event):
        self.clicked = False

    def on_move(self, event):
        if (self.clicked):   
            if event.inaxes is not None:
                self.x = event.xdata
                self.y = event.ydata
                print(self.x, self.y)
                self.final_pos.set(xdata = self.x, ydata = self.y)
                self.canvas.draw()
            else:
                print('Clicked ouside axes bounds but inside plot window')

root = Tk()
lp = Liveplot(root)
root.mainloop()