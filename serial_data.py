import serial, sys, time, os
# read the serial data, write to file or smth
cfd = os.path.dirname(__file__)
data_path = os.path.join(cfd, 'data')

def readSerial(comport, baudrate, timeA):
    t = time.time()
    ser = serial.Serial(comport, baudrate, timeout=0.1)         # 1/timeout is the frequency at which the port is read

    Q1 = []
    Q2 = []
    Q3 = []
    Q4 = []
    sa = []
    sb = []

    while True:
        data = ser.readline().decode().strip()
        if data:
            print(data)
            # extract quadrant bits and angles

        elapsed = time.time() - t
        if elapsed > timeA:
            break



if __name__ == '__main__':
    sysArgs = sys.argv[1:]
    tAllowed = int(sysArgs[0])
    if tAllowed > 100 or tAllowed == None:
        sysArgs = 10
    readSerial('COM3', 128000, tAllowed)