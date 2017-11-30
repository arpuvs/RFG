import sys, visa, time
# sys.path.append('../../Common/FMB_USB_Python_Files')
sys.path.append('../../Common')
# # C:\Git_Repositories\RFG\Common\FMB_USB_Python_Files
# from ADI_GPIB.AgilentN5181A import *
from ADI_GPIB.AgilentN9030A import *
from ADI_GPIB.WatlowF4 import *
# # from ADI_GPIB.AgilentN6705B import *
# from FMB import *
#

# import atexit
#
# def exit_handler():
#     print 'Handler run'
#
# atexit.register(exit_handler)

# asdfsadf asdfasd

# fmbDict = {1: "2.5 MHz", 2: "5 MHz", 3: "33 MHz", 4: "78 MHz",
#           5: "120 MHz", 6: "225.3 MHz", 7: "350.3 MHz", 8: "500 MHz",
#           9: "800.3 MHz", 10: "1 GHz", 11: "1.5 GHz", 12: "2 GHz",
#           13: "2.5 GHz", 14: "3 GHz", 15: "3.5 GHz", 16: "4 GHz",
#           17: "4.5 GHz", 18: "5 GHz", 19: "5.5 GHz", 20: "5.9 GHz",
#           21: "Aux"}
#
# Filter = FMB('COM3', fmbDict)
# Source2 = AgilentN5181A(11)
# Analyzer = AgilentN9030A(18)
#
# # # Filter.select_filter(3)
# # print Filter.get_filter_center_freq_hz(19)
#
# # Filter box test
# for i in range(1, 21):
#     # Filter.select_filter(i)
#     # Source2.__SetFreq__
#     val = fmbDict[i].split()
#     if val[1] == 'MHz': val = float(val[0]) * 1e6
#     elif val[1] == 'GHz': val = float(val[0]) * 1e9
#     print val
#     Source2.__SetFreq__(val)
#     Analyzer.__Setfc__(val)
#     Filter.select_filter(i)
#     Analyzer.__SetMarkerFreq__(1, val)
#     time.sleep(0.5)
#     carrierMag = float(Analyzer.__GetMarkerAmp__(1))

# Want -2dBm out of part

# Supply = AgilentN6705B(26)
# Source1 = AgilentN5181A(20)
# Source2 = AgilentN5181A(11)
# Analyzer = AgilentN9030A(18)
Oven = WatlowF4(4)
# #
#
print Oven.__GetTemp__()
print Oven.__GetSP__()

# print Analyzer.__ClearAverage__()
# print Analyzer.__SetAverage__(50)
# print time.sleep(1)
# print Analyzer.__CheckStatus__(600)

# print Analyzer.__Align__()
# print Analyzer.__CheckStatus__(600)
# print Analyzer.__CheckStatus__(30)
# Analyzer.__Align__()
# print Analyzer.__CheckStatus__(300)


# date = time.ctime(time.time())
# date = date.replace(':', '.')
# fh = open('Intermod_Dist_' + date + '.csv', 'w')
#
# # Source1.__SetState__(1)
# # Source2.__SetState__(1)
# # print Source1.__GetState__()
# # print Source2.__GetState__()
# # time.sleep(0.5)
# # Source1.__SetState__(0)
# # Source2.__SetState__(0)
# # print Source1.__GetState__()
# # print Source2.__GetState__()
#
# # Analyzer.__StoreState__('BS_Test_State')
# # time.sleep(1)
# # Analyzer.__LoadState__('BS_Test_State')
# # Source1.__SetFreq__(3.999e9)
# # Source2.__SetFreq__(4.001)
# # print Source1.__GetFreq__()
#
# # print Analyzer.__Setfc__(4.03e9)
# # Analyzer.__SetMarkerFreq__(1, 4.003e9)
# # print Analyzer.__GetMarkerAmp__(1)
# # Analyzer.__MarkerMax__(1)
# # print Analyzer.__GetSpan__()
# # print Analyzer.__SetSpan__(10e9)
# # print Analyzer.__Setfc__(4.03e9)
# # Analyzer.__LoadState__('BS_Test_State')
#
# # Analyzer.__LoadState__('BS_Test_State')
#
# freqlist = [100e6, 250e6, 500e6, 1e9, 4e9]
# lowerPeak = []
# higherPeak = []
#
# Analyzer.__SetSpan__(10e3)
# for i in range(11):
#     for freq in freqlist:
#         Source1.__SetFreq__(freq-1e6)
#         Source2.__SetFreq__(freq+1e6)
#         Analyzer.__Setfc__(freq-3e6)
#         Analyzer.__SetMarkerFreq__(1, freq-3e6)
#         time.sleep(1)
#         lowerPeak.append(float(Analyzer.__GetMarkerAmp__(1)))
#         Analyzer.__Setfc__(freq+3e6)
#         Analyzer.__SetMarkerFreq__(1, freq+3e6)
#         time.sleep(1)
#         higherPeak.append(float(Analyzer.__GetMarkerAmp__(1)))
#
#
#     fh.write('Test %d' % i)
#     fh.write('\n')
#     fh.write(str(freqlist).strip('[]'))
#     fh.write('\n')
#     fh.write(str(lowerPeak).strip('[]'))
#     fh.write('\n')
#     fh.write(str(higherPeak).strip('[]'))
# Analyzer.__SetAverage__(100e3)
# print Analyzer.__GetAverage__()
# print Analyzer.__GetAverage__()
# print Analyzer.__GetAverage__()
# print Analyzer.__GetAverage__()
# Analyzer.__ClearAverage__()
# for Temp in range(65496, 65496 + 100):
# print Oven.__SetTemp__(25)
# print Oven.__GetTemp__()
# Supply.__Enable__(0, 1)
# print Supply.__SetI__(0.04, (1, 2))
# print Supply.__SetV__(0, 1)
#
# print 1
# print 2
# raise Exception ('Blah')
# print 3

# print Supply.__GetI__(1)
