import sys

filepath = sys.argv[1]
num = sys.argv[2]

f = open(filepath, "r")
lines = f.readlines()
lines = list(map(lambda s: s.strip(), lines))

for line in lines:
    print(line)

print(num)
