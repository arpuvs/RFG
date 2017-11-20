#-------------------------------------------
# Python Interface to the DJs Tunable Filter
# @Author : Kaushal Shrestha  
#-------------------------------------------
# Ver 2.0
# Module function GetAllDJs_Filters() added
#  - function acts like GetAllGPIBDevices()
# Played some tricks to speed up the routine
#  - Removed __initialize__ call from __init__
#  - New class variables __class_addr__ and
#    __frequency__ added to speed up readbacks
#-------------------------------------------
# Ver 1.0
# Info : First Release, use the filters with
#        class addresses#
#-------------------------------------------
# Ver 0.1
# Info : Use the filters with device index
#-------------------------------------------
# import sys
# sys.path = ["C:\\Python27\\Lib\\site-packages\\ftd2xx"] + sys.path

#print "in DJsfilter"
import ftd2xx
#print "after ftd2xx import"
import time

#print "in DJsfilter after import"
all_filters = []
filters     = {}

class DJs_Filter(object):
    def __to_allow_collapse_in_Boa__ (self) : 
        return ""
    
    '''This is a driver object for a DJs tunable bandpass filter'''
    BAUD_RATE      = 2000000 #2457600
    DATA_BITS      = 8
    STOP_BITS      = 2
    PARITY_BITS    = 0
    SERIAL_TIMEOUT = 500
    TIMEOUT        = 5.0  # seconds
    END_CHARS      = '\nok '

    def __init__ ( self, class_address, __device__ = None ) :
        '''
        Constructor
        
        If __device__ is not None, then it is a device index from the list of devices    
        '''
        global filters
        self.__class_addr__ = None
        self.G_factor = 1
        
        if ( __device__ is None ) :
            #__device__ = self.__Get_Device_From_Class__( class_address )
            try:
                assert(class_address in filters.keys())
                params = filters[class_address]
                __device__ = params[0]
            except AssertionError, e:
                pass
            
        if ( __device__ is None ) :
            # If Device is still None, then there was a problem
            print '\n',79*"-"
            print "***** ERROR *****  : " + "Did not find a filter attached with Class '" + class_address + "'"
            print 79*"-", '\n'
            raise Exception( "Filter Not found : Class %s" % class_address )            

        self.__device__    = __device__
        self.__handle__    = None
        # self.__initialize__() ## We don't need self.__initialize__() anymore, 
        # self.__Get_Class__() will do the trick for us, this is done to improve        
        # Speed issues
        
        try:
            self.__class_addr__ = class_address
            self.__frequency__  = None
            self.G_factor = params[3]
            self.__low_freq_bound__, self.__high_freq_bound__ = float(params[1])*1e6, float(params[2])*1e6            
        except:        
            self.__class_addr__ = self.__Get_Class__()
            self.__frequency__  = None
            self.__low_freq_bound__, self.__high_freq_bound__, self.G_factor = self.__Get_Freq_Range__()
        
        

    def __del__ ( self ) :
        '''Desctructor'''
        self.__close__()            

    
    ##==========================================================================
    ##==========================================================================
    ##    
    ## Public methods for Users to Use
    ##
    ##==========================================================================
    ##==========================================================================
    def info ( self ) :
        '''Returns the filter information'''
        return self.__info__ ()
    
    def reset ( self ):
        '''Resets the DJ'''
        self.__reset__()
    
    def listFunctions ( self ) :
        '''Returns the list of filter functions available'''
        return self.__Get_Filter_Functions__()

    def getClass ( self ) :
        '''Accessor method : Get the class of the filter'''
        if ( self.__class_addr__ is None ) :
            self.__class_addr__ = self.__Get_Class__()
        return self.__class_addr__
        #return self.__Get_Class__()
        
    def getRange ( self ) :        
        '''Accessor method : Get the range of the filter'''
        return ( self.__low_freq_bound__, self.__high_freq_bound__ )
    
    def getFrequency ( self ) :
        '''Accessor method : Get the current frequency of the filter'''
        if self.__frequency__ is None or self.__frequency__ == 0:
            self.__frequency__ = self.__Get_Freq__()
        return self.__frequency__
        
    def setFrequency ( self, freq ) :
        '''Mutator method : Set the current frequency of the filter'''
        self.__frequency__ = self.__Set_Freq__( freq )
        return self.__frequency__


    ##==========================================================================
    ##==========================================================================
    ##
    ## Public properties for Users to Use
    ##
    ##==========================================================================
    ##==========================================================================
    Range     = property( getRange, None, None, None )
    Freq      = property( getFrequency, setFrequency, None, None )
    Frequency = property( getFrequency, setFrequency, None, None )

    #===========================================================================
    #===========================================================================
    #
    #  PRIVATE METHODS BELOW [DO NOT MODIFY]
    #
    #===========================================================================
    #===========================================================================    
    #---------------------------------------------------------------------------
    # Private method : open the serial com port (current handle)
    #---------------------------------------------------------------------------
    def __open__ ( self, second_attempt = False ) : 
        '''Private: Open the current handle'''
        if ( self.__handle__ is None ) :             
            self.__handle__ = ftd2xx.open( self.__device__ )
            time.sleep(0.002)
            self.__handle__.setBaudRate( self.BAUD_RATE )
            self.__handle__.setDataCharacteristics( self.DATA_BITS, self.STOP_BITS, self.PARITY_BITS )
            self.__handle__.setTimeouts( self.SERIAL_TIMEOUT, self.SERIAL_TIMEOUT )            
            try:                
                t = time.time()
                self.__write__( 'f(0)' )
                self.__read__()
                #print "Time to Do a Read on f(0)", time.time() - t
            except Exception, e:
                print "Inside Exception"
                if (second_attempt):
                    self.__reset__()                    
                    self.__handle__ = None
                    self.__open__ (second_attempt = True)
                else:
                    raise e
    
    #---------------------------------------------------------------------------
    # Private method : close the serial com port (current handle)
    #---------------------------------------------------------------------------
    def __close__ ( self ) :
        '''Private: Close the current handle'''
        if not ( self.__handle__ is None ) :
            self.__handle__.close()
            time.sleep(0.002)
        self.__handle__ = None
        
    #---------------------------------------------------------------------------
    # Private method : read from the serial com port (current handle)
    #---------------------------------------------------------------------------
    def __read__ ( self ) :
        '''Private: Read from the current open handle until timeout or END_CHARS'''
	    ## Read implies that the handle has already been opened
        if ( self.__handle__ is None ):raise "Handle needs to be opened first"        

        timeout = 0.0
        t0 = time.time()
        readback_str = ""
        end_chars_found = False
        
        ## Read command implies that there is something to be read, or timeout
        while ( timeout < self.TIMEOUT and end_chars_found == False ) :
            timeout = time.time() - t0 ## Update timeout
            while ( self.__handle__.getQueueStatus() > 0 ) :
                read_chars = self.__handle__.getQueueStatus()
                readback_str += self.__handle__.read( 1 )                
                if ( readback_str.endswith( self.END_CHARS ) ) :
                    
                    readback_str = readback_str.replace( self.END_CHARS, "" )
                    
                    ## Flush out the output buffer to make sure everything has
                    ## been cleared out
                    while ( self.__handle__.getQueueStatus() ) :                         
                        self.__handle__.read( 1 )                        
                    
                    end_chars_found = True ## Enables break out of outer loop                    
                    break                  ## Break out of the inner loop
                timeout = time.time() - t0 ## Update timeout
                
                
        if ( timeout >= self.TIMEOUT and end_chars_found == False ) :
            print "Error : Timeout occured during readback"
            raise Exception("Error : Timeout occured during readback")
        return readback_str
           
    #---------------------------------------------------------------------------
    # Private method : write the command to the serial com port (current handle)
    #---------------------------------------------------------------------------
    def __write__ ( self, command ) :  
        '''Private: Writes to the currently opened handle'''      
        ## Write command implies that the handle has already been opened
        if ( self.__handle__ is None ):raise "Handle needs to be opened first"
        self.__handle__.write( command + '\n' )        
                
    #---------------------------------------------------------------------------
    # Private method : initialize the device for serial port communication
    #---------------------------------------------------------------------------
    def __initialize__ ( self ) :
        self.__open__()
        self.__write__( 'f(0)' )
        self.__read__()
        self.__close__()
            
    #---------------------------------------------------------------------------
    # Private method : return the filter info
    #---------------------------------------------------------------------------
    def __info__ ( self ) :
        self.__open__()
        self.__write__('info')
        info = self.__read__()        
        self.__close__()
        return info        
    #---------------------------------------------------------------------------
    # Private method : reset the filter
    #---------------------------------------------------------------------------
    def __reset__ ( self ) :
        self.__open__()
        self.__handle__.setDtr()
        time.sleep(7)
        # Reopen
        self.__handle__ = None
        print "After Reset, OPEN"
        time.sleep(10)
        devices = ftd2xx.listDevices()
        print self.__device__
        print devices        
        self.__open__()
        time.sleep(1)
        #self.__write__('auto')
        print "Open successful, closing down"
        self.__close__()
    
    #---------------------------------------------------------------------------
    # Private method : Get the Device Index from Class Name on the USB bus
    #---------------------------------------------------------------------------
    def __Get_Device_From_Class__ ( self, class_address ) :
        __device__ = None
        class_addr = []   
             
        try :
            devices = ftd2xx.listDevices()
        except:
            raise Exception( "Problem with getting the ftd2xx filters or COM port" )
        
        #print devices
        for device in devices :
            #print device
            self.__device__     = devices.index( device )            
            self.__class_addr__ = None
            self.__handle__     = None
            
            __class_address__   = self.getClass()
            #print "\n\n\n ========================================"
            #print __class_address__
            #print "\n\n\n ========================================"
                        
            if ( __class_address__ == "error: undefined variable or sub []" ):
                print "Hung Filter on class_addr %s, Giving a Reset Command" % class_address
                self.__reset__()
                self.__device__     = devices.index( device )
                print "One more attempt at it... to fix the lock down of the filter issue"
                __class_address__   = self.getClass() # One more attempt at it... to fix the lock down of the filter issue            
                print __class_address__, " Received after Reset"
            
            if ( class_addr.__contains__( __class_address__ ) ) :
                print '\n',79*"-"
                print "***** ERROR *****  : " + "Multiple instances of Class Addresses '%s' Found" % __class_address__
                print 79*"-", '\n'
                raise Exception( 'Multiple instances of Class %s found' % __class_address__ )

            else:
                class_addr.append( __class_address__ )
            
            if ( __class_address__ == class_address ) :                
                __device__ = devices.index( device )
                return __device__
        return None
    
    #---------------------------------------------------------------------------
    # Private method : gets the loaded program in the filter and returns the
    #                  available functions
    #---------------------------------------------------------------------------
    def __Get_Filter_Functions__ ( self ) :
        command = 'type auto.bas'
        self.__open__()
        self.__write__( command )
        text = self.__read__()
        self.__close__()
        
        text = text.replace( command, "" ).strip()
        
        functions = []
        f_loc = -1
        while ( True ) :
            f_loc = text.find( 'function', f_loc + 1 )
            if ( f_loc == -1 ) : break
            r_loc = text.find( '\r', f_loc )
            functions.append( text[ 1 + f_loc + len( 'function' ) : r_loc ] )
        return functions

    #---------------------------------------------------------------------------
    # Private method : get the class of the filter
    #---------------------------------------------------------------------------
    def __Get_Class__ ( self ):
        '''Private: gets the class of the filter'''
        command = "get_class_address"        
        self.__open__()        
        self.__write__( command )        
        classAddr = self.__read__().replace( command, "" ).strip()
        self.__close__()
        return classAddr
        
    #---------------------------------------------------------------------------
    # Private method : get the frequency range of the filter
    #---------------------------------------------------------------------------
    def __Get_Freq_Range__ ( self ):
        '''Private: gets the current frequency range from the filter'''
        command = "get_filter"
        self.__open__()
        self.__write__( command )
        
        freq_range = self.__read__().replace( command, "" ).strip()        
        freq_range = freq_range.split( "\r\n" )                
        self.__close__()
        
        if (freq_range[0].endswith('G') or freq_range[1].endswith('G')):
            G_factor = 10.0
            freq_range = [ freq_range[0].replace('G','e9'), \
                           freq_range[1].replace('G','e9') ]
        else:
            G_factor = 1.0
        
        return ( float( freq_range[0] ), float( freq_range[1] ), G_factor )
    
    #---------------------------------------------------------------------------
    # Private method : get the current frequency setting of the filter
    #---------------------------------------------------------------------------
    def __Get_Freq__ ( self ) :
        '''Private: gets the current frequency'''
        freq_command = 'get_freq'
        self.__open__()
        self.__write__( freq_command )
        f = self.__read__()
        f = f.replace( freq_command, "" ).strip()
        self.__close__()
        try :            
            f = float( f ) * self.G_factor
        except ValueError, e:
            f = 0
        return f
    
    #---------------------------------------------------------------------------
    # Private method : set the current frequency of the filter
    #---------------------------------------------------------------------------
    def __Set_Freq__ ( self, freq ) :
        '''Private: sets the current frequency'''
        """
        Returns 0 if freq is out of bound, or if error, else return the 'freq'
        """    
        t = time.time()        
        self.__open__()
        
        f = 0
        if ( freq < self.__low_freq_bound__ or freq > self.__high_freq_bound__ ):
            print "Error : Freq %.2fM is outside filter range (%.2fM, %.2fM)" % \
            ( freq/1e6, self.__low_freq_bound__/1e6, self.__high_freq_bound__/1e6 )
        else:            
            freq_command = 'f(%i)' % (freq/self.G_factor)
            self.__write__( freq_command ) 
            #print "Time to write the freq command %f" % (time.time()-t)
            f = self.__read__()
            #print "Time to complete freq read command %f" % (time.time()-t)
            f = float( f.replace( freq_command, "" ).strip() )
        
        self.__close__()
        
        return f
    

def GetAllDJs_Filters():
    error = False
    for tries in [0,1]:
        device_list   = []    
        device_sn     = ftd2xx.listDevices()

        log_message   = ''
        if not ( device_sn is None ) :
            for device in device_sn :
                id  = device_sn.index( device )                
                try:
                    dev = DJs_Filter( class_address = None, __device__ = id )        
                    cls = dev.getClass()        
                    dev_range = dev.Range
                    dev_g_factor = dev.G_factor
                    
                    device_list.append( ('USB%d::%s' % ( id, cls ), 'KNL Filter (%d-%d)MHz, KNL Filter' % \
                                                ( dev_range[0]/1e6, dev_range[1]/1e6 ), dev_g_factor ) )  
                except Exception, e:
                    error = True
                    log_message += str(e) + '\n'
                    if (tries == 0):
                        print "Resetting DJs_Filters because one or more of them is hung"
                        ResetAllDJs_Filters()
                        time.sleep(10)
                        break ## break out of the device loop
            
            if (error == False):
                # This means we were successful
                break
        
        log_message = log_message.strip()
       
    if (log_message != ''): print log_message
    
    global all_filters, filters
    all_filters = device_list
    filters     = {} # Class Address is the key to the hash
    for i, (class_addr, desc, g_factor) in enumerate(all_filters):
        key        = class_addr.split("::")[-1]
        freq_range = desc.replace('KNL Filter (', '').replace(')MHz', '').split('-')        
        filters[key] = (i, freq_range[0], freq_range[1], g_factor)
    return device_list

def ResetAllDJs_Filters():
    device_sn = ftd2xx.listDevices()
    
    for i, d in enumerate( device_sn ):        
        try:
            dev = ftd2xx.open( i )
            dev.setDtr() 
            dev.close()
        except:
            print "Error trying to reset index %d" % i


if __name__ == '__main__' :
    #ResetAllDJs_Filters()
    import time
    t = time.time()    
    
    f1 = DJs_Filter(class_address = 'A')
    print f1.getRange()
    f2 = DJs_Filter(class_address = 'I')
    #print f2.info()
    f3 = DJs_Filter(class_address = 'B')
    print f3.getRange()
    
    f1.setFrequency(253e6)
    
    print time.time() - t, " for full run of GetALLDJs_Filters secs"
    
##    f = DJs_Filter(filters[0][0][-1])    
##    t = time.time()
##    print f.getFrequency()
##    f.setFrequency(750e6)
##    t = time.time() - t
##    print "Time to just set 500MHz %f sec " % t
##    