import sys, visa, time
sys.path.append('../Common')
from ADI_GPIB.AgilentN6705B import *

Supply = AgilentN6705B(26)

voltagelist = []

# Vsupply = Ch1, Ven = Ch2, Vcom = Ch3
Supply.__SetV__(5, 1)
Supply.__SetI__(0.25, 1)
Supply.__SetI__(0.25, 2)


for i in range(3):
    level = 1.3
    Supply.__SetV__(level, 2)
    Supply.__Enable__(True, (1, 2))
    Isupply = float(Supply.__GetI__(1))
    while Isupply < 0.1:
        level = level+0.0001
        Supply.__SetV__(level, 2)
        time.sleep(0.1)
        Isupply = float(Supply.__GetI__(1))
        if level >= 3.5:
            raise Exception ('Voltage higher than expected')

    print ('Enabled at Ven = %g' % level)

    level = 1.4
    Supply.__SetV__(level, 2)
    Supply.__Enable__(True, (1, 2))
    Isupply = float(Supply.__GetI__(1))
    while Isupply > 0.1:
        # print Isupply
        level = level-0.0001
        Supply.__SetV__(level, 2)
        time.sleep(0.1)
        Isupply = float(Supply.__GetI__(1))
        if level <= 0.5:
            raise Exception ('Voltage lower than expected')

    print ('Disabled at Ven = %g' % level)