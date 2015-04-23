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

#hard-coded C_1 values
C = [
    [male,female,any_sex,white,black,asian,american,white1,colored,any_race,n1,n2,n3,n4,n5,n6,n7],
    []
    ]
#hard-coded S_1 values obtained finally after one iteration
S = [
    [any_sex,white1,colored,any_race,n5,n6,n7]
    ]

for i in range(len(S[0])-1):
    for j in range(i+1,len(S[0])):
            attr = []                   #to put the attributes of the joining nodes into the new node
            c = 0
            for a in S[0][i].attributes:
                attr.append(a)
                c += 1
            for a in S[0][j].attributes:
                if a not in attr:
                    attr.append(a)
                    c += 1
            if c != (len(S[0][i].values)+1):   #the number of attributes of the newly formed node should be 1 greater than that of the node from which it is formed
                continue
            E = []
            C[1].append(Nodes(S[0][i].name + ' & ' + S[0][j].name, E, S[0][i].height + S[0][j].height, attr))
            C[1][len(C[1])-1].values.append(S[0][i])    #inserting the values present in the node i.e. the 2 nodes the new node is made up of
            C[1][len(C[1])-1].values.append(S[0][j])

for item1 in C[1]:      #basically to generate E and pointing_to
    for item2 in C[1]:
        c = 0
        for val1 in item1.values:   #comparing all nodes present in newly created Ci+1
            if val1 in item2.values:
                c += 1
        if c != (len(item1.values)-1):  #all but one values in the 2 compared nodes should be same. The one different value will have the same attribute 
            continue                    #but a different value. It will basically be the direct generalization of the node
        if (item2.height - item1.height == 1) and (set(item1.attributes) == set(item2.attributes)): #difference in height should only be 1 for direct generalization
            item2.E.append(item1)                                                                   #all attributes should be the same
            item1.pointing_to.append(item2)
