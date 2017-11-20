import sys
for key, item in sys.modules.items():
    if ( key.startswith ('ADI_USB.') ): ## Make sure not to remove ADI_USB itself         
        import sys
        sys.modules.pop( key )
# del key, item, sys

# print os.listdir()

try:
    #print "I am in here..."
    #import test
    #print "I am in here 2"
    import DJs_Filter
    #print "test", DJs_Filter.__file__
    reload(DJs_Filter)
    from DJs_Filter import DJs_Filter, GetAllDJs_Filters
except Exception, e:
    print "Cannot import DJs_Filter", e
    del e
try:
    import SenseBox
    reload(SenseBox)
    from SenseBox import SenseBox, GetAllSenseBoxes    
except Exception, e:
    print "Cannot import SenseBox", e
    del e

def GetAllUSBDevices(activate_usb_filters = True):
    rlist = []
    usb_visa_devices = USBObject.GetAllUSBVISADevices()
    djs_filters = []
    senseboxes  = []
    if (globals().has_key('DJs_Filter') and activate_usb_filters):
        djs_filters = GetAllDJs_Filters()
    if (globals().has_key('SenseBox')):
        senseboxes = GetAllSenseBoxes()
    
    rlist.extend(usb_visa_devices)
    rlist.extend(djs_filters)
    rlist.extend(senseboxes)
    
    return rlist

from USBObject import GetAllUSBVISADevices
from Keithley2230 import Keithley2230
from Agilent34461A import Agilent34461A
from CLE1000 import CLE1000
from KeyM8045A import KeyM8045A
