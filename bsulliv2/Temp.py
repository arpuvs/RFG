import sys, visa, time
sys.path.append('../Common')
from ADI_GPIB.AgilentN5181A import *

# Supply = E3631A(23)
Source1 = AgilentN5181A(20)
# Source1 = Generic(20)


# print Supply.__SetEnable__(True)
Source1.__SetState__(1)
print Source1.__GetState__()
time.sleep(0.5)
Source1.__SetState__(0)
print Source1.__GetState__()
