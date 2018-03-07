import sys, visa, time, smtplib, os
from openpyxl import *

# sys.path.append('../../Common/FMB_USB_Python_Files')
sys.path.append('../../Common')
sys.path.append('C:\\Users\\bsulliv2\\Documents\\Results\\Pronghorn\\Data\\IMD\\IMD3')
# print sys.path
# import fileinput
# test = fileinput.input('C:\\Users\\bsulliv2\\Documents\\Results\\Pronghorn\\Data\\IMD\\IMD3')
# print test.filename()
# for line in fileinput.input('C:\\Users\\bsulliv2\\Documents\\Results\\Pronghorn\\Data\\IMD\\IMD3'):
    # process(line)
    # print line

outPath = 'C:\\Users\\bsulliv2\\Documents\\Results\\Pronghorn\\Data\\IMD\\IMDTest.xlsx'
path = 'C:\\Users\\bsulliv2\\Documents\\Results\\Pronghorn\\Data\\IMD\\IMD3'
files =  os.listdir(path)
wb = Workbook()
ws1 = wb.active
ws1.title = 'Sheet1'
sheet_ranges = wb['Sheet1']
writeline = ['Part', 'Temp', 'Vcom', 'Test', 'Freq', 'Value']
ws1.append(writeline)
for file in files:
    # print file
    fh = open(path + '\\' + file)
    linenum = 0
    data = []
    for line in fh:
        line = line.split(',')
        data.append(line)
        # print line
        linenum = linenum + 1

    ptNum = data[0][0]
    frequency = data[3]

    # # print ptNum
    # PwrMainHi25 = data[5]
    # PwrMainLo25 = data[6]
    # IM3HI25 = data[7]
    # IM3LO25 = data[8]
    # PwrMainIN25 = data[9]
    # OIP3LO25 = data[10]
    # OIP3HI25 = data[11]
    #
    # PwrMainHi40 = data[16]
    # PwrMainLo40 = data[17]
    # IM3HI40 = data[18]
    # IM3LO40 = data[19]
    # PwrMainIN40 = data[20]
    # OIP3LO40 = data[21]
    # OIP3HI40 = data[22]
    #
    # PwrMainHi125 = data[27]
    # PwrMainLo125 = data[28]
    # IM3HI125 = data[29]
    # IM3LO125 = data[30]
    # PwrMainIN125 = data[31]
    # OIP3LO125 = data[32]
    # OIP3HI125 = data[33]



    # data25 = data[5:12]
    # data40 = data[16:23]
    # data125 = data[27:34]
    for i in range(1, 33):
        if (i > 4) & (i < 12):
            for j in range(1, 11):
                writeline = []
                writeline.append(ptNum)
                writeline.append(data[1][0][7:])
                writeline.append(data[2][0][7:])
                writeline.append(data[i][0])
                writeline.append(frequency[j * 100])
                writeline.append(data[i][j * 100])
                ws1.append(writeline)
        elif (i > 15) & (i < 23):
            for j in range(1, 11):
                writeline = []
                writeline.append(ptNum)
                writeline.append(data[12][0][7:])
                writeline.append(data[13][0][7:])
                writeline.append(data[i][0])
                writeline.append(frequency[j * 100])
                writeline.append(data[i][j * 100])
                ws1.append(writeline)
        elif (i > 26) & (i < 34):
            for j in range(1, 11):
                writeline = []
                writeline.append(ptNum)
                writeline.append(data[23][0][7:])
                writeline.append(data[24][0][7:])
                writeline.append(data[i][0])
                writeline.append(frequency[j * 100])
                writeline.append(data[i][j * 100])
                ws1.append(writeline)
        else:
            continue


path = 'C:\\Users\\bsulliv2\\Documents\\Results\\Pronghorn\\Data\\IMD\\IMD23'
files = os.listdir(path)

for file in files:
    fh = open(path + '\\' + file)
    linenum = 0
    data = []
    for line in fh:
        line = line.split(',')
        data.append(line)
        linenum = linenum + 1

    ptNum = data[0][0]
    frequency = data[4]
    # print len(data)

    for i in range(1, 64):
        if (i > 4) & (i < 21):
            if (i == 12) | (i == 13):
                continue
            for j in range(1, 11):
                writeline = []
                writeline.append(ptNum)
                writeline.append(data[1][0][7:])
                writeline.append(data[3][0][7:])
                writeline.append(data[i][0])
                writeline.append(frequency[j * 100])
                # print writeline
                writeline.append(data[i][j * 100])
                ws1.append(writeline)
        elif (i > 25) & (i < 42):
            if (i == 33) | (i == 34):
                continue
            for j in range(1, 11):
                writeline = []
                writeline.append(ptNum)
                writeline.append(data[22][0][7:])
                writeline.append(data[24][0][7:])
                writeline.append(data[i][0])
                writeline.append(frequency[j * 100])
                writeline.append(data[i][j * 100])
                ws1.append(writeline)
        elif (i > 46) & (i < 63):
            if (i == 54) | (i == 55):
                continue
            for j in range(1, 11):
                writeline = []
                writeline.append(ptNum)
                writeline.append(data[43][0][7:])
                writeline.append(data[45][0][7:])
                writeline.append(data[i][0])
                writeline.append(frequency[j * 100])
                # print writeline
                writeline.append(data[i][j * 100])
                ws1.append(writeline)
        else:
            continue

path = 'C:\\Users\\bsulliv2\\Documents\\Results\\Pronghorn\\Data\\IMD\\IMD23Temp'
files = os.listdir(path)
tests = ['PwrMainHi', 'PwrMainLo', 'IM3HI', 'IM3LO', 'PwrMainIN', 'OIP3LO', 'OIP3HI']

for file in files:
    fh = open(path + '\\' + file)
    linenum = 0
    data = []
    for line in fh:
        line = line.split(',')
        data.append(line)
        linenum = linenum + 1

    ptNum = data[0][0]
    frequency = data[4]
    # print len(data)

    for i in range(1, 632):
        if data[i][0][:4] == 'Temp':
            temp = data[i][0][7:]
        elif data[i][0][:4] == 'Vcom':
            vcom = data[i][0][7:]
        elif data[i][0] in tests:
            for j in range(1, 11):
                writeline = []
                writeline.append(ptNum)
                writeline.append(temp)
                writeline.append(vcom)
                writeline.append(data[i][0])
                writeline.append(frequency[j * 100])
                # print writeline
                writeline.append(data[i][j * 100])
                ws1.append(writeline)




                        # for i in range(len(data25)-1):
# print data25[i+1]
# writeline.append(ptNum)
# writeline.append(25)
# writeline.append(data25[i+1])
# ws1.append(writeline)

# frequency = data[3]
# for i in range(1, 11):
#     print frequency[i*100]

wb.save(filename=outPath)

# print frequency
# print PwrMainHi25
# print PwrMainLo25
# for line in data25:
#     print line
# print data25