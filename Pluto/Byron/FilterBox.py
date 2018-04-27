import sys
sys.path.append("T:\USB") # Brings in the drivers from the network drive
import ADI_GPIB
import time 
class FilterBox():

        MHz = 1e6
        ################################################################################
        #### Enter desired filters for sweep in this array.             #### 
        #### They should be in order of increasing value.               ####
        ################################################################################
        # Installed on 2/28/17 by Chas Frick for David Brandon's Lab                            ####
        #### 1=Aux      2=2.3MHz        3=10.3M         4=70M   5=100.3M        6=200M          ####
        #### 7=300M     8=400M          9=500M          10=700M 11=1G           12=1.5G         ####
        #### 13=2G      14=2.5G         15=3.1G         16=3.7G 17=4.0G         18=4.5G         ####
        #### 19=5G      20=5.5G         21=5.95G                                                ####
        ################################################################################
        AllFilters = [2,  3,  4,  5,  6,  7,  8,  9,  10,  11,  12,  13,  14,  15,  16,  17,  18,  19,  20,  21] 
        
        InstalledFilters = [2,  3,  4,  5,  6,  7,  8,  9,  10,  11,  12,  13,  14,  15,  16,  17,  18,  19,  20,  21] 
        #########################################################
        
        def __init__(self, addr=-1, delay=0.05):
                
                self.l4445a = ADI_GPIB.L4445A(addr, switches = {(1, 1) : 'L7206A', 
                                                                                        (1, 2) : 'L7206A', 
                                                                                        (2, 1) : 'L7206A', 
                                                                                        (2, 2) : 'L7206A',
                                                                                        (3, 1) : 'L7206A', 
                                                                                        (3, 2) : 'L7206A',
                                                                                        (4, 1) : 'L7206A', 
                                                                                        (4, 2) : 'L7206A'})
                self.SW0 = self.l4445a.SW11
                self.SW1 = self.l4445a.SW12                                  
                self.SW2 = self.l4445a.SW21
                self.SW3 = self.l4445a.SW22
                self.SW4 = self.l4445a.SW31
                self.SW5 = self.l4445a.SW32
                self.SW6 = self.l4445a.SW41
                self.SW7 = self.l4445a.SW42
                
                self.Delay = delay
                
                # Select the aux filter
                self.SW6.Channel = 4
                self.SW7.Channel = 1 
                self.CurrentFilter = 1
                self.CurrentFilterFreq = 'AUX'
        
        def SetFilterNum(self, SMA, filterNum, AuxSMAFreqMHz = 1800.332465132*MHz ):
                MHz = 1e6
                '''This function sets filter to the desired number with the given SMA Frequency'''
                # This is the auxiliary channel. To use it, enter the desired freq in the function call as AuxSMAFreqMHz 
                # Then attach the filter between the auxiliary ports. Then enter a "1" into the filters array and run the script.  
                if (filterNum == 1):
                        self.SW6.Channel = 4
                        self.SW7.Channel = 1
                        #SMA.Frequency = AuxSMAFreqMHz
                        SMA.Frequency = 4001.123456789*MHz
                        self.CurrentFilterFreq = '4.0G'
                                
                elif (filterNum == 2):
                        self.SW6.Channel = 6
                        self.SW7.Channel = 5
                        SMA.Frequency = 2.323456789*MHz
                        self.CurrentFilterFreq = '2.3M'
                                
                elif (filterNum == 3):
                        self.SW6.Channel = 5
                        self.SW7.Channel = 6
                        SMA.Frequency = 10.323456789*MHz
                        self.CurrentFilterFreq = '10.3M'
                                
                elif (filterNum == 4):
                        self.SW6.Channel = 3
                        self.SW7.Channel = 2
                        SMA.Frequency = 70.123456789*MHz
                        self.CurrentFilterFreq = '70M'                  
                                
                elif (filterNum == 5):
                        self.SW6.Channel = 2
                        self.SW7.Channel = 3
                        SMA.Frequency = 100.323456789*MHz
                        self.CurrentFilterFreq = '100.3M'                       
                                                 
                elif (filterNum == 6):
                        self.SW6.Channel = 1
                        self.SW7.Channel = 4
                        self.SW4.Channel = 6 
                        self.SW5.Channel = 5
                        SMA.Frequency = 200.123456789*MHz 
                        self.CurrentFilterFreq = '200.3M'
                        
                elif (filterNum == 7):
                        self.SW6.Channel = 1
                        self.SW7.Channel = 4
                        self.SW4.Channel = 5 
                        self.SW5.Channel = 6
                        SMA.Frequency = 300.123456789*MHz
                        self.CurrentFilterFreq = '300.3M'
                                
                elif (filterNum == 8):
                        self.SW6.Channel = 1
                        self.SW7.Channel = 4
                        self.SW4.Channel = 4 
                        self.SW5.Channel = 1
                        SMA.Frequency = 400.123456789*MHz
                        self.CurrentFilterFreq = '400.3M'                       
                                
                elif (filterNum == 9):
                        self.SW6.Channel = 1
                        self.SW7.Channel = 4
                        self.SW4.Channel = 3 
                        self.SW5.Channel = 2
                        SMA.Frequency = 503.123456789*MHz
                        self.CurrentFilterFreq = '500.3M'                       
                                
                                
                elif (filterNum == 10):
                        self.SW6.Channel = 1
                        self.SW7.Channel = 4
                        self.SW4.Channel = 2 
                        self.SW5.Channel = 3
                        SMA.Frequency = 703.123456789*MHz
                        self.CurrentFilterFreq = '700.3M'                       
                                
                elif (filterNum == 11):
                        self.SW6.Channel = 1
                        self.SW7.Channel = 4
                        self.SW4.Channel = 1
                        self.SW5.Channel = 4
                        self.SW2.Channel = 6
                        self.SW3.Channel = 5
                        SMA.Frequency = 1001.123456789*MHz # 1000.3M filterNum
                        self.CurrentFilterFreq = '1000.3M'                      
                                
                elif (filterNum == 12):
                        self.SW6.Channel = 1
                        self.SW7.Channel = 4
                        self.SW4.Channel = 1
                        self.SW5.Channel = 4
                        self.SW2.Channel = 5
                        self.SW3.Channel = 6
                        SMA.Frequency = 1501.123456789*MHz  
                        self.CurrentFilterFreq = '1.5G'
                        
                elif (filterNum == 13):
                        self.SW6.Channel = 1
                        self.SW7.Channel = 4
                        self.SW4.Channel = 1
                        self.SW5.Channel = 4
                        self.SW2.Channel = 4
                        self.SW3.Channel = 1
                        SMA.Frequency = 2001.123456789*MHz 
                        self.CurrentFilterFreq = '2G'
                                
                elif (filterNum == 14):
                        self.SW6.Channel = 1
                        self.SW7.Channel = 4
                        self.SW4.Channel = 1
                        self.SW5.Channel = 4
                        self.SW2.Channel = 3
                        self.SW3.Channel = 2
                        SMA.Frequency = 2503.123456789*MHz  
                        self.CurrentFilterFreq = '2.5G'                 
                                
                elif (filterNum == 15):
                        self.SW6.Channel = 1
                        self.SW7.Channel = 4
                        self.SW4.Channel = 1       
                        self.SW5.Channel = 4
                        self.SW2.Channel = 2
                        self.SW3.Channel = 3
                        SMA.Frequency = 3100.123456789*MHz   
                        self.CurrentFilterFreq = '3.1G'                 
                                
                elif (filterNum == 16):
                        self.SW6.Channel = 1
                        self.SW7.Channel = 4
                        self.SW4.Channel = 1
                        self.SW5.Channel = 4
                        self.SW2.Channel = 1
                        self.SW3.Channel = 4
                        self.SW0.Channel = 6
                        self.SW1.Channel = 5
                        SMA.Frequency = 3700.123456789*MHz
                        self.CurrentFilterFreq = '3.7G'                                         
                                
                elif (filterNum == 17):
                        self.SW6.Channel = 1
                        self.SW7.Channel = 4
                        self.SW4.Channel = 1
                        self.SW5.Channel = 4
                        self.SW2.Channel = 1
                        self.SW3.Channel = 4
                        self.SW0.Channel = 5
                        self.SW1.Channel = 6
                        SMA.Frequency = 5900.123456789*MHz 
                        self.CurrentFilterFreq = '5.9G'                 
                                
                elif (filterNum == 18):
                        self.SW6.Channel = 1
                        self.SW7.Channel = 4
                        self.SW4.Channel = 1
                        self.SW5.Channel = 4
                        self.SW2.Channel = 1
                        self.SW3.Channel = 4
                        self.SW0.Channel = 4
                        self.SW1.Channel = 1
                        SMA.Frequency = 4500.123456789*MHz
                        self.CurrentFilterFreq = '4.5G'                                         
                                
                
                elif (filterNum == 19):
                        self.SW6.Channel = 1
                        self.SW7.Channel = 4
                        self.SW4.Channel = 1
                        self.SW5.Channel = 4
                        self.SW2.Channel = 1
                        self.SW3.Channel = 4
                        self.SW0.Channel = 3
                        self.SW1.Channel = 2
                        SMA.Frequency = 5000.123456789*MHz 
                        self.CurrentFilterFreq = '5.0G'                 
                                
                elif (filterNum == 20):
                        self.SW6.Channel = 1
                        self.SW7.Channel = 4
                        self.SW4.Channel = 1
                        self.SW5.Channel = 4
                        self.SW2.Channel = 1
                        self.SW3.Channel = 4
                        self.SW0.Channel = 2
                        self.SW1.Channel = 3
                        SMA.Frequency = 5500.123456789*MHz
                        self.CurrentFilterFreq = '5.5G'                                         
                                
                elif (filterNum == 21):
                        self.SW6.Channel = 1
                        self.SW7.Channel = 4
                        self.SW4.Channel = 1
                        self.SW5.Channel = 4
                        self.SW2.Channel = 1
                        self.SW3.Channel = 4
                        self.SW0.Channel = 1
                        self.SW1.Channel = 4
                        SMA.Frequency = 4001.123456789*MHz
                        self.CurrentFilterFreq = '4.0G'                      
                        
                self.CurrentFilter = filterNum
                time.sleep(self.Delay)
                
        def __GetFilterNum__(self):
                '''This function returns the current filter selected'''
                return self.CurrentFilter
        
        def __GetFilterFreq__(self):
                '''This function returns the selected current filter freq'''
                return self.CurrentFilterFreq
        
        CurrentFilter  = property(__GetFilterNum__, None,    None, "Gets the current filter")
        CurrentFilterFreq = property(__GetFilterFreq__, None, None, "Gets the current filter freq")
        
        #Aliases
        CF  = property(__GetFilterNum__, None,    None, "Gets the current filter")
        CFF  = property(__GetFilterFreq__, None,    None, "Gets the current filter freq")
