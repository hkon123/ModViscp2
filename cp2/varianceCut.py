import numpy as np
import matplotlib.pyplot as plt

filename = "50by50variance(10000sweeps).txt"

new = []

with open(filename, 'r') as f:
    for line in f:
        test = line.split(' ')
        del(test[-1])
        new.append(test)

f.close()

new = np.array(new).astype(float)
arr = np.zeros((50,50))
count=0
count2 = 0
for i in range(50):
    for j in range(50):
        arr[j,i] = new[i,j]

for i in range(50):
    print(str(count2) + ' ' + str(count) + ' ' + str(arr[i]))
    count += 0.02
    count2 += 1

count = 0
f = open("varianceCut.txt", 'w')
f.write("p1 variance\n")
for i in range(50):
    f.write(str(count) + ' ' + str(arr[25,i]) + '\n')
    count += 0.02
f.close()

plt.plot(np.arange(0,1,0.02), arr[25])
plt.savefig('varianceCut.png')
plt.show()
