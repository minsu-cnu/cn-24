import subprocess
import re
import time
import matplotlib.pyplot as plt

x_data, y_data = [], []
count = 1
PORT = '5201'

while count <= 15:
    result = subprocess.run(['ss', '-i', 'sport', '=', PORT], capture_output=True, text=True)
    cwnd = None

    match = re.search(r'cwnd:(\d+)', result.stdout)
    if match:
        cwnd = int(match.group(1))
    
    x_data.append(count)
    y_data.append(cwnd if cwnd is not None else 0)
    
    count += 1
    time.sleep(1)

plt.plot(x_data, y_data)
plt.xlabel('time (s)')
plt.ylabel('cwnd')
plt.title('measure cwnd')

plt.savefig('measure_cwnd_result.png')
plt.show()