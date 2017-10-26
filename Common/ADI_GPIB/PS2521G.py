# Author: Tom MacLeod

# Date: 03/27/2012 by Kaushal Shrestha
# Added __GetEnabled__ function and Enabled read property

# Modified : 09/03/2008 by Kaushal Shrestha
# Modified the I1, I2, I3 properties as read-write
# Added 3 methods __SetI1__, __SetI2__, __SetI3__

# Date: 04/08/2008
# Added common aliases for properties (improves portability of scripts):
#   PS.V1, PS.V2, PS.V3
# Date: 07/05/2007
# Added GUI for GPIB Dashboard
# Rev History --------------------
# Date: 04/09/2007
# Debugged: Working
# Rev History --------------------
# Date: 04/09/2007
# Added Get properties for both Current and Voltage
# Rev History --------------------
# Date: 11/01/2006
# Added delay parameter
# Rev History --------------------
# Date: 10/27/2006
# Purpose: This module is a generic GPIB wrapper for:
# TEKTRONIX PS2521G Power Supply
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
from numpy import clip
import time

class PS2521G(GPIBObjectBaseClass):
    def __init__(self, addr=-1, delay=0.5):
        GPIBObjectBaseClass.__init__(self, 'TEKTRONIX,PS2521G', addr)
        self.__delay__ = delay

    def __GetPS1Setting__(self):
        '''This function gets the PS2521G PS1 Voltage Setting'''
        self.instr.write('INST:NSEL 1')
        return self.instr.ask('VOLT?')
    def __GetPS1__(self):
        '''This function gets the PS2521G PS1 Voltage'''
        self.instr.write('INST:NSEL 1')
        return self.instr.ask('MEAS:VOLT?').lower()
    def __SetPS1__(self, PS1):
        '''This function sets the PS2521G PS1 Voltage'''
        PS1 = clip(PS1, 0, 20)
        self.instr.write('INST:NSEL 1')
        self.instr.write('VOLT ' + str(PS1))
        time.sleep(self.__delay__)

    def __GetPS2Setting__(self):
        '''This function gets the PS2521G PS1 Voltage Setting'''
        self.instr.write('INST:NSEL 2')
        return self.instr.ask('VOLT?')
    def __GetPS2__(self):
        '''This function gets the PS2521G PS2 Voltage'''
        self.instr.write('INST:NSEL 2')
        return self.instr.ask('MEAS:VOLT?').lower()
    def __SetPS2__(self, PS2):
        '''This function sets the PS2521G PS2 Voltage'''
        PS2 = clip(PS2, 0, 20)
        self.instr.write('INST:NSEL 2')
        self.instr.write('VOLT ' + str(PS2))
        time.sleep(self.__delay__)

    def __GetPS3Setting__(self):
        '''This function gets the PS2521G PS1 Voltage Setting'''
        self.instr.write('INST:NSEL 3')
        return self.instr.ask('VOLT?')
    def __GetPS3__(self):
        '''This function gets the PS2521G PS3 Voltage'''
        self.instr.write('INST:NSEL 3')
        return self.instr.ask('MEAS:VOLT?').lower()
    def __SetPS3__(self, PS3):
        '''This function sets the PS2521G PS3 Voltage'''
        PS3 = clip(PS3, 0, 6)
        self.instr.write('INST:NSEL 3')
        self.instr.write('VOLT ' + str(PS3))
        time.sleep(self.__delay__)

    def __GetI1__(self):
        '''This function gets the PS2521G PS1 Current'''
        self.instr.write('INST:NSEL 1')
        return self.instr.ask('MEAS:CURR?').lower()

    def __SetI1__(self, current):
        '''This function sets the PS2521G PS1 Current'''
        current = clip(current, 0, 20)
        self.instr.write('INST:NSEL 1')
        self.instr.write('CURR ' + str(current))
        time.sleep(self.__delay__)

    def __GetI2__(self):
        '''This function gets the PS2521G PS2 Current'''
        self.instr.write('INST:NSEL 2')
        return self.instr.ask('MEAS:CURR?').lower()

    def __SetI2__(self, current):
        '''This function sets the PS2521G PS1 Current'''
        current = clip(current, 0, 20)
        self.instr.write('INST:NSEL 2')
        self.instr.write('CURR ' + str(current))
        time.sleep(self.__delay__)

    def __GetI3__(self):
        '''This function gets the PS2521G PS2 Current'''
        self.instr.write('INST:NSEL 3')
        return self.instr.ask('MEAS:CURR?').lower()

    def __SetI3__(self, current):
        '''This function sets the PS2521G PS3 Current'''
        current = clip(current, 0, 20)
        self.instr.write('INST:NSEL 3')
        self.instr.write('CURR ' + str(current))
        time.sleep(self.__delay__)

    def __SetEnable__(self, Enabled):
        '''This function enables the On/Off for the PS2521G'''
        if Enabled:
            self.instr.write('OUTP ON')
        else:
            self.instr.write('OUTP OFF')

    def __GetEnable__(self):
        '''This function returns the On/Off state for the PS2521G'''
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

    PS1     = property(__GetPS1__, __SetPS1__,    None, "Gets/Sets the PS2521G PS1 Voltage")
    PS2     = property(__GetPS2__, __SetPS2__,    None, "Gets/Sets the PS2521G PS2 Voltage")
    PS3     = property(__GetPS3__, __SetPS3__,    None, "Gets/Sets the PS2521G PS3 Voltage")

    I1      = property(__GetI1__,  __SetI1__,    None, "Gets/Sets the PS2521G PS1 Current")
    I2      = property(__GetI2__,  __SetI2__,    None, "Gets/Sets the PS2521G PS2 Current")
    I3      = property(__GetI3__,  __SetI3__,    None, "Gets/Sets the PS2521G PS3 Current")

    # Aliases
    V1     = property(__GetPS1__, __SetPS1__,    None, "Gets/Sets the PS2521G PS1 Voltage")
    V2     = property(__GetPS2__, __SetPS2__,    None, "Gets/Sets the PS2521G PS2 Voltage")
    V3     = property(__GetPS3__, __SetPS3__,    None, "Gets/Sets the PS2521G PS3 Voltage")

    Enabled = property(__GetEnable__, __SetEnable__, None, "Sets the PS2521G On/Off")

    Delay = property(__GetDelay__, __SetDelay__, None, "Delay")

# GUI Code
import GPIB_Dashboard.Utils
from wx import NewId as wxNewId

[wxID__, wxID__BTNP2, wxID__BTNP3, wxID__BTNSETP1, wxID__CHKENABLED,
 wxID__LBLGPIBADDR, wxID__LBLP1, wxID__LBLP2, wxID__LBLP3, wxID__PANEL1,
 wxID__SPNP1LSB, wxID__SPNP1MSB, wxID__SPNP2LSB, wxID__SPNP2MSP,
 wxID__SPNP3LSB, wxID__SPNP3MSB, wxID__STL1, wxID__TXTGPIBADDR, wxID__TXTP1,
 wxID__TXTP1USAGE, wxID__TXTP2, wxID__TXTP2USAGE, wxID__TXTP3,
 wxID__TXTP3USAGE,
] = [wxNewId() for _init_ctrls in range(24)]

class GPIB_DB_PS2521G( GPIB_Dashboard.Utils.InstrumentBaseClass ):
    def __init__(self):
        self.SetFunction( 'Power Supply' )
        self.SetName( 'PS2521G' )
        self.SetAddress( 0 )
        self.this_driver = PS2521G

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

        self.lblP1 = wx.StaticText(id=wxID__LBLP1, label=u'+20V:',
              name=u'lblP1', parent=staticbox, pos=wx.Point(80, 56),
              size=wx.Size(30, 13), style=0)

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

        self.lblP2 = wx.StaticText(id=wxID__LBLP2, label=u'+20V:',
              name=u'lblP2', parent=staticbox, pos=wx.Point(80, 84),
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

        self.txtP3Usage = wx.TextCtrl(id=wxID__TXTP3USAGE, name=u'txtP3Usage',
              parent=staticbox, pos=wx.Point(8, 112), size=wx.Size(64, 21),
              style=0, value=u'--Usage--')

        self.lblP3 = wx.StaticText(id=wxID__LBLP3, label=u'+6V:', name=u'lblP3',
              parent=staticbox, pos=wx.Point(88, 112), size=wx.Size(24, 13),
              style=0)

        self.txtP3 = wx.TextCtrl(id=wxID__TXTP3, name=u'txtP3',
              parent=staticbox, pos=wx.Point(112, 112), size=wx.Size(32, 21),
              style=0, value=u'')

        self.btnP3 = wx.Button(id=wxID__BTNP3, label=u'Set', name=u'btnP3',
              parent=staticbox, pos=wx.Point(144, 112), size=wx.Size(24, 23),
              style=0)
        self.btnP3.Bind(wx.EVT_BUTTON, self.OnBtnP3Button, id=wxID__BTNP3)

        self.spnP3MSB = wx.SpinButton(id=wxID__SPNP3MSB, name=u'spnP3MSB',
              parent=staticbox, pos=wx.Point(176, 112), size=wx.Size(16, 24),
              style=wx.SP_VERTICAL)
        self.spnP3MSB.Bind(wx.EVT_SPIN_DOWN, self.OnSpnP3MSBSpinDown,
              id=wxID__SPNP3MSB)
        self.spnP3MSB.Bind(wx.EVT_SPIN_UP, self.OnSpnP3MSBSpinUp,
              id=wxID__SPNP3MSB)

        self.spnP3LSB = wx.SpinButton(id=wxID__SPNP3LSB, name=u'spnP3LSB',
              parent=staticbox, pos=wx.Point(200, 112), size=wx.Size(16, 24),
              style=wx.SP_VERTICAL)
        self.spnP3LSB.Bind(wx.EVT_SPIN_DOWN, self.OnSpnP3LSBSpinDown,
              id=wxID__SPNP3LSB)
        self.spnP3LSB.Bind(wx.EVT_SPIN_UP, self.OnSpnP3LSBSpinUp,
              id=wxID__SPNP3LSB)

        return staticbox

    # PROPERTIES!!!
    # PROPERTIES!!!
    def GetP1(self):
        return float( self.txtP1.GetValue() )
    def SetP1(self, value):
        self.txtP1.SetValue( str(value) )

    def GetP2(self):
        return float( self.txtP2.GetValue() )
    def SetP2(self, value):
        self.txtP2.SetValue( str(value) )

    def GetP3(self):
        return float( self.txtP3.GetValue() )
    def SetP3(self, value):
        self.txtP3.SetValue( str(value) )

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
        obj['P3Usage'] = self.txtP3Usage.GetValue()
        obj['Enabled'] = self.chkEnabled.GetValue()
        obj['GPIBAddr'] = self.txtGPIBAddr.GetValue()
        obj['P1'] = self.txtP1.GetValue()
        obj['P2'] = self.txtP2.GetValue()
        obj['P3'] = self.txtP3.GetValue()
        return obj
    def SetINI(self, value):
        self.txtP1Usage.SetValue(value['P1Usage'])
        self.txtP2Usage.SetValue(value['P2Usage'])
        self.txtP3Usage.SetValue(value['P3Usage'])
        self.chkEnabled.SetValue(value['Enabled'])
        self.txtGPIBAddr.SetValue(value['GPIBAddr'])
        self.txtP1.SetValue(value['P1'])
        self.txtP2.SetValue(value['P2'])
        self.txtP3.SetValue(value['P3'])

    # EVENTS!!!
    def OnTxtGPIBAddrText(self, event):
        self.SetAddress( self.GetGPIBAddr() )

    def OnChkEnabledCheckbox(self, event):
        instr = self.this_driver( self.GetAddress() )
        instr.Enabled = self.GetEnable()

    def OnBtnSetP1Button(self, event):
        instr = self.this_driver( self.GetAddress() )
        instr.PS1 = self.GetP1()

    def OnSpnP1MSBSpinDown(self, event):
        instr = self.this_driver( self.GetAddress() )
        newvolt = self.GetP1() - 1
        instr.PS1 = newvolt
        self.SetP1(newvolt)

    def OnSpnP1MSBSpinUp(self, event):
        instr = self.this_driver( self.GetAddress() )
        newvolt = self.GetP1() + 1
        instr.PS1 = newvolt
        self.SetP1(newvolt)

    def OnSpnP1LSBSpinDown(self, event):
        instr = self.this_driver( self.GetAddress() )
        newvolt = self.GetP1() - 0.1
        instr.PS1 = newvolt
        self.SetP1(newvolt)

    def OnSpnP1LSBSpinUp(self, event):
        instr = self.this_driver( self.GetAddress() )
        newvolt = self.GetP1() + 0.1
        instr.PS1 = newvolt
        self.SetP1(newvolt)

    def OnBtnP2Button(self, event):
        instr = self.this_driver( self.GetAddress() )
        instr.PS2 = self.GetP2()

    def OnSpnP2MSPSpinDown(self, event):
        instr = self.this_driver( self.GetAddress() )
        newvolt = self.GetP2() - 1
        instr.PS2 = newvolt
        self.SetP2(newvolt)

    def OnSpnP2MSPSpinUp(self, event):
        instr = self.this_driver( self.GetAddress() )
        newvolt = self.GetP2() + 1
        instr.PS2 = newvolt
        self.SetP2(newvolt)

    def OnSpnP2LSBSpinDown(self, event):
        instr = self.this_driver( self.GetAddress() )
        newvolt = self.GetP2() - 0.1
        instr.PS2 = newvolt
        self.SetP2(newvolt)

    def OnSpnP2LSBSpinUp(self, event):
        instr = self.this_driver( self.GetAddress() )
        newvolt = self.GetP2() + 0.1
        instr.PS2 = newvolt
        self.SetP2(newvolt)

    def OnBtnP3Button(self, event):
        instr = self.this_driver( self.GetAddress() )
        instr.PS3 = self.GetP3()

    def OnSpnP3MSBSpinDown(self, event):
        instr = self.this_driver( self.GetAddress() )
        newvolt = self.GetP3() - 1
        instr.PS3 = newvolt
        self.SetP3(newvolt)

    def OnSpnP3MSBSpinUp(self, event):
        instr = self.this_driver( self.GetAddress() )
        newvolt = self.GetP3() + 1
        instr.PS3 = newvolt
        self.SetP3(newvolt)

    def OnSpnP3LSBSpinDown(self, event):
        instr = self.this_driver( self.GetAddress() )
        newvolt = self.GetP3() - 0.1
        instr.PS3 = newvolt
        self.SetP3(newvolt)

    def OnSpnP3LSBSpinUp(self, event):
        instr = self.this_driver( self.GetAddress() )
        newvolt = self.GetP3() + 0.1
        instr.PS3 = newvolt
        self.SetP3(newvolt)
