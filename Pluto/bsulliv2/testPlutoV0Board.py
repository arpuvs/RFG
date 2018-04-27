# Install with: python -m pip install XXX
# python -m pip uninstall pythonnet
# Had to clean out the clr.pyd files and the Python.Runtime.dll files in the Python27 folder
# python -m pip install pythonnet --upgrade

from PlutoV0 import PlutoV0

# DEVICE CS LINES
AMP_1_CS = "A"
AMP_2_CS = "B"	

dutDevice = PlutoV0() # 100kHz SPI, 16 bit R/W (8 bit addr, 8 bit data)

dutDevice.connect(DUT1_Default = 0x00, DUT2_Default = 0x00) # Used same ID. Change later

# No readback on these parts so have to either write 16 bits to verify what was put in or keep track
# Currently choose the keep track method. Defaults can be set above in the connect method

# Gain one of {"12dB", "20dB"}
dutDevice.Set_Amp_Gain(SPI_sel = AMP_1_CS, GainValue = "12dB")

# Coupling is one of {"ON", "OFF"}
dutDevice.Set_Amp_Coupling(SPI_sel = AMP_1_CS, Coupling = 'ON')

# Power mode one of {"Lo", "Hi"}
dutDevice.Set_Amp_Pwr_Mod(SPI_sel = AMP_1_CS, PowerMode = "Hi") 

# AmpEnable one of {0, 1}
dutDevice.Set_Amp_Enable(SPI_sel = AMP_1_CS, AmpEnable = 1)
#dutDevice.Set_Amp_Enable(SPI_sel = AMP_2_CS, AmpEnable = 1)

# Trim = 0 to 15
dutDevice.Set_Amp_Trim(SPI_sel = AMP_1_CS, AmpTrimCode = 15)
