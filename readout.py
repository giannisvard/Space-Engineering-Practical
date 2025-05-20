import serial
import time
import numpy as np

PORT = "COM9"  # Replace with your port

NUM_MEASUREMENTS = 10  # Number of measurements to take
EXTREME_ANGLE = 60 
NUM_STOPS = 10  # Number of steps to take in each direction

with serial.Serial(PORT, 1000000) as ser:
    ser.write(b"rst\n")
    print("Input file name or press enter to use timestamped file")
    fname = input()
    if fname == "":
        print("Using timestamped file")
        fname = time.strftime("%Y%m%d-%H%M%S") + ".txt"
    else:
        print("Using provided file name:", fname)
    with open("data/"+ fname, "w") as f:
        for i in np.linspace(-EXTREME_ANGLE, EXTREME_ANGLE, NUM_STOPS*2+1):
            ser.read_all()
            w = f"move:{int(i*16/0.9)}\n".encode()
            ser.write(w)
            ser.flush()
            print("Moving to:", i)
            while True:
                line = ser.readline()
                if line.decode().startswith("Movement completed"):
                    print("Movement completed")
                    break
            for j in range(NUM_MEASUREMENTS):
                line = ser.readline()
                f.write(line.decode().strip()+"\n")
        ser.write(b"rst\n")