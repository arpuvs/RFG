# --------------------------------------------------
# Rev. History
# Author: Rodney Kranz
# Date: 02/27/2013
# Added Clock Synthesizer (SMA-B29) Control
# --------------------------------------------------
# Rev. History
# Author: Kaushal Shrestha
# Date: 05/16/2011
# Added Attenuator Mode Control
# --------------------------------------------------
# Rev. History
# Author: Kaushal Shrestha
# Date: 03/05/2011
# Added Automatic Level Control
# --------------------------------------------------
# Rev. History
# Author: Kaushal Shrestha
# Date: 09/01/2010
# Added Phase "get" property
# --------------------------------------------------
# Rev. History
# Author: Rodney Kranz
# Date: 07/20/2010
# Truncated the Frequency write command to 8 digits to the right of the decimal.
# If this is not done, there were occasional problems with coherency.  JJ Ray and Kaushal
#   found this.
# --------------------------------------------------
# Rev. History
# Author: Rodney Kranz
# Date: 04/30/2009
# Added PhaseDeg
# --------------------------------------------------
# Rev. History
# Author: Tom MacLeod
# Date: 07/28/2008
# Added Frequency "get" property
# --------------------------------------------------
# Author: Tom MacLeod
# Date: 07/05/2007
# Added GUI for GPIB Dashboard
# --------------------------------------------------
# Author: Tom MacLeod
# Date: 11/06/2007
# Purpose: Added RemoteRelease() to release front panel
# --------------------------------------------------
# Author: Michael Viamari
# Date: 4/23/2007
# Purpose: Added Phase Modulation Control Commands
# --------------------------------------------------
# Author: Tom MacLeod
# Date: 12/1/2006
# Purpose: This module is a generic GPIB wrapper for:
# ROHDE & SCHWARZ SMA Generators
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
import time
from numpy import pi as Pi

class SMA(GPIBObjectBaseClass):
    # SMA properties, wished we had enums
    AMODE_HIGH = 'HPOW'
    AMODE_NORM = 'NORM'
    AMODE_AUTO = 'AUTO'

    def __init__(self, addr=-1, delay=0.01):
        GPIBObjectBaseClass.__init__(self, 'Rohde&Schwarz,SMA', addr)
        self.__delay__ = delay

    def __SetPhaseDeg__(self, PhaseDeg):
        '''This function sets the SMA phase'''
        self.instr.write( 'PHASE %sDEG' % (str(PhaseDeg)) )
        time.sleep(self.__delay__)

    def __GetPhaseDeg__(self):
        '''This function gets the SMA phase'''
        phase = self.instr.ask( 'PHASE?' )
        return float( phase )

    def __SetFrequency__(self, Frequency):
        '''This function sets the SMA frequency'''
        freq = "%.10f" % (Frequency/1e6)
        freq = freq.split('.')
        freq_1 = freq[0]
        freq_2 = freq[1][:8]
        self.instr.write( 'FREQ %s.%sMHz' % (freq_1, freq_2) )
        time.sleep(self.__delay__)

    def __GetFrequency__(self):
        '''This function gets the SMA frequency'''
        freq = self.instr.ask( 'FREQ?' )
        return float( freq )

    def __SetLevel__(self, Level):
        '''This function sets the SMA level'''
        self.instr.write( 'POW %sdBm' % (str(Level)) )
        time.sleep(self.__delay__)

    def __GetLevel__(self):
        '''This function gets the SMA level'''
        return float( self.instr.ask( 'POW?' ) )

    def __SetEnable__(self, enable):
        '''This function enables the RF On/Off for the SMA'''
        if enable:
            self.instr.write('OUTP:STAT ON')
        else:
            self.instr.write('OUTP:STAT OFF')
        time.sleep(self.__delay__)

    def __GetEnable__(self):
        '''This function gets the RF On/Off status for the SMA'''
        return bool(int(self.instr.ask('OUTP:STAT?')))

    def __SetDelay__(self, d):
        '''Sets this instruments settling time'''
        self.__delay__ = d

    def __GetDelay__(self):
        '''Gets this instrument's settling time'''
        return self.__delay__

    def __SetPMStatus__(self, status):
        '''This function sets the SMA Phase Modulation Status'''
        if status:
            self.instr.write('PM:STAT ON')
        else:
            self.instr.write('PM:STAT OFF')

    def __GetPMStatus__(self):
        '''This function gets the SMA level'''
        return self.instr.ask('PM:STAT?')

    def __SetPMMode__(self, mode):
        '''This function sets the SMA Phase Modulation Mode'''
        if (mode == 0) or (mode == "HBAN"):
            #High Bandwidth
            self.instr.write('PM:MODE HBAN')
        elif (mode == 1) or (mode == "HDEV"):
            #High Deviation
            self.instr.write('PM:MODE HDEV')
        elif (mode == 2) or (mode == "LNO"):
            #Low Noise
            self.instr.write('PM:MODE LNO')
        else:
            #Default to High Bandwidth
            self.instr.write('PM:MODE HBAN')

    def __GetPMMode__(self):
        '''This function gets the SMA level'''
        return self.instr.ask('PM:MODE?')

    def __SetPMDev__(self, dev):
        #dev is in radians, write command is in degrees
        '''This function sets the SMA Phase Mod Internal Devation'''
        dev_deg = (dev*180)/Pi
        self.instr.write('PM:DEV %s' % str(dev_deg))
        time.sleep(self.__delay__)

    def __GetPMDev__(self):
        #read command returns degrees
        #this function returns radians
        '''This function sets the SMA Phase Mod Internal Devation'''
        dev_deg = float(self.instr.ask('PM:DEV?'))
        dev = (dev_deg*Pi)/180
        return dev

    def __SetPMExtDev__(self, dev):
        #dev is in radians, write command is in degrees
        '''This function sets the SMA Phase Mod External Devation'''
        dev_deg = (dev*180)/Pi
        self.instr.write('PM:EXT:DEV %s' % str(dev_deg))
        time.sleep(self.__delay__)

    def __GetPMExtDev__(self):
        #read command returns degrees
        #this function returns radians
        '''This function sets the SMA Phase Mod External Devation'''
        dev_deg = float(self.instr.ask('PM:EXT:DEV?'))
        dev = (dev_deg*Pi)/180
        return dev

    def __SetPMExtImp__(self, impedance):
        if (impedance == 50) or (impedance == "50") or (impedance == "G50"):
            #50 Ohm to Ground
            self.instr.write('INP:MOD:IMP G50')
        else:
            #Default to High Impedance
            self.instr.write('INP:MOD:IMP HIGH')

    def __GetPMExtImp__(self):
        '''This function gets the SMA level'''
        return self.instr.ask('INP:MOD:IMP?')

    def __SetPMINTSource__(self, src):
        '''This function sets the SMA Phase Modulation Internal Source'''
        if (src == 0) or (src == "LF1"):
            #LF1
            self.instr.write('PM:INT:SOUR LF1')
        elif (src == 1) or (src == "LF2"):
            #LF2
            self.instr.write('PM:INT:SOUR LF2')
        elif (src == 2) or (src == "LF12"):
            #LF1 and LF2
            self.instr.write('PM:INT:SOUR LF12')
        elif (src == 3) or (src == "LF1Noise"):
            #LF1 with Noise
            self.instr.write('PM:INT:SOUR LF1Noise')
        elif (src == 4) or (src == "LF2Noise"):
            #LF2 with Noise
            self.instr.write('PM:INT:SOUR LF2Noise')
        elif (src == 5) or (src == "Noise"):
            #Noise
            self.instr.write('PM:INT:SOUR Noise')
        else:
            #Default to LF1
            self.instr.write('PM:INT:SOUR LF1')

    def __GetPMINTSource__(self):
        '''This function gets the SMA Phase Modulation Internal Source'''
        return self.instr.ask('PM:INT:SOUR?')

    def __SetPMSource__(self, src):
        '''This function sets the SMA Phase Modulation Source'''
        if (src == 0) or (src == "INT"):
            #LF1
            self.instr.write('PM:SOUR INT')
        elif (src == 1) or (src == "EXT"):
            #LF2
            self.instr.write('PM:SOUR EXT')
        else:
            #Default to Internal
            self.instr.write('PM:SOUR INT')

    def __GetPMSource__(self):
        '''This function gets the SMA Phase Modulation Source'''
        return self.instr.ask('PM:SOUR?')

    def __SetLF1Freq__(self, Freq):
        '''This function sets the LF Generator 1 frequency'''
        self.instr.write( 'LF01:FREQ %skHz' % (str(Freq/1e3)) )
        time.sleep(self.__delay__)

    def __SetLF2Freq__(self, Freq):
        #Not all SMA's have an LF2
        '''This function sets the LF Generator 2 frequency'''
        self.instr.write( 'LF02:FREQ %skHz' % (str(Freq/1e3)) )
        time.sleep(self.__delay__)

    def __SetALC__(self, ALC):
        '''This function sets the Auto Level Control
           ACL = { 'OFF', 'ON', 'AUTO' }
        '''
        ALC = ALC.upper()
        if ALC in ['ON', 'OFF', 'AUTO']:
            self.instr.write( 'POW:ALC %s' % ALC )
            time.sleep(self.__delay__)

    def __GetALC__(self):
        '''This function gets the Auto Level Control'''
        ALC = self.instr.ask('POW:ALC?')
        return ALC

    def __SetAMode__ ( self, MODE ) :
        '''
        This function sets the attenuator mode of the SMA
           MODE = { 'AUTO', 'NORMAL', 'HIGH' }
        '''
        if MODE in [ self.AMODE_HIGH, self.AMODE_AUTO, self.AMODE_NORM ] :
            self.instr.write( 'OUTP:AMOD %s' % MODE )
            time.sleep(self.__delay__)

    def __GetAMode__ ( self ) :
        '''
        This function gets the attenuator mode of the SMA
           MODE = { 'AUTO', 'NORMAL', 'HIGH' }
        '''
        MODE = self.instr.ask( 'OUTP:AMOD?' )
        return MODE

    def RemoteRelease(self):
        '''This function releases the SMA front panel'''
        self.instr.write( 'SYS:KLOC OFF' )

    def __GetCsynInstalled__(self):
        '''Returns if the unit has the B29 option installed '''
        return 'SMA-B29' in self.instr.ask('*OPT?')

    def __GetCsynEnabled__(self):
        '''Returns whether the clock synthesizer (B29) has been enabled'''
        return bool(int(self.instr.ask('CSYN:STAT?')))

    def __SetCsynEnabled__(self, enable):
        '''Enables / Disables the clock synthesizer (B29).'''
        if enable:
            self.instr.write('CSYN:STAT ON')
        else:
            self.instr.write('CSYN:STAT OFF')

    def __SetCsynFrequency__(self, Frequency):
        '''This function sets the SMA synthesized clock (B29) frequency'''
        freq = "%.10f" % (Frequency/1e6)
        freq = freq.split('.')
        freq_1 = freq[0]
        freq_2 = freq[1][:8]
        self.instr.write('CSYN:FREQ %s.%sMHz' % (freq_1, freq_2) )
        time.sleep(self.__delay__)

    def __GetCsynFrequency__(self):
        '''This function gets the SMA synthesized clock (B29) frequency'''
        freq = self.instr.ask('CSYN:FREQ?')
        return float(freq)

    Frequency = property(__GetFrequency__, __SetFrequency__, None, "Gets/Sets the SMA Frequency")
    Level     = property(__GetLevel__, __SetLevel__, None, "Gets/Sets the SMA Level")
    Enabled   = property(__GetEnable__, __SetEnable__,        None, "Gets/Sets the SMA RF On/Off")
    PhaseDeg  = property(__GetPhaseDeg__, __SetPhaseDeg__, None, "Gets/Sets the SMA Phase in Degrees")

    PMDev       = property(__GetPMDev__, __SetPMDev__, None, "Sets the Phase Modulation Internal Deviation")
    PMExtDev    = property(__GetPMExtDev__, __SetPMExtDev__, None, "Sets the Phase Modulation External Deviation")
    PMMode      = property(__GetPMMode__, __SetPMMode__, None, "Sets the Phase Modulation Mode")
    PMSource    = property(__GetPMSource__, __SetPMSource__, None, "Sets the Phase Modulation Source")
    PMINTSource = property(__GetPMINTSource__, __SetPMINTSource__, None, "Sets the Phase Modulation Internal Source")
    PMExtImp    = property(__GetPMExtImp__, __SetPMExtImp__, None, "Sets the Phase Modulation External Input Impedance")
    PMEnable    = property(__GetPMStatus__, __SetPMStatus__, None, "Sets the Phase Modulation On/Off")

    LF1Freq     = property(None, __SetLF1Freq__, None, "Sets the LF1 Generator Frequency")
    LF2Freq     = property(None, __SetLF2Freq__, None, "Sets the LF1 Generator Frequency")

    Delay = property(__GetDelay__, __SetDelay__, None, "Delay")

    ALC  = property(__GetALC__, __SetALC__, None, "Automatic Level Control")
    AMODE = property(__GetAMode__, __SetAMode__, None, "Attenuator Mode Control")

    CsynInstalled = property(__GetCsynInstalled__, None, "Checks to see if the B29 optional clock synthesizer (rear differential output) is installed.")
    CsynEnabled = property(__GetCsynEnabled__, __SetCsynEnabled__, None, "Enables the clock synthesizer (rear differential output).  B29 option is required.")
    CsynFrequency = property(__GetCsynFrequency__, __SetCsynFrequency__, None, "Sets the clock synthesizer frequency (rear differential output).  B29 option is required.")

#GUI Code
import GPIB_Dashboard.Utils
from wx import NewId as wxNewId

[wxID_BTNFREQ, wxID_BTNSETAMP, wxID_BTNSETFREQ,
 wxID_CHKENABLED, wxID_LBLAMP, wxID_LBLFREQ,
 wxID_LBLGPIBADDR, wxID_PANEL1, wxID_SPINBUTTON3,
 wxID_SPNAMPLSB, wxID_SPNAMPMSB, wxID_SPNFREQLSB,
 wxID_SPNFREQMSB, wxID_STL1, wxID_TXTAMP,
 wxID_TXTFREQ, wxID_TXTGPIBADDR, wxID_TXTUSAGE,
 wxID_SPNAMPTENTHS
] = [wxNewId() for _init_ctrls in range(19)]

class GPIB_DB_SMA( GPIB_Dashboard.Utils.InstrumentBaseClass ):
    def __init__(self):
        self.SetFunction( 'Generator' )
        self.SetName( 'SMA' )
        self.SetAddress( 0 )
        self.this_driver = SMA

    def CreateGUI(self, parent):
        # I import here so I don't waste memory if the user isn't using a GUI
        import wx

        staticbox = wx.StaticBox(parent, -1, self.GetName(), size=(264, 140))

        self.txtUsage = wx.TextCtrl(id=wxID_TXTUSAGE, name=u'txtUsage',
              parent=staticbox, pos=wx.Point(8, 16), size=wx.Size(64, 21),
              style=0, value=u'--Usage--')

        self.lblGPIBAddr = wx.StaticText(id=wxID_LBLGPIBADDR,
              label=u'GPIB Addr:', name=u'lblGPIBAddr', parent=staticbox,
              pos=wx.Point(168, 16), size=wx.Size(53, 13), style=0)

        self.txtGPIBAddr = wx.TextCtrl(id=wxID_TXTGPIBADDR,
              name=u'txtGPIBAddr', parent=staticbox, pos=wx.Point(232, 16),
              size=wx.Size(24, 21), style=0, value=u'')
        self.txtGPIBAddr.Bind(wx.EVT_TEXT, self.OnTxtGPIBAddrText,
              id=wxID_TXTGPIBADDR)

        self.chkEnabled = wx.CheckBox(id=wxID_CHKENABLED,
              label=u'Enabled?', name=u'chkEnabled', parent=staticbox,
              pos=wx.Point(88, 16), size=wx.Size(70, 13), style=0)
        self.chkEnabled.SetValue(True)
        self.chkEnabled.Bind(wx.EVT_CHECKBOX, self.OnChkEnabledCheckbox,
              id=wxID_CHKENABLED)

        self.stl1 = wx.StaticLine(id=wxID_STL1, name=u'stl1',
              parent=staticbox, pos=wx.Point(8, 48), size=wx.Size(248, 2),
              style=0)

        self.lblFreq = wx.StaticText(id=wxID_LBLFREQ,
              label=u'Frequency (MHz):', name=u'lblFreq', parent=staticbox,
              pos=wx.Point(16, 64), size=wx.Size(86, 13), style=0)

        self.txtFreq = wx.TextCtrl(id=wxID_TXTFREQ, name=u'txtFreq',
              parent=staticbox, pos=wx.Point(112, 64), size=wx.Size(72, 21),
              style=0, value=u'')

        self.btnSetFreq = wx.Button(id=wxID_BTNSETFREQ, label=u'Set',
              name=u'btnSetFreq', parent=staticbox, pos=wx.Point(184, 64),
              size=wx.Size(24, 23), style=0)
        self.btnSetFreq.Bind(wx.EVT_BUTTON, self.OnBtnSetFreqButton,
              id=wxID_BTNSETFREQ)

        self.lblAmp = wx.StaticText(id=wxID_LBLAMP,
              label=u'Ampitude (dBm):', name=u'lblAmp', parent=staticbox,
              pos=wx.Point(16, 104), size=wx.Size(80, 13), style=0)

        self.txtAmp = wx.TextCtrl(id=wxID_TXTAMP, name=u'txtAmp',
              parent=staticbox, pos=wx.Point(112, 104), size=wx.Size(72, 21),
              style=0, value=u'')

        self.btnFreq = wx.Button(id=wxID_BTNFREQ, label=u'Set',
              name=u'btnFreq', parent=staticbox, pos=wx.Point(184, 64),
              size=wx.Size(24, 23), style=0)

        self.spnFreqMSB = wx.SpinButton(id=wxID_SPNFREQMSB,
              name=u'spnFreqMSB', parent=staticbox, pos=wx.Point(216, 64),
              size=wx.Size(18, 25), style=wx.SP_VERTICAL)
        self.spnFreqMSB.Bind(wx.EVT_SPIN_DOWN, self.OnSpnFreqMSBSpinDown,
              id=wxID_SPNFREQMSB)
        self.spnFreqMSB.Bind(wx.EVT_SPIN_UP, self.OnSpnFreqMSBSpinUp,
              id=wxID_SPNFREQMSB)

        self.spinButton3 = wx.SpinButton(id=wxID_SPINBUTTON3,
              name='spinButton3', parent=staticbox, pos=wx.Point(248, 72),
              size=wx.Size(0, 17), style=wx.SP_HORIZONTAL)

        self.spnFreqLSB = wx.SpinButton(id=wxID_SPNFREQLSB,
              name=u'spnFreqLSB', parent=staticbox, pos=wx.Point(240, 64),
              size=wx.Size(16, 24), style=wx.SP_VERTICAL)
        self.spnFreqLSB.Bind(wx.EVT_SPIN_DOWN, self.OnSpnFreqLSBSpinDown,
              id=wxID_SPNFREQLSB)
        self.spnFreqLSB.Bind(wx.EVT_SPIN_UP, self.OnSpnFreqLSBSpinUp,
              id=wxID_SPNFREQLSB)

        self.spnAmpMSB = wx.SpinButton(id=wxID_SPNAMPMSB,
              name=u'spnAmpMSB', parent=staticbox, pos=wx.Point(212, 104),
              size=wx.Size(16, 25), style=wx.SP_VERTICAL)
        self.spnAmpMSB.Bind(wx.EVT_SPIN_DOWN, self.OnSpnAmpMSBSpinDown,
              id=wxID_SPNAMPMSB)
        self.spnAmpMSB.Bind(wx.EVT_SPIN_UP, self.OnSpnAmpMSBSpinUp,
              id=wxID_SPNAMPMSB)

        self.spnAmpTenths = wx.SpinButton(id=wxID_SPNAMPTENTHS,
              name=u'spnAmpTenths', parent=staticbox, pos=wx.Point(228, 104),
              size=wx.Size(16, 25), style=wx.SP_VERTICAL)
        self.spnAmpTenths.Bind(wx.EVT_SPIN_DOWN, self.OnSpnAmpTenthsSpinDown,
              id=wxID_SPNAMPTENTHS)
        self.spnAmpTenths.Bind(wx.EVT_SPIN_UP, self.OnSpnAmpTenthsSpinUp,
              id=wxID_SPNAMPTENTHS)

        self.spnAmpLSB = wx.SpinButton(id=wxID_SPNAMPLSB,
              name=u'spnAmpLSB', parent=staticbox, pos=wx.Point(244, 104),
              size=wx.Size(16, 25), style=wx.SP_VERTICAL)
        self.spnAmpLSB.Bind(wx.EVT_SPIN_DOWN, self.OnSpnAmpLSBSpinDown,
              id=wxID_SPNAMPLSB)
        self.spnAmpLSB.Bind(wx.EVT_SPIN_UP, self.OnSpnAmpLSBSpinUp,
              id=wxID_SPNAMPLSB)

        self.btnSetAmp = wx.Button(id=wxID_BTNSETAMP, label=u'Set',
              name=u'btnSetAmp', parent=staticbox, pos=wx.Point(184, 104),
              size=wx.Size(24, 23), style=0)
        self.btnSetAmp.Bind(wx.EVT_BUTTON, self.OnBtnSetAmpButton,
              id=wxID_BTNSETAMP)

        return staticbox

    def RemoteRelease(self):
        instr = self.this_driver( self.GetAddress() )
        instr.RemoteRelease()

    # PROPERTIES!!!
    def GetFreq(self):
        return float( self.txtFreq.GetValue() ) * 1e6
    def SetFreq(self, value):
        self.txtFreq.SetValue( str(value / 1e6) )
        self.RemoteRelease()

    def GetAmp(self):
        return float( self.txtAmp.GetValue() )
    def SetAmp(self, value):
        self.txtAmp.SetValue( str(value) )
        self.RemoteRelease()

    def GetEnable(self):
        return self.chkEnabled.GetValue()

    def GetGPIBAddr(self):
        return int( self.txtGPIBAddr.GetValue() )
    def SetGPIBAddr(self, value):
        self.txtGPIBAddr.SetValue( str(value) )

    def GetINI(self):
        obj = {}
        obj['Usage'] = self.txtUsage.GetValue()
        obj['Enabled'] = self.chkEnabled.GetValue()
        obj['GPIBAddr'] = self.txtGPIBAddr.GetValue()
        obj['Freq'] = self.txtFreq.GetValue()
        obj['Amp'] = self.txtAmp.GetValue()
        return obj
    def SetINI(self, value):
        self.txtUsage.SetValue(value['Usage'])
        self.chkEnabled.SetValue(value['Enabled'])
        self.txtGPIBAddr.SetValue(value['GPIBAddr'])
        self.txtFreq.SetValue(value['Freq'])
        self.txtAmp.SetValue(value['Amp'])

    # EVENTS!!!
    def OnTxtGPIBAddrText(self, event):
        self.SetAddress( self.GetGPIBAddr() )

    def OnBtnSetFreqButton(self, event):
        instr = self.this_driver( self.GetAddress() )
        instr.Frequency = self.GetFreq()

    def OnBtnSetAmpButton(self, event):
        instr = self.this_driver( self.GetAddress() )
        instr.Level = self.GetAmp()

    def OnChkEnabledCheckbox(self, event):
        instr = self.this_driver( self.GetAddress() )
        instr.Enabled = self.GetEnable()

    def OnSpnFreqMSBSpinDown(self, event):
        instr = self.this_driver( self.GetAddress() )
        newfreq = self.GetFreq() - 1e6
        instr.Frequency = newfreq
        self.SetFreq(newfreq)

    def OnSpnFreqMSBSpinUp(self, event):
        instr = self.this_driver( self.GetAddress() )
        newfreq = self.GetFreq() + 1e6
        instr.Frequency = newfreq
        self.SetFreq(newfreq)

    def OnSpnFreqLSBSpinDown(self, event):
        instr = self.this_driver( self.GetAddress() )
        newfreq = self.GetFreq() - 1
        instr.Frequency = newfreq
        self.SetFreq(newfreq)

    def OnSpnFreqLSBSpinUp(self, event):
        instr = self.this_driver( self.GetAddress() )
        newfreq = self.GetFreq() + 1
        instr.Frequency = newfreq
        self.SetFreq(newfreq)

    def OnSpnAmpMSBSpinDown(self, event):
        instr = self.this_driver( self.GetAddress() )
        newamp = self.GetAmp() - 1
        instr.Level = newamp
        self.SetAmp(newamp)

    def OnSpnAmpMSBSpinUp(self, event):
        instr = self.this_driver( self.GetAddress() )
        newamp = self.GetAmp() + 1
        instr.Level = newamp
        self.SetAmp(newamp)

    def OnSpnAmpTenthsSpinDown(self, event):
        instr = self.this_driver( self.GetAddress() )
        newamp = self.GetAmp() - 0.1
        instr.Level = newamp
        self.SetAmp(newamp)

    def OnSpnAmpTenthsSpinUp(self, event):
        instr = self.this_driver( self.GetAddress() )
        newamp = self.GetAmp() + 0.1
        instr.Level = newamp
        self.SetAmp(newamp)

    def OnSpnAmpLSBSpinDown(self, event):
        instr = self.this_driver( self.GetAddress() )
        newamp = self.GetAmp() - 0.01
        instr.Level = newamp
        self.SetAmp(newamp)

    def OnSpnAmpLSBSpinUp(self, event):
        instr = self.this_driver( self.GetAddress() )
        newamp = self.GetAmp() + 0.01
        instr.Level = newamp
        self.SetAmp(newamp)
