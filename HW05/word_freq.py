import sys
import re
import operator

filepath = sys.argv[1]
num = int(sys.argv[2])
dic = {}

with open(filepath, "r") as file:
    lines = file.readlines()

for ii in lines:
    ii = re.sub("[-+=!@#$:;%^&*\"~`,.?/]", " ", ii)
    words = ii.split()
    for cnt in words:
        dic[cnt] = dic.get(cnt, 0) + 1

dic = sorted(dic.items(), key=operator.itemgetter(1))

print(dic)
for ii in range(len(dic) - 1, -1, -1):
    if (dic[ii][1] <= num):
        break
    print("%-10s %5s" % (dic[ii][0], dic[ii][1]))
