import subprocess
import re
import time
import matplotlib.pyplot as plt

x_data, y_data = [], []
start_time = time.time()
PORT = '5201'
ss_results = []

while time.time() - start_time <= 15:
    result = subprocess.run(['ss', '-i', 'sport', '=', PORT], capture_output=True, text=True)
    ss_results.append(result.stdout)
    x_data.append(time.time() - start_time)

    time.sleep(0.1)

client_port = input("Input target port number: ").strip()

for ss_result in ss_results:
    target_idx = ss_result.find(']:' + client_port)
    cwnd = None

    match = re.search(r'cwnd:(\d+)', ss_result[target_idx:])
    if match:
        cwnd = int(match.group(1))
    
    y_data.append(cwnd if cwnd is not None else 0)

plt.plot(x_data, y_data)
plt.xlabel('time (s)')
plt.ylabel('cwnd')
plt.title('measure cwnd')

plt.savefig('measure_cwnd_result.png')
plt.show()