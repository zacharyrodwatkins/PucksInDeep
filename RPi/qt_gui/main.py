from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer
import mplwidget
import rospy
from std_msgs.msg import String
import sys
import BP_Coms

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        #Load the UI Page
        uic.loadUi('layout.ui', self)
        self.fin_x_vel.valueChanged.connect(self.update_fin_x_vel)
        self.fin_y_vel.valueChanged.connect(self.update_fin_y_vel)
        self.fin_x_acc.valueChanged.connect(self.update_fin_x_vel)
        self.fin_y_acc.valueChanged.connect(self.update_fin_y_acc)
        self.path_time.valueChanged.connect(self.update_path_time)
        self.gen_button.clicked.connect(self.table_plot.canvas.generate_path)
        self.send_button.clicked.connect(self.table_plot.canvas.send_path)

        # Timer configuration
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_cur_mallet)
        self.timer.start(10)
    
    # ROS listener for getting mallet status
    def listener(self):
        rospy.init_node('GUI', anonymous=True)
        rospy.Subscriber('chatter', String, self.subCallback)

    # Update doublespinbox value callbacks
    def update_fin_x_vel(self, value):
        self.table_plot.canvas.final_x_vel = value
        print(self.table_plot.final_x_v)

    def update_fin_y_vel(self, value):
        self.table_plot.canvas.final_y_vel = value

    def update_fin_x_acc(self, value):
        self.table_plot.canvas.final_x_acc = value

    def update_fin_y_acc(self, value):
        self.table_plot.canvas.final_y_acc = value

    def update_path_time(self, value):
        self.table_plot.canvas.path_time = value

    def update_cur_mallet(self):
        stat = BP_Coms.get_mallet_stat()
        if stat == -1:
            return  # No mallet data available
        if sum(stat[0:4]) == stat[4]:
            (x,y) = stat[0:2]
        self.table_plot.canvas.current_pos.set(xdata = x, ydata = y)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()