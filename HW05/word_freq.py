import sys
import re
import operator

filepath = sys.argv[1]
num = sys.argv[2]
dic = {}

with open(filepath, "r") as file:
    lines = file.readlines()

for ii in lines:
    ii=re.sub("[-+=!@#$%^&*\"~`,.?/]"," ",ii)
    words = ii.split()
    for cnt in words:
        dic[cnt] = dic.get(cnt,0)+1

dic = sorted(dic.items(), key=operator.itemgetter(1))

for i in range(dic.count(), num):
    print("%10s %-5s"%(dic[i][0],dic[i][1]))
