# Author: Tom MacLeod / Mike Hughes
# Date: 07/06/2007
# Added GUI for GPIB Dashboard
# Rev History --------------------
# Date: 11/13/2006
# Added delay parameter
# Purpose: This module is a generic GPIB wrapper for:
# Analogic Data Precision 8200 Precision DC Source
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
from numpy import clip
import time
import string

class DP8200(GPIBObjectBaseClass):
    def __init__(self, addr=-1, delay=0.1):
        GPIBObjectBaseClass.__init__(self, 'Data Precision,8200', addr)
        self.__delay__ = delay
        
    def __SetV__(self, V):
        '''This function sets the 8200 Voltage in 10V Range'''
        V = clip(V, -9.99999, 9.99999) #Revisit absolute values
        v = self.DP8200Str(V)
        print v
        self.instr.write(v)
        time.sleep(self.__delay__)
          
    V = property(None, __SetV__, None, "Sets the 8200 Voltage")
    
    def DP8200Str(self, num):
        st = 'V1'
        
        if num >= 0:
            st += '+0'
            num /= 10.0
            st += str(num)[2:]
        else:
            st += '-0'
            num /= 10.0
            st += str(num)[3:]
            
        return string.ljust(st, 10, '0')
    

# GUI Code
import GPIB_Dashboard.Utils
from wx import NewId as wxNewId

[wxID__, wxID__BTNSETP1, wxID__CHKENABLED, wxID__CHKSIGN, wxID__LBLGPIBADDR, 
 wxID__LBLP1, wxID__PANEL1, wxID__SPNP1MSB0, wxID__SPNP1MSB1, wxID__SPNP1MSB2, 
 wxID__SPNP1MSB3, wxID__SPNP1MSB4, wxID__SPNP1MSB5, wxID__STATICTEXT1, 
 wxID__STATICTEXT2, wxID__STATICTEXT3, wxID__STATICTEXT4, wxID__STATICTEXT5, 
 wxID__STATICTEXT6, wxID__STL1, wxID__TXTGPIBADDR, wxID__TXTP1, 
 wxID__TXTUSAGE, 
] = [wxNewId() for _init_ctrls in range(23)]

from math import log10
        
class GPIB_DB_DP8200( GPIB_Dashboard.Utils.InstrumentBaseClass ):
    def __init__(self):
        self.SetFunction( 'Power Supply' )
        self.SetName( 'DP8200' )
        self.SetAddress( 0 )
        self.this_driver = DP8200
        
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
        self.chkEnabled.Hide()

        self.stl1 = wx.StaticLine(id=wxID__STL1, name=u'stl1',
              parent=staticbox, pos=wx.Point(8, 48), size=wx.Size(248, 2),
              style=0)

        self.lblP1 = wx.StaticText(id=wxID__LBLP1, label=u'V:', name=u'lblP1',
              parent=staticbox, pos=wx.Point(48, 56), size=wx.Size(10, 13),
              style=0)

        self.txtP1 = wx.TextCtrl(id=wxID__TXTP1, name=u'txtP1',
              parent=staticbox, pos=wx.Point(64, 56), size=wx.Size(56, 21),
              style=0, value=u'')

        self.btnSetP1 = wx.Button(id=wxID__BTNSETP1, label=u'Set',
              name=u'btnSetP1', parent=staticbox, pos=wx.Point(120, 56),
              size=wx.Size(24, 23), style=0)
        self.btnSetP1.Bind(wx.EVT_BUTTON, self.OnBtnSetP1Button,
              id=wxID__BTNSETP1)

        self.txtUsage = wx.TextCtrl(id=wxID__TXTUSAGE, name=u'txtUsage',
              parent=staticbox, pos=wx.Point(8, 16), size=wx.Size(64, 21),
              style=0, value=u'--Usage--')

        self.spnP1MSB5 = wx.SpinButton(id=wxID__SPNP1MSB5, name=u'spnP1MSB5',
              parent=staticbox, pos=wx.Point(152, 56), size=wx.Size(16, 24),
              style=wx.SP_VERTICAL)
        self.spnP1MSB5.Bind(wx.EVT_SPIN_DOWN, self.OnSpnP1MSB5SpinDown,
              id=wxID__SPNP1MSB5)
        self.spnP1MSB5.Bind(wx.EVT_SPIN_UP, self.OnSpnP1MSB5SpinUp,
              id=wxID__SPNP1MSB5)

        self.spnP1MSB4 = wx.SpinButton(id=wxID__SPNP1MSB4, name=u'spnP1MSB4',
              parent=staticbox, pos=wx.Point(168, 56), size=wx.Size(16, 24),
              style=wx.SP_VERTICAL)
        self.spnP1MSB4.Bind(wx.EVT_SPIN_DOWN, self.OnSpnP1MSB4SpinDown,
              id=wxID__SPNP1MSB4)
        self.spnP1MSB4.Bind(wx.EVT_SPIN_UP, self.OnSpnP1MSB4SpinUp,
              id=wxID__SPNP1MSB4)

        self.spnP1MSB3 = wx.SpinButton(id=wxID__SPNP1MSB3, name=u'spnP1MSB3',
              parent=staticbox, pos=wx.Point(184, 56), size=wx.Size(16, 24),
              style=wx.SP_VERTICAL)
        self.spnP1MSB3.Bind(wx.EVT_SPIN_DOWN, self.OnSpnP1MSB3SpinDown,
              id=wxID__SPNP1MSB3)
        self.spnP1MSB3.Bind(wx.EVT_SPIN_UP, self.OnSpnP1MSB3SpinUp,
              id=wxID__SPNP1MSB3)

        self.spnP1MSB2 = wx.SpinButton(id=wxID__SPNP1MSB2, name=u'spnP1MSB2',
              parent=staticbox, pos=wx.Point(200, 56), size=wx.Size(16, 24),
              style=wx.SP_VERTICAL)
        self.spnP1MSB2.Bind(wx.EVT_SPIN_DOWN, self.OnSpnP1MSB2SpinDown,
              id=wxID__SPNP1MSB2)
        self.spnP1MSB2.Bind(wx.EVT_SPIN_UP, self.OnSpnP1MSB2SpinUp,
              id=wxID__SPNP1MSB2)

        self.spnP1MSB1 = wx.SpinButton(id=wxID__SPNP1MSB1, name=u'spnP1MSB1',
              parent=staticbox, pos=wx.Point(216, 56), size=wx.Size(16, 24),
              style=wx.SP_VERTICAL)
        self.spnP1MSB1.Bind(wx.EVT_SPIN_DOWN, self.OnSpnP1MSB1SpinDown,
              id=wxID__SPNP1MSB1)
        self.spnP1MSB1.Bind(wx.EVT_SPIN_UP, self.OnSpnP1MSB1SpinUp,
              id=wxID__SPNP1MSB1)

        self.spnP1MSB0 = wx.SpinButton(id=wxID__SPNP1MSB0, name=u'spnP1MSB0',
              parent=staticbox, pos=wx.Point(232, 56), size=wx.Size(16, 24),
              style=wx.SP_VERTICAL)
        self.spnP1MSB0.Bind(wx.EVT_SPIN_DOWN, self.OnSpnP1MSB0SpinDown,
              id=wxID__SPNP1MSB0)
        self.spnP1MSB0.Bind(wx.EVT_SPIN_UP, self.OnSpnP1MSB0SpinUp,
              id=wxID__SPNP1MSB0)

        self.chkSign = wx.CheckBox(id=wxID__CHKSIGN, label=u'(+)',
              name=u'chkSign', parent=staticbox, pos=wx.Point(8, 56),
              size=wx.Size(40, 13), style=0)
        self.chkSign.SetValue(True)
        self.chkSign.Bind(wx.EVT_CHECKBOX, self.OnChkSignCheckbox,
              id=wxID__CHKSIGN)

        self.staticText1 = wx.StaticText(id=wxID__STATICTEXT1, label=u'5',
              name='staticText1', parent=staticbox, pos=wx.Point(156, 88),
              size=wx.Size(6, 13), style=0)

        self.staticText2 = wx.StaticText(id=wxID__STATICTEXT2, label=u'4',
              name='staticText2', parent=staticbox, pos=wx.Point(172, 88),
              size=wx.Size(6, 13), style=0)

        self.staticText3 = wx.StaticText(id=wxID__STATICTEXT3, label=u'3',
              name='staticText3', parent=staticbox, pos=wx.Point(188, 88),
              size=wx.Size(6, 13), style=0)

        self.staticText4 = wx.StaticText(id=wxID__STATICTEXT4, label=u'2',
              name='staticText4', parent=staticbox, pos=wx.Point(204, 88),
              size=wx.Size(6, 13), style=0)

        self.staticText5 = wx.StaticText(id=wxID__STATICTEXT5, label=u'1',
              name='staticText5', parent=staticbox, pos=wx.Point(220, 88),
              size=wx.Size(6, 13), style=0)

        self.staticText6 = wx.StaticText(id=wxID__STATICTEXT6, label=u'0',
              name='staticText6', parent=staticbox, pos=wx.Point(236, 88),
              size=wx.Size(6, 13), style=0)

        return staticbox

    # PROPERTIES!!!
    def GetP1(self):
        return float( self.txtP1.GetValue() )
    def SetP1(self, value):
        self.txtP1.SetValue( str(value) )
        
    def GetEnable(self):
        return self.chkEnabled.GetValue()
    
    def GetSign(self):
        return self.chkSign.GetValue()
    
    def GetGPIBAddr(self):
        return int( self.txtGPIBAddr.GetValue() )
    def SetGPIBAddr(self, value):
        self.txtGPIBAddr.SetValue( str(value) )
    
    def GetINI(self):
        obj = {}
        obj['Usage'] = self.txtP1Usage.GetValue()
        obj['Enabled'] = self.chkEnabled.GetValue()
        obj['GPIBAddr'] = self.txtGPIBAddr.GetValue()
        obj['P1'] = self.txtP1.GetValue()
        return obj
    def SetINI(self, value):
        self.txtP1Usage.SetValue(value['Usage'])
        self.chkEnabled.SetValue(value['Enabled'])
        self.txtGPIBAddr.SetValue(value['GPIBAddr'])
        self.txtP1.SetValue(value['P1'])
        
    # Function
    def AdjustSomeSigBit(self, val, pos, increment=True):
        #val *= 1e5
        #dig = int( log10( abs(val) ) ) + 1
        #inc = 10.0**dig / 10**(5-pos)
        #if increment:
        #    val += inc
        #else:
        #    val -= inc
        #return val / 1e5
        if increment:
            val += 10.0**(pos-5)
        else:
            val -= 10.0**(pos-5)
        return val
        
    # EVENTS!!!
    def OnTxtGPIBAddrText(self, event):
        self.SetAddress( self.GetGPIBAddr() )

    def OnChkEnabledCheckbox(self, event):
        #instr = self.this_driver( self.GetAddress() )
        #instr.Enabled = self.GetEnable()
        pass

    def OnBtnSetP1Button(self, event):
        instr = self.this_driver( self.GetAddress() )
        instr.V = self.GetP1()
    
    def OnChkSignCheckbox(self, event):
        instr = self.this_driver( self.GetAddress() )
        val = self.GetP1()
        if val < 0 and self.GetSign():
            self.SetP1(-val)
        if val >= 0 and not self.GetSign():
            self.SetP1(-val)
        instr.V = self.GetP1()

    def OnSpnP1MSB5SpinDown(self, event):
        instr = self.this_driver( self.GetAddress() )
        newvolt = self.AdjustSomeSigBit(self.GetP1(), 5, False)
        self.SetP1(newvolt)
        instr.V = newvolt

    def OnSpnP1MSB5SpinUp(self, event):
        instr = self.this_driver( self.GetAddress() )
        newvolt = self.AdjustSomeSigBit(self.GetP1(), 5, True)
        self.SetP1(newvolt)
        instr.V = newvolt

    def OnSpnP1MSB4SpinDown(self, event):
        instr = self.this_driver( self.GetAddress() )
        newvolt = self.AdjustSomeSigBit(self.GetP1(), 4, False)
        self.SetP1(newvolt)
        instr.V = newvolt

    def OnSpnP1MSB4SpinUp(self, event):
        instr = self.this_driver( self.GetAddress() )
        newvolt = self.AdjustSomeSigBit(self.GetP1(), 4, True)
        self.SetP1(newvolt)
        instr.V = newvolt

    def OnSpnP1MSB3SpinDown(self, event):
        instr = self.this_driver( self.GetAddress() )
        newvolt = self.AdjustSomeSigBit(self.GetP1(), 3, False)
        self.SetP1(newvolt)
        instr.V = newvolt

    def OnSpnP1MSB3SpinUp(self, event):
        instr = self.this_driver( self.GetAddress() )
        newvolt = self.AdjustSomeSigBit(self.GetP1(), 3, True)
        self.SetP1(newvolt)
        instr.V = newvolt

    def OnSpnP1MSB2SpinDown(self, event):
        instr = self.this_driver( self.GetAddress() )
        newvolt = self.AdjustSomeSigBit(self.GetP1(), 2, False)
        self.SetP1(newvolt)
        instr.V = newvolt

    def OnSpnP1MSB2SpinUp(self, event):
        instr = self.this_driver( self.GetAddress() )
        newvolt = self.AdjustSomeSigBit(self.GetP1(), 2, True)
        self.SetP1(newvolt)
        instr.V = newvolt

    def OnSpnP1MSB1SpinDown(self, event):
        instr = self.this_driver( self.GetAddress() )
        newvolt = self.AdjustSomeSigBit(self.GetP1(), 1, False)
        self.SetP1(newvolt)
        instr.V = newvolt

    def OnSpnP1MSB1SpinUp(self, event):
        instr = self.this_driver( self.GetAddress() )
        newvolt = self.AdjustSomeSigBit(self.GetP1(), 1, True)
        self.SetP1(newvolt)
        instr.V = newvolt

    def OnSpnP1MSB0SpinDown(self, event):
        instr = self.this_driver( self.GetAddress() )
        newvolt = self.AdjustSomeSigBit(self.GetP1(), 0, False)
        self.SetP1(newvolt)
        instr.V = newvolt

    def OnSpnP1MSB0SpinUp(self, event):
        instr = self.this_driver( self.GetAddress() )
        newvolt = self.AdjustSomeSigBit(self.GetP1(), 0, True)
        self.SetP1(newvolt)
        instr.V = newvolt
    