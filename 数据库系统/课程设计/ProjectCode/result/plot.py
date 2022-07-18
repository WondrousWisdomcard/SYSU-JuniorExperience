import matplotlib.pyplot as plt
import pandas as pd

plt.figure('threadNum')
df = pd.read_csv("./result_threadNum.csv", sep=' ')
x = df.threadNum
par = df.partime
plt.title('Figure about parallel runtime and number of threads')
plt.plot(x, par, 'g*-')
plt.xlabel('thread number')
plt.ylabel('run time/sec')
plt.grid()
plt.savefig('./threadNum.jpg')

plt.figure('bufferSize')
df = pd.read_csv("./result_bufferSize.csv", sep=' ')
x = df.bufferSize
ser = df.sertime
par = df.partime
plt.title('Figure about runtime and size of memory buffer')
plt.plot(x, ser, 'g*-',color='blue', label='serial')
plt.plot(x, par, 'g*-',color='red', label='parallel')
plt.xlabel('buffer size')
plt.ylabel('run time/sec')
plt.legend()
plt.grid()
plt.savefig('./bufferSize.jpg')

plt.figure('entryNum1')
df = pd.read_csv("./result_entryNum.csv", sep=' ')
x = df.entryNum[:3]
ser = df.sertime[:3]
par = df.partime[:3]
plt.title('Figure about runtime and entry number')
plt.plot(x, ser, 'g*-',color='blue', label='serial')
plt.plot(x, par, 'g*-',color='red', label='parallel')
plt.xlabel('entry number')
plt.ylabel('run time/sec')
plt.legend()
plt.grid()
plt.savefig('./entryNum1.jpg')


plt.figure('entryNum2')
df = pd.read_csv("./result_entryNum.csv", sep=' ')
x = df.entryNum
ser = df.sertime
par = df.partime
plt.title('Figure about runtime and entry number')
plt.plot(x, ser, 'g*-',color='blue', label='serial')
plt.plot(x, par, 'g*-',color='red', label='parallel')
plt.xlabel('entry number')
plt.ylabel('run time/sec')
plt.legend()
plt.grid()
plt.savefig('./entryNum2.jpg')

plt.show()


