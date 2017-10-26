# Date: 10/29/15
# Author: Lloyd Weida
# Purpose: This module is a generic GPIB wrapper for:
# Agilent 83752A RF sweeper
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
import time
from numpy import pi as Pi

class Agilent83752A(GPIBObjectBaseClass):
    # 
    AMODE_HIGH = 'HPOW'
    AMODE_NORM = 'NORM'
    AMODE_AUTO = 'AUTO'

    def __init__(self, addr=-1, delay=0.01):
        GPIBObjectBaseClass.__init__(self, 'Rohde&Schwarz,SMA', addr)
        self.__delay__ = delay


    def __SetFrequency__(self, Frequency):
        '''This function sets the frequency'''
        freq= Frequency
        #freq = "%.10f" % (Frequency/1e6)
        self.instr.write( 'FREQ %7.6f' % (freq) )
        time.sleep(self.__delay__)

    def __SetLevel__(self, Level):
        '''This function sets the  level in dbm'''
        self.instr.write( 'POWer:LEVel %3.3f DBM\r\n' % (Level) )
        time.sleep(self.__delay__)


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
