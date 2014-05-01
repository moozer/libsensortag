import os
readit = os.popen('ifconfig', 'r')
now = readit.read()
f = open('output.txt', 'w')
f.write(now)
f.close()
f = open('output.txt', 'r')
totallines = 0
for line in f.readlines():
    f.readline
    totallines += 1
f.close()
print(now)
print(totallines)
