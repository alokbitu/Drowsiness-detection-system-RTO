import time

import serial


comport = "COM3"
def ser_comm():
    ser1 = serial.Serial(port=comport, baudrate=9600, timeout=2)
    if not ser1.is_open:
        ser1.open()
        # print('serial Port1 Open for sending #01')

    ser1.flush()
    ser1.flushInput()
    ser1.flushOutput()

    ser1.write(b'relay2_on\n')
    response = ser1.readline().decode('ascii')
    print(response)
    time.sleep(2)

    ser1.write(b'relay2_off\n')
    response = ser1.readline().decode('ascii')
    print(response)
    time.sleep(2)

    ser1.flush()
    ser1.flushInput()
    ser1.flushOutput()
    ser1.close()


if __name__ == "__main__":
    ser_comm()