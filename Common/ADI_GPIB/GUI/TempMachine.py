# Kaushal Shrestha
# 10/22/2010
# Rev0

#Boa:Frame:MainFrame
import MessageBox as MB
import ADI_GPIB
import wx

def create(parent):
    return MainFrame(parent)

[wxID_MAINFRAME, wxID_MAINFRAMEBUTTONINIT, wxID_MAINFRAMEBUTTONSETTEMP, 
 wxID_MAINFRAMECHOICETEMPMACHINE, wxID_MAINFRAMEPANEL1, 
 wxID_MAINFRAMERADIOBOXTEMP, wxID_MAINFRAMETEXTCTRLMANUALTEMP, 
] = [wx.NewId() for _init_ctrls in range(7)]

class MainFrame(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_MAINFRAME, name=u'MainFrame',
              parent=prnt, pos=wx.Point(454, 299), size=wx.Size(181, 176),
              style=wx.DEFAULT_FRAME_STYLE, title=u'TemperatureControl')
        self.SetClientSize(wx.Size(173, 142))
        self.Bind(wx.EVT_CLOSE, self.OnMainFrameClose)

        self.panel1 = wx.Panel(id=wxID_MAINFRAMEPANEL1, name='panel1',
              parent=self, pos=wx.Point(0, 0), size=wx.Size(173, 142),
              style=wx.TAB_TRAVERSAL)

        self.radioBoxTemp = wx.RadioBox(choices=['-40', '25', '85', 'Manual'],
              id=wxID_MAINFRAMERADIOBOXTEMP, label=u'Temperature',
              majorDimension=2, name=u'radioBoxTemp', parent=self.panel1,
              pos=wx.Point(8, 40), size=wx.Size(160, 64),
              style=wx.RA_SPECIFY_COLS)
        self.radioBoxTemp.SetSelection(1)
        self.radioBoxTemp.Bind(wx.EVT_RADIOBOX, self.OnRadioBoxTempRadiobox,
              id=wxID_MAINFRAMERADIOBOXTEMP)

        self.choiceTempMachine = wx.Choice(choices=[],
              id=wxID_MAINFRAMECHOICETEMPMACHINE, name=u'choiceTempMachine',
              parent=self.panel1, pos=wx.Point(8, 8), size=wx.Size(112, 21),
              style=0)
        self.choiceTempMachine.SetStringSelection(u'')
        self.choiceTempMachine.SetSelection(0)

        self.textCtrlManualTemp = wx.TextCtrl(id=wxID_MAINFRAMETEXTCTRLMANUALTEMP,
              name=u'textCtrlManualTemp', parent=self.panel1, pos=wx.Point(10,
              112), size=wx.Size(62, 21), style=0, value=u'')
        self.textCtrlManualTemp.Enable(False)
        self.textCtrlManualTemp.Bind(wx.EVT_KILL_FOCUS,
              self.OnTextCtrlManualTempKillFocus)

        self.buttonSetTemp = wx.Button(id=wxID_MAINFRAMEBUTTONSETTEMP,
              label=u'Set Temperature', name=u'buttonSetTemp',
              parent=self.panel1, pos=wx.Point(80, 112), size=wx.Size(88, 23),
              style=0)
        self.buttonSetTemp.Enable(False)
        self.buttonSetTemp.Bind(wx.EVT_BUTTON, self.OnButtonSetTempButton,
              id=wxID_MAINFRAMEBUTTONSETTEMP)

        self.buttonInit = wx.Button(id=wxID_MAINFRAMEBUTTONINIT, label=u'Init',
              name=u'buttonInit', parent=self.panel1, pos=wx.Point(128, 8),
              size=wx.Size(40, 23), style=0)
        self.buttonInit.Bind(wx.EVT_BUTTON, self.OnButtonInitButton,
              id=wxID_MAINFRAMEBUTTONINIT)

    def __init__(self, parent):
        self._init_ctrls(parent)
        
        
        # ADI Temp Machines 
        self.TempMachine = None
        
        airjet_model = 'XE75 AirJet'
        
        gpib_devices = ADI_GPIB.GetAllGPIBDevices()
        for gpib, model in gpib_devices :
            if ( airjet_model in model ) :
                gpib = int( gpib.split( '::')[-1])
                self.choiceTempMachine.Append( 'AirJet XE75::' + str( gpib ) )
                self.choiceTempMachine.Select( 0 )
                self.TempMachineGPIB  = gpib
                self.TempMachineModel = ADI_GPIB.AirJetXE75
                break
        
    def OnRadioBoxTempRadiobox(self, event):
        if self.TempMachine is None :
            MB.Show( 'Please Initialize the Machine First' )
            event.Skip()
            return
        sel = self.radioBoxTemp.GetSelection()                
        temp = [ -40, 25, 85 ] 
        if ( sel in range( len( temp ) ) ) :            
            self.buttonSetTemp.Enable( False )
            self.textCtrlManualTemp.Enable( False )
                        
            try :
                self.TempMachine.Temp = temp[ sel ]            
            except :
                MB.Show( "Cannot set temperature %d" % temp[ sel ] )
        else :
            self.textCtrlManualTemp.Enable( True )
            self.buttonSetTemp.Enable( True )
            
        event.Skip()
    
    def OnButtonSetTempButton(self, event):
        self.TempMachine.Temp = int( self.textCtrlManualTemp.GetValue() )
        event.Skip()

    def OnButtonInitButton(self, event):
        self.TempMachine = self.TempMachineModel( self.TempMachineGPIB, 0.5 )
        self.buttonInit.Enable( False )
        self.buttonInit.SetBackgroundColour( wx.Colour( 0, 225, 0 ) )
        event.Skip()

    def OnTextCtrlManualTempKillFocus(self, event):
        value = self.textCtrlManualTemp.GetValue()
        try :
            value = int( value )
            if ( value < -200 or value > +150 ) :
                raise Exception( 'Cannot Set to %s' % str( value ) )
        except :
            MB.Show( 'Invalid Temperature %s' % str( value ) )
            value = 25
                                
        self.textCtrlManualTemp.SetValue( str( value ) )
        event.Skip()

    def OnMainFrameClose(self, event):
        if not ( self.TempMachine is None ) :
            retVal = MB.Show( 'Should we set the Temp Machine to Idle?','Question', MB.S_YESNO )
            if retVal == MB.R_YES :
                self.TempMachine.SetIdleMode()
        event.Skip()

if __name__ == '__main__':
    app = wx.PySimpleApp()
    dlg = MainFrame(None)
    dlg.Show()
    app.MainLoop()
