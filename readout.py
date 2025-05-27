import serial
import time
import numpy as np
import os

PORT = "COM5"  # Replace with your port

NUM_MEASUREMENTS = 100  # Number of measurements to take
EXTREME_ANGLE = 45
NUM_STOPS = 10  # Number of steps to take in each direction
Orientation = 180 # Orientation of the sunsensor on the mount

with serial.Serial(PORT, 1000000) as ser:
    ser.write(b"move:0\n")
    print("Input file name or press enter to use timestamped file")
    fname = input()
    if fname == "":
        print("Using timestamped file")
        fname = time.strftime("%Y%m%d-%H%M%S") + ".txt"
    else:
        print("Using provided file name:", fname)
    if not os.path.exists("data"):
        os.mkdir("data")
    with open("data/"+ fname, "w") as f:
        f.write(f"time, stepper position, q1, q2, q3, q4, sum, tanA, tanB, A, B, orientation={Orientation}\n")
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
                line = ser.readline().decode().strip()
                f.write(line + "\n")
        ser.write(b"move:0\n")