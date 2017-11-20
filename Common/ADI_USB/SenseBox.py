#-----------------------------------------------------------------------------
# Name:        SenseBox.py
# Purpose:     Device Interface Wrapper for the inhouse build sense boxes.
#
# Author:      Kaushal Shrestha
#
# Created:     2012/04/13, first as CurrentMeasurement.py.
# RCS-ID:      $Id: SenseBox.py 421 2014-03-12 14:57:26Z kshresth $
# Copyright:   (c) Kaushal Shrestha, Analog Devices Inc.
# Licence:     Analog Devices Inc.
#-----------------------------------------------------------------------------

import serial as __serial__, sys as __sys__, os as __os__
import _winreg as __reg__ ; reload (__reg__)
from itertools import count as __count__

"""
http://electronics-diy.com/USB_IO_Board.php
"""
class SenseBox( object ):
    def _(self):
        """
        Dummy method just to allow easy code folding in Boa Constructor.
        """
        pass
    #---------------------------------------------------------------------------
    # Constructor
    #---------------------------------------------------------------------------
    def __init__ ( self, port = None, auto = True ):
        """
        __init__ ( port = None ), None is auto detect or use other COM port identifier like 'COM9'.
        """        
        self.__baudrate__   = 57600
        self.__timeout__    = 3
        self.__connected__  = False
        self.__ports__      = None
        self.__port__       = None
        self.__serial__     = None
        self.__relay__      = 0
        self.__tsleep__     = 0.0075
        self.__switch_map__ = { 0 : 'B,0',
                                1 : 'B,1',
                                2 : 'B,2',
                                3 : 'B,3',
                                4 : 'B,4',
                                5 : 'B,5',
                                6 : 'B,6',
                                7 : 'B,7',
                                8 : 'C,7',
                              }
        self.__sense_map__  = { 0 : 'A,0',
                                1 : 'A,1',
                                2 : 'A,2',
                                3 : 'A,3',
                              }
        self.__toggle_port__ = 'C,6'

        if ( port is None ) :
            self.__ports__ = self.RegistryDetect()
            if ( self.__ports__ is None or self.__ports__ == [] ) :
                print "Unable to automatically detect ports that the device is connected to, please try and assign in a port."
        elif ( type(port) == type([])):
            self.__ports__ = [ i.upper() for i in port ]
        else:
            self.__ports__ = [ str( port ).upper() ]
        self.__initialize__()
        
        if (auto):
            self.__configure__()
            self.__connect__()        

    #---------------------------------------------------------------------------
    # Destructor
    #---------------------------------------------------------------------------
    def __del__ ( self ) :        
        if (self.__connected__):
            print "You will need to reconnect and call Local method to regain manual control"
            #self.__disconnect__()
    
    #---------------------------------------------------------------------------
    # Private low level methods.
    #---------------------------------------------------------------------------
    def __configure__ (self):                
        self.__open__()
        # ----------------------------------------------------------------------
        # Configure Port A, B, C as Outputs
        # C,0x0F,0x0,0x0,0x0,
        # C,<DirA>,<DirB>,<DirC>,<Analog Enable __count__><CR>
        # ----------------------------------------------------------------------
        # 4 ports on A are inputs, Port C6 is input, rest are all outputs.
        # 0b0000_1111, 0b0000_0000, 0b0100_0000, 0b0000_0000
        # 0x0F,        0b00,        0x40,        0x00
        #   15,          0,           64,          0        
        # ----------------------------------------------------------------------
        command = 'C,15,0,64,0'
        self.__write__ ( command )
        print "Config Status    : %s [%s]" % (" ",self.__read__())
        self.__close__()

    def __initialize__( self ) :
        try :
            assert( self.__ports__ is not None and self.__ports__ <> [])
            for port in self.__ports__:
                try:
                    self.__serial__ = __serial__.Serial( "\\\\.\\%s" % port, 
                                                         baudrate = self.__baudrate__, 
                                                         parity   = __serial__.PARITY_NONE,
                                                         stopbits = __serial__.STOPBITS_ONE,                                                        
                                                         timeout = self.__timeout__ )
                    #self.__serial__.close()
                    self.__port__ = port
                    break
                except __serial__.serialutil.SerialException, err:
                    err_expected = "The system cannot find the file specified"
                    if not ( err_expected in str(err) ):
                        raise
                except ValueError, errors:
                    print 80*"*"
                    print "*** ERROR *** : Error during connection attempt to [%s]" % port
                    errors = str(errors).split("Original message: ")
                    for error in errors:
                        print "*** ERROR *** : %s" % str(error)
                    print 80*"*"
                    __sys__.exit( 9 )

        except __serial__.serialutil.SerialException, err:
            print 80*"*"
            print "*** ERROR *** : Could not connect to Serial port in range of  "
            print "    %s." % str(self.__ports__)
            print "              Please make sure that the device is connected."
            print 80*"*"
            print "*** Exception *** : %s" % str(err)
            print 80*"*"
            __sys__.exit( 9 )

        try:
            assert (self.__serial__ is not None)
            if ( not (self.__serial__.isOpen()) ): self.__open__()
            assert( self.__serial__.isOpen() )
            self.__close__()
            assert( self.__serial__.isOpen() == False )
        except AssertionError:
            print "Could not open connection to Serial ports %s, make sure the device is connected!!!" % str(self.__ports__)
            __sys__.exit( 9 )

        print 80*"*"
        print "*** INFO  *** : Successfully connected and initialized to [%s]" % self.__port__
        print 80*"*"        
        print
        
    def __connect__( self ):
        # No need to try and reconnect again.
        if (self.__connected__ == True): 
            print "Already Connected"
            return
        
        curr_pos = self.__GetRelay__()
        self.__SetRelay__(0)
        command = 'PO,%s,1' % self.__switch_map__[0]

        if ( not self.__isopen__() ) : self.__open__()
        self.__write__( command )
        print "Connect Status   : %s [%s]" % (" ",self.__read__())        
        if ( self.__isopen__() ) : self.__close__()
        self.__connected__ = True
        self.__SetRelay__(curr_pos)

    def __disconnect__ ( self ) :        
        # No need to try and disconnect again.
        if (self.__connected__ == False): 
            print "Already Disconnected"
            return
        
        # Get the last position of the relays before disconnecting
        curr_pos = self.__GetRelay__()
        
        # Configure everything as input except for C6 as output, this resets
        # the counter
        command = 'C,255,255,191,0'
        if ( not self.__isopen__() ) : self.__open__()
        self.__write__ ( command )
        print "Re-Config Status : %s [%s]" % (" ", self.__read__())        
        
        # Set it high, as there is a pull-up in the circuit. This will toggle the
        # clock once
        self.__write__ ( 'PO,%s,1' % self.__toggle_port__ )
        self.__read__()
        
        # Just need to toggle it to the channel less than N
        num_switches = len(self.__switch_map__.keys())
        curr_pos = (curr_pos - 1 + num_switches) % num_switches
        
        # Pulse the counter N times to put the switch back to the location
        for i in range(curr_pos): self.__pulse__()
        
        # Issue a Reset to the PIC"
        command = "R"        
        self.__write__( command )
        print "Disconnect Status: %s [%s]" % (" ",self.__read__())
        if ( self.__isopen__() ) : self.__close__()
        self.__connected__ = False              

    def __close__ ( self ) :
        self.__serial__.close()

    def __isopen__ ( self ) :
        return self.__serial__.isOpen()

    def __open__ ( self ) :
        self.__serial__.open()
        ## Reason for importing here is because this gets called by the __del__ as well.
        import time as __time__
        __time__.sleep(self.__tsleep__)

    def __pulse__(self):
        import time as __time__        
        self.__write__ ( 'PO,%s,0' % self.__toggle_port__ )
        self.__read__()
        __time__.sleep(self.__tsleep__)
        self.__write__ ( 'PO,%s,1' % self.__toggle_port__ )
        self.__read__()
        __time__.sleep(self.__tsleep__)
        
    def __read__ ( self ) :
        ## Reason for importing here is because this gets called by the __del__ as well.
        import time as __time__
        
        # Opening the port for every write is slow, but it is safe to put in an
        # open here if required. However don't close the port unless it was 
        # opened here.
        local_port_open = False
        if ( not self.__isopen__() ) : 
            self.__open__()
            __time__.sleep(self.__tsleep__)
            local_port_open = True
            
        out = ''
        inwaiting = self.__serial__.inWaiting()
        
        __time__.sleep(self.__tsleep__)
        out = self.__serial__.read(inwaiting)
        
        # If locally opened and is open, then close.
        if ( local_port_open and self.__isopen__() ) : 
            self.__close__()
            __time__.sleep(self.__tsleep__)
            
        return out.strip()
    
    def __write__ ( self, command ) :
        ## Reason for importing here is because this gets called by the __del__ as well.
        import time as __time__        
        
        # Opening the port for every write is slow, but it is safe to put in an
        # open here if required. However don't close the port unless it was 
        # opened here.
        local_port_open = False
        if ( not self.__isopen__() ) : 
            self.__open__()
            __time__.sleep(self.__tsleep__)
            local_port_open = True
            
        # Strip command of whitespaces (leading and trailing)
        command = command.strip()
        self.__serial__.write( command + '\n' )
        __time__.sleep(self.__tsleep__)
        
        # If locally opened and is open, then close.
        if ( local_port_open and self.__isopen__() ) : 
            self.__close__()
            __time__.sleep(self.__tsleep__)

    #---------------------------------------------------------------------------
    # Private attribute methods.
    #---------------------------------------------------------------------------
    def __GetRelay__ ( self ) :        
        if ( not self.__isopen__() ) : self.__open__()
        try:
            keys = self.__sense_map__.keys()
            relay = 0
            for r in sorted(keys):
                command = 'PI,%s' % self.__sense_map__[r]
                self.__write__( command )
                value = self.__read__()
                value = value.strip("PI,")
                relay += int(value)
                
                if (relay > max(self.__switch_map__.keys())):
                    # Then software tracking
                    relay = self.__relay__
        except ValueError, e:
            print "ValueError", e
        except Exception, e:
            # Stupid 2.4 doesn't support finally
            if ( self.__isopen__() ) : self.__close__()
            raise e        
        if ( self.__isopen__() ) : self.__close__()
        return relay

    def __SetRelay__ ( self, relay_no = 0 ):
        """
        If __SetRelay__ is called with param relay_no = 0 (or no param), it will
        set all the switches to zero and nothing more.
        """
        if not relay_no in range( 0, max(self.__switch_map__.keys()) + 1 ) :
            print "  -- Supply index (%d) out of range, please use 1 through %d, or 0 to disable all" % \
                    (relay_no, max(self.__switch_map__.keys())+1)
            return

        # ----------------------------------------------------------------------
        # Port Output control
        # PO,B,0,1
        # PO,<Chan>,<Port>,<State>
        # ----------------------------------------------------------------------
        if ( not self.__isopen__() ) : self.__open__()
        # Disable All
        keys = self.__switch_map__.keys()
        keys.sort(); keys.reverse()
        keys.remove(0)
        for r in keys:
            command = 'PO,%s,0' % self.__switch_map__[r]
            self.__write__( command )
            self.__read__()

        # Enable Relay
        if ( relay_no != 0 ) :
            # PO,<Chan>,<Port>,<State>
            command = 'PO,%s,1' % self.__switch_map__[relay_no]
            self.__write__( command )
            print "Switch Status    : %d [%s]" % (relay_no, self.__read__())

        if ( self.__isopen__() ) : self.__close__()
        self.__relay__ = relay_no
    
    def __GetVersion__( self ):
        if ( not self.__isopen__() ) : self.__open__()        
        try:
            command = 'V'
            self.__write__( command )
            value = self.__read__()
        except Exception, e:
            # Stupid 2.4 doesn't support finally
            if ( self.__isopen__() ) : self.__close__()
            raise e
        if ( self.__isopen__() ) : self.__close__()
        return value
    
    #---------------------------------------------------------------------------
    # Public methods.
    #---------------------------------------------------------------------------
    def Local( self ):
        if (self.__connected__):
            self.__disconnect__()
            
    #---------------------------------------------------------------------------
    # Properties
    #---------------------------------------------------------------------------    
    Relay = property( __GetRelay__, __SetRelay__, None, "SenseBox Relay Property" )

    #---------------------------------------------------------------------------    
    # Static methods that don't require instance of object
    #---------------------------------------------------------------------------    
    @staticmethod
    def RegistryDetect() :
        """
        Automatically scan the registry and find out the port number attached to.
        """
        def Handle_Windows_Error(error):
            errno, errstr = error
            if (errno == 259):
                assert( errstr == "No more data is available" )
                pass # No more data is available
            else:
                "Unhandled Windows Error/Exception caught during traversal of registry : [%d] %s" % (errno, str(errstr))

        ports        = []
        usbkey       = 'SYSTEM\\CurrentControlSet\\Enum\\USB'
        devicekey    = 'Vid_04d8&Pid_000a'
        instancekeys = []
        paramkey     = 'Device Parameters'

        try:
            masterkey = usbkey + '\\' + devicekey
            regkey    = __reg__.OpenKey(__reg__.HKEY_LOCAL_MACHINE, masterkey )
            for i in __count__():
                instancekey = __reg__.EnumKey(regkey, i)
                instancekeys.append( instancekey )
        except WindowsError, error:
            Handle_Windows_Error(error)

        try :
            assert( instancekeys <> [] )
        except AssertionError:
            print "The instance ID for the device is not detectable"

        for instancekey in instancekeys:
            masterkey = usbkey + '\\' + devicekey + '\\' + instancekey + '\\' + paramkey
            try:
                regkey = __reg__.OpenKey(__reg__.HKEY_LOCAL_MACHINE, masterkey )
                for i in __count__():
                    key, value, size = __reg__.EnumValue(regkey, i)
                    if ( key == 'PortName' ) :
                        port = value
                        ports.append( port )
            except WindowsError, error:
                Handle_Windows_Error(error)

        ports = [ str(i) for i in ports ] # Remove the unicode
        print
        print 80*"*"
        print "*** INFO  *** : Ports from Registry : ", str(ports).replace("'", "").replace(",","")
        print 80*"*"
        print
        return ports

def GetAllSenseBoxes():
    """
    GetAllSenseBoxes(), get all the connected (RegistryDetect and attemted connection) sense boxes.
    """
    f = open(__os__.devnull, 'w')
    stdout = __sys__.stdout
    __sys__.stdout = f
    device_list   = []
    for port in SenseBox.RegistryDetect():
        try:
            dev = SenseBox( port = port, auto = False )
            device_list.append( ('USB0::%s' % ( port ), 'SenseBox, SenseBox') )
            del dev
        except:
            pass
    __sys__.stdout = stdout
    f.close()
    return device_list

if __name__ == '__main__' :    
    print GetAllSenseBoxes()
    import time, random
    psr = SenseBox()
    MAX_CHANNELS = 8
    TRANSITIONS  = 5

    for i in [ random.randint(0,MAX_CHANNELS) for j in xrange(TRANSITIONS) ]:        
        print "Switching to Relay : %d" % i
        psr.Relay = i
        
    #raw_input("Press Return to Exit")
    