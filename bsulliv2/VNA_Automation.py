# Incorporating structure from ADL5569_VNA_Automation Vee file
import sys, visa, time
sys.path.append('../Common')

from ADI_GPIB.AgilentE5071C import *
VNA = AgilentE5071C(01)


def VNAinit():
    VNA.__SetSweepType(1, 'LOG')
    VNA.__SetStartf__(1, 10e06)
    VNA.__SetStopf__(1, 10.01e09)
    VNA.__SetNumPoints__(1, 1e3)
    VNA.__SetAvg__(1, 16)
    VNA.__SetAutoTime__(1, True)
    VNA.__SetTrigType__('MAN')
    VNA.__SetContinuous__(1, False)
    VNA.__EnableAvg(1, True)
    VNA.__EnableTrigAvg__(True)

def setTemp():
    print 'Temp'

def setSupply():
    print 'SCPI in SET_VPOS'

def getData():
    print 'Final calls at end of program'


supplies = []
temps = []

VNAinit()
for temp in temps:
    setTemp()
    for supply in supplies:
        setSupply()
        getData()

