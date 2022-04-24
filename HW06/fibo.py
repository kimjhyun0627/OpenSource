num = int(input("fibonacci number: "))

fiboList = [0 for i in range(num + 1)]
fiboList[0] = 0
fiboList[1] = 1
for i in range(2, num + 1):
    if i == 0:
        print('0')
    elif i == 1:
        print('1')
    else:
        fiboList[i] = fiboList[i - 1] + fiboList[i - 2]

i = 1;
while (i <= num):
    print(fiboList[i], end=" ")
    i += 1

print("\nF" + str(num) + " = " + str(fiboList[i - 1]))
