#-----------------------------------------------------------------------------
# Name:        TEK_DPO70604.py
# Purpose:     Driver for the Tektronix DPO70604 scope.
#
# Author:      Dave Shoudy
#
# Created:     2007/08/10
#-----------------------------------------------------------------------------

from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
import time

class TEK_DPO70604(GPIBObjectBaseClass):
    def __init__(self, addr=-1):
        '''Initializes the GPIB interface'''
        GPIBObjectBaseClass.__init__(self, 'Tektronixs,DPO70604', addr)
 
    def __ConfigChannel__(self,channel=1,scale=1,position=0,coupling='DC'):
        '''This function configures a channel for the vertical axis and any other properties'''
        self.instr.write('CH%s:BAN FUL' %str(channel))          # No bandwidth limiting
        self.instr.write('CH%s:BAN:ENH AUTO' %str(channel))     # Auto DSP bandwidth limiting
        
        # Setup coupling: coupling = {AC|DC|GND|DCREJect}
        coup = 'CH' + str(channel) + ':COUP ' + coupling
        self.instr.write(coup)  
        
        self.instr.write('CH%s:OFFS 0' %str(channel))            # No offset of waveform
        
        # Set the vertical position of the waveform on the scope. "position" has units of divisions
        pos = 'CH' + str(channel) + ':POS ' + str(position)
        self.instr.write(pos)
        
        # Set the vertical scale in volts per division
        sca = 'CH' + str(channel) + ':SCA ' + str(scale)
        self.instr.write(sca)
        
        # Select the channel and turn it on
        self.instr.write('SELECT:CH%s ON' %str(channel))
        self.instr.write('SELECT:CONTROL CH%s' %str(channel))   # Selects this channel for the front panel buttons
        
    
    def __ConfigHORIZaxis__(self,t_div=1E-9):
        '''This function configures the horizontal axis on the scope'''
        self.instr.write('HOR:DEL:MOD OFF')    # Turn off the delay mode
        self.instr.write('HOR:DEL:TIM 50')     # Is this needed?
        self.instr.write('HOR:POS 50')         # Center the horizontal axis
        self.instr.write('HOR:SCA %s' %str(t_div))       # Set the time per division
        
    def __ConfigTrigger__(self,channel=1,level=0,edge='RE',type='NORM'):
        '''This function configures the trigger on the scope'''
        self.instr.write('TRIG:A:EDGE:COUP DC')         # Setup DC coupling for the trigger
        
        # Parameter 'edge' should be 'RE' or 'FE', setup edge for triggering here
        if edge == 'FE':
            self.instr.write('TRIG:A:EDGE:SLO FALL')        
        else:
            self.instr.write('TRIG:A:EDGE:SLO RISE')
        
        self.instr.write('TRIG:A:EDGE:SOURCE CH%s' %str(channel))   # Set the triggering source
        self.instr.write('TRIG:A:LEV %s' %str(level))       # Set the trigger level
        
        # Set the triggering mode (parameter "type" should be 'AUTO' or 'NORM')
        if type == 'AUTO':
            self.instr.write('TRIG:A:MODE AUTO')
        else:
            self.instr.write('TRIG:A:MODE NORM')
        
    def __RunStop__(self,runstop=1):
        '''This function configures the aquisition parameters.  Currently just being used to start and stop
           the scope, but it could eventually be used to setup averaging or other acquisition parameters'''
        if runstop:
            self.instr.write('ACQ:STATE RUN')
        else:
            self.instr.write('ACQ:STATE STOP')   
        
    def __ExportToFile__(self,filename):    # ********* FILENAME must have double slashes \\ between directories ***********
        '''This function exports a screenshot of the scope waveforms to a file'''
        # Get the scopes current running state
        state = self.instr.ask('ACQ:STATE?')
        # Stop the scope first
        self.RunStop(0)
        
        self.instr.write('EXP:VIEW FULLSCREEN')     # Capture the full screen in the image
        self.instr.write('EXP:IMAGE NORM')          # Normal colors (black background)
        self.instr.write('EXP:FORMAT JPEG')         # Save in JPEG format
        self.instr.write('EXP:FILENAME "%s"' %str(filename))    # Set the output filename
        self.instr.write('EXP START')     # Export the file
        
        # Put the scope back in the state it was in previously
        self.RunStop(int(state))

    def __SetupMeas__(self,meas_num=1,channel=1,type='FREQ',avg=100):
        '''This function initializes measurement "meas_num" (1-8) for the specified channel and type'''
        '''Refer to the scope programmers manual for all the variables that can go in "type"'''
        # Setup the specified channel for measurement number "meas_num"
        s1 = 'MEASU:MEAS' + str(meas_num) + ':SOURCE1 CH' + str(channel)
        self.instr.write(s1)
        
        # Setup the type of measurement
        s2 = 'MEASU:MEAS' + str(meas_num) + ':TYPE ' + str(type)
        self.instr.write(s2)
        '''Valid Types are:
           {AMPlitude|AREa|BURst|CARea|CMEan|CRMs|DELay|DISTDUty|EXTINCTDB|EXTINCTPCT|EXTINCTRATIO|EYEHeight|
            EYEWIdth|FALL|FREQuency|HIGH|HITs|LOW|MAXimum|MEAN|MEDian|MINImum|NCROss|NDUty|
            NOVershoot|NWIdth|PBASe|PCROss|PCTCROss|PDUty|PEAKHits|PERIod|PHAse|PK2Pk|PKPKJitter|
            PKPKNoise|POVershoot|PTOP|PWIdth|QFACtor|RISe|RMS|RMSJitter|RMSNoise|SIGMA1|SIGMA2|
            SIGMA3|SIXSigmajit|SNRatio|STDdev|UNDEFINED| WAVEFORMS}'''
            
        # Turn on the measurement
        self.instr.write('MEASU:MEAS%s:STATE ON' %str(meas_num))
        
        # Setup averaging for statistical calcs like mean and stdev
        self.instr.write('MEASU:STATI:WEI %s' %str(avg))
    
    def __GetVal__(self,meas_num=1):
        '''This function gets the value of measurement "meas_num"'''
        return self.instr.ask('MEASU:MEAS%s:VAL?' %str(meas_num))
    
    def __GetMin__(self,meas_num=1):
        '''This function gets the minimum value of measurement "meas_num"'''
        return self.instr.ask('MEASU:MEAS%s:MINI?' %str(meas_num))
    
    def __GetMax__(self,meas_num=1):
        '''This function gets the maximum value of measurement "meas_num"'''
        return self.instr.ask('MEASU:MEAS%s:MAX?' %str(meas_num))
    
    def __GetMean__(self,meas_num=1):
        '''This function gets the mean value of measurement "meas_num"'''
        return self.instr.ask('MEASU:MEAS%s:MEAN?' %str(meas_num))
    
    def __GetSTDdev__(self,meas_num=1):
        '''This function gets the standard deviation value of measurement "meas_num"'''
        return self.instr.ask('MEASU:MEAS%s:STD?' %str(meas_num))
        
    def __GetCount__(self,meas_num=1):
        '''This function gets the statical count total for measurement "meas_num" since the last statistical reset'''
        return self.instr.ask('MEASU:MEAS%s:COUNT?' %str(meas_num))
        
        
        
        
        