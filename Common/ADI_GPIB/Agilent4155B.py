# Author: Tom MacLeod
# ---------------------------------------------------------------------
# Date: 10/01/2008
# Purpose: This module is a generic GPIB wrapper for:
# Agilent 4155B Parameter Analyzer
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
import os
import time

#pth_network = r'\\greensborohsc\LAB\Barnett\Hp4155_Data'
pth_network = r'Z:\\esd_hp4155_data'
class Agilent4155B(GPIBObjectBaseClass):
    ##############################################################################################################################################
    def __init__(self, addr=-1):
        GPIBObjectBaseClass.__init__(self, 'HEWLETT-PACKARD,4155B', addr)
    
                   # Sets screendump format to TIFF
        #self.instr.write(":HCOP:DEV:LANG TIFF")

                   # Set color to BW
        #self._set_color(False)
    
                   # Initialize 4155B to write to the network
        #self.instr.write(":MMEM:DEST NET1")
        
                   # Initialize 4155B to Disable Autocalibration
        #self.instr.write(":CAL:AUTO OFF")
        
                   # Initialize 4155B to Enable Autocalibration
        #self.instr.write(":CAL:AUTO ON")
        
                   # Turns Trigger Function to OFF
        #self.instr.write(":PAGE:MEAS:OSEQ:TRIG OFF")
        
                   # Turns Trigger Function to ON
        #self.instr.write(":PAGE:MEAS:OSEQ:TRIG ON")
        
                   # Sets Trigger Function to Positive Polarity
        #self.instr.write(":PAGE:MEAS:OSEQ:TRIG:POL POS")
        
                   # Sets Trigger Function to Negative Polarity
        #self.instr.write(":PAGE:MEAS:OSEQ:TRIG:POL NEG")
        
                   # Sets Trigger Function to Accept Input Triggers
        #self.instr.write(":PAGE:MEAS:OSEQ:TRIG:FUNC INP")
        
                   # Sets Trigger Function to Output a Trigger
        #self.instr.write(":PAGE:MEAS:OSEQ:TRIG:FUNC OUT")
        
                   # Sets Trigger Output Timing
        #self.instr.write(":PAGE:MEAS:OSEQ:TRIG:TIME 0.0001")
        
                   # Sets Trigger Output Level to LOW State
        #self.instr.write(":PAGE:SCON:TRIG:OUTP:LEV LOW")
        
                   # Sets Trigger Output Level to Hi State
        #self.instr.write(":PAGE:SCON:TRIG:OUTP:LEV HI")
        
                   # Initialize Operation Complete Command
        #self.instr.write("*OPC")
        
                   # Insures the X/Y Graph Page is displayed          
        #self.ShowGraph()
        
                   # Insures the List Page is displayed
        #self.ShowList()
    ##############################################################################################################################################
    def ResetAgilent(self):
        '''Resets instrument to Power-Up default state'''
        self.instr.write("*RST")
        
        time.sleep(.2)    
    ##############################################################################################################################################
    def SetTrigOn(self):
        '''Turns Trigger Function to ON'''
        self.instr.write(":PAGE:MEAS:OSEQ:TRIG ON")
        
        time.sleep(.2)
    ##############################################################################################################################################
    def SetTrigOff(self):
        '''Turns Trigger Function to OFF'''
        self.instr.write(":PAGE:MEAS:OSEQ:TRIG OFF")
        
        time.sleep(.2)
    ##############################################################################################################################################
    def SetTrigNeg(self):
        '''Sets Trigger Function to Negative Polarity'''
        self.instr.write(":PAGE:MEAS:OSEQ:TRIG:POL NEG")
        
        time.sleep(.2)
    ##############################################################################################################################################
    def SetTrigPos(self):
        '''Sets Trigger Function to Positive Polarity'''
        self.instr.write(":PAGE:MEAS:OSEQ:TRIG:POL POS")
        
        time.sleep(.2)
    ##############################################################################################################################################
    def SetTrigIn(self):
        '''Sets Trigger Function to Accept Input Triggers'''
        self.instr.write(":PAGE:MEAS:OSEQ:TRIG:FUNC INP")
        self.instr.write(":PAGE:MEAS:OSEQ:TRIG:POL NEG")
        self.instr.write(":PAGE:MEAS:OSEQ:TRIG:TIME 0.0001")
        
        time.sleep(.2)
    ##############################################################################################################################################
    def SetTrigOut(self):
        '''Sets Trigger Function to Output a Trigger'''
        self.instr.write(":PAGE:MEAS:OSEQ:TRIG:FUNC OUT")
        self.instr.write(":PAGE:MEAS:OSEQ:TRIG:POL POS")
        self.instr.write(":PAGE:MEAS:OSEQ:TRIG:TIME 1.0")
        self.instr.write(":PAGE:SCON:TRIG:OUTP:LEV LOW")
        time.sleep(.2)
        self.instr.write(":PAGE:SCON:TRIG:OUTP:LEV HIGH")
        
        time.sleep(.2)
    ##############################################################################################################################################
    def SetTrigOutTime(self):
    # Sets Trigger Output Timing
        self.instr.write(":PAGE:MEAS:OSEQ:TRIG:TIME 0.0001")
        
        time.sleep(.2)
    ##############################################################################################################################################
    def SetTrigOutState_Lo(self):
        '''Sets Trigger Output Level to LOW State'''
        self.instr.write(":PAGE:SCON:TRIG:OUTP:LEV LOW")
        
        time.sleep(.2)
    ##############################################################################################################################################
    def SetTrigOutState_Hi(self):
        '''Sets Trigger Output Level to LOW State'''
        self.instr.write(":PAGE:SCON:TRIG:OUTP:LEV HI")
        
        time.sleep(.2)
    ##############################################################################################################################################
    def SenseNegTrigIn(self):
        '''Senses Negative Trigger Intput'''
        retval = self.instr.ask(":PAGE:SCON:TRIG:INP? NEG")
        
        ##return retval == 0
        if ( retval == 1 ) :
            return True
        return False
        
    
    
    ##############################################################################################################################################
    ##############################################################################################################################################
    ##############################################################################################################################################
    ##############################################################################################################################################
    ##############################################################################################################################################
    ##############################################################################################################################################
    ##############################################################################################################################################
    ##############################################################################################################################################
    ##############################################################################################################################################
    ##############################################################################################################################################
    def ShowList(self):
        '''Shows the list screen'''
        #self.instr.write(":PAGE:GLIS:LIST")
        self.instr.write(":PAGE:DISP:SET:MODE LIST")
        self._wait()
    ##############################################################################################################################################    
    def ShowGraph(self):
        '''Shows the graph screen'''
        self.instr.write(":PAGE:GLIS:GRAP")
        
        self._wait()
    ##############################################################################################################################################
    def LoadSetup(self, filename):
        '''Loads a 4155B setup file (*.mes)'''
        fn_tmp = os.path.join(pth_network, '!temp.mes')
        
        # Copy file
        self._copy_file(filename, fn_tmp)
        
        self.instr.write(":MMEM:LOAD:STAT 0,'TEMP.MES'")
        
        self._wait()
        
        # Delete temp file
        if os.path.exists(fn_tmp):
            os.remove(fn_tmp)
            
        self.ShowGraph()
    ##############################################################################################################################################        
    def SaveSetup(self, filename):
        '''Saves a 4155B setup file (*.mes)'''
        fn_tmp = os.path.join(pth_network, '!temp.mes')
        self.instr.write(":MMEM:STOR:STAT 0,'TEMP.MES'")
        
        self._wait()
        
        # Copy file
        self._copy_file(fn_tmp, filename)
        
        # Delete temp file
        if os.path.exists(fn_tmp):
            os.remove(fn_tmp)
            
        self.ShowGraph()
    ##############################################################################################################################################            
    def Single(self):
        '''Runs a single capture'''
        #self.ShowGraph()
        self.ShowList()
        self.instr.write(":PAGE:SCON:SING")        
        self._wait()
        #self._readCatalog()
    ##############################################################################################################################################    
    def Append(self):
        '''Runs an append capture'''
        #self.ShowGraph()
        self.ShowList()
        self.instr.write(":PAGE:SCON:APP")        
        self._wait()
    ##############################################################################################################################################    
    def SaveGraph(self, filename):
        '''Saves the screen capture of the current graph.
           The user can specify the file format with its extention'''
        self.ShowGraph()
        fn_tmp = os.path.join(pth_network, '!temp.tif')
        
        # Delete it if it exists already
        if os.path.exists(fn_tmp):
            os.remove(fn_tmp)
        
        # Set name of file to write to
        self.instr.write(":MMEM:NAME 'TEMP'")
        
        # Screendump
        self.instr.write(":HCOP:SDUM")
        
        self._wait()
        
        try:
            import PIL.Image
            img  = PIL.Image.open(fn_tmp)
            cimg = img.crop( (0, 20, 520, 400) )  # xmin, ymin, xmax, ymax
            cimg.save(filename) 
            del img
            os.remove(fn_tmp)
        finally:
            pass
    ##############################################################################################################################################
    def SaveSheet(self, filename):
        '''Saves a CSV spreadsheet of the current graph'''
        ##self.ShowGraph()
        ##self.ShowList()
        fn_tmp = os.path.join(pth_network, '!temp.txt')
        
        # Delete it if it exists already
        if os.path.exists(fn_tmp):os.remove(fn_tmp)
        
        # Save the spreadsheet
        self.instr.write(":MMEM:STOR:SSH 'TEMP'")
        self._wait()
        
        try:
            f_dest = open(filename, 'w')
            f_source = open(fn_tmp, 'r')
            blank_line = f_source.readline()
            f_dest.write( f_source.readline() )
            for line in f_source:
                f_dest.write( line.replace(' ', ',') )
            f_source.close()
            f_dest.close()
            os.remove(fn_tmp)
        finally:
            pass        
    ##############################################################################################################################################
    def SaveCSV( self, filename, mode = 'a' ):
        '''
        Saves a CSV spreadsheet of the current graph in the format we want
        
        mode = 'w' or 'a', write will overwrite the file, and append will append
               to the csv file
        '''
        t = time.time()
        fn_tmp = os.path.join(pth_network, '!temp.txt')
        
        # Delete it if it exists already
        if os.path.exists(fn_tmp):os.remove(fn_tmp)
        
        # Save the spreadsheet
        self.instr.write(":MMEM:STOR:SSH 'TEMP'")                        
        print "Time to save temp file : %f" % ( time.time() - t )
        t = time.time()
        self._wait()
        print "Time to be ready : %f" % ( time.time() - t )
        
        try:            
            f_dest = open(filename, mode );   
            f_source = open(fn_tmp, 'r');     
            blank_line  = f_source.readline();
            nop_line    = f_source.readline();
            header_line = f_source.readline().split( ' ' );
            units_line  = f_source.readline().split( ' ' );
            
            header_str  = ''
            for header, unit in zip( header_line, units_line ) :                
                header = header.strip( '\n' )
                unit   = unit.strip( '\n' )
                if not ( unit == '' ) : header = header + "(%s)" % unit
                header_str  = header_str + header + ','
            header_str = header_str.strip(',') + '\n'            
            
            f_dest.write( header_str )            
            for line in f_source:
                f_dest.write( line.replace(' ', ',') )            
                
            f_source.close()
            f_dest.close()
            os.remove(fn_tmp)            
        finally:
            pass        
        
        #self.instr.write(":MMEM:DEL 'TEMP'")
        #self.instr.write(":MMEM:DEL '!temp.txt'")
        #self._wait()
    ##############################################################################################################################################
    def _wait(self):
        self.instr.write("*OPC")
        attempt_n = 1
        done = False
        while not done:
            try:
                # Wait until 4155B is done
                retval = self.instr.ask("*OPC?")
                done = True
            except:
                attempt_n -= 1
                done = attempt_n == 0
    ##############################################################################################################################################
    def AutoCalOn(self):
        self.instr.write(":CAL:AUTO ON")
    
        self._wait()
    ##############################################################################################################################################
    def AutoCalOff(self):
        self.instr.write(":CAL:AUTO OFF")
        
        self._wait()
    ##############################################################################################################################################
    def ExecuteCal(self):
        #self.instr.write("*CAL?")
        #self._wait()
        
        retval = self.instr.ask("*CAL?")
        return retval == 0
    ##############################################################################################################################################                 
    def _copy_file(self, fn_source, fn_dest):
        f_d = open(fn_dest, 'wb')
        f_s = open(fn_source, 'rb')
        f_d.write( f_s.read() )
        f_s.close()
        f_d.close()
    ##############################################################################################################################################                     
    def _get_color(self):
        retval = self.instr.ask("HCOP:DEV:CMOD?")
        return retval == 'FULL'
    ##############################################################################################################################################
    def _set_color(self, color):
        if color:
            self.instr.write("HCOP:DEV:CMOD FULL")
        else:
            self.instr.write("HCOP:DEV:CMOD BW")

    Color = property(_get_color, _set_color, None, 'Enables the 4155B color mode')
    ##############################################################################################################################################
    def _SetNetworkCom(self):
        self.instr.write(":SYST:COMM:NET:FILE:NET:NAME 'HSC_Z_DATA'")
        self.instr.write(":SYST:COMM:NET:FILE:NET:DIR '/z/esd_hp4155_data'")
        self.instr.write(":SYST:COMM:NET:FILE:SET:NET1")
        #
        self.instr.write(":MMEM:DEST NET1")
        self.instr.write(":MMEM:CDIR '/z/esd_hp4155_data','DISK'")
        #
        time.sleep(.2)
    ##############################################################################################################################################
    def _readCatalog(self):
        retval = self.instr.ask(":MMEM:CAT?")
        #self._wait()
    ##############################################################################################################################################
#if __name__ == '__main__':
    #a = Agilent4155B(10)
    #a._SetNetworkCom()
    #a.ExecuteCal()
    #a.LoadSetup(r'Z:\esd_hp4155_data\!ad9434_3v.mes')
    #a.instr.write(":PAGE:MEAS:OSEQ:TRIG ON")
    #a.SetTrigOn()
    #a.SetTrigNeg()
    #a.SetTrigIn()
    #a.SetTrigOutTime()
    #a.SenseNegTrigIn()
    #a.Single()
    #time.sleep(.2)
    #a.SaveSheet()
    #a.LoadSetup(r'c:\temp\mess_long.mes')
    #a.SaveSetup(r'c:\temp\tom_med.mes')
    
    #a.SaveGraph(r'c:\temp\wonka2.png')
    
    #a.SaveSheet(r'Z:\esd_hp4155_data\test.txt')
    #a._wait() 
    
##    a.instr.write(':MMEM:DEST INT')                    # Internal Memory
##    a.instr.write(":MMEM:LOAD:STAT 0,'SAMPLE.MES'")    # Load saved config.
    #a.instr.write(":PAGE:SYST:CDI")
    #a.instr.write(":CAL:AUTO ON")
##    a.instr.write(':PAGE:SCON:APP')    # Append command
##    a.instr.write(':PAGE:SCON:REP')    # Repeat command
##    a.instr.write(':PAGE:SCON:SING')   # Single command
##        
##    a.instr.write(':MMEM:DEST NET1')      #  Specifies data storage location
##    a.instr.write(":MMEM:STOR:TRAC DEF,'DEF.DAT','DISK'")  # Saves the trace
##    a.instr.write(":MMEM:STOR:SSH 'TEST'")     # Saves spreadsheet in ASCII
##    a.instr.write(":CAL:AUTO:ON")
##    a.instr.write(":HCOP:DEV:LANG TIFF")   # Specifies the image type (TIFF)
##    a.instr.write(":PAGE:GLIS")    # Sets the instr screen to plot image  
##    a.instr.write(":HCOP:SDUM")    # Screendump
##    
    #a.instr.ask("*OPC?")   # Queries to see if instr is busy
    
