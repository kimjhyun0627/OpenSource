import sys
import re
import operator

filepath = sys.argv[1]
num = int(sys.argv[2])
dic = {}

with open(filepath, "r") as file:
    input = file.readlines()

for ii in input:
    ii = re.sub("[-+=!@#$:;%^&*_\"~`,.?/]", " ", ii)
    words = ii.split()
    for jj in words:
        dic[jj] = dic.get(jj, 0) + 1

dic = sorted(dic.items(), key=operator.itemgetter(1))

for ii in range(len(dic) - 1, -1, -1):
    if dic[ii][1] <= num:
        break
    print("%-10s %5s" % (dic[ii][0], dic[ii][1]))