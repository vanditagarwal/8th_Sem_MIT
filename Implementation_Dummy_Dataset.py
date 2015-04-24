from operator import attrgetter     #for sorting
import itertools                    #for forming all possible combinations of values from multiple lists
import copy                         #for deepcopy
import time

#--------------------------------------------
#Compute the frequency set
#--------------------------------------------
def compute_freq_set(combi,l):
    temp = []
    for item in combi:
        stack = []
        if item.height == 0:
            temp.append([item])
            continue
        else:
            stack.append(item)
            final = []
            while len(stack) > 0:
                node = stack[0]
                stack.remove(node)

                if node.height != 0:
                    for j in node.E:
                        stack.append(j)
                else:
                    final.append(node)
        temp.append(final)
    temp = list(itertools.product(*temp))
    '''print "\ntemp: ",
    for j in temp:
        print
        for item in j:
            print item.name'''

    for j in temp:
        for k in db:
            if (set([item.name for item in j]) < set(db[k])) == True:
                freq_count[l] += 1
    #print "freq_count: ", freq_count



#--------------------------------------------
#Alpha-Protection Algorithm 2
#--------------------------------------------
def alpha_protection(i, node):
    #print "alpha: ", node.name
    l = i
    PD_groups = []
    Il = []     #I_l

    for val in node.values:         #creating Il
        for attr in val.attributes:
            Il.append(attr_val[attr][val.height])
    Il = list(itertools.product(*Il))

    t = []          #itertools returns sth different from a list. So converting it back to a list so that append func can work on it
    for j in range(len(Il)):
        t.append([])
        for item in Il[j]:
            t[j].append(item)
    Il = t
    '''print "Test Il: ",
    for j in Il:
        print [item.name for item in j],'''
    
    for j in Il:    #caluclating the frequency of itemsets in Il
        final = []
        for k in range(len(j)):
            final.append([])
            stack = [j[k]]
            while len(stack) > 0:
                temp = stack[0]
                stack.remove(temp)
                if temp.height == 0:
                    final[k].append(temp)
                else:
                    for item in temp.E:
                        stack.append(item)
        #print "final1: ", final
        final = list(itertools.product(*final))
        #print "final2: ", final
        '''for k in final:
            for item in k:
                print item.name'''

        count = 0
        for k in final:
            for row in db:
                if set([item.name for item in k]) < set(db[row]):
                    count += 1
        j.append(count)
                
    print "\nIl: ",     #displaying Il with respective frequencies
    for j in t:
        for item in j:
            if type(item) == int:
                print item,
            else:
                print item.name,

    #computing I_l_1
    Il1 = []
    for val in node.values:
        for attr in val.attributes:
            Il1.append(attr_val[attr][val.height])
    Il1.append(attr_val["Classifier"])
    Il1 = list(itertools.product(*Il1))

    t = []          #itertools returns sth different from a list. So converting it back to a list so that append func can work on it
    for j in range(len(Il1)):
        t.append([])
        for item in Il1[j]:
            t[j].append(item)
    Il1 = t
    
    '''print "\nIL1: ",   #printing intital IL1 w/o the count
    for j in Il1:
        print
        for item in j:
            print item.name,'''

    for j in Il1:
        final = []
        for k in range(len(j)):
            final.append([])
            stack = [j[k]]
            #print "test: ", j[k].name
            while len(stack) > 0:
                temp = stack[0]
                stack.remove(temp)
                if temp.height == 0 or temp.height == -1:
                    final[k].append(temp)
                else:
                    for item in temp.E:
                        stack.append(item)
        final = list(itertools.product(*final))

        '''print "\nfinal:"
        print final,'''
        
        count = 0       #calculating freq of all otems in I_l_1
        for k in final:
            for row in db:
                if set([item.name for item in k]) < set(db[row]):
                    count += 1
        if count > 0:
            j.append(count)
        else:
            Il1.remove(j)

    '''print "\nIL1: ",     #displaying Il1 with respective frequencies
    for j in t:
        for item in j:
            if type(item) == int:
                print item,
            else:
                print item.name,
    print'''

    for R in Il1:       #step 4
        X = []      #computing X
        for item in R:
            if item != yes and item != no:
                X.append(item)
        X = [X[i] for i in range(len(X)-1)]
        
        '''print "X: ",
        for j in X:
            j.name'''
        
        t = []
        for j in range(len(X)):
            t.append([])
            stack = [X[j]]
            while len(stack) > 0:
                temp = stack[0]
                stack.remove(temp)
                if temp.height == 0:
                    t[j].append(temp)
                else:
                    for item in temp.E:
                        stack.append(item)
        t = list(itertools.product(*t))
        X = t

        t = []      #changing X from set form to list form
        for j in range(len(X)):
            if type(X[j]) == int:
                t.append(X[j])
            else:
                t.append([])
                for item in X[j]:
                    t[j].append(item)
        X = t
        #print "X: ", X

        '''print "X: ", X
        for j in X:
            for item in j:
                print item.name'''

        count = 0
        for row in db:
            for j in X:
                if (set([item.name for item in j]) < set(db[row])) == True:
                    count += 1
                    break
        #X.append(count)
                
        n1 = count          #n1
        a1 = R[len(R)-1]    #a1
        
        #print "X: ", [item for item in X]

        X = []      #computing original X again
        for item in R:
            if item != yes and item != no:
                X.append(item)
        X = [X[i] for i in range(len(X)-1)]

        A = []              #computing A
        for item in X:
            if (type(item) is not int) and (item in Cpd):
                #print "test: ", item
                A.append(item)

        T = []              #computing T
        for item in R:
            if (type(item) is not int) and (item not in A):
                T.append(item)

        '''print "A: ", [item.name for item in A]
        print "T: ", [item.name for item in T]'''
        
        #for nodes which have generalized values in them. eg: say node is <colored, n1>, then the final A will have values (black,n1) (black,n2)
        #(asian,n1) (asian,n2) (american,n1) (american,n2). Now negation of these values can be looked for in db to calculate a2 and n2
        t = []                  
        for j in range(len(A)):
            t.append([])
            stack = [A[j]]
            while len(stack) > 0:
                temp = stack[0]
                stack.remove(temp)
                if temp.height == 0:
                    t[j].append(temp)
                else:
                    for item in temp.E:
                        stack.append(item)
        t = list(itertools.product(*t))
        A = t

        #Doing the same for T as we did for A above
        t = []
        for j in range(len(T)):
            t.append([])
            stack = [T[j]]
            while len(stack) > 0:
                temp = stack[0]
                stack.remove(temp)
                if temp.height == 0 or temp.height == -1:
                    t[j].append(temp)
                else:
                    for item in temp.E:
                        stack.append(item)
        t = list(itertools.product(*t))
        T = t

        '''print "A: ", A
        print "T: ", T'''

        a2 = 0
        for row in db:
            flag = 1
            flag2 = 0
            for j in A:     #checking for NOT A
                for item in j:
                    if item.name in db[row]:
                        flag = 0
                        break
            for j in T:
                if (set([item.name for item in j]) < set(db[row])) == True:
                    flag2 = 1
                    #print "check"
                    break
            if flag == 1 and flag2 == 1:
                a2 += 1

        n2 = 0
        for row in db:
            flag = 1
            flag2 = 0
            for j in A:
                for item in j:
                    if item.name in db[row]:
                        flag = 0
                        break
            for j in T:
                if (set([j[k] for k in range(len(j)-1)]) < set(db[row])) == True:
                    flag2 = 1
                    break
            if flag == 1 and flag2 == 1:
                n2 += 1

        #print "Values: ", a1, n1, a2, n2
                
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

            #print "ratio: ", ratio
            if group[1] >= ms and ratio > alpha:    #step9(2)
                print 'case1, ratio: ', ratio
                return 'case1'          #step 10

        for group in PD_groups:     #step 11(1)
            if f == 'clift':
                ratio = 5678
            else:
                ratio = (float(group[1])/float(group[2]))/(float(group[1]+group[3])/float(group[2]+group[4]))

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
start_time = time.clock()
                
F = open("Dummy Dataset.txt","r")   #opening the dummy database
db = {}

#creating QI
qi = {
    0: "Sex",
    1: "Race",
    2: "Hours"
    }

#Initially taknig DA = {Sex}
#Creating DA = QI. This means that t=|QI|
da = ["Sex"]#, "Race", "Hours"]

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

yes = Nodes("Yes",[],-1,["Class"])     #for classifier
no = Nodes("No",[],-1,["Class"])
yes.freq = 6
no.freq = 4
classifier = [yes,no]


male = Nodes("Male",[],0,["Sex"])
female = Nodes("Female",[],0,["Sex"])
any_sex = Nodes("Any_sex",[male,female],1,["Sex"])

male.pointing_to.append(any_sex)
female.pointing_to.append(any_sex)
male.values.append(male)
female.values.append(female)
any_sex.values.append(any_sex)


white = Nodes("White",[],0,["Race"])
black = Nodes("Black",[],0,["Race"])
asian = Nodes("Asian",[],0,["Race"])
american = Nodes("American",[],0,["Race"])
white1 = Nodes("White1",[white],1,["Race"])
colored = Nodes("Colored",[black,asian,american],1,["Race"])
any_race = Nodes("Any_Race",[white,colored],2,["Race"])

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


n1 = Nodes("35",[],0,["Hours"])
n2 = Nodes("37",[],0,["Hours"])
n3 = Nodes("40",[],0,["Hours"])
n4 = Nodes("50",[],0,["Hours"])
n5 = Nodes("1 to 39",[n1,n2],1,["Hours"])
n6 = Nodes("40 to 99",[n3,n4],1,["Hours"])
n7 = Nodes("Any_hours",[n5,n6],2,["Hours"])

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
    "Hours": [[n1,n2,n3,n4],[n5,n6],[n7]],
    "Classifier": [yes,no]
    }


#creating Domi
dom = {
    0: [[male,female],[any_sex]],
    1: [[white,black,asian,american],[white1,colored],[any_race]],
    2: [[n1,n2,n3,n4],[n5,n6],[n7]]
    }

print
print

#other parameters
alpha = 1.2 
k = 1
ms = 1  #min support
tau = 1   #t is tau       change it to 3 later on
f = 'elift'     #discrimination parameter

#Creating DB
for row in range(0,10):
    temp = F.readline().split("\t")
    temp.remove(temp[0])
    if "\n" in temp:
        temp.remove("\n")
    db[row] = temp
F.close()

'''print "DB: "
for row in db:
    print row, db[row]
print
print db
print'''

#-------------------------------------------------

#C = nodes in the domain generalization hierarchies of attributes in QI
#C1 means it contains 1-attribute subsets of attributes in QI
#Cn means it contains n-attribute subsets of attributes in QI
C = [
        []     #C1
    ]        
for i in dom:
    for j in dom[i]:
        for item in j:
            C[0].append(item)

'''print "C: "
print " ".join(item.name for item in C[0])'''

Cpd = []            #step 2

#Hard-coding values of Cpd
Cpd = [male, female, any_sex]#, white, black, asian, american, white1, colored, any_race, n1, n2, n3, n4, n5, n6, n7]#, white, black, asian, american, white1, colored, any_race]

queue = []  #step 4
n = 3
roots = []
S = []
freq_set = []
freq_count = []
#%%
for i in range(n):      #step 5
    print "\ni: ", i

    C.append([])

    freq_set = []
    freq_count = []
    
    S.append(list())
    for item in C[i]:
        S[i].append(item)         #step 7
    '''S.append([])
    S[i] = copy.deepcopy(C[i])'''

    roots = []
    for item in C[i]:
        if len(item.E)==0:      #ie. there is no edge Ei directed to them
            roots.append(item)

    #print "Roots: ", [item.name for item in roots]

    for item in roots:          #step 9
        queue.append(item)

    queue = sorted(queue, key=attrgetter('height'))   #sorting values in queue by height
    #print "queue: ", [item.name for item in queue]

    while len(queue)>0:     #step 10
        node = queue[0]
        del(queue[0])       #step 11
        print
        print "node: ", node.name
        print "---%s seconds---" % (time.clock() - start_time)
        #print "Private: ", node.private
        queue = sorted(queue, key=attrgetter('height'))
        '''print "Queue: "
        for item in queue:
            print item.name,'''

        if node.private==False or (node.private==False and node.prot==False):    #step 12
            combi = []
            freq_set = []
            freq_count = []

            for l in range(len(node.attributes)):           #to traverse different attributes present in the node
                combi.append(attr_val[node.attributes[l]][node.values[l].height])   #to get all the values of the attributes in the corresponding height from attr_val

            freq_set = copy.deepcopy(combi)
            freq_set = list(itertools.product(*freq_set))   #creates freq_set for all possible combinations of values corresponding to the height and
                                                            #attributes of the node
            combi = list(itertools.product(*combi))     #because this itertools func doesn't return a list but sth a bit different on which we cannot perform the append function
            #print "combi: ", combi
            t = []       #so we copy the elements from combi into temp, in a list form
            for l in range(len(combi)):
                t.append(list())
                for item in combi[l]:
                    t[l].append(item)
            combi = t        #copying this created list back to combi so that we can operate with the variable combi and perform append function later on
            '''print "\n\ncombi: "
            for j in combi:
                print [item.name for item in j]'''

            for l in range(len(combi)):
                freq_count.append(0)
                compute_freq_set(combi[l],l)
            
            anonymous = True    #checking if DB is k-anonymous wrt attributes of the node
            for c in freq_count:
                k = 3               #k has been used as a variable somewhere ad its value is changing. Check where that is happening
                if c < k:
                    anonymous = False

            #print "Anonymous: ", anonymous    
            if anonymous == True:   #if DB is k-anonymous step 19
                #print "Enter, ", node.name
                node.private = True
                #print node.name, "is private: ", node.private
                for item in node.pointing_to:
                    item.private = True         #marking all direct generalization
                                                #as k-anonymous
                flag = 0
                N = []
                for item in Cpd:       #step 21(1)
                    if item in node.values:
                        N.append(item)
                        flag = 1

                if (flag == 1) and (i <= tau):    #step 21
                    if node.height == 0:
                        MR = alpha_protection(i,node)   #step 23
                    else:
                        MR = alpha_protection(i,node)  #step 25

                    if MR == 'case3':
                        #marking all direct generalizations of node that
                        #contain the generalization of N as k-anonymous
                        #and alpha-protective
                        for item in node.pointing_to:   #list of all direct generalizations one by one in item
                            for val in N:               #values in N
                                if (set(val.pointing_to) <= set(item)) == True: #checking the presence of values in N inside item
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
                #print "test i: ", i
                for item in S[i]:
                    if node==item:      #delete node from Si step 31
                        S[i].remove(item)
                for item in node.pointing_to:
                    if item not in queue:
                        queue.append(item)  #insert direct gen into queue
                queue = sorted(queue, key=attrgetter('height'))   #sorting by height

        elif node.private == True:      #step 21-36     step 38
            #print node.name, "is private: ", node.private
            flag = 0
            N = []
            for item in Cpd:       #step 21(1)
                if item in node.values:
                    N.append(item)
                    flag = 1

            if flag == 1 and i <= t:    #step 21
                if node.height == 0:
                    MR = alpha_protection(i,node)   #step 23
                else:
                    #print "check: ", node.name
                    MR = alpha_protection(i,node)  #step 25

                if MR == 'case3':
                    #marking all direct generalizations of node that
                    #contain the generalization of N as k-anonymous
                    #and alpha-protective
                    for item in node.pointing_to:   #list of all direct generalizations one by one in item
                        for val in N:               #values in N
                            if (set(val.pointing_to) <= set(item)) == True: #checking the presence of values in N inside item
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

    '''print "S: "
    for j in range(len(S)):
        print [item.name for item in S[j]]'''

    #------------------------------------------------------
        #Creating (i+1)-itemset from i-itemset
        #PRUNING
    #------------------------------------------------------

    for j in range(len(S[i])-1):
        for k in range(j+1,len(S[i])):
            attr = []                   #to put the attributes of the joining nodes into the new node
            values = []
            name = []
            c = 0
            flag = 1
            for index in range(len(S[i][j].attributes)):
                if index == (len(S[i][j].attributes) - 1) and (S[i][j].attributes[index] != S[i][k].attributes[index]):
                    name.append(S[i][j].values[index].name)
                    name.append(S[i][k].values[index].name)
                    attr.append(S[i][j].attributes[index])
                    attr.append(S[i][k].attributes[index])
                    values.append(S[i][j].values[index])
                    values.append(S[i][k].values[index])
                    break
                else:
                    if S[i][j].values[index] != S[i][k].values[index]:
                        flag = 0
                        break
                    else:
                        name.append(S[i][j].values[index].name)
                        attr.append(S[i][j].attributes[index])
                        values.append(S[i][j].values[index])
                        
            if flag == 1:
                E = []
                flag = 1
                for item in C[i+1]:
                    if set(values) == set(item.values):
                        flag = 0
                        break
                if flag == 1:
                    #C[i+1].append(Nodes(S[i][j].name + ' & ' + S[i][k].name, E, S[i][j].height + S[i][k].height, attr))
                    name = ' & '.join(item for item in name)
                    C[i+1].append(Nodes(name, E, S[i][j].height + S[i][k].values[len(S[i][k].values)-1].height, attr))
                    #C[i+1].append(Nodes(name, E, S[i][j].height + S[i][k].height, attr))
                    C[i+1][len(C[i+1])-1].values = values

    CC = []
    for item in C[i+1]:
        temp = []
        for j in range(len(item.values)):
            temp.append([])
            for k in range(len(item.values)):
                if j == k:
                    continue
                temp[j].append(item.values[k])
        flag1 = 1
        for t in temp:
            flag = 0
            for s in S[i]:
                if t == s.values:
                    flag = 1
                    break
            if flag == 0:
                print "Remove: ", item.name
                flag1 = 0
                break
        if flag1 == 1:
            CC.append(item)

    C[i+1] = copy.deepcopy(CC)
                
    for item1 in C[i+1]:        #basically to generate E and pointing_to
        for item2 in C[i+1]:
            c = 0
            for val1 in item1.values:       #comparing all nodes present in newly created Ci+1
                if val1 in item2.values:
                    c += 1
            if c != (len(item1.values)-1):  #all but one values in the 2 compared nodes should be same. The one different value will have the same attribute 
                continue                    #but a different value. It will basically be the direct generalization of the node
            if (item2.height - item1.height == 1) and (set(item1.attributes) == set(item2.attributes)): #difference in height should only be 1 for direct generalization
                item2.E.append(item1)                                                                   #all attributes should be the same
                item1.pointing_to.append(item2)
