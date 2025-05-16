import serial, sys, time, os
import numpy as np
# read the serial data, write to file or smth
cfd = os.path.dirname(__file__)
data_path = os.path.join(cfd, 'data')

def readSerial(comport, baudrate, timeA):
    t = time.time()
    #ser = serial.Serial(comport, baudrate, timeout=0.1)         # 1/timeout is the frequency at which the port is read

    Q1 = []
    Q2 = []
    Q3 = []
    Q4 = []
    sa = []
    sb = []

    while True:
        #data = ser.readline().decode().strip()
        data = "A0,11 0.00 \n A1,7 0.00 \n A2,25 0.00 \n A3,1, 0.00 \n Sunangle alpha, -37.33 \n Sunangle beta, -16.96"
        if data:
            # extract quadrant bits and angles
            lines = data.strip().split('\n')
            #shape is a0-a1-a2-a3-alpha-beta
            numbers = []
            # Process each line
            for line in lines:
                # Replace any remaining commas with spaces and split by space
                parts = line.replace(',', ' ').split()
                for part in parts:
                    try:
                        # Try to convert to float
                        num = float(part)
                        numbers.append(num)
                    except ValueError:
                        # Ignore non-numeric parts (e.g., 'A3', 'Sunangle', 'alpha')
                        continue
            Q1.append(numbers[0])
            Q2.append(numbers[2])
            Q3.append(numbers[4])
            Q4.append(numbers[6])
            sa.append(numbers[8])
            sb.append(numbers[9])



        elapsed = time.time() - t
        if elapsed > timeA:
            quadrants = np.array([Q1,Q2,Q3,Q4])
            angles = np.array([sa,sb])
            np.savetxt(os.path.join(data_path, 'quadrants.csv'), quadrants, delimiter='\n', header = "Q1,Q2,Q3,Q4")
            np.savetxt(os.path.join(data_path, 'angles.csv'), angles, delimiter='\n', header = "sa, sb")
            print(Q1, Q2, Q3, Q4, sa, sb)
            break



if __name__ == '__main__':
    sysArgs = sys.argv[1:]
    tAllowed = int(sysArgs[0])
    if tAllowed > 100 or tAllowed == None:
        sysArgs = 10
    readSerial('COM3', 128000, tAllowed)