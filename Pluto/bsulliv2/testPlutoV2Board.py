# EEPROM IDs
PLUTO_BOARD_V0_ID = ""
PLUTO_BOARD_V1_ID = ""
PLUTO_BOARD_V2_ID = "0000000000000123"

# Install with: python -m pip install XXX
# python -m pip uninstall pythonnet
# Had to clean out the clr.pyd files and the Python.Runtime.dll files in the Python27 folder
# python -m pip install pythonnet --upgrade

from PlutoV2 import PlutoV2

# DEVICE CS LINES
AMP_1_CS = "A"
AMP_2_CS = "B"	

dutDevice = PlutoV2() # 100kHz SPI, 16 bit R/W (8 bit addr, 8 bit data)

dutDevice.connect(PLUTO_BOARD_V2_ID)


#dutDevice.Set_Amp_Trim(SPI_sel = AMP_1_CS, AmpTrimCode = 10, readDataBackFirst = False) # Remove the readDataBackFrist param before testing with real board

# Amp enable one of {1,0}
#dutDevice.Set_Amp_Enable(SPI_sel = AMP_1_CS, AmpEnable = 1, readDataBackFirst = False) # Remove the readDataBackFrist param before testing with real board

# Power mode one of {"Lo", "Hi"}
#dutDevice.Set_Amp_Pwr_Mod(SPI_sel = AMP_1_CS, PowerMode = "Hi", readDataBackFirst = False) # Remove the readDataBackFrist param before testing with real board

# Gain one of {"12dB", "20dB"}
#dutDevice.Set_Amp_Gain(SPI_sel = AMP_1_CS, GainValue = "20dB", readDataBackFirst = False) # Remove the readDataBackFrist param before testing with real board

# Atten = Attenuation in dB (between 0 and 0.9 dB)
#dutDevice.Set_Amp_Atten(SPI_sel = AMP_1_CS, AmpAtten = 0.9, readDataBackFirst = False) # Remove the readDataBackFrist param before testing with real board

# powerStr = {"ON", "OFF"}
dutDevice.set_amp1_power_state("ON")

dutDevice.set_amp2_power_state("ON")