"""
This is a module to help scripts interact with users via dialogs
Author: Tom MacLeod
-----------------------------------------------------------------------
Data: 12/18/2006
Added new functionality!
New Function:
--You can now type in "age = MessageBox.Ask('What is your age?')"
-----------------------------------------------------------------------
Date: 11/16/2006
Company: Analog Devices, Inc.
Functions:
    MessageBox.Show()
"""
import wx
import winxpgui

#Style Constants
S_OK                     = 0
S_OKCANCEL               = 1
S_ABORTRETRYIGNORE       = 2
S_YESNOCANCEL            = 3
S_YESNO                  = 4
S_RETRYCANCEL            = 5
S_CANCELTRYAGAINCONTINUE = 6


#Return Type Constants
R_OK       = 1
R_CANCEL   = 2
R_ABORT    = 3
R_RETRY    = 4
R_IGNORE   = 5
R_YES      = 6
R_NO       = 7
R_TRYAGAIN = 10
R_CONTINUE = 11

def Show(message, title='', style=S_OK):
    return winxpgui.MessageBox(0, message, title, style)

class QuestionDialog(wx.Dialog):
    def __init__(self, question, title=''):
        wx.Dialog.__init__( self, None, wx.ID_ANY, title, size=wx.Size(298, 121) )
        
        #init controls
        self.txtAnswer = wx.TextCtrl( self, pos=wx.Point(8, 24), size=wx.Size(272, 21) )
        
        self.lblQuestion =  wx.StaticText( self, label=question, pos=(8, 8) )
        
        self.btnOK     = wx.Button( self, id=wx.ID_OK,     label='OK',     pos=wx.Point(120, 56) )
        self.btnCancel = wx.Button( self, id=wx.ID_CANCEL, label='Cancel', pos=wx.Point(208, 56) )

    def Answer(self):
        return self.txtAnswer.GetValue()
                
def Ask(question, title='Input Dialog'):
    app = wx.PySimpleApp()
    
    dlg = QuestionDialog(question, title)
    
    try:
        if dlg.ShowModal() == wx.ID_OK:
            retval = dlg.Answer()
        else:
            retval = ''
    finally:
        dlg.Destroy()
        
    app.MainLoop()
        
    return retval 

if __name__ == '__main__':
    print Ask('What is your name?')
    
