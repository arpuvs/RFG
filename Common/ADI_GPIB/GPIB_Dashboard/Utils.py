"""
Name:    Utils.py 
Purpose: A colection of necessary utilities
Author:  Tom MacLeod
Date:    6/28/07
Version: 0.0.0.1 Alpha
-------------------
Revision History
-------------------
6/28/07, 0.0.0.1 Alpha
  First pass

"""

import wx

class InstrumentBaseClass:
    def __init__(self):
        self._function = 'None'
        self._name     = 'None'
        self._address  = 0
                
    def GetFunction(self):
        return self._function
        
    def SetFunction(self, function):
        self._function = function
        
    def GetName(self):
        return self._name
        
    def SetName(self, name):
        self._name = name
        
    def GetAddress(self):
        return self._address
        
    def SetAddress(self, address):
        self._address = address
        
"""
def NewSizer( form, lst, sizer, orientation ):
    new_sizer = wx.BoxSizer( orientation )
    for item in lst[1:]:
        item[0]( form, item, new_sizer )
    sizer.Add( new_sizer, 1, wx.GROW )
    
def Vbox( form, lst, sizer ):
    NewSizer( form, lst, sizer, wx.VERTICAL )
    
def Hbox( form, lst, sizer ):
    NewSizer( form, lst, sizer, wx.HORIZONTAL )
    
def Spacer( form, lst, sizer ):
    '''grows can be 1 or 0'''
    (cmd, bounds, grows) = lst

    sizer.Add( bounds, grows )

def Button( form, lst, sizer ):
    (cmd, label, method, flag, border) = lst

    id = wx.NewId()
    #sizer.Add( wx.Button( form, id, label ), 0, wx.GROW )
    sizer.Add( wx.Button( form, id, label ), 0, flag, border )
    wx.EVT_BUTTON( form, id, method )
    
def CreateMasterSizer( parent, spec ):
    master_sizer = wx.BoxSizer( wx.VERTICAL )
    spec[0]( parent, spec, master_sizer ) # build from spec
    parent.SetSizer( master_sizer )
    parent.SetAutoLayout( True )
    return master_sizer
"""