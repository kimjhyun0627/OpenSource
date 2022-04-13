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

print(dic)
