from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer
import mplwidget
import sys
# import BP_Coms
from gui_node import gui_node
import rclpy

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

        self.gui_node = gui_node()

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
        rclpy.spin_once(self.gui_node)
        self.table_plot.canvas.current_pos.set(xdata = self.gui_node.x, ydata = self.gui_node.y)


def main(args=None):
    rclpy.init(args=args)
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()