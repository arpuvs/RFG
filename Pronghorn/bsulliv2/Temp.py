import sys, visa, time, smtplib, os
from openpyxl import *

def imdSift():
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

    # poi = ['\'3-6 ChA\'', '\'1-7 ChB\'', '\'3-9 ChB\'', '\'2-8 ChA\'', '\'3-9 ChA\'', '\'2-3 ChB\'']

    poi = ['\'1-9 ChA\'']

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
        if ptNum in poi:
            print ptNum, file, path
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
                writeline = []
                writeline.append(ptNum)
                writeline.append(data[12][0][7:])
                writeline.append(data[13][0][7:])
                writeline.append(data[i][0])
                writeline.append(frequency[ord('k')-ord('a')])
                writeline.append(data[i][ord('k')-ord('a')])
                ws1.append(writeline)
                writeline = []
                writeline.append(ptNum)
                writeline.append(data[12][0][7:])
                writeline.append(data[13][0][7:])
                writeline.append(data[i][0])
                writeline.append(frequency[ord('y') - ord('a') + 26])
                writeline.append(data[i][ord('y') - ord('a') + 26])
                ws1.append(writeline)
                writeline = []
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
                writeline = []
                writeline.append(ptNum)
                writeline.append(data[12][0][7:])
                writeline.append(data[13][0][7:])
                writeline.append(data[i][0])
                writeline.append(frequency[ord('k')-ord('a')])
                writeline.append(data[i][ord('k')-ord('a')])
                ws1.append(writeline)
                writeline = []
                writeline.append(ptNum)
                writeline.append(data[12][0][7:])
                writeline.append(data[13][0][7:])
                writeline.append(data[i][0])
                writeline.append(frequency[ord('y') - ord('a') + 26])
                writeline.append(data[i][ord('y') - ord('a') + 26])
                ws1.append(writeline)
                writeline = []
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
                writeline = []
                writeline.append(ptNum)
                writeline.append(data[23][0][7:])
                writeline.append(data[24][0][7:])
                writeline.append(data[i][0])
                writeline.append(frequency[ord('k')-ord('a')])
                writeline.append(data[i][ord('k')-ord('a')])
                ws1.append(writeline)
                writeline = []
                writeline.append(ptNum)
                writeline.append(data[23][0][7:])
                writeline.append(data[24][0][7:])
                writeline.append(data[i][0])
                writeline.append(frequency[ord('y') - ord('a') + 26])
                writeline.append(data[i][ord('y') - ord('a') + 26])
                ws1.append(writeline)
                writeline = []
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
        if ptNum in poi:
            print ptNum, file, path
        frequency = data[4]
        # print len(data)

        for i in range(1, 64):
            if (i > 4) & (i < 21):
                if (i == 12) | (i == 13):
                    continue
                writeline = []
                writeline.append(ptNum)
                writeline.append(data[1][0][7:])
                writeline.append(data[3][0][7:])
                writeline.append(data[i][0])
                writeline.append(frequency[ord('k')-ord('a')])
                writeline.append(data[i][ord('k')-ord('a')])
                ws1.append(writeline)
                writeline = []
                writeline.append(ptNum)
                writeline.append(data[1][0][7:])
                writeline.append(data[3][0][7:])
                writeline.append(data[i][0])
                writeline.append(frequency[ord('y') - ord('a') + 26])
                writeline.append(data[i][ord('y') - ord('a') + 26])
                ws1.append(writeline)
                writeline = []
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
                writeline = []
                writeline.append(ptNum)
                writeline.append(data[22][0][7:])
                writeline.append(data[24][0][7:])
                writeline.append(data[i][0])
                writeline.append(frequency[ord('k')-ord('a')])
                writeline.append(data[i][ord('k')-ord('a')])
                ws1.append(writeline)
                writeline = []
                writeline.append(ptNum)
                writeline.append(data[22][0][7:])
                writeline.append(data[24][0][7:])
                writeline.append(data[i][0])
                writeline.append(frequency[ord('y') - ord('a') + 26])
                writeline.append(data[i][ord('y') - ord('a') + 26])
                ws1.append(writeline)
                writeline = []
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
                writeline = []
                writeline.append(ptNum)
                writeline.append(data[43][0][7:])
                writeline.append(data[45][0][7:])
                writeline.append(data[i][0])
                writeline.append(frequency[ord('k')-ord('a')])
                writeline.append(data[i][ord('k')-ord('a')])
                ws1.append(writeline)
                writeline = []
                writeline.append(ptNum)
                writeline.append(data[43][0][7:])
                writeline.append(data[45][0][7:])
                writeline.append(data[i][0])
                writeline.append(frequency[ord('y') - ord('a') + 26])
                writeline.append(data[i][ord('y') - ord('a') + 26])
                ws1.append(writeline)
                writeline = []
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
        if ptNum in poi:
            print ptNum, file, path
        frequency = data[4]
        # print len(data)

        for i in range(1, 632):
            if data[i][0][:4] == 'Temp':
                temp = data[i][0][7:]
            elif data[i][0][:4] == 'Vcom':
                vcom = data[i][0][7:]
            elif data[i][0] in tests:
                writeline = []
                writeline.append(ptNum)
                writeline.append(temp)
                writeline.append(vcom)
                writeline.append(data[i][0])
                writeline.append(frequency[ord('k')-ord('a')])
                writeline.append(data[i][ord('k')-ord('a')])
                ws1.append(writeline)
                writeline = []
                writeline.append(ptNum)
                writeline.append(temp)
                writeline.append(vcom)
                writeline.append(data[i][0])
                writeline.append(frequency[ord('y') - ord('a') + 26])
                writeline.append(data[i][ord('y') - ord('a') + 26])
                ws1.append(writeline)
                writeline = []
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

def p1dBwrite(ws1, ptNum, temp, line, frequency, val):
    writeline = []
    writeline.append(ptNum)
    writeline.append(temp)
    writeline.append(line[0])
    writeline.append(float(frequency[val]))
    writeline.append(float(line[val]))
    ws1.append(writeline)

def p1dBsift():
    path = 'C:\\Users\\bsulliv2\\Documents\\Results\\Pronghorn\\Data\\P1dB\\3 Temps'
    outPath = 'C:\\Users\\bsulliv2\\Documents\\Results\\Pronghorn\\Data\\P1dB\\P1dBTest.xlsx'
    files = os.listdir(path)
    wb = Workbook()
    ws1 = wb.active
    ws1.title = 'Sheet1'
    sheet_ranges = wb['Sheet1']
    writeline = ['Part', 'Temp', 'Test', 'Freq', 'Value']
    ws1.append(writeline)
    for file in files:
        fh = open(path + '\\' + file)
        linenum = 0
        data = []
        for line in fh:
            line = line.split(',')
            data.append(line)
            linenum = linenum + 1

        ptNum = data[0][0]
        frequency = data[3]
        # print frequency
        for line in data:
            if line[0][:4] == 'Temp':
                temp = line[0][7:]
                # print temp
            elif line[0] == 'P1dB':
                # 1 GHz Steps
                p1dBwrite(ws1, ptNum, temp, line, frequency, 330)
                p1dBwrite(ws1, ptNum, temp, line, frequency, 564)
                p1dBwrite(ws1, ptNum, temp, line, frequency, 665)
                p1dBwrite(ws1, ptNum, temp, line, frequency, 766)
                p1dBwrite(ws1, ptNum, temp, line, frequency, 825)
                p1dBwrite(ws1, ptNum, temp, line, frequency, 865)
                p1dBwrite(ws1, ptNum, temp, line, frequency, 899)
                p1dBwrite(ws1, ptNum, temp, line, frequency, 926)
                p1dBwrite(ws1, ptNum, temp, line, frequency, 948)
                p1dBwrite(ws1, ptNum, temp, line, frequency, 967)
                p1dBwrite(ws1, ptNum, temp, line, frequency, 985)
                p1dBwrite(ws1, ptNum, temp, line, frequency, 1000)

                # 50Mhz Steps to 500
                p1dBwrite(ws1, ptNum, temp, line, frequency, 1)
                p1dBwrite(ws1, ptNum, temp, line, frequency, 228)
                # 100MHz above
                p1dBwrite(ws1, ptNum, temp, line, frequency, 388)
                p1dBwrite(ws1, ptNum, temp, line, frequency, 430)
                p1dBwrite(ws1, ptNum, temp, line, frequency, 463)
                p1dBwrite(ws1, ptNum, temp, line, frequency, 489)
                p1dBwrite(ws1, ptNum, temp, line, frequency, 512)
                p1dBwrite(ws1, ptNum, temp, line, frequency, 531)
                p1dBwrite(ws1, ptNum, temp, line, frequency, 548)
                # 500MHz above

    wb.save(filename=outPath)



if __name__ == '__main__':
    imdSift()
