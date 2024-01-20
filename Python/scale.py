from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QLabel, QProgressBar
import sys
import csv
import serial
import time
from datetime import datetime

ser = serial.Serial(
           port='/dev/ttyUSB0',
           baudrate=9600,
       )


class UI(QtWidgets.QWidget):
   def __init__(self):
       super(UI, self).__init__()
       uic.loadUi('/home/tflunch/Matsvinn/Python/scale_ui_extension.ui', self)

       self.food_waste = self.findChild(QLabel, "food_waste")
       self.daily_goal = self.findChild(QLabel, "daily_goal")
       self.progressBar = self.findChild(QProgressBar, "progressBar")

       self.n = 1000
       self.progressBar.setMaximum(self.progressBar.maximum() * self.n)

       self.showFullScreen()

       self.prevW = 0
       weight = 0.000
       self.update_waste(float(weight))
       QApplication.processEvents()
       
       self.cont = True
       self.main_function()

   
   def main_function(self):
       while self.cont:
           dataIn = str(ser.readline(), 'ascii')
           dataArray = dataIn.split(" ")
           for x in dataArray:
               if x.replace(".", "", 1).isdigit():
                   save_data(x, self.prevW)
                   weight = x
                   self.prevW = x
                   self.update_waste(float(weight))
                   QApplication.processEvents()
                      

   def update_waste(self, max_weight):
       self.food_waste.setText("%.3f kg" % max_weight)
       multiplied_max = round(max_weight * self.n)
       if multiplied_max >= self.progressBar.maximum():
           self.progressBar.setValue(self.progressBar.maximum())
       else:
           self.progressBar.setValue(multiplied_max)
       self.bar_color(multiplied_max)

   def bar_color(self, max_weight):
       if max_weight < (self.progressBar.maximum() * 0.5):
           self.progressBar.setStyleSheet("QProgressBar::chunk "
                                          "{"
                                            "background-color: green;"
                                          "}")
       elif (self.progressBar.maximum() * 0.5) <= max_weight < (self.progressBar.maximum() * 0.75):
           self.progressBar.setStyleSheet("QProgressBar::chunk "
                                          "{"
                                            "background-color: yellow;"
                                          "}")
       elif max_weight >= (self.progressBar.maximum() * 0.75):
           self.progressBar.setStyleSheet("QProgressBar::chunk "
                                          "{"
                                            "background-color: red;"
                                          "}")

def save_data(weight, previous):
    if previous != weight:
       curDate = datetime.now().strftime("%d_%m_%Y")
       curTime = datetime.now().strftime("%H:%M:%S")
       with open('/home/tflunch/Matsvinn/Excel/kuk.csv', 'a') as log:
           log.write(f"{weight}, {curTime}, {curDate}\n")
       log.close()
       


app = QtWidgets.QApplication(sys.argv)
window = UI()
app.exec_()


