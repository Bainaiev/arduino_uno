"""This module for creation user graphical interface."""
from graph import Graph
from PyQt5 import QtCore, QtWidgets, QtGui

class Ui_MainWindow():

    def setChannel(self, MainWindow):
        """Create channel menu."""
        self.CH16 = QtWidgets.QAction(QtGui.QIcon('icons/ch.png'),'CH16', MainWindow)
        self.CH26 = QtWidgets.QAction(QtGui.QIcon('icons/ch.png'),'CH26', MainWindow)
        self.CH36 = QtWidgets.QAction(QtGui.QIcon('icons/ch.png'),'CH36', MainWindow)
        self.CH46 = QtWidgets.QAction(QtGui.QIcon('icons/ch.png'),'CH46', MainWindow)
        self.CH12 = QtWidgets.QAction(QtGui.QIcon('icons/ch.png'),'CH12', MainWindow)
        self.CH34 = QtWidgets.QAction(QtGui.QIcon('icons/ch.png'),'CH34', MainWindow)
        self.CH56 = QtWidgets.QAction(QtGui.QIcon('icons/ch.png'),'CH56', MainWindow)
        self.CH66 = QtWidgets.QAction(QtGui.QIcon('icons/ch.png'),'CH66', MainWindow)

    def setGraph(self, MainWindow):
        """Create graph menu."""
        self.aPort = QtWidgets.QAction(QtGui.QIcon('icons/A-port.png'), 'A(t)', MainWindow)
        self.bPort = QtWidgets.QAction(QtGui.QIcon('icons/B-port.png'), 'B(t)', MainWindow)
        self.AB = QtWidgets.QAction(QtGui.QIcon('icons/AB.png'), 'A(B)', MainWindow)

    def setGain(self, MainWindow):
        """Create gain menu."""
        self.G1 = QtWidgets.QAction(QtGui.QIcon('icons/ch.png'),'G1', MainWindow)
        self.G2 = QtWidgets.QAction(QtGui.QIcon('icons/ch.png'),'G2', MainWindow)
        self.G4 = QtWidgets.QAction(QtGui.QIcon('icons/ch.png'),'G4', MainWindow)
        self.G8 = QtWidgets.QAction(QtGui.QIcon('icons/ch.png'),'G8', MainWindow)
        self.G16 = QtWidgets.QAction(QtGui.QIcon('icons/ch.png'),'G16', MainWindow)
        self.G32 = QtWidgets.QAction(QtGui.QIcon('icons/ch.png'),'G32', MainWindow)
        self.G64 = QtWidgets.QAction(QtGui.QIcon('icons/ch.png'),'G64', MainWindow)
        self.G128 = QtWidgets.QAction(QtGui.QIcon('icons/ch.png'),'G128', MainWindow)
        
    def setMenu(self, MainWindow):
        """Create a menubar."""
        self.setGraph(MainWindow)
        self.setChannel(MainWindow)
        self.setGain(MainWindow)
        
        menubar = MainWindow.menuBar()
        
        graph = menubar.addMenu('&Graph')
        graph.addAction(self.aPort)
        graph.addAction(self.bPort)
        graph.addAction(self.AB)

        channel = menubar.addMenu('&Channel')
        channel.addAction(self.CH16)
        channel.addAction(self.CH26)
        channel.addAction(self.CH36)
        channel.addAction(self.CH46)
        channel.addAction(self.CH12)
        channel.addAction(self.CH34)
        channel.addAction(self.CH56)
        channel.addAction(self.CH66)

        gain = menubar.addMenu('&Gain')
        gain.addAction(self.G1)
        gain.addAction(self.G2)
        gain.addAction(self.G4)
        gain.addAction(self.G8)
        gain.addAction(self.G16)
        gain.addAction(self.G32)
        gain.addAction(self.G64)
        gain.addAction(self.G128)

    def setPolicy(self, widget, hSizePolicy, vSizePolicy):
        widget.setSizePolicy(QtWidgets.QSizePolicy(hSizePolicy, vSizePolicy))
    def setFixedPolicy(self, widget):
        widget.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
    
    def setupUi(self, MainWindow):
        """Create user graphical interface with buttons, lineedits and so on."""
        MainWindow.resize(500, 500)

        self.setMenu(MainWindow)


        widget = QtWidgets.QWidget()
        MainWindow.setCentralWidget(widget)
        

        grid = QtWidgets.QGridLayout()

        # label horizontally expanding!
        emptyLabel = QtWidgets.QLabel('')
        self.setPolicy(emptyLabel, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        # label horizontally and vertically expanding!
        labExpExp = QtWidgets.QLabel('')
        self.setPolicy(labExpExp, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        # label vertically expanding!
        labFixExp = QtWidgets.QLabel('')
        self.setPolicy(labFixExp, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)

        # Connect command line!
        self.refreshPorts = QtWidgets.QPushButton()
        self.refreshPorts.resize(32, 27)
        self.setFixedPolicy(self.refreshPorts)
        self.refreshPorts.setIcon(QtGui.QIcon('icons/refresh.png'))
        grid.addWidget(self.refreshPorts, 2, 0)
        
        self.ports = QtWidgets.QComboBox()
        self.ports.resize(247, 27)
        self.setPolicy(self.ports, QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        grid.addWidget(self.ports, 2, 1)
        
        self.connectPort = QtWidgets.QPushButton('connect')
        self.setFixedPolicy(self.connectPort)
        grid.addWidget(self.connectPort, 2, 2)
        
        self.disconnectPort = QtWidgets.QPushButton('disconnect')
        self.setFixedPolicy(self.disconnectPort)
        grid.addWidget(self.disconnectPort, 2, 3)
        
        # graph widget!
        self.graph = Graph()
        self.setPolicy(self.graph.canvas, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        grid.addWidget(self.graph.canvas, 3, 0, 3, 2)
       
        # File field line!
        self.fileNameInput = QtWidgets.QLineEdit()
        self.fileNameInput.setText('./output.csv')
        self.setPolicy(self.fileNameInput, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.fileName = QtWidgets.QLabel('File name: ')
        self.setFixedPolicy(self.fileName)
        fileFieldLine = QtWidgets.QHBoxLayout()
        fileFieldLine.addWidget(self.fileName)
        fileFieldLine.addWidget(self.fileNameInput)
        fileFieldLine.addWidget(emptyLabel)

        # File command line!        
        self.startWriteButton = QtWidgets.QPushButton('start recording')
        self.setFixedPolicy(self.startWriteButton)
        self.stopWriteButton = QtWidgets.QPushButton('stop recording')
        self.setFixedPolicy(self.stopWriteButton)
        self.stopWriteButton.setEnabled(False)
        self.openFileButton = QtWidgets.QPushButton('open file')
        self.setFixedPolicy(self.openFileButton)
        fileCommandLine = QtWidgets.QHBoxLayout()
        fileCommandLine.addWidget(self.startWriteButton)
        fileCommandLine.addWidget(self.stopWriteButton)
        fileCommandLine.addWidget(self.openFileButton)
        

        # time line field!
        timeLayout = QtWidgets.QHBoxLayout()
        self.time = QtWidgets.QLineEdit()
        self.setPolicy(self.time, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.timeLabel = QtWidgets.QLabel('time:')
        self.setFixedPolicy(self.timeLabel)
        timeLayout.addWidget(self.timeLabel)
        timeLayout.addWidget(self.time)

        # calculate data line field!
        calcDataLayout = QtWidgets.QHBoxLayout()
        self.calcData = QtWidgets.QLineEdit()
        self.setPolicy(self.calcData, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.calcDataLabel = QtWidgets.QLabel('data:')
        self.setFixedPolicy(self.calcDataLabel)
        calcDataLayout.addWidget(self.calcDataLabel)
        calcDataLayout.addWidget(self.calcData)

        # arduino analogRead() data!
        ardAnalogLayout = QtWidgets.QHBoxLayout()
        self.ardAnalog = QtWidgets.QLineEdit()
        self.setPolicy(self.ardAnalog, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.ardAnalogLabel = QtWidgets.QLabel('A5:')
        self.setFixedPolicy(self.ardAnalogLabel)
        ardAnalogLayout.addWidget(self.ardAnalogLabel)
        ardAnalogLayout.addWidget(self.ardAnalog)

        # raw data!
        rawDataLayout = QtWidgets.QHBoxLayout()
        self.rawData = QtWidgets.QLineEdit()
        self.setPolicy(self.rawData, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.rawDataLabel = QtWidgets.QLabel('Raw data:')
        self.setFixedPolicy(self.rawDataLabel)
        rawDataLayout.addWidget(self.rawDataLabel)
        rawDataLayout.addWidget(self.rawData)

        fileCommandLine.addWidget(emptyLabel)
        fileCommandLine.addLayout(timeLayout)
        fileCommandLine.addWidget(emptyLabel)
        fileCommandLine.addLayout(calcDataLayout)
        fileCommandLine.addWidget(emptyLabel)
        fileCommandLine.addLayout(ardAnalogLayout)
        fileCommandLine.addWidget(emptyLabel)
        fileCommandLine.addLayout(rawDataLayout)
        

        # Graph command line!
        graphCommandLine = QtWidgets.QHBoxLayout()
        self.startDraw = QtWidgets.QPushButton('start Drawing')
        self.setFixedPolicy(self.startDraw)
        self.stopDraw = QtWidgets.QPushButton('stop Drawing')
        self.setFixedPolicy(self.stopDraw)
        self.stopDraw.setEnabled(False)
        self.clear = QtWidgets.QPushButton('clear')
        self.setFixedPolicy(self.clear)
        graphCommandLine.addWidget(self.startDraw)
        graphCommandLine.addWidget(self.stopDraw)
        graphCommandLine.addWidget(self.clear)
        graphCommandLine.addWidget(emptyLabel)

        # Widgets below the graphs
        vLayout = QtWidgets.QVBoxLayout()
        vLayout.addLayout(fileFieldLine)
        vLayout.addLayout(fileCommandLine)
        vLayout.addLayout(graphCommandLine)
        vLayout.addWidget(labExpExp)
        grid.addLayout(vLayout, 6, 0, 2, 2)

        
        rightBlockLayout = QtWidgets.QVBoxLayout()

        self.captureZero = QtWidgets.QPushButton('detect 0')
        self.setPolicy(self.captureZero, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.captureCoef = QtWidgets.QPushButton('to measure the coefficient')
        self.setPolicy(self.captureCoef, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        # zero line field!
        zeroLineField = QtWidgets.QHBoxLayout()
        self.zeroKg = QtWidgets.QLineEdit()
        self.setPolicy(self.zeroKg, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.zeroLabel = QtWidgets.QLabel('zero:')
        self.setFixedPolicy(self.zeroLabel)
        zeroLineField.addWidget(self.zeroLabel)
        zeroLineField.addWidget(self.zeroKg)

        # coef line field!
        coefLineField = QtWidgets.QHBoxLayout()
        self.coef = QtWidgets.QLineEdit()
        self.setPolicy(self.coef, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.coefLabel = QtWidgets.QLabel('coef:')
        self.setFixedPolicy(self.coefLabel)
        coefLineField.addWidget(self.coefLabel)
        coefLineField.addWidget(self.coef)

        # weight line field!
        weightLineField = QtWidgets.QHBoxLayout()
        self.measureMass = QtWidgets.QLineEdit()
        self.setPolicy(self.measureMass, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.weightLabel = QtWidgets.QLabel('weight:')
        self.setFixedPolicy(self.weightLabel)
        weightLineField.addWidget(self.weightLabel)
        weightLineField.addWidget(self.measureMass)
        
        rightBlockLayout.addWidget(self.captureZero)
        rightBlockLayout.addWidget(self.captureCoef)
        rightBlockLayout.addLayout(zeroLineField)
        rightBlockLayout.addLayout(coefLineField)
        rightBlockLayout.addLayout(weightLineField)
        rightBlockLayout.addWidget(labFixExp)

        grid.addLayout(rightBlockLayout, 3, 2, 3, 2)

        widget.setLayout(grid)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)