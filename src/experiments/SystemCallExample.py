#
#This program is doing a systemcall. After the system call it writes
#the output to a file and counts the number of lines
#

import os

#Variables
command = 'ipconfig'
filename = 'SystemCallExample.txt'
# totallines is the amount of lines in the filename

#Program
def main():
    systemcall()
    
def systemcall():
    readit = os.popen(command, 'r')
    now = readit.read()
    f = open(filename, 'w')
    f.write(now)
    f.close()
    f = open(filename, 'r')
    totallines = 0
    for line in f.readlines():
        f.readline
        totallines += 1
    f.close()
    output(now, totallines)
    
def output(now, totallines):
    print(now)
    print(' The number of lines in the','\n','SystemCallExample.txt file is',\
          totallines)
main()
