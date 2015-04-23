def measure_disc(alpha,ms,f,PD_groups):
    if f == 'slift' or f == 'olift':
        for group in PD_groups:
            if f == 'slift':
                ratio = (group[1]/group[2])/(group[3]/group[4])
            else:
                ratio = 1234
            print group









F = open("Dummy Dataset.txt","r")   #opening the dummy database
db = {}
f = 'slift'
alpha = 1.2
ms = 3

#Creating DB
for row in range(0,10):
    temp = F.readline().split("\t")
    temp.remove(temp[0])
    if "\n" in temp:
        temp.remove("\n")
    db[row] = temp
F.close()

print "DB: "
for row in db:
    print row, db[row]
print

print [db[ls] for ls in db]
print
print

da = ["Sex"]

class Nodes:
    def __init__(self,name,freq,attributes):
        self.name = name
        self.freq = freq
        self.attributes = attributes

male = Nodes('Male',6,["Sex"])
female = Nodes('Female',4,["Sex"])
l1 = [[male],[female]]

yes = Nodes('Yes',6,["Class"])
no = Nodes('No',4,["Class"])
l2 = [[yes],[no]]

IL = []
PD_groups = []

for i in l1:
    for j in l2:
       IL.append([i[0],j[0]])


for R in IL:
    count = 0
    for i in db:
        if (set([item.name for item in R]) < set(db[i])) == True:
            count += 1
    print count
    R.append(count)

for item in IL:
    print item

print
print

for i in IL:
    print
    for item in i:
        print item,

for R in IL:
    for item in R:
        if item == yes or item == no:
            C = item
            break

    X = []
    for item in R:
        if item != yes and item != no:
            X.append(item)
    X = [X[i] for i in range(len(X)-1)]
    
    count = 0
    for row in db:
        if (set([item.name for item in X]) < set(db[row])) == True:
            count += 1
    X.append(count)

    print
    print
    a1 = R[len(R)-1]
    n1 = X[len(X)-1]
    print a1
    print n1

    A = []
    for item in X:
        if (type(item) is not int) and set(item.attributes) <=set(da):
            A.append(item)

    T = []
    for item in R:
        if (type(item) is not int) and (item not in A):
            T.append(item)

    a2 = 0
    for row in db:
        flag = 1
        for item in A:
            if item.name in db[row]:
                flag = 0
                break
        for item in T:
            if item.name not in db[row]:
                flag = 0
                break
        if flag == 1:
            a2 += 1

    n2 = 0
    for row in db:
        flag = 1
        for item in A:
            if item.name in db[row]:
                flag = 0
                break
        for item in T:
            if item != yes and item != no:
                if item.name not in db[row]:
                    flag = 0
                    break
        if flag == 1:
            n2 += 1
    PD_groups.append([R,a1,n1,a2,n2])

    print measure_disc(alpha,ms,f,PD_groups)
