import subprocess
import re
import time
import matplotlib.pyplot as plt

x_data, y_data = [], []
start_time = time.time()
PORT = '5201'

while time.time() - start_time <= 15:
    result = subprocess.run(['ss', '-i', 'sport', '=', PORT], capture_output=True, text=True)
    cwnd = None

    match = re.search(r'cwnd:(\d+)', result.stdout)
    if match:
        cwnd = int(match.group(1))
    
    x_data.append(time.time() - start_time)
    y_data.append(cwnd if cwnd is not None else 0)
    
    time.sleep(0.3)

plt.plot(x_data, y_data)
plt.xlabel('time (s)')
plt.ylabel('cwnd')
plt.title('measure cwnd')

plt.savefig('measure_cwnd_result.png')
plt.show()