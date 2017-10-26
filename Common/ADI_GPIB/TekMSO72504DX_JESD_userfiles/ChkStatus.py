import visa                    # imports GPIB VISA functions
import sys
import wx

#-# wrtmsg *******************************************
def wrtmsg(scope, msg): # send message to instrument
    scope.write(msg)
    return

#-# rdmsg ***********************************************
def rdmsg(scope):
    sndok = False
    tries = 0
    while sndok == False:
        try:
            msg = scope.read()
            sndok = True
        except Exception:
            print ".",    #errmsg.args      # arguments stored in .args
            tries=tries+1
            if tries>10:
                    scope.close()
                    print
                    sys.exit('scope busy')
    if tries > 0: print
    return msg

#-# ChkStatus********************************************
def chkbusy(scope):  # Wait for the acquisition to complete
    tries = 0
    busy = "1"
    while busy =="1":
        try:
            busy = scope.ask("busy?")
            #raise ValueError 
            #print busy
        except Exception:
            print ".",          #errmsg.args      # arguments stored in .args
            tries=tries+1
            if tries>10:
                    scope.close()
                    print
                    sys.exit("busy?")
    if tries > 0: print
    return
    print 'testing chkbusy'
# ********************************************
def chkerr(scope):
# Check for communication errors
    print scope.ask("*ESR?")
    print scope.ask("ALLEV?")
    return
# ********************************************

# ********************************************
def chkDpoJetMeasureIfIdle(scope):
# Check for communication errors
    timeout = 100
    counter = 1
    while ('STOP' not in scope.DpoJet_Measure_State()):
        wx.MilliSleep(1000)
        counter += 1
        if counter > timeout:
            print "ERROR: timeout"
            return   
            
# ********************************************