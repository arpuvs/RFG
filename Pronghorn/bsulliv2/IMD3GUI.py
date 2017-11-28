# Author: Ben Sullivan
# Date: 11/28/2017

# File initialization and instrument import
import sys
sys.path.append('../../Common')
sys.path.append('../../Common/FMB_USB_Python_Files')
from ADI_GPIB.AgilentN5181A import *
from ADI_GPIB.AgilentN9030A import *
from ADI_GPIB.AgilentN6705B import *
from ADI_GPIB.WatlowF4 import *

# PyQT and IMD3 import
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from IMD import IMD3main

class IMDGUI(QMainWindow):
    def __init__(self):
        # Defines window
        super(IMDGUI, self).__init__(None)
        win = QWidget()

        # Top menu bar
        bar = self.menuBar()
        fil = bar.addMenu('File')
        self.load = QAction('Open preset', self)
        self.load.setShortcut('Ctrl+O')
        fil.addAction(self.load)
        self.save = QAction('Save preset', self)
        self.save.setShortcut('Ctrl+S')
        fil.addAction(self.save)
        self.save.triggered.connect(lambda: self.fileBar(self.save))
        self.load.triggered.connect(lambda: self.fileBar(self.load))

        # Line prompts
        self.dutPrompt = QLineEdit()
        self.dutPrompt.setText('0')
        self.freqLine = QLineEdit()
        self.freqLine.setText('4e9')
        self.tempLine = QLineEdit()
        self.tempLine.setText('25')
        self.vcomLine = QLineEdit()
        self.vcomLine.setText('2.5')
        self.fileLine = QLineEdit()
        self.fileLine.setText('C:\\Users\\bsulliv2\\Desktop\\Pronghorn_Results\\IMD3\\')

        # Push Buttons
        self.freqDef = QPushButton('Default Frequency')
        self.freqDef.clicked.connect(lambda: self.fillButton(self.freqDef))
        self.freqSweepDef = QPushButton('Default Frequency Sweep')
        self.freqSweepDef.clicked.connect(lambda: self.fillButton(self.freqSweepDef))
        self.tempDef = QPushButton('Default Temperature')
        self.tempDef.clicked.connect(lambda: self.fillButton(self.tempDef))
        self.tempSweepDef = QPushButton('Default Temperature Sweep')
        self.tempSweepDef.clicked.connect(lambda: self.fillButton(self.tempSweepDef))
        self.run = QPushButton('Run Measurement')
        self.run.clicked.connect(lambda: self.runProgram())
        self.vcomDef = QPushButton('Default VCom')
        self.vcomDef.clicked.connect(lambda: self.fillButton(self.vcomDef))
        self.vcomSweepDef = QPushButton('Default VCom Sweep')
        self.vcomSweepDef.clicked.connect(lambda: self.fillButton(self.vcomSweepDef))
        self.filePrompt = QPushButton('Browse')
        self.filePrompt.clicked.connect(lambda: self.fillButton(self.filePrompt))

        # Frequency prompt layout
        freqLayout1 = QHBoxLayout()
        freqLayout = QVBoxLayout()
        freqLayout1.addWidget(self.freqDef)
        freqLayout1.addStretch()
        freqLayout1.addWidget(self.freqSweepDef)
        freqLayout.addWidget(self.freqLine)
        freqLayout.addStretch()
        freqLayout.addLayout(freqLayout1)

        # Temperature prompt layout
        tempLayout1 = QHBoxLayout()
        tempLayout = QVBoxLayout()
        tempLayout1.addWidget(self.tempDef)
        tempLayout1.addStretch()
        tempLayout1.addWidget(self.tempSweepDef)
        tempLayout.addWidget(self.tempLine)
        tempLayout.addStretch()
        tempLayout.addLayout(tempLayout1)

        # Vcom prompt layout
        vcomLayout1 = QHBoxLayout()
        vcomLayout = QVBoxLayout()
        vcomLayout1.addWidget(self.vcomDef)
        vcomLayout1.addStretch()
        vcomLayout1.addWidget(self.vcomSweepDef)
        vcomLayout.addWidget(self.vcomLine)
        vcomLayout.addStretch()
        vcomLayout.addLayout(vcomLayout1)

        # Path layout
        pathLayout = QHBoxLayout()
        pathLayout.addWidget(self.fileLine)
        pathLayout.addStretch()
        pathLayout.addWidget(self.filePrompt)

        # Form layout
        flo = QFormLayout()
        flo.addRow('Output File Path:', pathLayout)
        flo.addRow('DUT #:', self.dutPrompt)
        flo.addRow('Frequencies to Run:', freqLayout)
        flo.addRow('Temperatures to Run:', tempLayout)
        flo.addRow('Common Mode Voltages to Run:', vcomLayout)

        # Final layout
        layout = QVBoxLayout()
        layout.addLayout(flo)
        layout.addStretch()
        layout.addWidget(self.run)

        # Window properties
        win.setLayout(layout)
        self.setCentralWidget(win)
        self.setWindowTitle('IMD3 GUI')

    def fileBar(self, option):
        # If save menu bar item is hit a file prompt is opened and the preset is saved in the given lcacation
        if option.text() == 'Save preset':
            fname = QFileDialog.getExistingDirectory(self, 'Open Directory')
            fh = open(fname + '\\IMD3_Preset.txt', 'w')
            fh.write(self.fileLine.text() + '\n')
            fh.write(self.dutPrompt.text() + '\n')
            fh.write(self.freqLine.text() + '\n')
            fh.write(self.tempLine.text() + '\n')
            fh.write(self.vcomLine.text() + '\n')
            fh.close()

        # When the open item is hit a file prompt is open and the selected file is loaded into the gui
        if option.text() == 'Open preset':
            fname = QFileDialog.getOpenFileName(self, 'Open preset')
            fh = open(fname, 'r')
            data = fh.read().split('\n')
            if len(data) != 6:
                print 'Invalid data'
                return
            self.fileLine.setText(data[0])
            self.dutPrompt.setText(data[1])
            self.freqLine.setText(data[2])
            self.tempLine.setText(data[3])
            self.vcomLine.setText(data[4])
            fh.close()

    # Fills line prompts based on button pressed
    def fillButton(self, button):
        if button == self.freqDef:
            self.freqLine.setText('4e9')
        elif button == self.freqSweepDef:
            self.freqLine.setText('1.20E+08, 2.253E+08, 5.00E+08, 1.00E+09, 1.50E+09, 2.00E+09, '
                                  '2.50E+09, 3.00E+09, 3.50E+09, 4.00E+09')
        elif button == self.tempDef:
            self.tempLine.setText('25')
        elif button == self.tempSweepDef:
            self.tempLine.setText('25, 80, -40')
        elif button == self.vcomDef:
            self.vcomLine.setText('2.5')
        elif button == self.vcomSweepDef:
            self.vcomLine.setText('2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0')

        # Opens file prompt to fill line prompt
        elif button == self.filePrompt:
            fname = QFileDialog.getExistingDirectory(self, 'Open Directory')
            self.fileLine.setText(fname)

    def runProgram(self):
        # Filter box dictionary
        fmbDict = {1: "2.5 MHz", 2: "5 MHz", 3: "33 MHz", 4: "78 MHz",
                   5: "120 MHz", 6: "225.3 MHz", 7: "350.3 MHz", 8: "500 MHz",
                   9: "800.3 MHz", 10: "1 GHz", 11: "1.5 GHz", 12: "2 GHz",
                   13: "2.5 GHz", 14: "3 GHz", 15: "3.5 GHz", 16: "4 GHz",
                   17: "4.5 GHz", 18: "5 GHz", 19: "5.5 GHz", 20: "5.9 GHz",
                   21: "Aux"}

        error = 'Invlaid input'  # Default error message

        # try:
        # Collect input from line prompts
        dut = self.dutPrompt.text()
        path = self.fileLine.text()
        temps = str(self.tempLine.text()).split()
        freqs = str(self.freqLine.text()).split()
        vcoms = str(self.vcomLine.text()).split()

        # Converts and constrains temperature input
        for index in range(len(temps)):
            temps[index] = float(temps[index].strip(','))
            if (temps[index] < -40) | (temps[index] > 125):
                error = 'Temperature out of range'
                raise Exception

        # Converts and constrains frequency input
        for index in range(len(freqs)):
            freqs[index] = float(freqs[index].strip(','))
            if (freqs[index] < 0) | (freqs[index] > 6e9):
                error = 'Frequency out of range'
                raise Exception

            # Converts frequency given to filter box format
            if (freqs[index] >= 1e6) & (freqs[index] < 1e9):
                freqs[index] = '%g MHz' % (freqs[index]/1.0e6)
            elif freqs[index] >= 1e9:
                freqs[index] = '%g GHz' % (freqs[index]/1.0e9)
            print freqs[index]

            # Cross references dictionary to find relevant frequency
            for key in fmbDict:
                if fmbDict[key] == freqs[index]:
                    freqs[index] = key
                    break
                if key >= len(fmbDict):
                    error = 'Frequency not in filter box'
                    raise Exception

        # Converts and constrains common mode voltages
        for index in range(len(vcoms)):
            vcoms[index] = float(vcoms[index].strip(','))
            if (vcoms[index] < 2) | (vcoms[index] > 3):
                error = 'Vcom out of range'
                raise Exception

        print'DUT # = %s' % dut
        print'Temp = %s' % temps
        print'Freq = %s' % freqs

        IMD3main(path, freqs, vcoms, temps, dut)  # Main program call

        print 'Done!'

        # except:
        #     print error  # If execution fails print determined cause



def main():
    # Initialization
    app = QApplication(sys.argv)
    ex = IMDGUI()
    ex.show()
    sys.exit(app.exec_())

main()