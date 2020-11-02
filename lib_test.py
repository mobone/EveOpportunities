
from ctypes import *
import ctypes
asset_lib = cdll.LoadLibrary("./go-evepraisal-master/parsers/assets.so")
fitting_lib = cdll.LoadLibrary("./go-evepraisal-master/parsers/fitting.so")

asset_lib.ParseAssetsTest.restype = ctypes.c_char_p
fitting_lib.ParseFittingTest.restype = ctypes.c_char_p

input_string = '''
Isogen	14,517	Mineral			145.17 m3	580,970.34 ISK
Bistot	11,155	Bistot			178,480 m3	48,965,876.45 ISK
Nocxium	8,095	Mineral			80.95 m3	8,894,866.95 ISK
'''

result = str( asset_lib.ParseAssetsTest(input_string))
for i in result.split('\n'):
    print(i)

print('-----')
input_string = '''
[Ishtar, Ishtar Tharde *]
Power Diagnostic System II
Drone Damage Amplifier II
Drone Damage Amplifier II
Drone Damage Amplifier II
Drone Damage Amplifier II
Assault Damage Control II

Compact Multispectrum Shield Hardener
Large Shield Extender II
100MN Y-S8 Compact Afterburner
Compact EM Shield Amplifier

Drone Link Augmentor II

Medium Drone Speed Augmentor I
Medium Drone Speed Augmentor II

Acolyte II x9
Imperial Navy Praetor x5
Infiltrator II x8
'''
input_string = input_string.replace("[","").replace("]","")
import re
input_string = re.sub(r',[a-zA-Z*0-9 ]*', '', input_string)

result = str( fitting_lib.ParseFittingTest(input_string))
for i in result.split('\n'):
    print(i)
print('-----')
