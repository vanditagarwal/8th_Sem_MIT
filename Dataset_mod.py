'''F = open("adult.txt", "r")
F1 = open("Adult_Large_Final.txt", "w")
db = {}

for row in range(0,32561):
    temp = F.readline().split(", ")
    if "?" in temp:
        continue
    else:
        #if "\n" in temp:
        temp[len(temp)-1] = temp[len(temp)-1][0:len(temp[len(temp)-1])-1]
        temp.remove(temp[0])
        temp.remove(temp[1])
        temp.remove(temp[2])
        temp.remove(temp[7])
        temp.remove(temp[7])
        temp.remove(temp[7])
        temp.append('\n')
        F1.write("\t".join(temp))
        temp.remove("\n")
        db[row] = temp
        
F.close()
F1.close()

for row in db:
    print row, db[row]
'''

'''F = open("Adult_Small_Final.txt", "r")

for row in range(0,15056):
    temp = F.readline().split("\t")
    c = 0
    for item in temp:
        if item == "Male" or item == "Female":
            c += 1
    if c > 1:
        print row
F.close()'''

F = open("Adult_Small_Final.txt","r")
c = 0
for row in range(0,1000):
    temp = F.readline().split("\t")
    if ((set(["Black"])<set(temp)) or (set(["Asian-Pac-Islander"])<set(temp)) or (set(["American-Indian_Eskimo"])<set(temp)) or (set(["Other"])<set(temp))) and (set(["Never-married"])<set(temp)) and (set([">50K"])<set(temp)):
        print row
        c += 1
print c
F.close()
