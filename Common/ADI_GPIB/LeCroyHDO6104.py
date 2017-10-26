import visa
import time

class HDO6104(object):
    def __init__(self, USBaddr, delay=0):
        self.__delay_time = 0
        visaObj = visa.ResourceManager()
        self.instr = visaObj.open_resource(USBaddr)
        self.set_delay(delay)
        self.instr.timeout=5000
        self.instr.clear()
        self.instr.write("COMM_HEADER OFF") # default setting would return cmd sent, this turns that off

    def __del__(self):
        self.instr.close()

    def set_delay(self, delay):
        self.__delay_time = delay

    def writestr(self, writestring):
        headstr = 'vbs '
        formatstring = headstr + writestring
        self.instr.write(formatstring)
        return formatstring

    def querystr(self, writestring):
        headstr = 'vbs? return='
        formatstring = headstr + writestring
        result = self.instr.query(formatstring)
        return result
    def readstr(self, writestring):
        headstr = 'vbs? return='
        formatstring = headstr + writestring
        result = self.instr.query(formatstring)
        return result


    def ident(self):
        '''
        Returns a tuple with the following:
            0) Manufacturer
            1) Inst Model
            2) Inst Serial Number
            3) Inst Firmware
        '''
        return tuple(self.instr.query("*IDN?").split(','))

    def reset(self):
        '''
        Resets the instrument to default settings.
        '''
        self.instr.write("*RST")

    def clearsweeps(self):
        '''
        clear sweep data
        '''
        self.writestr("'app.measure.clearsweeps ' ")

    def SetEdgeTriggertoMean(self):
        '''
        set edge trigger to mean
        '''
        self.writestr("'app.Acquisition.Trigger.edge.FindLevel ' ")


    def set_measureparameters(self,measuredict):
        self.writestr('app.measure.clearsweeps ')  # clears the sweep data
        self.writestr('app.measure.showmeasure = true ') # make sure the measurements view is displayed
        self.writestr('app.measure.p1.view = true ')  # turns on an individul measurement
        self.writestr('app.measure.p2.view = true ')  # turns on an individul measurement
        self.writestr('app.measure.p3.view = true ')  # turns on an individul measurement
        self.writestr('app.measure.p4.view = true ')  # turns on an individul measurement
        self.writestr('app.measure.p5.view = true ')  # turns on an individul measurement
        self.writestr('app.measure.p6.view = true ')  # turns on an individul measurement
        self.writestr('app.measure.p7.view = true ')  # turns on an individul measurement
        self.writestr('app.measure.p8.view = true ')  # turns on an individul measurement

        self.writestr('app.measure.p1.paramengine = "amplitude" ')  # set the measurement type
        self.writestr('app.measure.p1.source1 = "C1"')  # set the measurement source
        self.writestr('app.measure.p2.paramengine = "pkpk" ')  # set the measurement type
        self.writestr('app.measure.p2.source1 = "C1"')  # set the measurement source
        self.writestr('app.measure.p3.paramengine = "mean" ')  # set the measurement type
        self.writestr('app.measure.p3.source1 = "C1"')  # set the measurement source
        self.writestr('app.measure.p4.paramengine = "freq" ')  # set the measurement type
        self.writestr('app.measure.p4.source1 = "C1"')  # set the measurement source
        self.writestr('app.measure.p5.paramengine = "amplitude" ')  # set the measurement type
        self.writestr('app.measure.p5.source1 = "C3"')  # set the measurement source
        self.writestr('app.measure.p6.paramengine = "pkpk" ')  # set the measurement type
        self.writestr('app.measure.p6.source1 = "C3"')  # set the measurement source
        self.writestr('app.measure.p7.paramengine = "mean" ')  # set the measurement type
        self.writestr('app.measure.p7.source1 = "C3"')  # set the measurement source
        self.writestr('app.measure.p8.paramengine = "freq" ')  # set the measurement type
        self.writestr('app.measure.p8.source1 = "C3"')  # set the measurement source

    def make_acquisition(self, timeseconds=1):
        for i in range (0,4):
            result = self.querystr('app.acquisition.acquire(%s , True )') % timeseconds # make sure the measurements view is displayed
            idlecheck = self.querystr('app.WaitUntilIdle(1)')
            if ~idlecheck:
                result=999 # could not aquire signal
        return result
    def readback_measurements_value (self):
        resultsdict = {}
        resultsdict['P1value']="{:.5e}".format(float(self.readstr('app.Measure.P1.Out.Result.value')))
        resultsdict['P2value']="{:.5e}".format(float(self.readstr('app.Measure.P2.Out.Result.value')))
        resultsdict['P3value']="{:.5e}".format(float(self.readstr('app.Measure.P3.Out.Result.value')))
        resultsdict['P4value']="{:.5e}".format(float(self.readstr('app.Measure.P4.Out.Result.value')))
        resultsdict['P5value']="{:.5e}".format(float(self.readstr('app.Measure.P5.Out.Result.value')))
        resultsdict['P6value']="{:.5e}".format(float(self.readstr('app.Measure.P6.Out.Result.value')))
        resultsdict['P7value']="{:.5e}".format(float(self.readstr('app.Measure.P7.Out.Result.value')))
        resultsdict['P8value']="{:.5e}".format(float(self.readstr('app.Measure.P8.Out.Result.value')))
            # Value = app.measure.p1.out.Result.Value
            # Mean = app.measure.p1.Mean.Result.Value
            # Min = app.measure.p1.Min.Result.Value
            # Max = app.measure.p1.Max.Result.Value
            # Sdev = app.measure.p1.Sdev.Result.Value
            # Num = app.measure.p1.Num.Result.Value
        return resultsdict

    def readback_measurements_mean (self):
        resultsdict = {}
        resultsdict['P1mean']="{:.5e}".format(float(self.querystr('app.measure.p1.Mean.Result.Value')))
        resultsdict['P2mean']="{:.5e}".format(float(self.querystr('app.Measure.P2.mean.Result.Value')))
        resultsdict['P3mean']="{:.5e}".format(float(self.querystr('app.Measure.P3.mean.Result.Value')))
        resultsdict['P4mean']="{:.5e}".format(float(self.querystr('app.Measure.P4.mean.Result.Value')))
        resultsdict['P5mean']="{:.5e}".format(float(self.querystr('app.Measure.P5.mean.Result.Value')))
        resultsdict['P6mean']="{:.5e}".format(float(self.querystr('app.Measure.P6.mean.Result.Value')))
        resultsdict['P7mean']="{:.5e}".format(float(self.querystr('app.Measure.P7.mean.Result.Value')))
        resultsdict['P8mean']="{:.5e}".format(float(self.querystr('app.Measure.P8.mean.Result.Value')))
        return resultsdict