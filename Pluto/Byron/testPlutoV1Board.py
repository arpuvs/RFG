# Install with: python -m pip install XXX
# python -m pip uninstall pythonnet
# Had to clean out the clr.pyd files and the Python.Runtime.dll files in the Python27 folder
# python -m pip install pythonnet --upgrade

from PlutoV1 import PlutoV1

# DEVICE CS LINES
AMP_1_CS = "A"
AMP_2_CS = "B"	

dutDevice = PlutoV1() # 100kHz SPI, 16 bit R/W (8 bit addr, 8 bit data)
dutDevice.connect(DUT1_Default = 0x00, DUT2_Default = 0x00) # Used same ID. Change later

# No readback on these parts so have to either write 16 bits to verify what was put in or keep track
# Currently choose the keep track method. Defaults can be set above in the connect method

# AmpEnable one of {0, 1}
dutDevice.Set_Amp_Enable(SPI_sel = AMP_1_CS, AmpEnable = 1)
#dutDevice.Set_Amp_Enable(SPI_sel = AMP_2_CS, AmpEnable = 1)

#dutDevice.Write16BitData([0xfe])
#dutDevice.Write8BitData([0xfe])

# Atten = Attenuation in dB (between 0 and 0.9 dB)
dutDevice.Set_Amp_Atten(SPI_sel = AMP_1_CS, AmpAtten = 0)