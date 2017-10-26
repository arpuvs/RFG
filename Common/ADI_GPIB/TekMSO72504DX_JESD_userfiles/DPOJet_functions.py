import visa 
import wx  

rm = visa.ResourceManager()
scope1= rm.get_instrument("GPIB0::15")

from datetime import datetime
def SaveReportToFile(report_filename):
    
    device_name = report_filename
    fpath ='C:\\TekApplications\\DPOJET\\JESD204B\Reports\\'
    dt = str(datetime.today()) #adds date\time stamp to file name
    dt = dt.replace(" ","_")
    dt = dt.replace(":","_")
    dt = str.split(dt,".")
    print 'Saving to file:' + fpath + device_name + "_" + dt[0] +"';"
    scope1.write("DPOJET:REPORT:VIEWreport 0") #1 will view report 0 does not view report
    scope1.write("DPOJET:REPORT:REPORTN '" + fpath + device_name + "_" + dt[0] +"';")
    scope1.write("DPOJET:REPORT EXEC")

def SaveScreenToFile(report_filename):
    device_name = report_filename
    fpath = 'C:\\TekApplications\\DPOJET\\JESD204B\ScreenImages\\'
    dt = str(datetime.today())  # adds date\time stamp to file name
    dt = dt.replace(" ", "_")
    dt = dt.replace(":", "_")
    dt = str.split(dt, ".")
    print 'Saving to file:' + fpath + device_name + "_" + dt[0] + "';"
    scope1.write("EXPort:FORMat  JPG")
    scope1.write("EXPort:FILEName '" + fpath + device_name + "_" + dt[0] + "';")
    scope1.write("EXPort STARt")
def JESD204BMask11G(frequency):
    MaskName = 'OIF LV11G'
    mask_label = 'LV-OIF-11GSR'
    mlabel = mask_label
    mask_ui = [[0.0,0.385,1.0,0.385,1.0,0.41,0.0,0.41,0.0,0.385],
                [0.15,0.0,0.4,-0.18,0.6,-0.18,0.85,0.0,0.6,0.18,0.4,0.18,0.15,0.0],
                [0.0,-0.385,1.0,-0.385,1.0,-0.41,0.0,-0.41,0.0,-0.385]]  
    
    data_rate = frequency*1e9
    #data_rate = float(data_rate)
    
    ui_sec = 1/data_rate
    d_rate = data_rate/1e9      #convert to Gbs
    mask = ':MASK:USER:WIDTH ' + str(ui_sec) + ';\n:MASK:USER:LAB "' + mlabel + str(d_rate) + "Gb" + '";\n'       
    
    mask = mask + ':MASK:USER:SEG1:POINTS '        
    for i in range(len(mask_ui[0])-1):
        if i - (2*(i/2)) == 0:
            point = mask_ui[0][i]*ui_sec - (ui_sec/2)
        else:
            point = mask_ui[0][i]
        mask = mask + str(point) + ","
        
    mask = mask + str(mask_ui[0][i+1]) + ";\n"
    
    mask = mask + ':MASK:USER:SEG2:POINTS '
    for i in range(len(mask_ui[1])-1):
        if i - (2*(i/2)) == 0:
            point = mask_ui[1][i]*ui_sec - (ui_sec/2)
        else:
            point = mask_ui[1][i]
        mask = mask + str(point) + ","
    mask =mask + str(mask_ui[1][i+1]) + ";\n"
    
    mask = mask + ':MASK:USER:SEG3:POINTS '
    for i in range(len(mask_ui[2])-1):
        if i - (2*(i/2)) == 0:
            point = mask_ui[2][i]*ui_sec - (ui_sec/2)
        else:
            point = mask_ui[2][i]
        mask = mask + str(point) + ","
    mask =mask + str(mask_ui[2][i+1]) + ";\n"  
    text = mask    
   
    strlen = str(len(text))
    strcount = str(len(strlen))
    text = "#" +strcount + strlen + text    
    
    fpath = "C:\\TekApplications\\DPOJET\\Masks\\JESD204B\\Temp\\"
    fname = "temp.msk" 
    scope1.write(':FILES:WRITEF "' + fpath + fname +'", ' + text)
    
def JESD204BMask11GRx(frequency):
    MaskName = 'OIF LV11G'
    mask_label = 'LV-OIF-11GSR'
    mlabel = mask_label
    mask_ui = [[0.0,0.525,1.0,0.525,1.0,0.55,0.0,0.55,0.0,0.525],
                [0.35,0,0.5,-0.055,0.65,0,0.5,0.055,0.35,0],
                [0.0,-0.525,1.0,-0.525,1.0,-0.55,0.0,-0.55,0.0,-0.525]] 
    
    data_rate = frequency*1e9
    #data_rate = float(data_rate)
    
    ui_sec = 1/data_rate
    d_rate = data_rate/1e9      #convert to Gbs
    mask = ':MASK:USER:WIDTH ' + str(ui_sec) + ';\n:MASK:USER:LAB "' + mlabel + str(d_rate) + "Gb" + '";\n'       
    
    mask = mask + ':MASK:USER:SEG1:POINTS '        
    for i in range(len(mask_ui[0])-1):
        if i - (2*(i/2)) == 0:
            point = mask_ui[0][i]*ui_sec - (ui_sec/2)
        else:
            point = mask_ui[0][i]
        mask = mask + str(point) + ","
        
    mask = mask + str(mask_ui[0][i+1]) + ";\n"
    
    mask = mask + ':MASK:USER:SEG2:POINTS '
    for i in range(len(mask_ui[1])-1):
        if i - (2*(i/2)) == 0:
            point = mask_ui[1][i]*ui_sec - (ui_sec/2)
        else:
            point = mask_ui[1][i]
        mask = mask + str(point) + ","
    mask =mask + str(mask_ui[1][i+1]) + ";\n"
    
    mask = mask + ':MASK:USER:SEG3:POINTS '
    for i in range(len(mask_ui[2])-1):
        if i - (2*(i/2)) == 0:
            point = mask_ui[2][i]*ui_sec - (ui_sec/2)
        else:
            point = mask_ui[2][i]
        mask = mask + str(point) + ","
    mask =mask + str(mask_ui[2][i+1]) + ";\n"  
    text = mask    
   
    strlen = str(len(text))
    strcount = str(len(strlen))
    text = "#" +strcount + strlen + text    
    
    fpath = "C:\\TekApplications\\DPOJET\\Masks\\JESD204B\\Temp\\"
    fname = "temp.msk" 
    scope1.write(':FILES:WRITEF "' + fpath + fname +'", ' + text)
    
def JESD204BMask6G(frequency): 
    MaskName = 'OIF LV6G'
    mask_label = ('LV-OIF-6G-SR')
    mlabel = mask_label
    mask_ui =[[0.0,0.375,1.0,0.375,1.0,0.40,0.0,0.40,0.0,0.375],
                [0.15,0,0.4,-0.2,0.6,-0.2,0.85,0,0.6,0.2,0.4,0.2,0.15,0.0],
                [0.0,-0.375,1.0,-0.375,1.0,-0.40,0.0,-0.40,0.0,-0.375]]
                    
    data_rate = frequency*1e9
    #data_rate = float(data_rate)
    
    ui_sec = 1/data_rate
    d_rate = data_rate/1e9      #convert to Gbs
    mask = ':MASK:USER:WIDTH ' + str(ui_sec) + ';\n:MASK:USER:LAB "' + mlabel + str(d_rate) + "Gb" + '";\n'       
    
    mask = mask + ':MASK:USER:SEG1:POINTS '        
    for i in range(len(mask_ui[0])-1):
        if i - (2*(i/2)) == 0:
            point = mask_ui[0][i]*ui_sec - (ui_sec/2)
        else:
            point = mask_ui[0][i]
        mask = mask + str(point) + ","
        
    mask = mask + str(mask_ui[0][i+1]) + ";\n"
    
    mask = mask + ':MASK:USER:SEG2:POINTS '
    for i in range(len(mask_ui[1])-1):
        if i - (2*(i/2)) == 0:
            point = mask_ui[1][i]*ui_sec - (ui_sec/2)
        else:
            point = mask_ui[1][i]
        mask = mask + str(point) + ","
    mask =mask + str(mask_ui[1][i+1]) + ";\n"
    
    mask = mask + ':MASK:USER:SEG3:POINTS '
    for i in range(len(mask_ui[2])-1):
        if i - (2*(i/2)) == 0:
            point = mask_ui[2][i]*ui_sec - (ui_sec/2)
        else:
            point = mask_ui[2][i]
        mask = mask + str(point) + ","
    mask =mask + str(mask_ui[2][i+1]) + ";\n"  
    text = mask    
   
    strlen = str(len(text))
    strcount = str(len(strlen))
    text = "#" +strcount + strlen + text    
    
    fpath = "C:\\TekApplications\\DPOJET\\Masks\\JESD204B\\Temp\\"
    fname = "temp.msk" 
    scope1.write(':FILES:WRITEF "' + fpath + fname +'", ' + text)
    
def JESD204BMask6GRx(frequency): 
    MaskName = 'OIF LV6G'
    mask_label = ('LV-OIF-6G-SR')
    mlabel = mask_label
    mask_ui =[[0.0,0.375,1.0,0.375,1.0,0.40,0.0,0.40,0.0,0.375],
                [0.30,0,0.5,-0.0625,0.7,0,0.5,0.0625,0.3,0],
                [0.0,-0.375,1.0,-0.375,1.0,-0.40,0.0,-0.40,0.0,-0.375]]
                    
    data_rate = frequency*1e9
    #data_rate = float(data_rate)
    
    ui_sec = 1/data_rate
    d_rate = data_rate/1e9      #convert to Gbs
    mask = ':MASK:USER:WIDTH ' + str(ui_sec) + ';\n:MASK:USER:LAB "' + mlabel + str(d_rate) + "Gb" + '";\n'       
    
    mask = mask + ':MASK:USER:SEG1:POINTS '        
    for i in range(len(mask_ui[0])-1):
        if i - (2*(i/2)) == 0:
            point = mask_ui[0][i]*ui_sec - (ui_sec/2)
        else:
            point = mask_ui[0][i]
        mask = mask + str(point) + ","
        
    mask = mask + str(mask_ui[0][i+1]) + ";\n"
    
    mask = mask + ':MASK:USER:SEG2:POINTS '
    for i in range(len(mask_ui[1])-1):
        if i - (2*(i/2)) == 0:
            point = mask_ui[1][i]*ui_sec - (ui_sec/2)
        else:
            point = mask_ui[1][i]
        mask = mask + str(point) + ","
    mask =mask + str(mask_ui[1][i+1]) + ";\n"
    
    mask = mask + ':MASK:USER:SEG3:POINTS '
    for i in range(len(mask_ui[2])-1):
        if i - (2*(i/2)) == 0:
            point = mask_ui[2][i]*ui_sec - (ui_sec/2)
        else:
            point = mask_ui[2][i]
        mask = mask + str(point) + ","
    mask =mask + str(mask_ui[2][i+1]) + ";\n"  
    text = mask    
   
    strlen = str(len(text))
    strcount = str(len(strlen))
    text = "#" +strcount + strlen + text    
    
    fpath = "C:\\TekApplications\\DPOJET\\Masks\\JESD204B\\Temp\\"
    fname = "temp.msk" 
    scope1.write(':FILES:WRITEF "' + fpath + fname +'", ' + text)
    
