# Imports
from PyQt5 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import matplotlib.pyplot as plt
import matplotlib
from gui_node import gui_node
# import BP_Coms
import path_generator
from PIL import Image

# Ensure using PyQt5 backend
matplotlib.use('QT5Agg')

# Matplotlib canvas class to create figure
class MplCanvas(Canvas):
    def __init__(self, parent=None, **kwargs):        
        # Making Matplotlib figure object with data
        self.canvas = Canvas(Figure())
        Canvas.__init__(self, self.canvas.figure)
        self.gui_node = gui_node
        # Configure base frame of interactive plot
        playspace_width = 760
        playspace_height = 1120
        self.ax = self.canvas.figure.add_subplot(111)
        self.ax.set_xlim((0, playspace_width))
        self.ax.set_ylim((0, playspace_height))
        self.half_table = Image.open('HalfTable.png')
        self.half_table = self.half_table.resize((playspace_width, playspace_height), Image.ANTIALIAS).transpose(Image.FLIP_TOP_BOTTOM)
        self.ax.imshow(self.half_table)

        # Create Click/Drag callbacks
        self.clicked = False
        self.click_clb = self.canvas.mpl_connect('button_press_event', self.on_click)
        self.release_clb = self.canvas.mpl_connect('button_release_event', self.on_release)
        self.move_clb = self.canvas.mpl_connect('motion_notify_event', self.on_move)

        # Configure layout
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)

        # Setup path attributes
        self.x = 0
        self.y = 0
        self.final_x_vel = 0
        self.final_y_vel = 0
        self.final_x_acc = 0
        self.final_y_acc = 0
        self.path_time = 1
        self.x_path = [0]
        self.y_path = [0]
        self.x_stop = [0,0,0]
        self.y_stop = [0,0,0]

        # Setup plots
        self.current_pos = self.ax.plot([self.x], [self.y], 'o', color='black', markersize=10)[0]
        self.final_pos = self.ax.plot([self.x], [self.y], 'o', color='blue', markersize=10)[0]
        self.path = self.ax.plot(self.x_path, self.y_path, color='red')[0]

    def generate_path(self):
        x_start = [self.current_pos.get_data()[0], 0, 0]
        self.x_stop = [self.x, self.final_x_vel, self.final_x_acc]
        y_start = [self.current_pos.get_data()[1], 0, 0]
        self.y_stop = [self.y, self.final_y_vel, self.final_y_acc]
        self.time_to_complete = self.path_time
        (self.x_path, self.y_path, self.t_path) = \
            path_generator.gen_path(x_start, y_start, self.x_stop, self.y_stop, self.time_to_complete)
        self.path.set(xdata=self.x_path, ydata=self.y_path)
        self.canvas.draw()

    def send_path(self):
        # send_x = self.x_stop + [self.path_time]
        # send_y = self.y_stop + [self.path_time]
        self.gui_node.send_path(self.x, self.y, float(self.final_x_vel), float(self.final_y_vel), \
            float(self.final_x_acc), float(self.final_y_acc), float(self.time_to_complete))

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


# Matplotlib widget
class MplWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)   # Inherit from QWidget
        self.canvas = MplCanvas()                  # Create canvas object
        self.vbl = QtWidgets.QVBoxLayout()         # Set box for plotting
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)