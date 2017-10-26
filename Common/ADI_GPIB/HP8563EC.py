# Author: Lloyd Weida

# Purpose: This module is for Agilent 8563EC Spectrum Analyser
# 
from ADI_GPIB.GPIBObject import GPIBObjectBaseClass as GPIBObjectBaseClass
import time

class HP8563EC(GPIBObjectBaseClass):
    def __init__(self, addr=-1, delay=0.1):
        GPIBObjectBaseClass.__init__(self, 'HP8563EC', addr)
        self.__delay__ = delay
        
    def __get_mkr_freq__(self):     
        return float( self.instr.ask('mkn?') )

    def __get_mkr_amp__(self):     
        return float( self.instr.ask('mka?') )
		
    def __set_mkr_pk_thresh__(self, mkr_peak_thresh):
        self.instr.write( 'mkpt  ' + str(mkr_peak_thresh) )
        time.sleep(self.__delay__)				
		
    def __set_start_freq__(self, start_freq):
        self.instr.write( 'FA  ' + str(start_freq) )
        time.sleep(self.__delay__)		
		
    def __set_stop_freq__(self, stop_freq):
        self.instr.write( 'FB  ' + str(stop_freq) )
        time.sleep(self.__delay__)		
                
    def __set_set_center_freq__(self, center_frequency):
        self.instr.write( 'cf  ' + str(center_frequency) )
        time.sleep(self.__delay__)            	
        self.instr.write( 'cf  ' + str(center_frequency) )
        time.sleep(self.__delay__)                

    def __set_set_span__(self, span):
        self.instr.write( 'sp  ' + str(span) )
        time.sleep(self.__delay__)

                		
    def __put_marker_at_peak__(self):
        self.instr.write( 'mkpk hi' )
        time.sleep(self.__delay__)
		
    def __continuous_sweep__(self):
        self.instr.write( 'CONTS ' )
        time.sleep(self.__delay__)
		
    def __single_sweep__(self):
        self.instr.write( 'SNGLS ' )
        time.sleep(self.__delay__)
				
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# not converted yet:
# void hp_8563_set_markers (double *center_frequency, double *sideband_frequency)
  # {
  # char command [256], data [2048];
  
  # sprintf (command, "clrw tra\r\n");
  # transmit (HP8563, command);

  # Delay (1.0);
  
  # sprintf (command, "mkoff all\r\n");
  # transmit (HP8563, command);

  # sprintf (command, "mkpk hi\r\n");
  # transmit (HP8563, command);

  # sprintf (command, "mkf?\r\n");
  # transmit (HP8563, command);
    
  # receive (ASCII, HP8563, data); 
  # *center_frequency = extract_number (1, data);

  # sprintf (command, "mkpk nr\r\n");
  # transmit (HP8563, command);

  # sprintf (command, "mkf?\r\n");
  # transmit (HP8563, command);
    
  # receive (ASCII, HP8563, data); 
  # *sideband_frequency = extract_number (1, data);
  # }
# double hp_8563_get_sideband_power (double center_frequency, double sideband_frequency)
  # {
  # char command [256], data [2048];
  # double center_amplitude, sideband_amplitude;

  # sprintf (command, "clrw tra\r\n");
  # transmit (HP8563, command);

  # Delay (1.0);
  
  # sprintf (command, "mkn %e\r\n", center_frequency);
  # transmit (HP8563, command);
    
  # sprintf (command, "mka?\r\n");
  # transmit (HP8563, command);

  # receive (ASCII, HP8563, data); 
  # center_amplitude = extract_number (1, data);
 
  # sprintf (command, "mkn %e\r\n", sideband_frequency);
  # transmit (HP8563, command);
    
  # sprintf (command, "mka?\r\n");
  # transmit (HP8563, command);
    
  # receive (ASCII, HP8563, data); 
  # sideband_amplitude = extract_number (1, data);

  # return (sideband_amplitude - center_amplitude);
  # }
# double setSpecAnalyzer_crse_mkr_freq(void)
# {
# double mkr_freq;
# float wait=0.500,fwait;

# wait=0.2,fwait=0.050;
# hp_8563_set_start_freq(0.010E9); Delay(wait); hp_8563_set_start_freq(0.010E9);
# hp_8563_set_stop_freq(20.0E9); Delay(fwait); hp_8563_set_stop_freq(20.0E9); 
# hp_8563_set_span(18.0E9);  Delay(fwait);   hp_8563_set_span(18.0E9); Delay(3.0);
# hp_8563_put_marker_at_peak(); Delay(wait); hp_8563_put_marker_at_peak();Delay(1.0); 

# mkr_freq= hp_8563_get_mkr_freq(); Delay(wait); mkr_freq= hp_8563_get_mkr_freq(); 

# hp_8563_set_center(mkr_freq); Delay(fwait); hp_8563_set_center(mkr_freq);
	
# hp_8563_put_marker_at_peak(); Delay(fwait); hp_8563_put_marker_at_peak();

# hp_8563_set_span(0.800E9);	Delay(fwait);  hp_8563_set_span(0.800E9);Delay(3.0);

# hp_8563_put_marker_at_peak(); Delay(wait); hp_8563_put_marker_at_peak();

# mkr_freq= hp_8563_get_mkr_freq(); Delay(wait); mkr_freq= hp_8563_get_mkr_freq();
# hp_8563_put_marker_at_peak(); Delay(wait); hp_8563_put_marker_at_peak();

# return(mkr_freq);
# }

# double setSpecAnalyzer_crse_mkr_freq2(void)  //more fine-tuned
# {
# double mkr_freq,strt_freq,end_freq,span_freq;
# float wait=0.500,fwait;
# int doagain=0;

# wait=0.2,fwait=0.050;
# strt_freq= 3.010E9; end_freq= 14.0E9;
# span_freq=end_freq-strt_freq;

# hp_8563_set_start_freq(strt_freq); Delay(wait); if(doagain) hp_8563_set_start_freq(strt_freq);
# hp_8563_set_stop_freq(end_freq); Delay(fwait); if(doagain) hp_8563_set_stop_freq(end_freq); 
# hp_8563_set_span(span_freq);  Delay(fwait);   if(doagain) hp_8563_set_span(span_freq); Delay(3.0);
# hp_8563_put_marker_at_peak(); Delay(wait); if(doagain) hp_8563_put_marker_at_peak();Delay(1.0); 

# mkr_freq= hp_8563_get_mkr_freq(); Delay(wait); if(doagain) mkr_freq= hp_8563_get_mkr_freq(); 

# hp_8563_set_center(mkr_freq); Delay(fwait); if(doagain) hp_8563_set_center(mkr_freq);
	
# hp_8563_put_marker_at_peak(); Delay(fwait); if(doagain) hp_8563_put_marker_at_peak();

# hp_8563_set_span(0.800E9);	Delay(fwait);  if(doagain) hp_8563_set_span(0.800E9);Delay(3.0);

# hp_8563_put_marker_at_peak(); Delay(wait); if(doagain) hp_8563_put_marker_at_peak();

# mkr_freq= hp_8563_get_mkr_freq(); Delay(wait); if(doagain) mkr_freq= hp_8563_get_mkr_freq();
# hp_8563_put_marker_at_peak(); Delay(wait); if(doagain) hp_8563_put_marker_at_peak();

# return(mkr_freq);
# }
# int hp_8563_read_trace (int trace, double frequency_points [], double amplitude_points [])
  # {
  # char command [256], data [2048], *sample_pointer, temp;
  # int byte_count, sample_size, measurement_result, i, units, scale;
  # double frequency_start, frequency_span, ref_level, units_per_div;
  
  # Delay (0.1);

  # sprintf (command, "fa?\r\n");
  # transmit (HP8563, command);

  # receive (ASCII, HP8563, data); 
  # frequency_start = extract_number (1, data);

  # sprintf (command, "sp?\r\n");
  # transmit (HP8563, command);
  
  # receive (ASCII, HP8563, data); 
  # frequency_span = extract_number (1, data);
  
  # sprintf (command, "rl?\r\n");
  # transmit (HP8563, command);

  # receive (ASCII, HP8563, data); 
  # ref_level = extract_number (1, data);

  # sprintf (command, "aunits?\r\n");
  # transmit (HP8563, command);

  # receive (ASCII, HP8563, data); 
  # if (strncmp (data, "DBM", 3) == 0) units = UNITS_DBM;
  # if (strncmp (data, "DBMV", 4) == 0) units = UNITS_DBMV;
  # if (strncmp (data, "DBUV", 4) == 0) units = UNITS_DBUV;
  # if (strncmp (data, "V", 1) == 0) units = UNITS_VOLTS;
  # if (strncmp (data, "W", 1) == 0) units = UNITS_WATTS;

  # sprintf (command, "lg?\r\n");
  # transmit (HP8563, command);

  # receive (ASCII, HP8563, data); 
  # units_per_div = extract_number (1, data);

  # if (units_per_div < 0.1)
    # {
    # scale = SCALE_LIN;
    # units_per_div = 1.0;
    # }
  # else
    # {
    # scale = SCALE_LOG; 
    # }
  
  # sprintf (command, "tdf a\r\n");
  # transmit (HP8563, command);
  
  # switch (trace)
    # {
    # case 0: sprintf (command, "tra?\r\n");
            # break;
    # case 1: sprintf (command, "trb?\r\n");
            # break;
    # }
  # transmit (HP8563, command);    
  # receive (BINARY, HP8563, data);

  # if (strncmp (data, "#A", 2) == 0)
    # {
    # //printf ("\nValid Header in Measurement String\n");
    # //printf ("%u Characters in Measurement String\n", strlen (data));
    # //printf ("%s", data);
    # //printf ("\n");

    # // Reverse the order of the byte count. Big Endian to Little Endian or Vice Versa? 
    # temp = data [2];
    # data [2] = data [3];
    # data [3] = temp;

    # sample_pointer = &data [2];
    
    # byte_count = *((unsigned short*) sample_pointer);
    # printf ("Byte Count = %d\n", byte_count);

    # sample_size = byte_count / 2;
    # printf ("Sample Size = %d\n", sample_size);

    # // Reverse the order of the measurement results. Big Endian to Little Endian or Vice Versa?
    # for (i = 0; i < sample_size; i++)
      # {
      # temp = data [2 * i + 4];
      # data [2 * i + 4] = data [2 * i + 5];
      # data [2 * i + 5] = temp;
      # }
    
    # sample_pointer = &data [4];

    # for (i = 0; i < sample_size; i++)
      # {
      # measurement_result = *((unsigned short*) sample_pointer);

      # if (scale == SCALE_LOG)
        # {
        # if (units == UNITS_VOLTS || units == UNITS_WATTS)
          # {        
          # amplitude_points [i] = ref_level * pow (10.0, (units_per_div * (((double) measurement_result) / 60.0 - 10.0) / 20.0));
          # }
        # else
          # {
          # amplitude_points [i] = ref_level + units_per_div * (((double) measurement_result) / 60.0 - 10.0);
          # }
        # }
      # else
        # {
        # amplitude_points [i] = ref_level * ((double) measurement_result) / 600.0;
        # }
       
      # frequency_points [i] = frequency_span * (((double) i) / ((double) sample_size)) + frequency_start;  

      # sample_pointer +=2;
      # }
    # }
  # else
    # {
    # printf ("\nInvalid Header in Measurement String\n");
    # printf ("%u Characters in Measurement String\n", strlen (data));
    # printf ("%s", data);

    # sample_size = 0;
    # }
  
  # return sample_size;
  # }   // end of "hp_8563_read_trace"
	
# void hp_8563_set_markers (double *center_frequency, double *sideband_frequency)
  # {
  # char command [256], data [2048];
  
  # sprintf (command, "clrw tra\r\n");
  # transmit (HP8563, command);

  # Delay (1.0);
  
  # sprintf (command, "mkoff all\r\n");
  # transmit (HP8563, command);

  # sprintf (command, "mkpk hi\r\n");
  # transmit (HP8563, command);

  # sprintf (command, "mkf?\r\n");
  # transmit (HP8563, command);
    
  # receive (ASCII, HP8563, data); 
  # *center_frequency = extract_number (1, data);

  # sprintf (command, "mkpk nr\r\n");
  # transmit (HP8563, command);

  # sprintf (command, "mkf?\r\n");
  # transmit (HP8563, command);
    
  # receive (ASCII, HP8563, data); 
  # *sideband_frequency = extract_number (1, data);
  # }	
		
		
    def __SetV__(self, V1):
        '''This function sets the V Voltage'''
        self.instr.write( 'VOLTage ' + str(V1) )
        time.sleep(self.__delay__)
               
    def __GetI__(self):
        '''This function gets the I Current'''
        return float( self.instr.ask('MEASure:CURRent?') )
    def __SetI__(self, I1):
        '''This function sets the I Current'''
        self.instr.write( 'CURRent ' + str(I1) )
        time.sleep(self.__delay__)
    
    def __SetEnable__(self, Enabled):
        '''This function enables the On/Off for the PST-3202'''
        if Enabled:
            self.instr.write('OUTPut:STATe ON')
        else:
            self.instr.write('OUTPut:STATe OFF')
    
    def __GetEnable__(self):
        '''This function returns the On/Off state'''
        status = self.instr.ask('OUTPut:STATe?')
        if (status == "1" ):
            return True
        return False        
    
    def __SetDelay__(self, d):
        '''Sets this instruments settling time'''
        self.__delay__ = d
        
    def __GetDelay__(self):
        '''Gets this instrument's settling time'''
        return self.__delay__
   