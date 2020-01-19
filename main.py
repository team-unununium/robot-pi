import serial

# Delayed due to technical difficulties with the Raspberry Pi
def main():
    ser = serial.Serial('/dev/ttyACM0', 9600)
    s = []
    temp_s = []
    while True:
        byte_object = []

        read_serial = ser.readline()
        s.append(read_serial)
        print(s)

        if len(s) > 10:
            temp_s = s[-10:]
            if all(current_s == 0 for current_s in temp_s):
                # Get byte object
                byte_object = s[:-10]
                s = []

        if len(byte_object) > 0:
            # Translate byte object
            if len(byte_object) == 4:
                pass
            elif len(byte_object) == 8:
                pass
            try: 
                # Byte object is string
                tr_string = byte_object.decode()
            except (UnicodeDecodeError, AttributeError):
                # Not String
                pass
                
if __name__ == "__main__":
    main()