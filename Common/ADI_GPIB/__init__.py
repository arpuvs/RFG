## Revised by Leah Magaldi on May 5th, 2014
"""
May 5, 2014
Added instument to the list
sept 2010
Unloading all modules under ADI_GPIB and reloading them again.... This is done
so that you just need to do reload( ADI_GPIB ) instead of exiting out of Boa or
your Shell after making some changes to the individual instrument files

Talk to Kaushal Shrestha or Rodney Kranz if you have questions about this.
"""
import sys
for key, item in sys.modules.items() :
    if ( key.startswith ('ADI_GPIB.') or
         'ADI_GPIB_DEBUG' in key)     : ## Make sure not to remove ADI_GPIB itself
        sys.modules.pop( key )
        #print "Popping ", key
del key, item, sys

# Package initialisation
from GPIBObject import GetAllGPIBDevices

#Drivers
from SMG            import SMG
from SMHU           import SMHU
from SMA            import SMA
from SML            import SML
from SMJ            import SMJ
from SMIQ           import SMIQ
from SG384          import SG384
from KnL_Filter     import KnL_Filter
from FSEA           import FSEA
from E3631A         import E3631A
from E3646A         import E3646A
from E5052          import E5052
from HP34401A       import HP34401A
from HP34410A       import HP34410A
from HP53181A       import HP53181A
from HP8644         import HP8644
from L4445A         import L4445A
from PS2521G        import PS2521G
from T2420          import T2420
from TurboJet       import TurboJet
from ThermoJet      import ThermoJet
from AirJetXE75     import AirJetXE75
from TurboJet       import AF_MIN as C_TURBOJET_AF_MIN
from TurboJet       import AF_MED as C_TURBOJET_AF_MED
from TurboJet       import AF_MAX as C_TURBOJET_AF_MAX
from DP8200         import DP8200
from Thermo4300     import Thermo4300
from Agilent34970A  import Agilent34970A
from Agilent83752A  import Agilent83752A
from TEK_DPO70604   import TEK_DPO70604
from Agilent11713A  import Agilent11713A
from Agilent33250A  import Agilent33250A
from TEK_HFS9003    import TEK_HFS9003
from Boonton9232    import Boonton9232
from AgilentL7206A  import AgilentL7206A
from TEK_DG2020A    import TEK_DG2020A
from InstekPST3202  import InstekPST3202
from Agilent4155B   import Agilent4155B
from TenneyJr       import TenneyJr
from Generic        import Generic

#imports added May 2014
from Keithley2700   import Keithley2700
from HP661XC        import HP661XC
from Agilent_86100D import Agilent86100d
from HP6629A        import HP6629A
from HP6624A        import HP6624A
from Agilent3499    import Agilent3499

#imports added June 2015
from TekDSA72504D   import TekDSA72504D
from TekDSA72504D_alt   import TekDSA72504D_alt
from Keithley2400_SMU import Keithley2400SMU
from E3633A         import E3633A
from SDG12070       import SDG12070
from SDG12060       import SDG12060

# Merged from Lloyds person ADI_GPIB Library 2017-02-07
from ADV_D3186      import ADV_D3186
from HP8563EC       import HP8563EC
from ADI_GPIB.LeCroyHDO6104 import HDO6104

# import added from Lloyds May 2017
from AgilentE8257D        import AgilentE8257D

#GPIB Dashboard
from GPIB_DB  import GPIB_DB

#Import each GUI
from HP8644   import GPIB_DB_HP8644 as __GPIB_DB_HP8644__
from SMG      import GPIB_DB_SMG    as __GPIB_DB_SMG__
from SMHU     import GPIB_DB_SMHU   as __GPIB_DB_SMHU__
from SMA      import GPIB_DB_SMA    as __GPIB_DB_SMA__
from SML      import GPIB_DB_SML    as __GPIB_DB_SML__

from E3631A   import GPIB_DB_E3631A  as __GPIB_DB_E3631A__
from E3646A   import GPIB_DB_E3646A  as __GPIB_DB_E3646A__
from PS2521G  import GPIB_DB_PS2521G as __GPIB_DB_PS2521G__
from DP8200   import GPIB_DB_DP8200  as __GPIB_DB_DP8200__
from InstekPST3202 import GPIB_DB_PST3202 as __GPIB_DB_PST3202__

#Add GUI to GPIB_DB Container
GPIB_DB.HP8644 = __GPIB_DB_HP8644__
GPIB_DB.SMG    = __GPIB_DB_SMG__
GPIB_DB.SMHU   = __GPIB_DB_SMHU__
GPIB_DB.SMA    = __GPIB_DB_SMA__
GPIB_DB.SML    = __GPIB_DB_SML__

GPIB_DB.E3631A  = __GPIB_DB_E3631A__
GPIB_DB.E3646A  = __GPIB_DB_E3646A__
GPIB_DB.PS2625G = __GPIB_DB_PS2521G__
GPIB_DB.DP8200  = __GPIB_DB_DP8200__
GPIB_DB.PST3202 = __GPIB_DB_PST3202__

#TESTING
#from TDS654C import TDS654C
#from TDS7404 import TDS7404
