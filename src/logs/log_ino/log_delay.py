import serial
import matplotlib.pyplot as plt
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

# Open the serial port
ser = serial.Serial('COM7', 115200)

# Initialize the delay list
delays = []

# Read data from the serial port
while 0:
    try:
        # Read a line of data
        line = ser.readline().decode().strip()
        print(line)
        # Check if the line contains the delay value
        if line.startswith("final Adelay"):
            delay = float(line.split(":")[-1].strip())
            delays.append(delay)

            # Print and store the delay value
            # print("Delay: ", delay)

            # Store the delay value in a text file
            with open(f"{THIS_FOLDER}/delays_81.txt", "a") as f:
                f.write(str(delay) + "\n")

    except KeyboardInterrupt:
        # Stop reading data if the user presses Ctrl+C
        f.close()
        break

# Close the serial port
ser.close()


import numpy as np
delays = np.genfromtxt(f"{THIS_FOLDER}/delays_83.txt", delimiter=',')
print(np.mean(delays))
# Plot the delays
plt.plot(delays)
plt.title("Antenna Delays")
plt.xlabel("Iter")
plt.ylabel("Delays")
plt.show()
