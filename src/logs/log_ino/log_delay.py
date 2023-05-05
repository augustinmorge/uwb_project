import serial
import matplotlib.pyplot as plt
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

# Initialize the delay list
delays = []

# Read data from the serial port
i = 0
while 1:
    if i == 0 : ser = serial.Serial('COM8', 115200); i+=1
    try:
        line = ser.readline().decode().strip()
        print(line)
        # Check if the line contains the delay value
        if line.startswith("final Adelay"):
            delay = float(line.split(":")[-1].strip())
            delays.append(delay)

            # Print and store the delay value
            # print("Delay: ", delay)

            # Store the delay value in a text file
            with open(f"{THIS_FOLDER}/delays_82_M100HB2.txt", "a") as f:
                f.write(str(delay) + "\n")
                f.flush()

    except KeyboardInterrupt:
        # Stop reading data if the user presses Ctrl+C
        f.close()
        # Close the serial port
        ser.close()
        break




import numpy as np
delays = np.genfromtxt(f"{THIS_FOLDER}/delays_83_M100HB.txt", delimiter=',')


# Plot the delays
plt.plot(delays)
# mask = np.abs(delays - np.mean(delays)) > np.std(delays)
# delays = delays[~mask]
print(f"mean without outlayers : {np.mean(delays)}")
plt.plot([np.mean(delays) for _ in range(delays.shape[0])],label=f"mean : {np.mean(delays)}")
plt.plot([np.mean(delays) + np.std(delays) for _ in range(delays.shape[0])], label = f"mean + std : {np.mean(delays) + np.std(delays)}")
plt.plot([np.mean(delays) - np.std(delays) for _ in range(delays.shape[0])], label = f"mean - std : {np.mean(delays) - np.std(delays)}")
# plt.title("Antenna Delays with 5V battery")
plt.title("Antenna Delays with max 4.2V battery")
plt.xlabel("Iter")
plt.ylabel("Delays")
plt.legend()
plt.show()
