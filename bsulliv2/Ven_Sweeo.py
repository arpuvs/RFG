import sys, visa, time
sys.path.append('../Common')
from ADI_GPIB.AgilentN6705B import *

Supply = AgilentN6705B(26)

voltagelist = []

# Vsupply = Ch1, Ven = Ch2, Vcom = Ch3
Supply.__SetV__(5, 1)
Supply.__SetI__(0.25, 1)
Supply.__SetI__(0.25, 2)

level = 0
Supply.__SetV__(level, 2)
Isupply = Supply.__GetI__(2)
while Isupply() < 0.1:
    level = level+0.01
    Supply.__SetV__(level)
    time.sleep(0.1)
    if level >= 3.5:
        raise Exception ('Voltage higher than expected')

print ('Enabled at Ven = %g' % level)
