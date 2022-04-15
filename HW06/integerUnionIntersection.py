
listA = input("input the 1st list: ")
listA = list(listA.split())

listB = input("input the 2st list: ")
listB = list(listB.split())

listUnion = listA + listB
listUnion = list(map(int, listUnion))
listIntersection = []

for ii in range(0, len(listUnion) - 1):
    for jj in range(ii + 1, len(listUnion)):
        if listUnion[ii] == listUnion[jj]:
            listIntersection.append(listUnion[jj])

for ii in listIntersection:
    del listUnion[listUnion.index(ii)]

listUnion.sort()
listIntersection.sort()

print("union :", listUnion)
print("intersection :", listIntersection)
