# hp3478a calibration ram utilities

### Usage
Read calibration data from hp3478a and write to file:
```
py hp3478a_cal_ram_util.py <gpib_address> <output_file_name>
```

Validate calibration data from file:
```
py hp3478a_cal_ram_util.py -v <calibration_data_file_name>
```

### Sample validation output:
```
----------------------------------------------------------------------------------------------------------------
byteidx|     raw     |offset|gain |chk| chksum validation |result|offset_const|gain_constant|range
----------------------------------------------------------------------------------------------------------------
  1: 13|@@@AGEBCDBANF|000175|23421|E6 |  25 +  230 =   255|Pass  |         175|     1.023421|30 mV DC
 14: 26|@@@@DABCB@@OC|000041|23200|F3 |  12 +  243 =   255|Pass  |          41|     1.023200|300 mV DC
 27: 39|@@@@@CBCNBNMI|000003|23E2E|D9 |  38 +  217 =   255|Pass  |           3|     1.022818|3 V DC
 40: 52|IIIIIGBCDNNJF|999997|234EE|A6 |  89 +  166 =   255|Pass  |          -3|     1.023378|30 V DC
 53: 65|@@@@@@BC@OANJ|000000|230F1|EA |  21 +  234 =   255|Pass  |           0|     1.022991|300 V DC
 66: 78|@@@@@@@@@@@OO|000000|00000|FF |   0 +  255 =   255|Pass  |           0|     1.000000|Not used
 79: 91|@@A@@HBAOB@NB|001008|21F20|E2 |  29 +  226 =   255|Pass  |        1008|     1.020920|All AC Volts ranges
 92:104|IIIHIH@ECCOKA|999898|0533F|B1 |  78 +  177 =   255|Pass  |        -102|     1.005329|30 Ω 2W,4W
105:117|IIIIHI@EA@MKG|999989|0510D|B7 |  72 +  183 =   255|Pass  |         -11|     1.005097|300 Ω 2W,4W
118:130|IIIIIH@EMCNJG|999998|05D3E|A7 |  88 +  167 =   255|Pass  |          -2|     1.004728|3 KΩ 2W,4W
131:143|IIIIIH@E@CEKM|999998|05035|BD |  66 +  189 =   255|Pass  |          -2|     1.005035|30 KΩ 2W,4W
144:156|IIIIII@EO@EK@|999999|05F05|B0 |  79 +  176 =   255|Pass  |          -1|     1.004905|300 KΩ 2W,4W
157:169|IIIIII@ENCDJO|999999|05E34|AF |  80 +  175 =   255|Pass  |          -1|     1.004834|3 MΩ 2W,4W
170:182|IIIIIH@EBOEJO|999998|052F5|AF |  80 +  175 =   255|Pass  |          -2|     1.005195|30 MΩ 2W,4W
183:195|@@@@@DCEMNOLI|000004|35DEF|C9 |  54 +  201 =   255|Pass  |           4|     1.034679|300 mA DC
196:208|@@@@@ACDCLENC|000001|343C5|E3 |  28 +  227 =   255|Pass  |           1|     1.034265|3 A DC
209:221|@@@@@@@@@@@OO|000000|00000|FF |   0 +  255 =   255|Pass  |           0|     1.000000|Not used
222:234|@@@HHACBE@BNB|000881|32502|E2 |  29 +  226 =   255|Pass  |         881|     1.032502|300 mA and 3 A AC
235:247|@@@@@@@@@@@OO|000000|00000|FF |   0 +  255 =   255|Pass  |           0|     1.000000|Not used
----------------------------------------------------------------------------------------------------------------
```

### Sample [file](https://github.com/vinayshanbhag/hp3478a/blob/main/hp3478a_2619A46970_cal_data_dump.bin) with calibration ram data 
```
@              : byte index 0: 0x40 Calibration switch off | 0x40 Calibration switch on
@@@AGEBCDBANF  : 1:13        : 30 mV DC
@@@@DABCB@@OC  : 14:26       : 300 mV DC
@@@@@CBCNBNMI  : 27:39       : 3 V DC
IIIIIGBCDNNJF  : 40:52       : 30 V DC
@@@@@@BC@OANJ  : 53:65       : 300 V DC
@@@@@@@@@@@OO  : 66:78       : Not used
@@A@@HBAOB@NB  : 79:91       : All AC Volts ranges
IIIHIH@ECCOKA  : 92:104      : 30 Ω 2W,4W
IIIIHI@EA@MKG  : 105:117     : 300 Ω 2W,4W
IIIIIH@EMCNJG  : 118:130     : 3 KΩ 2W,4W
IIIIIH@E@CEKM  : 131:143     : 30 KΩ 2W,4W
IIIIII@EO@EK@  : 144:156     : 300 KΩ 2W,4W
IIIIII@ENCDJO  : 157:169     : 3 MΩ 2W,4W
IIIIIH@EBOEJO  : 170:182     : 30 MΩ 2W,4W
@@@@@DCEMNOLI  : 183:195     : 300 mA DC
@@@@@ACDCLENC  : 196:208     : 3 A DC
@@@@@@@@@@@OO  : 209:221     : Not used
@@@HHACBE@BNB  : 222:234     : 300 mA and 3 A AC
@@@@@@@@@@@OO  : 235:247     : Not used
@@@@@@@@       : 248:255     : padding 
```

### Checksum validation

```
raw bytes from calibration entry :    @    @    @    A    G    E    B    C    D    B    A    N    F
in hex                           : 0x40 0x40 0x40 0x41 0x47 0x45 0x42 0x43 0x44 0x42 0x41 0x4e 0x46
lower nibbles in hex (&0x0F)     :    0    0    0    1    7    5    2    3    4    2    1    E    6
in decimal                       :    0    0    0    1    7    5    2    3    4    2    1   14    6
sum digits                       :    ^-------------------------------------------------^           = 25
check digits                     :                                                          ^-----^ = 14*16 + 6 = 230
sum (should add up to 255)       :                                                                  = 255 (valid)

```

### Prerequisites

Requires [pyvisa](https://pyvisa.readthedocs.io/en/latest/introduction/getting.html) and [drivers](https://www.ni.com/en/support/downloads/drivers/download.ni-488-2.html#484357) for National Instruments GPIB-USB-HS controller.

### Hardware setup

Multiple instruments can be daisy-chained with standard gpib cables. Single gpib-usb-hs interface can work with multiple devices.

<img src='https://docs-be.ni.com/bundle/gpib-usb-getting-started/page/GUID-3A7DE663-6ABE-4A40-ADFB-23E069EBA6F5-a5.svg?_LANG=enus' width='500px'/>

Tested with National Instruments NI GPIB-USB-HS controller IEEE 488 on <strong>Windows</strong> only. 

### HP3478A program codes

![image](https://github.com/vinayshanbhag/hp3478a/assets/5519039/654d088f-2da0-4233-8a05-1eb07b88a76e)

