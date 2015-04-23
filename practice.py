import itertools
import copy

#--------------------------------------------------------------
F = open("Dummy Dataset.txt","r")   #opening the dummy database

db = {}

#Creating DB
for row in range(0,10):
    temp = F.readline().split("\t")
    temp.remove(temp[0])
    if "\n" in temp:
        temp.remove("\n")
    db[row] = temp
F.close()
#--------------------------------------------------------------

def compute_freq_set(combi,i):
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
    print "temp: "
    for j in temp:
        print
        for item in j:
            print item.name

    for j in temp:
        for k in db:
            if (set([item.name for item in j]) < set(db[k])) == True:
                freq_count[i] += 1
    
    
#---------------------------------------------------------------    

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

attr_val = {
    "Sex": [[male,female],[any_sex]],
    "Race": [[white, black, asian, american],[white1,colored],[any_race]],
    "Hours": [[n1,n2,n3,n4],[n5,n6],[n7]]
    }

#--------------------------------------------------------------------------

test = Nodes("Test",[],2,["Sex"])    #test node
test.values = [male]

combi = []
freq_set = []
freq_count = []
for i in range(len(test.attributes)):           #to traverse different attributes present in the node
    combi.append(attr_val[test.attributes[i]][test.values[i].height])   #to get all the values of the attributes in the corresponding height from attr_val
    
freq_set = copy.deepcopy(combi)
freq_set = list(itertools.product(*freq_set))   #creates freq_set for all possible combinations of values corresponding to the height and attributes of the node

combi = list(itertools.product(*combi))     #because this itertools func doesn't return a list but sth a bit different on which we cannot perform the append function
t = []       #so we copy the elements from combi into temp, in a list form
for i in range(len(combi)):
    t.append(list())
    for item in combi[i]:
        t[i].append(item)
combi = t        #copying this created list back to combi so that we can operate with the variable combi and perform append function later on

for i in range(len(combi)):
    freq_count.append(0)
    compute_freq_set(combi[i],i)
    print freq_count
