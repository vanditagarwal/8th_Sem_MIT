from operator import attrgetter     #for sorting
import itertools                    #for forming all possible combinations of values from multiple lists

#--------------------------------------------
#Alpha-Protection Algorithm 2
#--------------------------------------------
def alpha_protection(i, node):
    print "alpha: ", node.name
    l = i
    PD_groups = []
    Il = []     #I_l
    for attr in node.attributes:
        for item in attr_val[attr][node.height]:
                Il.append([item])

    for k in Il:
        count = 0
        for row in db:
            if set([item.name for item in k]) < set(db[row]):
                count += 1
        k.append(count)

    if node.height > 0:
        for k in Il:
            k[len(k)-1] = node.freq

    print "Il: ", Il

    Il1 = []    #I_l_1
    for k in Il:
        for j in classifier:
            Il1.append([k[0],j])

    for R in Il1:       #computing frequency of R
        count = 0
        for row in db:
            if (set([item.name for item in R]) < set(db[row])) == True:
                count += 1
        R.append(count)

    for R in Il1:       #step 4
        X = []      #computing X
        for item in R:
            if item != yes and item != no:
                X.append(item)
        X = [X[i] for i in range(len(X)-1)]

        count = 0
        for row in db:  #computing frequency of X
            if (set([item.name for item in X]) < set(db[row])) == True:
                count += 1
        X.append(count)
        print "X: ", [item for item in X]

        a1 = R[len(R)-1]    #a1
        n1 = X[len(X)-1]    #n1

        A = []              #computing A
        for item in X:
            if (type(item) is not int) and set(item.attributes) <= set(da):
                A.append(item)

        T = []              #computing T
        for item in R:
            if (type(item) is not int) and (item not in A):
                T.append(item)

        a2 = 0
        for row in db:          #computing a2
            flag = 1
            for item in A:      #checking for not A
                if item.name in db[row]:
                    flag = 0
                    break
            for item in T:      #checking for union T
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
                
        if node == any_sex:
            a1,a2 = a2,a1
            n1,n2 = n2,n1
        print "Values: ", a1, n1, a2, n2
                
        PD_groups.append([R,a1,n1,a2,n2])

    return measure_disc(alpha,ms,f,PD_groups)



#--------------------------------------------
#Algorithm 3
#--------------------------------------------
def measure_disc(alpha,ms,f,PD_groups):
    
    if f == 'slift' or f == 'olift':
        for group in PD_groups:     #step 2(1)
            if f == 'slift':        #calculating whether alpha-discriminatory or nto
                ratio = (float(group[1])/float(group[2]))/(float(group[3])/float(group[4]))
            else:
                p1 = float(group[1])/float(group[2])
                p2 = float(group[3])/float(group[4])
                ratio = (p1*(1-p2))/(p2*(1-p1))

            if group[1] >= ms and ratio > alpha:    #step 2
                return 'case1'
        return 'case2'

    if f == 'elift' or f == 'clift':    #step8
        for group in PD_groups:         #step9(1)
            if f == 'elift':
                print "group: ", group
                ratio = (float(group[1])/float(group[2]))/(float(group[1]+group[3])/float(group[2]+group[4]))
            else:
                ratio = 1234

            if group[1] >= ms and ratio > alpha:    #step9(2)
                return 'case1'          #step 10

        for group in PD_groups:     #step 11(1)
            if f == 'elift':
                ratio = 5678
            else:
                ratio = (group[1]/group[2])/((group[1]+group[3])/(group[2]+group[4]))

            if group[1] < ms and ratio > alpha:     #step 11
                return 'case2'

        if f == 'clift':    #step13(1)
            for group in PD_groups:
                if group[1] < ms and False:  #handle case of confidence as in step 13 (3)
                    return 'case2'
                else:
                    return 'case3'
             
    
    
            
                
            


#--------------------------------------------
#Algorithm 1
#--------------------------------------------
F = open("Dummy Dataset.txt","r")   #opening the dummy database
db = {}

#creating QI
qi = {
    0: "sex",
    1: "race",
    2: "hours"
    }

#Initially taknig DA = {Sex}
#Creating DA = QI. This means that t=|QI|
da = ["sex"]
#da = qi

'''#Class item
classifier = {
    4: "Credit"
    }'''

class Nodes:
    freq = 0                    #to compute and store the frequency of the node
    def __init__(self, name, E, height, attributes):
        self.name = name
        self.private = False    #whether node is k-anonymous or not
        self.prot = False       #whether node is alpha-protective or not
        self.E = E
        self.pointing_to = []   #to store what all nodes it points to;
                                #to show direct generalizations of this node
        self.height = height    #height in the generalization graph
                                #if height=0, then it is a root node
        self.attributes = attributes    #attributes in node in ith iteration
        self.values = []        #values of different attributes in the node specially in case of multi-attribute nodes

yes = Nodes("Yes",[],-1,["class"])     #for classifier
no = Nodes("No",[],-1,["class"])
yes.freq = 6
no.freq = 4
classifier = [yes,no]


male = Nodes("Male",[],0,["sex"])
female = Nodes("Female",[],0,["sex"])
any_sex = Nodes("Any_sex",[male,female],1,["sex"])

male.pointing_to.append(any_sex)
female.pointing_to.append(any_sex)
male.values.append(male)
female.values.append(female)
any_sex.values.append(any_sex)


white = Nodes("White",[],0,["race"])
black = Nodes("Black",[],0,["race"])
asian = Nodes("Asian",[],0,["race"])
american = Nodes("American",[],0,["race"])
white1 = Nodes("White1",[white],1,["race"])
colored = Nodes("Colored",[black,asian,american],1,["race"])
any_race = Nodes("Any_Race",[white,colored],2,["race"])

white.pointing_to.append(white1)
black.pointing_to.append(colored)
asian.pointing_to.append(colored)
american.pointing_to.append(colored)
white1.pointing_to.append(any_race)
colored.pointing_to.append(any_race)
white.values.append(white)
black.values.append(black)
asian.values.append(asian)
american.values.append(american)
white1.values.append(white1)
colored.values.append(colored)
any_race.values.append(any_race)


n1 = Nodes("35",[],0,["hours"])
n2 = Nodes("37",[],0,["hours"])
n3 = Nodes("40",[],0,["hours"])
n4 = Nodes("50",[],0,["hours"])
n5 = Nodes("1 to 39",[n1,n2],1,["hours"])
n6 = Nodes("40 to 99",[n3,n4],1,["hours"])
n7 = Nodes("Any_hours",[n5,n6],2,["hours"])

n1.pointing_to.append(n5)
n2.pointing_to.append(n5)
n3.pointing_to.append(n6)
n4.pointing_to.append(n6)
n5.pointing_to.append(n7)
n6.pointing_to.append(n7)
n1.values.append(n1)
n2.values.append(n2)
n3.values.append(n3)
n4.values.append(n4)
n5.values.append(n5)
n6.values.append(n6)
n7.values.append(n7)

#A dictionary for attributes and corresponding possible values
#This can be used to compute frequency set etc
attr_val = {
    "Sex": [[male,female],[any_sex]],
    "Race": [[white, black, asian, american],[white1,colored],[any_race]],
    "Hours": [[n1,n2,n3,n4],[n5,n6],[n7]]
    }


#creating Domi
dom = {
    0: [[male,female],[any_sex]],
    1: [[white,black,asian,american],[white1,colored],[any_race]],
    2: [[n1,n2,n3,n4],[n5,n6],[n7]]
    }

print "Dom:",
for i in dom:
    print
    for j in dom[i]:
        for items in j:
            print items.name,

print
print

#other parameters
alpha = 1.2 
k = 3
ms = 3  #min support
t = 1   #t is tau       change it to 3 later on
f = 'elift'     #discrimination parameter

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
print db
print

#-------------------------------------------------

#C = nodes in the domain generalization hierarchies of attributes in QI
#C1 means it contains 1-attribute subsets of attributes in QI
#Cn means it contains n-attribute subsets of attributes in QI
C = [
        [],     #C1
        [],     #C2 (remove later on)
        []      #C3 (remove later on)
    ]        
for i in dom:
    for j in dom[i]:
        for item in j:
            C[0].append(item)

print "C: "
print " ".join(item.name for item in C[0])

Cpd = []            #step 2
"""for item in C[0]:
    if item.attributes in da:
        Cpd.append(item)"""

#Hard-coding values of Cpd
Cpd = [male, female, any_sex]

queue = []  #step 4
n = 3
roots = []
S = []
freq_set = []
freq_count = []
anonymity = {           #To define the k-anonymity status of DB wrt attribute
    "sex": False,       #of the node
    "race": False,
    "hours": False
    }

for i in range(n):      #step 5
    print "\ni: ", i

    freq_set = []
    freq_count = []
    
    S.append(list())
    for item in C[i]:
        S[i].append(item)         #step 7

    roots = []
    for item in C[i]:
        if len(item.E)==0:      #ie. there is no edge Ei directed to them
            roots.append(item)

    for item in roots:          #step 9
        queue.append(item)

    queue = sorted(queue, key=attrgetter('height'))   #sorting values in queue by height

    while len(queue)>0:     #step 10
        node = queue[0]
        del(queue[0])       #step 11
        print
        print "node: ", node.name
        print "Private: ", node.private
        queue = sorted(queue, key=attrgetter('height'))
        print "Queue: "
        for item in queue:
            print item.name,

        #see if this is required later on
        '''for item in node.E:     #computing freq of the node in case its not a root
            node.freq += item.freq
        print "Frequency: ", node.freq'''

        if node.private==False or (node.private==False and node.prot==False):    #step 12
            '''if len(node.E)==0:            #step 13 to check if it is root
                for j in db:        #computing frequency of the node for 1-attribute
                    if node.name in db[j]:
                        node.freq += 1
                        
                for attr in node.attributes:    #computing the frequency set
                    freq_set[0][attr] = {}
                    for item in attr_val[attr][0]:
                        freq_set[0][attr][item.name] = 0
                        
                for attr in node.attributes:
                    for item in attr_val[attr][0]:
                        for j in db:
                            if item.name in db[j]:
                                freq_set[0][attr][item.name] += 1
                print "Freq set: ", freq_set

                for attr in node.attributes:
                
            else:                       #if node is not a root node, step 15
                for item in node.E:
                    node.freq += item.freq      #frequency of the node if its not a root

                if len(freq_set)-1 != node.height:
                    freq_set.append({})
                    
                for attr in node.attributes:
                    print freq_set
                    freq_set[node.height][attr] = {}
                    for item in attr_val[attr][node.height]:
                        freq_set[node.height][attr][item.name] = 0

                for attr in node.attributes:
                    for item in attr_val[attr][node.height]:
                        freq_set[node.height][attr][item.name] = node.freq
                    

            print "Frequency: ", node.freq'''

            anonymous = True    #checking if DB is k-anonymous wrt attributes of the node
            for attr in node.attributes:
                for item in freq_set[node.height][attr]:
                    if freq_set[node.height][attr][item] < k:
                        anonymous = False
                        break
            if anonymous == True:   #if DB is k-anonymous step 19
                for attr in node.attributes:
                    anonymity[attr] = True      #not required
                    node.private = True
                    print 'Private: ', node.private
                    
            if anonymous == True:   #if DB is k-anonymous step 19
                for item in node.pointing_to:
                    item.private = True         #marking all direct generalization
                                                #as k-anonymous
                flag = 0
                for N in Cpd:       #step 21(1)
                    if N in node.values:
                        flag = 1
                        break
                
                if flag == 1 and i <= t:    #step 21
                    if node.height == 0:
                        MR = alpha_protection(i,node)   #step 23
                    else:
                        MR = alpha_protection(i,node)  #step 25

                    if MR == 'case3':
                        #marking all direct generalizations of node that
                        #contain the generalization of N as k-anonymous
                        #and alpha-protective
                        for item in node.pointing_to:
                            print "Test: ", N.name
                            item.private = True
                            item.prot = True
                    elif MR == 'case1':         #step 30
                        for item in S[i]:
                            if node==item:      #delete node from Si step 31
                                S[i].remove(item)
                        for item in node.pointing_to:
                            if item not in queue:
                                queue.append(item)  #insert direct gen into queue
                        queue = sorted(queue, key=attrgetter('height'))   #sorting by height
            
            else:       #step 31-32     step 35
                for item in S[i]:
                    if node==item:      #delete node from Si step 31
                        S[i].remove(item)
                for item in node.pointing_to:
                    if item not in queue:
                        queue.append(item)  #insert direct gen into queue
                queue = sorted(queue, key=attrgetter('height'))   #sorting by height

        elif node.private == True:      #step 21-36     step 38
            flag = 0
            for N in Cpd:       #step 21(1)
                if N in node.values:
                    flag = 1
                    break

            if flag == 1 and i <= t:    #step 21
                if node.height == 0:
                    MR = alpha_protection(i,node)   #step 23
                else:
                    MR = alpha_protection(i,node)  #step 25

                if MR == 'case3':
                    #marking all direct generalizations of node that
                    #contain the generalization of N as k-anonymous
                    #and alpha-protective
                    for item in node.pointing_to:
                        item.private = True
                        item.prot = True
                elif MR == 'case1':         #step 30
                    for item in S[i]:
                        if node==item:      #delete node from Si step 31
                            S[i].remove(item)
                    for item in node.pointing_to:
                        queue.append(item)  #insert direct gen into queue
                    queue = sorted(queue, key=attrgetter('height'))   #sorting by height
            
            else:
                for item in S[i]:
                    if node==item:      #delete node from Si step 31
                        S[i].remove(item)
                for item in node.pointing_to:
                    queue.append(item)  #insert direct gen into queue
                queue = sorted(queue, key=attrgetter('height'))   #sorting by height

    for j in range(len(S)):
        print [item.name for item in S[j]]
    #Ci+1, Ei+1 = GraphGeneration(Si,Ei)
