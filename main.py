"""This main module which run application."""
import sys
import os
import re
import serial
import threading
import time
import datetime
import subprocess
import yaml
import matplotlib.pyplot as plt
import numpy as np
import os
import math

from PyQt5 import QtCore, QtWidgets
from window import Ui_MainWindow
from graph import Graph


SPEED = 9600
"""Data transfer rate."""



class RealWindow(QtWidgets.QMainWindow):
    """
    Define the internal implementation for user graphical interface.

    Attributes
    ----------
    app : MyApp
        An instance of the MyApp class
    ui: Ui_MainWindow
        Graphical interface.
    list_num_1 : list
        List for storage num_1.
    list_num_2 : list
        List for storage num_2.
    graphFlag : bool
        If graphFlag is True, we will draw graph and otherwise no.
    first_time : float
        Start time.
    file_descriptor : file
        File object for writing data.
    conf : file
        Attribute for storage config file object.
                    
    """
    
    def __init__(self, app, ui: Ui_MainWindow):
        super().__init__()
        self.app = app
        self.ui = ui
        self.ui.setupUi(self)
        self.list_num_1 = []
        self.list_num_2 = []
        self.graphFlag = False
        self.fill_ports()
        self.attach_handlers()
        self.first_time = time.time()
        self.file_descriptor = None
        self.conf = self.load_conf()
        self.init_conf()
        self.capture_in_progress = False
        self.captured_nums_count = 0
        self.captured_nums_avg = 0

    def menu_handlers(self):
        """Connect the user interface menubar with their actions."""
        self.ui.CH16.triggered.connect(self.app.serial.get_CH16)
        self.ui.CH26.triggered.connect(self.app.serial.get_CH26)
        self.ui.CH36.triggered.connect(self.app.serial.get_CH36)
        self.ui.CH46.triggered.connect(self.app.serial.get_CH46)
        self.ui.CH12.triggered.connect(self.app.serial.get_CH12)
        self.ui.CH34.triggered.connect(self.app.serial.get_CH34)
        self.ui.CH56.triggered.connect(self.app.serial.get_CH56)
        self.ui.CH66.triggered.connect(self.app.serial.get_CH66) 
        self.ui.G1.triggered.connect(self.app.serial.get_G1)
        self.ui.G2.triggered.connect(self.app.serial.get_G2)
        self.ui.G4.triggered.connect(self.app.serial.get_G4)
        self.ui.G8.triggered.connect(self.app.serial.get_G8)
        self.ui.G16.triggered.connect(self.app.serial.get_G16)
        self.ui.G32.triggered.connect(self.app.serial.get_G32)
        self.ui.G64.triggered.connect(self.app.serial.get_G64)
        self.ui.G128.triggered.connect(self.app.serial.get_G128) 

    def attach_handlers(self):
        """Connect buttons and interface menu with their actions."""
        self.ui.refreshPorts.clicked.connect(self.fill_ports)
        self.ui.connectPort.clicked.connect(self.connect_click)
        self.ui.disconnectPort.clicked.connect(self.disconnect_click)
        self.app.serial.line_readed.connect(self.data_arrived)
        self.ui.captureZero.pressed.connect(self.captureZeroBegin)
        self.ui.captureZero.released.connect(self.captureZeroEnd)
        self.ui.captureCoef.pressed.connect(self.captureCoefBegin)
        self.ui.captureCoef.released.connect(self.captureCoefEnd)
        self.ui.startWriteButton.clicked.connect(self.startWriteFile)
        self.ui.stopWriteButton.clicked.connect(self.stopWriteFile)
        self.ui.openFileButton.clicked.connect(self.openFile)
        self.ui.startDraw.clicked.connect(self.startDrawGraph)
        self.ui.stopDraw.clicked.connect(self.stopDrawGraph)
        self.ui.clear.clicked.connect(self.clear)
        self.menu_handlers()

    def update_conf(self):
        """Update configuration for config.yml file."""
        self.conf["coef"] = float(self.ui.coef.text())
        self.conf["zero"] = float(self.ui.zeroKg.text())
        self.conf["measure_mass"] = float(self.ui.measureMass.text())
        self.conf["filename"] = self.ui.fileNameInput.text()

    def init_conf(self):
        """Extract values from config.yml and define the name of the file for writing as default."""
        coef = self.conf.get("coef", 1)
        zero = self.conf.get("zero", 0)
        measureMass = self.conf.get("measure_mass", 1)
        filename = self.conf.get("filename", "./output.csv")
        self.ui.coef.setText(str(coef))
        self.ui.zeroKg.setText(str(zero))
        self.ui.measureMass.setText(str(measureMass))
        if os.path.exists(filename):
            namepart, extpart = os.path.splitext(filename)
            matches = re.search("(?P<full>_(?P<num>[0-9]+))", namepart)
            if matches:
                num = int(matches.groupdict()['num']) # int()
                full_num = matches.groupdict()['full']
                numless_name = namepart[0:-len(full_num)]
                
            else:
                num = 1
                numless_name = namepart

            filename_full = numless_name + "_" + str(num + 1) + extpart
            self.ui.fileNameInput.setText(filename_full)

        else:
            self.ui.fileNameInput.setText(filename)

    def load_conf(self):
        """If the config.yml exists, return file object."""
        conf = {}
        if os.path.exists("./config.yml"):
            with open("./config.yml", "r") as f:
                conf = yaml.load(f)
        return conf
    
    def save_conf(self, conf):
        """Save the last settings into config.yml."""
        with open("./config.yml", "w") as f:
            yaml.dump(conf, f)
    
    def beginMeasure(self):
        """Reset the accumulating variables."""
        self.captured_nums_avg = 0
        self.captured_nums_count = 0
        self.capture_in_progress = True

    def endMeasure(self):
        """Return the average value measured during the hold time of the button."""
        self.capture_in_progress = False
        if self.captured_nums_count == 0:
            return None
        else:
            return self.captured_nums_avg

    def measure(self, num):
        """Accumulate the mathematical expectation of the measured values."""
        if self.capture_in_progress:
            self.captured_nums_avg = (
                (self.captured_nums_avg * self.captured_nums_count + num) / (self.captured_nums_count + 1)
            )
            self.captured_nums_count += 1

    def captureZeroBegin(self):
        """Start calculate zero."""
        self.beginMeasure()

    def captureZeroEnd(self):
        """End calculate zero."""
        measured = self.endMeasure()
        if measured is not None:
            self.ui.zeroKg.setText(str(round(measured, 4)))

    def captureCoefBegin(self):
        """Start calculate coefficient."""
        self.beginMeasure()

    def captureCoefEnd(self):
        """End calculate coefficient."""
        measured = self.endMeasure()
        nonZeroKg = self.get_number(self.ui.measureMass)
        if measured is not None and measured != 0 and nonZeroKg != 0:
            zeroKg = self.get_number(self.ui.zeroKg)
            coef = round((measured - zeroKg) / nonZeroKg, 12)
            self.ui.coef.setText(str(round(coef, 9)))
    
    def startWriteFile(self):
        """Create a file object for writing or appending."""
        if not self.app.serial.serial.isOpen():
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Подключение не установлено!")
        else:
            filename = self.ui.fileNameInput.text()
            try:
                if os.path.exists(filename):
                    f = open(filename, "a")
                else:
                    f = open(filename, "w")
                    if sys.platform.startswith('lin'):
                        f.write("\ufeff")
                    f.write("{},{},{},\n".format("Время ", "Вход А", "Вход Б"))
                self.file_descriptor = f
            except PermissionError as e:
                QtWidgets.QMessageBox.warning(self, "Ошибка создания фала", str(e))
            self.ui.fileNameInput.setEnabled(False)
            self.ui.startWriteButton.setEnabled(False)
            self.ui.stopWriteButton.setEnabled(True)
    
    def stopWriteFile(self):
        """Close a file object."""
        if self.file_descriptor is None:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Файл не был открыт")
        else:
            self.file_descriptor.close()
            self.file_descriptor = None
            self.ui.fileNameInput.setEnabled(True)
            self.ui.startWriteButton.setEnabled(True)
            self.ui.stopWriteButton.setEnabled(False)
    
    def openFile(self):
        """Visually open the file for the user."""
        filename = self.ui.fileNameInput.text()
        if not os.path.exists(filename):
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Файл не существует")
        else:
            fullpath = os.path.realpath(filename)
            if sys.platform.startswith('lin'):
                process = subprocess.Popen(['xdg-open',fullpath])
            if sys.platform.startswith('win'):
                os.startfile(fullpath)

    def data_arrived(self, s):
        """Parse a string of data into numbers."""
        try:
            n_str = s.decode("UTF-8")
            if n_str.rstrip() == 'D':
                return
            num_1 = float(n_str.split('A')[0])
            num_2 = float(n_str.split('A')[1])
            self.number_arrived(num_1, num_2)
        except ValueError as e:
            print("ValueError: " + str(e))
    
    def number_arrived(self, num_1, num_2):
        """Transfer data for display and calculation of zero."""
        self.measure(num_1)
        self.add_line(0, num_1, num_2)
    
    def get_number(self, lineedit):
        """Read data from lineedit field of the graphical user interface."""
        try:
            v = float(lineedit.text())
        except ValueError as e:
            v = 0
            print("ValueError: " + str(e))
        return v

    def get_mass(self, num):
        """Calculate data based on zero and coefficient."""
        coef = self.get_number(self.ui.coef)
        zeroKg = self.get_number(self.ui.zeroKg)
        kg = round((num - zeroKg) / coef, 4)
        return kg

    def add_line(self, timestamp, num_1, num_2):
        """Write data to a file, draw a graph, provide data to the user interface."""
        average_1 = 0
        average_2 = 0
        if len(self.list_num_1) <= 1:
            self.list_num_1.append(num_1)
        else:
            average_1 = self.get_average(self.list_num_1)
            del self.list_num_1[:]
        if len(self.list_num_2) <= 1:
            self.list_num_2.append(num_2)
        else:
            average_2 = self.get_average(self.list_num_2)
            del self.list_num_2[:]
        zeroKg = float(self.ui.zeroKg.text())
        coef = float(self.ui.coef.text())
        # draw a graph
        if self.graphFlag and len(self.list_num_1) == 0:
            self.ui.graph.draw(round(time.time() - self.first_time, 3), (average_1 - zeroKg)*coef)
        self.t = int(time.time() - self.first_time)
        if len(self.list_num_1) == 0:
            # provide data to the user interface
            self.ui.time.setText(str(self.t))
            self.ui.calcData.setText(str((average_1 - zeroKg)*coef))
            self.ui.ardAnalog.setText(str(average_2))
            self.ui.rawData.setText(str(average_1))
            if self.file_descriptor is not None:
                # Write data to a file
                self.file_descriptor.write(str(self.t) + "," + str(average_1)+ "," + str(average_2) +"\n")
            
    def get_average(self, lst):
        """Calculate the arithmetic mean of the list."""
        total = 0
        for num in lst:
            total += num
        total = float(total / len(lst))  
        return total
    
    def startDrawGraph(self):
        self.graphFlag = True
        self.ui.stopDraw.setEnabled(True)
        self.ui.startDraw.setEnabled(False)
        
    def stopDrawGraph(self):
        self.graphFlag = False
        self.ui.stopDraw.setEnabled(False)
        self.ui.startDraw.setEnabled(True)

    def clear(self):
        """Clean the graph and reset the time."""
        self.ui.graph.clear()
        self.first_time = time.time()

    def fill_ports(self):
        """Clears the port values, then search all ports again."""
        self.ui.ports.clear()
        for port in self.app.serial.get_ports():
            self.ui.ports.addItem(port)
    
    def closeEvent(self, QCloseEvent):
        """Final actions after close programm."""
        self.update_conf()
        self.save_conf(self.conf)
        self.app.suicide()
     
    def connect_click(self):
        """Connect to the selected port."""
        port = self.ui.ports.currentText()
        if port:
            self.app.serial.open_connection(port)

            self.ui.refreshPorts.setEnabled(False)
            self.ui.ports.setEnabled(False)
            self.ui.connectPort.setEnabled(False)
            self.ui.disconnectPort.setEnabled(True)
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Вы не выбрали порт!")
    
    def disconnect_click(self):
        """Disconnect from port."""
        self.ui.refreshPorts.setEnabled(True)
        self.ui.ports.setEnabled(True)
        self.ui.connectPort.setEnabled(True)
        self.ui.disconnectPort.setEnabled(False)
        self.app.serial.close_connection()

class Serial(QtCore.QObject):
    """
    Define the interaction with the port.

    Attributes
    ----------
    app : MyApp
        An instance of the MyApp class.
    serial: serial.serialwin32.Serial
        An instance of the Serial class.
    channel: str
        Attribute define pair of channel (see Arduino programm and ad7714 datasheet).
    gain: str
        Attribute define gain (see Arduino programm and ad7714 datasheet).     
    flag: bool
        If flag is True change gain, otherwise channel.
                    
    """

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.serial = serial.Serial()
        self.read_thread = None
        self.stop_thread_event = None
        self.channel = 'G'
        self.gain = '1'
        self.flag = False
    
    def open_connection(self, port, speed=SPEED):
        """Open a connection in a separate thread."""
        if sys.platform.startswith('lin'):
            self.serial.port = "/dev/" + port
        if sys.platform.startswith('win'):    
            self.serial.port = port
        self.serial.baudrate = speed
        self.serial.open()
        if self.read_thread is not None:
            self.stop_thread_event.set()
            self.read_thread.join(1)
        self.stop_thread_event = threading.Event()
        self.read_thread = threading.Thread(target = self.read_loop, args=(self.stop_thread_event,))
        self.read_thread.start()
    
    def read_loop(self, stop_event):
        """In the cycle read data from the port."""
        print("read loop started")
        while not stop_event.is_set():
            if self.serial.isOpen():
                try:
                    if self.flag:
                        self.serial.write(bytes(self.gain, 'utf-8'))
                        self.flag = False   
                    self.serial.write(bytes(self.channel, 'utf-8'))

                    line = self.serial.readline()
                except serial.serialutil.SerialException as e:
                    if ("device reports readiness to read but returned no data" in str(e)):
                        pass
                    else:
                        raise e
                self.data_arrived(line)
        print("read loop stopped")
    
    def close_connection(self):
        """Close a connection."""
        self.stop_thread_event.set()
        self.read_thread.join(1)
        self.serial.close()
        if self.serial.isOpen():
            print("Serial is not closed, as it should be!")
    
    @staticmethod
    def get_ports():
        """
        Search all port.

        Returns
        -------
        list
            List ports.

        """
        ports = []
        if sys.platform.startswith('lin'):
            for path, files, dirs in os.walk("/sys/class/tty"):
                for file in files:
                    fullname = "/sys/class/tty/" + file
                    link = os.readlink(fullname)
                    if re.search("/usb[0-9]+/", link):
                        ports.append(file)
                break
        if sys.platform.startswith('win'):
            ports_win = ['COM%s' % (i + 1) for i in range(256)]
            for port in ports_win:
                try:
                    s = serial.Serial(port)
                    s.close()
                    ports.append(port)
                except (OSError, serial.SerialException):
                    pass
        return ports   

    def data_arrived(self, line):
        self.line_readed.emit(line)

    line_readed = QtCore.pyqtSignal(bytes)
    
    def get_CH16(self):
        self.channel = 'A'

    def get_CH26(self):
        self.channel = 'B'

    def get_CH36(self):
        self.channel = 'C'
        
    def get_CH46(self):
        self.channel = 'D'

    def get_CH12(self):
        self.channel = 'E'

    def get_CH34(self):
        self.channel = 'F'

    def get_CH56(self):
        self.channel = 'G'
        
    def get_CH66(self):
        self.channel = 'H'

    def get_G1(self):
        self.gain = '1'
        self.flag = True

    def get_G2(self):
        self.gain = '2' 
        self.flag = True

    def get_G4(self):
        self.gain = '3'
        self.flag = True 
        
    def get_G8(self):
        self.gain = '4'
        self.flag = True
        
    def get_G16(self):
        self.gain = '5'
        self.flag = True

    def get_G32(self):
        self.gain = '6' 
        self.flag = True

    def get_G64(self):
        self.gain = '7'
        self.flag = True 
        
    def get_G128(self):
        self.gain = '8'
        self.flag = True            

class MyApp(QtWidgets.QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.serial = Serial(self)

    def suicide(self):
        if self.serial.serial.isOpen():
            self.serial.close_connection()
        self.quit()


app = MyApp(sys.argv)
window = RealWindow(app, Ui_MainWindow())
window.show()
app.exec_()