# Author: Tom MacLeod

# Date: 03/27/2012 by Kaushal Shrestha
# Added __GetEnabled__ function and Enabled read property

# Date: 04/08/2008
# Added common aliases for properties (improves portability of scripts):
#   PS.V1, PS.V2, PS.V3, PS.I1, PS.I2, PS.I3
# Date: 01/15/2008
# __SetN25V__, __SetN25I__, __MeasN25I__ functions added by Michael Viamari 
# set the Voltage and Current Limits as well as read back current output for -25V Output
# Date: 08/06/2007
# __MeasP6I__ and __MeasP25I__ functions added by Dave Shoudy to 
# readback the current output of each supply
# Data: 12/06/2007
# Added current readback
# Date: 07/05/2007
# Added GUI for GPIB Dashboard
# Rev History --------------------
# Date: 11/01/2006
# Added delay parameter
# Date: 10/27/2006
# Purpose: This module is a generic GPIB wrapper for:
# HEWLETT-PACKARD E3631A Power Supply
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
from numpy import clip
import time

class E3631A(GPIBObjectBaseClass):
    def __init__(self, addr=-1, delay=0.5):
        GPIBObjectBaseClass.__init__(self, 'HEWLETT-PACKARD,E3631A', addr)
        self.__delay__ = delay
        
    def __MeasP6V__(self):
        '''This function measures the voltage output of the 6V supply'''
        volt = self.instr.ask('MEAS:VOLT:DC? P6V')
        time.sleep(self.__delay__)
        return volt
        
    def __MeasP6I__(self):
        '''This function measures the current output of the 6V supply'''
        curr = self.instr.ask('MEAS:CURR:DC? P6V')
        time.sleep(self.__delay__)
        return curr
    
    def __MeasP25V__(self):
        '''This function measures the voltage output of the 25V supply'''
        volt = self.instr.ask('MEAS:VOLT:DC? P25V')
        time.sleep(self.__delay__)
        return volt
        
    def __MeasP25I__(self):
        '''This function measures the current output of the 25V supply'''
        curr = self.instr.ask('MEAS:CURR:DC? P25V')
        time.sleep(self.__delay__)
        return curr
    
    def __MeasN25V__(self):
        '''This function measures the voltage output of the N25V supply'''
        volt = self.instr.ask('MEAS:VOLT:DC? N25V')
        time.sleep(self.__delay__)
        return volt
        
    def __MeasN25I__(self):
        '''This function measures the current output of the N25V supply'''
        curr = self.instr.ask('MEAS:CURR:DC? N25V')
        time.sleep(self.__delay__)
        return curr
    
    def __SetP6V__(self, P6V):
        '''This function sets the E3631A P6V'''
        P6V = clip(P6V, 0, 6.18)
        self.instr.write('INST P6V')
        self.instr.write('VOLT ' + str(P6V))
        time.sleep(self.__delay__)
    
    def __SetP6I__(self, P6I):
        '''This function sets the E3631A P6V Current'''
        P6I = clip(P6I, 0, 5.15)
        self.instr.write('INST P6V')
        self.instr.write('CURR ' + str(P6I))
        time.sleep(self.__delay__)
    
    def __SetP25V__(self, P25V):
        '''This function sets the E3631A P25V Voltage'''
        P25V = clip(P25V, 0, 25.75)
        self.instr.write('INST P25V')
        self.instr.write('VOLT ' + str(P25V))
        time.sleep(self.__delay__)
    
    def __SetP25I__(self, P25I):
        '''This function sets the E3631A P25V Current'''
        P25I = clip(P25I, 0, 1.03)
        self.instr.write('INST P25V')
        self.instr.write('CURR ' + str(P25I))
        time.sleep(self.__delay__)

    def __SetN25V__(self, N25V):
        '''This function sets the E3631A N25V Voltage'''
        N25V = clip(N25V, -25.75, 0)
        self.instr.write('INST N25V')
        self.instr.write('VOLT ' + str(N25V))
        time.sleep(self.__delay__)
    
    def __SetN25I__(self, N25I):
        '''This function sets the E3631A N25V Current'''
        P25I = clip(N25I, 0, 1.03)
        self.instr.write('INST N25V')
        self.instr.write('CURR ' + str(N25I))
        time.sleep(self.__delay__)
        
    def __SetEnable__(self, Enabled):
        '''This function enables the On/Off for the E3631A'''
        if Enabled:
            self.instr.write('OUTP ON')
        else:
            self.instr.write('OUTP OFF')
        time.sleep(self.__delay__)
    
    def __GetEnable__(self):
        '''This function returns the On/Off state for the E3631A'''
        status = self.instr.ask('OUTP?')
        if (status == "1" or status == "ON" ):
            return True
        return False        
        
    def __SetDelay__(self, d):
        '''Sets this instruments settling time'''
        self.__delay__ = d
        
    def __GetDelay__(self):
        '''Gets this instrument's settling time'''
        return self.__delay__
    
    P6V  = property(__MeasP6V__, __SetP6V__,    None, "Sets the E3631A P6V")
    P6I  = property(__MeasP6I__, __SetP6I__,    None, "Sets the E3631A P6V Current")
    
    P25V = property(__MeasP25V__, __SetP25V__,   None, "Sets the E3631A P25V")
    P25I = property(__MeasP25I__, __SetP25I__,   None, "Sets the E3631A P25V Current")

    N25V = property(__MeasN25V__, __SetN25V__,   None, "Sets the E3631A N25V")
    N25I = property(__MeasN25I__, __SetN25I__,   None, "Sets the E3631A N25V Current")

    #Aliases
    V1 = property(__MeasP6V__, __SetP6V__,    None, "Sets the E3631A P6V")
    I1 = property(__MeasP6I__, __SetP6I__,    None, "Sets the E3631A P6V Current")

    V2 = property(__MeasP25V__, __SetP25V__,   None, "Sets the E3631A P25V")
    I2 = property(__MeasP25I__, __SetP25I__,   None, "Sets the E3631A P25V Current")

    V3 = property(__MeasN25V__, __SetN25V__,   None, "Sets the E3631A N25V")
    I3 = property(__MeasN25I__, __SetN25I__,   None, "Sets the E3631A N25V Current")
   

    Enabled = property(__GetEnable__, __SetEnable__, None, "Sets the E3631A On/Off")
    
    Delay = property(__GetDelay__, __SetDelay__, None, "Delay")
  
    
# GUI Code
import GPIB_Dashboard.Utils
from wx import NewId as wxNewId

[wxID__, wxID__BTNP2, wxID__BTNSETP1, wxID__CHKENABLED, wxID__LBLGPIBADDR, 
 wxID__LBLP1, wxID__PANEL1, wxID__SPNP1LSB, wxID__SPNP1MSB, wxID__SPNP2LSB, 
 wxID__SPNP2MSP, wxID__STATICTEXT1, wxID__STL1, wxID__TXTGPIBADDR, 
 wxID__TXTP1, wxID__TXTP1USAGE, wxID__TXTP2, wxID__TXTP2USAGE, 
] = [wxNewId() for _init_ctrls in range(18)]

class GPIB_DB_E3631A( GPIB_Dashboard.Utils.InstrumentBaseClass ):
    def __init__(self):
        self.SetFunction( 'Power Supply' )
        self.SetName( 'E3631A' )
        self.SetAddress( 0 )
        self.this_driver = E3631A
        
    def CreateGUI(self, parent):
        # I import here so I don't waste memory if the user isn't using a GUI
        import wx
        
        staticbox = wx.StaticBox(parent, -1, self.GetName(), size=(264, 140))
        
        self.lblGPIBAddr = wx.StaticText(id=wxID__LBLGPIBADDR,
              label=u'GPIB Addr:', name=u'lblGPIBAddr', parent=staticbox,
              pos=wx.Point(168, 16), size=wx.Size(53, 13), style=0)

        self.txtGPIBAddr = wx.TextCtrl(id=wxID__TXTGPIBADDR,
              name=u'txtGPIBAddr', parent=staticbox, pos=wx.Point(232, 16),
              size=wx.Size(24, 21), style=0, value=u'')
        self.txtGPIBAddr.Bind(wx.EVT_TEXT, self.OnTxtGPIBAddrText,
              id=wxID__TXTGPIBADDR)

        self.chkEnabled = wx.CheckBox(id=wxID__CHKENABLED, label=u'Enabled?',
              name=u'chkEnabled', parent=staticbox, pos=wx.Point(88, 16),
              size=wx.Size(70, 13), style=0)
        self.chkEnabled.SetValue(True)
        self.chkEnabled.Bind(wx.EVT_CHECKBOX, self.OnChkEnabledCheckbox,
              id=wxID__CHKENABLED)

        self.stl1 = wx.StaticLine(id=wxID__STL1, name=u'stl1',
              parent=staticbox, pos=wx.Point(8, 48), size=wx.Size(248, 2),
              style=0)

        self.lblP1 = wx.StaticText(id=wxID__LBLP1, label=u'+6V:', name=u'lblP1',
              parent=staticbox, pos=wx.Point(88, 56), size=wx.Size(24, 13),
              style=0)

        self.txtP1 = wx.TextCtrl(id=wxID__TXTP1, name=u'txtP1',
              parent=staticbox, pos=wx.Point(112, 56), size=wx.Size(32, 21),
              style=0, value=u'')

        self.btnSetP1 = wx.Button(id=wxID__BTNSETP1, label=u'Set',
              name=u'btnSetP1', parent=staticbox, pos=wx.Point(144, 56),
              size=wx.Size(24, 23), style=0)
        self.btnSetP1.Bind(wx.EVT_BUTTON, self.OnBtnSetP1Button,
              id=wxID__BTNSETP1)

        self.txtP1Usage = wx.TextCtrl(id=wxID__TXTP1USAGE, name=u'txtP1Usage',
              parent=staticbox, pos=wx.Point(8, 56), size=wx.Size(64, 21),
              style=0, value=u'--Usage--')

        self.spnP1MSB = wx.SpinButton(id=wxID__SPNP1MSB, name=u'spnP1MSB',
              parent=staticbox, pos=wx.Point(176, 56), size=wx.Size(16, 24),
              style=wx.SP_VERTICAL)
        self.spnP1MSB.Bind(wx.EVT_SPIN_DOWN, self.OnSpnP1MSBSpinDown,
              id=wxID__SPNP1MSB)
        self.spnP1MSB.Bind(wx.EVT_SPIN_UP, self.OnSpnP1MSBSpinUp,
              id=wxID__SPNP1MSB)

        self.spnP1LSB = wx.SpinButton(id=wxID__SPNP1LSB, name=u'spnP1LSB',
              parent=staticbox, pos=wx.Point(200, 56), size=wx.Size(16, 24),
              style=wx.SP_VERTICAL)
        self.spnP1LSB.Bind(wx.EVT_SPIN_DOWN, self.OnSpnP1LSBSpinDown,
              id=wxID__SPNP1LSB)
        self.spnP1LSB.Bind(wx.EVT_SPIN_UP, self.OnSpnP1LSBSpinUp,
              id=wxID__SPNP1LSB)

        self.txtP2Usage = wx.TextCtrl(id=wxID__TXTP2USAGE, name=u'txtP2Usage',
              parent=staticbox, pos=wx.Point(8, 84), size=wx.Size(64, 21),
              style=0, value=u'--Usage--')

        self.staticText1 = wx.StaticText(id=wxID__STATICTEXT1, label=u'+25V:',
              name='staticText1', parent=staticbox, pos=wx.Point(80, 84),
              size=wx.Size(30, 13), style=0)

        self.txtP2 = wx.TextCtrl(id=wxID__TXTP2, name=u'txtP2',
              parent=staticbox, pos=wx.Point(112, 84), size=wx.Size(32, 21),
              style=0, value=u'')

        self.btnP2 = wx.Button(id=wxID__BTNP2, label=u'Set', name=u'btnP2',
              parent=staticbox, pos=wx.Point(144, 84), size=wx.Size(24, 23),
              style=0)
        self.btnP2.Bind(wx.EVT_BUTTON, self.OnBtnP2Button, id=wxID__BTNP2)

        self.spnP2MSP = wx.SpinButton(id=wxID__SPNP2MSP, name=u'spnP2MSP',
              parent=staticbox, pos=wx.Point(176, 84), size=wx.Size(16, 24),
              style=wx.SP_VERTICAL)
        self.spnP2MSP.Bind(wx.EVT_SPIN_DOWN, self.OnSpnP2MSPSpinDown,
              id=wxID__SPNP2MSP)
        self.spnP2MSP.Bind(wx.EVT_SPIN_UP, self.OnSpnP2MSPSpinUp,
              id=wxID__SPNP2MSP)

        self.spnP2LSB = wx.SpinButton(id=wxID__SPNP2LSB, name=u'spnP2LSB',
              parent=staticbox, pos=wx.Point(200, 84), size=wx.Size(16, 24),
              style=wx.SP_VERTICAL)
        self.spnP2LSB.Bind(wx.EVT_SPIN_DOWN, self.OnSpnP2LSBSpinDown,
              id=wxID__SPNP2LSB)
        self.spnP2LSB.Bind(wx.EVT_SPIN_UP, self.OnSpnP2LSBSpinUp,
              id=wxID__SPNP2LSB)
              
        return staticbox

    # PROPERTIES!!!
    def GetP1(self):
        return float( self.txtP1.GetValue() )
    def SetP1(self, value):
        self.txtP1.SetValue( str(value) )
        
    def GetP2(self):
        return float( self.txtP2.GetValue() )
    def SetP2(self, value):
        self.txtP2.SetValue( str(value) )
    
    def GetEnable(self):
        return self.chkEnabled.GetValue()
    
    def GetGPIBAddr(self):
        return int( self.txtGPIBAddr.GetValue() )
    def SetGPIBAddr(self, value):
        self.txtGPIBAddr.SetValue( str(value) )
    
    def GetINI(self):
        obj = {}
        obj['P1Usage'] = self.txtP1Usage.GetValue()
        obj['P2Usage'] = self.txtP2Usage.GetValue()
        obj['Enabled'] = self.chkEnabled.GetValue()
        obj['GPIBAddr'] = self.txtGPIBAddr.GetValue()
        obj['P1'] = self.txtP1.GetValue()
        obj['P2'] = self.txtP2.GetValue()
        return obj
    def SetINI(self, value):
        self.txtP1Usage.SetValue(value['P1Usage'])
        self.txtP2Usage.SetValue(value['P2Usage'])
        self.chkEnabled.SetValue(value['Enabled'])
        self.txtGPIBAddr.SetValue(value['GPIBAddr'])
        self.txtP1.SetValue(value['P1'])
        self.txtP2.SetValue(value['P2'])

    # EVENTS!!!
    def OnTxtGPIBAddrText(self, event):
        self.SetAddress( self.GetGPIBAddr() )

    def OnChkEnabledCheckbox(self, event):
        instr = self.this_driver( self.GetAddress() )
        instr.Enabled = self.GetEnable()

    def OnBtnSetP1Button(self, event):
        instr = self.this_driver( self.GetAddress() )
        instr.P6V = self.GetP1()

    def OnSpnP1MSBSpinDown(self, event):
        instr = self.this_driver( self.GetAddress() )
        newvolt = self.GetP1() - 1
        instr.P6V = newvolt
        self.SetP1(newvolt)
        
    def OnSpnP1MSBSpinUp(self, event):
        instr = self.this_driver( self.GetAddress() )
        newvolt = self.GetP1() + 1
        instr.P6V = newvolt
        self.SetP1(newvolt)
        
    def OnSpnP1LSBSpinDown(self, event):
        instr = self.this_driver( self.GetAddress() )
        newvolt = self.GetP1() - 0.1
        instr.P6V = newvolt
        self.SetP1(newvolt)
        
    def OnSpnP1LSBSpinUp(self, event):
        instr = self.this_driver( self.GetAddress() )
        newvolt = self.GetP1() + 0.1
        instr.P6V = newvolt
        self.SetP1(newvolt)
        
    def OnBtnP2Button(self, event):
        instr = self.this_driver( self.GetAddress() )
        instr.P25V = self.GetP2()
        
    def OnSpnP2MSPSpinDown(self, event):
        instr = self.this_driver( self.GetAddress() )
        newvolt = self.GetP2() - 1
        instr.P25V = newvolt
        self.SetP2(newvolt)
        
    def OnSpnP2MSPSpinUp(self, event):
        instr = self.this_driver( self.GetAddress() )
        newvolt = self.GetP2() + 1
        instr.P25V = newvolt
        self.SetP2(newvolt)
        
    def OnSpnP2LSBSpinDown(self, event):
        instr = self.this_driver( self.GetAddress() )
        newvolt = self.GetP2() - 0.1
        instr.P25V = newvolt
        self.SetP2(newvolt)
        
    def OnSpnP2LSBSpinUp(self, event):
        instr = self.this_driver( self.GetAddress() )
        newvolt = self.GetP2() + 0.1
        instr.P25V = newvolt
        self.SetP2(newvolt)
        
