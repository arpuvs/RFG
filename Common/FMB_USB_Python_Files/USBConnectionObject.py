from ConnectionObject import ConnectionObject

class USBConnectionObject(ConnectionObject):
    
    def __init__(self, addr, debug):
        
        ConnectionObject.__init__(self, addr, debug)
        
    def check_serial_port(self, COM_PORT):
        
        import serial.tools.list_ports 
        portListing = serial.tools.list_ports.comports()
        
        for port in portListing:
            print "port: ", port[0]
        
        FMB_Port = COM_PORT

        strPortList = [str(port.device) for port in portListing] # Create list of ports

        print "ports line 27: ",strPortList
        if(not FMB_Port in strPortList):
            print "FMB port %s not found!" % FMB_Port
            
            print "Other possible ports are:" ,
            for port in portListing:
                print port.device,
            
            newPortNum = raw_input("\nWhich port or port number is the FMB supposed to be on? ")
            newPortNum = newPortNum.strip()
            print "Entered port number: %s" % newPortNum
            
            try:
                portNum = int(newPortNum) # try converting to int if the user enters a 1 etc.
                newPortNum = "COM" + str(portNum) 
            except:
                pass 
            
            newPortNum = newPortNum.upper()
            
            portListing = serial.tools.list_ports.comports()

            strPortList = [str(port.device) for port in portListing] # Create list of ports
            
            while(newPortNum not in strPortList):
                print "FMB port %s not found!" % newPortNum
                
                print "Other possible ports are:" ,
                for port in portListing:
                    print port.device,
                    
                newPortNum = raw_input("Which port or port number is the FMB supposed to be on? ")
                newPortNum = newPortNum.strip()
                print "Entered port number: %s" % newPortNum
                
                try:
                    portNum = int(newPortNum) # try converting to int if the user enters a 1 etc.
                    newPortNum = "COM" + str(portNum) 
                except:
                    pass
                
                newPortNum = newPortNum.upper()
                
                portListing = serial.tools.list_ports.comports()
                strPortList = [str(port.device) for port in portListing] # Create list of ports
                
            FMB_Port = newPortNum
            
        print "\nUsing FMB on port %s" % FMB_Port
        
        return FMB_Port
        
    def check_address(self, addr):
    
        FMB_Port = self.check_serial_port(addr) # see if the port is valid    
    
        self.update_address(FMB_Port)
        
        return self.addr
        
    def send_write_command(self, commandToSend):
        
        if(self.debug):
            print "CommandToSend: %s" % commandToSend
            #return
        
        import serial
        import time
            
        response = ''
        with serial.Serial(port=self.addr, baudrate = 115200, timeout=0.5) as FMBSerial:
            FMBSerial.write(commandToSend)
            while(FMBSerial.inWaiting() == 0):
                time.sleep(0.01)
            response = FMBSerial.readline()
            
            response = response.strip() # trim any whitespace
            print response
            
        if(response != 'OK'):
            raise Exception("Communication to FMB via COM port failed! Response received was not excepted. Check connection")
    
    def send_query_command(self, commandToSend):
        raise Exception("sendQueryCommand not implemented!")
    
    def close(self):
        raise Exception("not implemented")
            