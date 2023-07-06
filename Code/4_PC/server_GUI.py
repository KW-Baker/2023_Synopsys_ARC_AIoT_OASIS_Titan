import socket
import sys
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QSizePolicy, QApplication, QSizePolicy, QLabel, QWidget
from PyQt5.QtCore import QTimer, Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import MultipleLocator
import random
import time
import numpy as np
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from PyQt5.QtGui import QFont
import pandas as pd

class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.fig.patch.set_facecolor('black')
        self.axes.set_facecolor('black')
        self.axes.spines['bottom'].set_color('white')
        self.axes.spines['top'].set_color('white') 
        self.axes.spines['right'].set_color('white')
        self.axes.spines['left'].set_color('white')

        self.axes.xaxis.label.set_color('white')
        self.axes.yaxis.label.set_color('white')
        self.axes.tick_params(axis='x', colors='white')
        self.axes.tick_params(axis='y', colors='white')

        self.axes.grid(color='gray', linestyle='--', linewidth=0.5)

        self.data = []
        self.times = []

    def plot(self, y):
        self.data.append(y)
        self.times.append(0)

        while self.times and self.times[0] < -30:
            self.times.pop(0)
            self.data.pop(0)

        self.axes.clear()
        self.axes.set_facecolor('black')
        self.axes.grid(color='gray', linestyle='--', linewidth=0.5)

        self.axes.step(self.times, self.data, 'g-', where='post')
        self.axes.fill_between(self.times, self.data, 0, color='green', alpha=0.3, step='post')
        
        self.axes.set_xlim([-30, 0])
        self.axes.set_ylim([0, 5])
        self.axes.set_xlabel('Time (s)', color='white')
        self.axes.set_ylabel('Value (bar)', color='white')
        self.axes.set_title('Gauge Historical Data', color='white', fontsize=20)

        self.axes.yaxis.set_major_locator(MultipleLocator(0.5))

        self.draw()
        
        self.times = [t - 1.5 for t in self.times]


class GaugeCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111, polar=True)
        self.axes.set_yticklabels([])
        self.axes.set_title("Gauge Degree Prediction", color='white', fontsize=20) 
        
        self.axes.set_xticks(np.deg2rad(np.arange(0, 360, 15)))
        
        labels = [(label + 105) % 360 for label in range(0, 360, 15)]
        self.axes.set_xticklabels(labels[::-1], color = 'white')

        self.axes.set_rticks([])
        self.axes.spines['polar'].set_visible(False)
        self.axes.grid(color='gray', linestyle='--', linewidth=0.5)
        self.axes.set_facecolor('black')
        self.fig.patch.set_facecolor('black')

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.arrow, = self.axes.plot([0, 0], [0, 0.5], color='green', linewidth=2) 

        self.target_theta = 0
        self.current_theta = 0
        self.anim = FuncAnimation(self.fig, self._update_frame, frames=np.arange(0, 4), interval=50) # interval: 50 seconds between each frame

    def _adjust_angle(self, y):
        return -np.radians(y - 90)

    def plot(self, y):
        self.target_theta = self._adjust_angle(y)
        
    def _update_frame(self, i):
        if self.current_theta != self.target_theta:
            self.current_theta += (self.target_theta - self.current_theta) / 4
            
            self.arrow.set_data([0, self.current_theta], [0, 0.5])
            self.draw()


class ApplicationWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.val = 45

    def initUI(self):
        self.setWindowTitle("Gauge Historical Data")
        self.setGeometry(240, 240, 1800, 900)

        self.canvas = MyMplCanvas(self, width=5, height=4, dpi=100)
        self.gauge = GaugeCanvas(self, width=5, height=4, dpi=100)

        self.label = QLabel(self)
        self.label.setFont(QFont("Times", 20, QFont.Bold))
        self.label.setStyleSheet("color: white; background-color: black; border: 0px")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setContentsMargins(0, 0, 0, 20)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_figure)
        self.timer.start(1500)

        gaugeLayout = QVBoxLayout()
        gaugeLayout.setSpacing(0)
        gaugeLayout.setContentsMargins(0, 0, 0, 0)
        gaugeLayout.addWidget(self.gauge)
        gaugeLayout.addWidget(self.label)

        layoutWidget = QWidget(self)
        layoutWidget.setLayout(gaugeLayout)
        layoutWidget.setStyleSheet("background-color: black")

        layout = QHBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(layoutWidget)
        self.setLayout(layout)

    def update_figure(self):
        client, addr = s.accept()
        while True:
            data = client.recv(1024)
            if len(data) == 0:
                break
            else:
                try:
                    pred = int(data.decode())
                    val = pred * scaling
                    map_degree = (pred*scaling + 360 - init_degree) % 360
                    gauge_val = round((map_degree*value_per_scale) / degree_per_scale, 2)
                    self.canvas.plot(gauge_val) # plot value
                    print(gauge_val)
                    self.gauge.plot(val)
                    self.label.setText(f"Predict Degree: {val}, Gauge Value: {gauge_val}")
                    
                except:
                    pass

        client.close()   

        
if __name__ == '__main__':
    init_degree = 216
    scaling = 5
    degree_per_scale = 7.2
    value_per_scale = 0.1
    map_degree = init_degree
    gauge_val = 0

    ip = '*****'
    port = 8888

    s = socket.socket()
    s.bind((ip, port))
    s.listen(0)
    app = QApplication(sys.argv)

    main = ApplicationWindow()
    main.show()

    sys.exit(app.exec_())
