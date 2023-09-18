import sys
import pyvisa

# Calibration range names
cal_entries=['30 mV DC','300 mV DC','3 V DC','30 V DC','300 V DC','Not used','All AC Volts ranges','30 Ω 2W,4W','300 Ω 2W,4W','3 KΩ 2W,4W','30 KΩ 2W,4W','300 KΩ 2W,4W','3 MΩ 2W,4W','30 MΩ 2W,4W','300 mA DC','3 A DC','Not used','300 mA and 3 A AC','Not used']

def get_offset_const(s):
    """ 
        get_offset_const: returns an offset constant (int) from input string s. 
        e.g. 
            first 6 bytes of a calibration entry:    @    @    @    A    G    E
            the same in hex                     : 0x40 0x40 0x40 0x41 0x47 0x45
            lower nibbles after anding with 0x0F:    0    0    0    1    7    5
            input string s is                   : '000175'
            return value is 175 
    """
    if int(s)>900000:
        return (int(s)-1_000_000)
    else:
        return int(s)

def get_gain_const(s):
    """
        get_gain_const: returns a gain constant from hex string s.
        e.g.
            bytes 7-11 of a calibration entry    :    B    C    D    B    A
            the same in hex                      : 0x42 0x43 0x44 0x42 0x41
            lower nibbles after anding with 0x0F :    2    3    4    2    1
            input string s is                    : '23421'
            return value is 1.023421 
    """
    gain_digits = [int(i,16) if int(i,16)<8 else int(i,16)-16 for i in s]
    result = 1
    for idx,digit in enumerate(gain_digits):
        #print(idx, digit, digit/(10*10**(idx+1)))
        result += digit/(10*10**(idx+1))
    return round(result,6)

def validate(calib, print_result=True):
    """
       validate: takes entire 256 bytes of calibration data (calib) and validates checksum for each calibration entry.
       print detailed result if print_result==True[default]
       returns True only if all checksums are valid
       e.g.
           raw bytes from calibration entry :    @    @    @    A    G    E    B    C    D    B    A    N    F
           in hex                           : 0x40 0x40 0x40 0x41 0x47 0x45 0x42 0x43 0x44 0x42 0x41 0x4e 0x46
           lower nibbles in hex (&0x0F)     :    0    0    0    1    7    5    2    3    4    2    1    E    6
           in decimal                       :    0    0    0    1    7    5    2    3    4    2    1   14    6
           sum digits                       :    ^-------------------------------------------------^           = 25
           check digits                     :                                                          ^-----^ = 14*16 + 6 = 230
           sum (should add up to 255)       :                                                                  = 255 (valid)
    """
    r = [hex(i&0x0F).split('x')[1].upper() for i in calib] # get all lower nibbles in hex format
    i = 1 # Start from 2nd byte (index 1), since 1st byte is used to flag if calbration switch is enabled (0x41) or not (0x40)
    idx=0 # index for displaying calibration entry names
    result=[] # checksum validation results for each calibration entry

    hdr = "byteidx|     raw     |offset|gain |chk| chksum validation |result|offset_const|gain_constant|range              "
    if print_result:print(f"\nCalibration mode is {'off' if int(r[0])==0 else 'on'}\n")
    if print_result:print("-"*len(hdr));print(hdr);print("-"*len(hdr))
    
    while (i<248):
        if print_result:print(f"{i:3d}:{i+12:3d}|{(calib[i:i+13]).decode()}|{''.join(r[i:i+6]).upper()}|{''.join(r[i+6:i+11]).upper()}|{''.join(r[i+11:i+13]).upper():3s}", end="")
        val = sum([int(i,16) for i in r[i:i+11]])
        crc = int(''.join(r[i+11:i+13]),16)
        if print_result:print(f"|{val:4d} + {crc:4d} = {val+crc:5d}|{'Pass' if (val+crc)==255 else 'Fail':6s}|{get_offset_const(''.join(r[i:i+6]).upper()):12d}|{get_gain_const(''.join(r[i+6:i+11]).upper()):13.6f}|{cal_entries[idx]}")
        result.append((val+crc)==255)
        i+=13
        idx+=1
    if print_result: print("-"*len(hdr))
    return all(result)    

def get_cal_ram_contents(instr)->bytearray:
    """
       get_cal_ram_contents: connect to hp3478a dmm at gpib address (instr)
       and retrieve 256 bytes of calibration ram data returned as a bytearray
    """
    rm = pyvisa.ResourceManager()
    try:
        dvm = rm.open_resource(instr)
        dvm.query('F1')
    except:
        print(f"Failed to open device at {instr}")
        exit()

    result = bytearray()
    for addr in range(256):
        dvm.write_raw(bytes([ord('W'), addr]))
        val = dvm.read_raw()
        result.append(ord(val))
    dvm.close()
    rm.close()
    return result

def main():
    args = sys.argv[1:]
    if len(args) !=2:
        print("Usage: ")
        print("\nRead calibration data from hp3478a and write to file:")
        print(f"{sys.argv[0]} <gpib_address> <output_file_name>")
        print("\nValidate calibration data from file:")
        print(f"{sys.argv[0]} -v <calibration_data_file_name>")
        exit()

    if args[0] == '-v': # verify cal ram data
        fname = args[1]
        result = bytearray()
        try:
            with open(fname,'rb') as f:
                result = f.read()
        except:
            print(f"Failed to read file {fname}")
        validate(bytes(result))
    else: # retrieve cal ram data
        instr_addr = args[0]
        fname = args[1]

        result = get_cal_ram_contents(instr_addr)

        try:
            with open(fname,'xb') as f:
                f.write(bytes(result))
        except:
            print(f"Failed to write to file {fname}")
            
        print('\n--- cal data ---')
        for i,b in enumerate(bytes(result)):
            if i>0 and i%16==0: print()
            print(chr(b),end='')
        print('\n----------------\n')    
        validate(bytes(result))
    

if __name__ == "__main__":
    main()
    

