# Author: Ben Sullivan
# Date: 11/22/2017

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Subs.HD23_P3dB_guissub import HD23Main

class HDGUI(QMainWindow):
    def __init__(self):
        # Defines window
        super(HDGUI, self).__init__(None)

        win = QWidget()

        # Top menu bar
        bar = self.menuBar()
        fil = bar.addMenu('File')
        load = QAction('Open preset', self)
        load.setShortcut('Ctrl+O')
        fil.addAction(load)
        save = QAction('Save preset', self)
        save.setShortcut('Ctrl+S')
        fil.addAction(save)



        # Line prompts
        self.dutPrompt = QLineEdit()
        self.dutPrompt.setText('0')
        self.freqLine = QLineEdit()
        self.freqLine.setText('4e9')
        self.tempLine = QLineEdit()
        self.tempLine.setText('25')

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
        self.run.clicked.connect(lambda: self.runProgram(self.run))

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

        # Form layout
        flo = QFormLayout()
        flo.addRow('DUT #:', self.dutPrompt)
        flo.addRow('Frequencies to Run:', freqLayout)
        flo.addRow('Temperatures to Run:', tempLayout)

        # Final layout
        layout = QVBoxLayout()
        layout.addLayout(flo)
        layout.addStretch()
        layout.addWidget(self.run)

        # Window properties
        win.setLayout(layout)
        self.setCentralWidget(win)
        self.setWindowTitle('HD23 GUI')
        # self.show()

    # Fils line prompts based on button pressed
    def fillButton(self, button):
        if button == self.freqDef:
            self.freqLine.setText('4e9')
        elif button == self.freqSweepDef:
            self.freqLine.setText('1.20E+08, 2.25E+08, 5.00E+08, 1.00E+09, 1.50E+09, 2.00E+09, '
                                  '2.50E+09, 3.00E+09, 3.50E+09, 4.00E+09')
        elif button == self.tempDef:
            self.tempLine.setText('25')
        elif button == self.tempSweepDef:
            self.tempLine.setText('25, 80, -40')

    def runProgram(self, button):

        error = 'Invlaid input'
        # print self.tempLine.text()
        try:
            temps = str(self.tempLine.text()).split()
            freqs = str(self.freqLine.text()).split()

            for index in range(len(temps)):
                temps[index] = float(temps[index].strip(','))
                if (temps[index] < -40) | (temps[index] > 125):
                    error = 'Temperature out of range'
                    raise Exception

            for index in range(len(freqs)):
                freqs[index] = float(freqs[index].strip(','))
                if (freqs[index] < 0) | (freqs[index] > 6e9):
                    error = 'Frequency out of range'
                    raise Exception

            print'DUT # = %s' % self.dutPrompt.text()
            print'Temp = %s' % temps
            print'Freq = %s' % freqs

            HD23Main(path, freqs, vcoms, temps)



        except:
            print error


        # HD23(self.dutPrompt.text(), self.tempLine.text(), self.freqLine.text(), self.fileLine.text())


def main():
    app = QApplication(sys.argv)
    ex = HDGUI()
    ex.show()
    sys.exit(app.exec_())

main()