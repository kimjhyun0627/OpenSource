
list1 = input("input the 1st list : ")
list1 = list(list1.split())

list2 = input("input the 2st list : ")
list2 = list(list2.split())

listUnion = list1 + list2
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
