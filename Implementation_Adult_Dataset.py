from operator import attrgetter     #for sorting
import itertools                    #for forming all possible combinations of values from multiple lists
import copy                         #for deepcopy
import time                         #to time the code

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
                
    '''print "Il: ",     #displaying Il with respective frequencies
    for j in t:
        for item in j:
            if type(item) == int:
                print item,
            else:
                print item.name,'''

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
        '''if count > 0:
            j.append(count)
        else:
            Il1.remove(j)'''
        j.append(count)

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
        X = [X[j] for j in range(len(X)-1)]
        
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
        X = [X[k] for k in range(len(X)-1)]

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

        '''print "Values: ", a1, n1, a2, n2
        if type(a1) != int:
            print a1.name'''

        if a1 != 0:
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
                '''if (group[2] == 0) or (group[1] + group[3] == 0) or (group[2] + group[4] == 0):
                    continue'''
                #print "group: ", group
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
                
F = open("Adult_Small_Final.txt","r")   #opening the dummy database
db = {}

#creating QI
qi = {
    0: "Education",
    1: "Marital_Status",
    2: "Native_Country",
    3: "Occupation",
    4: "Race",
    5: "Relationship",
    6: "Sex",
    7: "Work_Class"
    }

#Initially taknig DA = {Sex}
#Creating DA = QI. This means that t=|QI|
#da = ["Education", "Marital_Status", "Native_Country", "Occupation", "Race", "Relationship", "Sex", "Work_Class"]
da = ["Sex", "Race"]

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

yes = Nodes("<=50K",[],-1,["Class"])     #for classifier
no = Nodes(">50K",[],-1,["Class"])
classifier = [yes,no]


#gender
male = Nodes("Male",[],0,["Sex"])
female = Nodes("Female",[],0,["Sex"])
any_sex = Nodes("Any_Sex",[male,female],1,["Sex"])

male.pointing_to.append(any_sex)
female.pointing_to.append(any_sex)

male.values.append(male)
female.values.append(female)
any_sex.values.append(any_sex)


#race
white = Nodes("White",[],0,["Race"])
black = Nodes("Black",[],0,["Race"])
asian_pacific_islander = Nodes("Asian-Pac-Islander",[],0,["Race"])
amer_indian_eskimo = Nodes("Amer-Indian-Eskimo",[],0,["Race"])
other_race = Nodes("Other",[],0,["Race"])
white1 = Nodes("White1",[white],1,["Race"])
colored = Nodes("Coloured",[black,asian_pacific_islander,amer_indian_eskimo,other_race],1,["Race"])
any_race = Nodes("Any_Race",[white1,colored],2,["Race"])

white.pointing_to.append(white1)
black.pointing_to.append(colored)
asian_pacific_islander.pointing_to.append(colored)
amer_indian_eskimo.pointing_to.append(colored)
other_race.pointing_to.append(colored)
white1.pointing_to.append(any_race)
colored.pointing_to.append(any_race)

white.values.append(white)
black.values.append(black)
asian_pacific_islander.values.append(asian_pacific_islander)
amer_indian_eskimo.values.append(amer_indian_eskimo)
other_race.values.append(other_race)
white1.values.append(white1)
colored.values.append(colored)
any_race.values.append(any_race)


#marital status
never_married = Nodes("Never-married",[],0,["Marital_Status"])
divorced = Nodes("Divorced",[],0,["Marital_Status"])
separated = Nodes("Separated",[],0,["Marital_Status"])
widowed = Nodes("Widowed",[],0,["Marital_Status"])
married_spouse_absent = Nodes("Married-spouse-absent",[],0,["Marital_Status"])
married_af_spouse = Nodes("Married-AF-spouse",[],0,["Marital_Status"])
married_civ_spouse = Nodes("Married-civ-spouse",[],0,["Marital_Status"])
never_married1 = Nodes("Never-married1",[never_married],1,["Marital_Status"])
partner_absent = Nodes("Partner-absent",[divorced,separated,widowed,married_spouse_absent],1,["Marital_Status"])
partner_present = Nodes("Partner-present",[married_af_spouse,married_civ_spouse],1,["Marital_Status"])
never_married2 = Nodes("Never-married2",[never_married1],2,["Marital_Status"])
married = Nodes("Married",[partner_absent,partner_present],2,["Marital_Status"])
any_marital_status = Nodes("Any Marital Status",[never_married2,married],3,["Marital_Status"])

never_married.pointing_to.append(never_married1)
divorced.pointing_to.append(partner_absent)
separated.pointing_to.append(partner_absent)
widowed.pointing_to.append(partner_absent)
married_spouse_absent.pointing_to.append(partner_absent)
married_af_spouse.pointing_to.append(partner_present)
married_civ_spouse.pointing_to.append(partner_present)
never_married1.pointing_to.append(never_married2)
partner_absent.pointing_to.append(married)
partner_present.pointing_to.append(married)
never_married2.pointing_to.append(any_marital_status)
married.pointing_to.append(any_marital_status)

never_married.values.append(never_married)
divorced.values.append(divorced)
separated.values.append(separated)
widowed.values.append(widowed)
married_spouse_absent.values.append(married_spouse_absent)
married_af_spouse.values.append(married_af_spouse)
married_civ_spouse.values.append(married_civ_spouse)
never_married1.values.append(never_married1)
partner_absent.values.append(partner_absent)
partner_present.values.append(partner_present)
never_married2.values.append(never_married2)
married.values.append(married)
any_marital_status.values.append(any_marital_status)


#work class
work_pvt = Nodes("Private",[],0,["Work_Class"])
self_emp_not_inc = Nodes("Self-emp-not-inc",[],0,["Work_Class"])
self_emp_inc = Nodes("Self-emp-inc",[],0,["Work_Class"])
federal_gov = Nodes("Federal-gov",[],0,["Work_Class"])
local_gov = Nodes("Local-gov",[],0,["Work_Class"])
state_gov = Nodes("State-gov",[],0,["Work_Class"])
without_pay = Nodes("Without-pay",[],0,["Work_Class"])
never_worked = Nodes("Never-worked",[],0,["Work_Class"])
work_pvt1 = Nodes("Private1",[work_pvt],1,["Work_Class"])
self_emp = Nodes("Self-emp",[self_emp_not_inc,self_emp_inc],1,["Work_Class"])
gov = Nodes("Gov",[federal_gov,local_gov,state_gov],1,["Work_Class"])
without_pay1 = Nodes("Without-pay1",[without_pay],1,["Work_Class"])
never_worked1 = Nodes("Never-worked1",[never_worked],1,["Work_Class"])
with_pay = Nodes("With-pay",[work_pvt1,self_emp,gov],2,["Work_Class"])
without_pay2 = Nodes("Without-pay2",[without_pay1],2,["Work_Class"])
never_worked2 = Nodes("Never-worked2",[never_worked1],2,["Work_Class"])
worked = Nodes("Worked",[with_pay,without_pay2],3,["Work_Class"])
never_worked3 = Nodes("Never-worked3",[never_worked2],3,["Work_Class"])
any_work_class = Nodes("Any-work-class",[worked,never_worked3],4,["Work_Class"])

work_pvt.pointing_to.append(work_pvt1)
self_emp_not_inc.pointing_to.append(self_emp)
self_emp_inc.pointing_to.append(self_emp)
federal_gov.pointing_to.append(gov)
local_gov.pointing_to.append(gov)
state_gov.pointing_to.append(gov)
without_pay.pointing_to.append(without_pay1)
never_worked.pointing_to.append(never_worked1)
work_pvt1.pointing_to.append(with_pay)
self_emp.pointing_to.append(with_pay)
gov.pointing_to.append(with_pay)
without_pay1.pointing_to.append(without_pay2)
never_worked1.pointing_to.append(never_worked2)
with_pay.pointing_to.append(worked)
without_pay2.pointing_to.append(worked)
never_worked2.pointing_to.append(never_worked3)
worked.pointing_to.append(any_work_class)
never_worked3.pointing_to.append(any_work_class)

work_pvt.values.append(work_pvt)
self_emp_not_inc.values.append(self_emp_not_inc)
self_emp_inc.values.append(self_emp_inc)
federal_gov.values.append(federal_gov)
local_gov.values.append(local_gov)
state_gov.values.append(state_gov)
without_pay.values.append(without_pay)
never_worked.values.append(never_worked)
work_pvt1.values.append(work_pvt1)
self_emp.values.append(self_emp)
gov.values.append(gov)
without_pay1.values.append(without_pay1)
never_worked1.values.append(never_worked1)
with_pay.values.append(with_pay)
without_pay2.values.append(without_pay2)
never_worked2.values.append(never_worked2)
worked.values.append(worked)
never_worked3.values.append(never_worked3)
any_work_class.values.append(any_work_class)


#education
preschool = Nodes("Preschool",[],0,["Education"])
e1 = Nodes("1st-4th",[],0,["Education"])
e2 = Nodes("5th-6th",[],0,["Education"])
e3 = Nodes("7th-8th",[],0,["Education"])
e4 = Nodes("9th",[],0,["Education"])
e5 = Nodes("10th",[],0,["Education"])
e6 = Nodes("11th",[],0,["Education"])
e7 = Nodes("12th",[],0,["Education"])
hs_grad = Nodes("HS-grad",[],0,["Education"])
some_college = Nodes("Some-college",[],0,["Education"])
assoc_acdm = Nodes("Assoc-acdm",[],0,["Education"])
assoc_voc = Nodes("Assoc-voc",[],0,["Education"])
bachelors = Nodes("Bachelors",[],0,["Education"])
prof_school = Nodes("Prof-school",[],0,["Education"])
masters = Nodes("Masters",[],0,["Education"])
doctorate = Nodes("Doctorate",[],0,["Education"])
preschool1 = Nodes("Preschool1",[preschool],1,["Education"])
elementary = Nodes("Elementary",[e1,e2,e3],1,["Education"])
junior_secondary = Nodes("Junior-Secondary",[e4,e5],1,["Education"])
senior_secondary = Nodes("Senior-Secondary",[e6,e7,hs_grad],1,["Education"])
some_college1 = Nodes("Some-college1",[some_college],1,["Education"])
assoc = Nodes("Assoc",[assoc_acdm,assoc_voc],1,["Education"])
university = Nodes("University",[bachelors,prof_school],1,["Education"])
post_grad = Nodes("Post-grad",[masters,doctorate],1,["Education"])
preschool2 = Nodes("Preschool2",[preschool1],2,["Education"])
elementary1 = Nodes("Elementary1",[elementary],2,["Education"])
secondary = Nodes("Secondary",[junior_secondary,senior_secondary],2,["Education"])
post_secondary = Nodes("Post-secondary",[some_college1,assoc,university,post_grad],2,["Education"])
without_post_secondary = Nodes("Without-post-secondary",[preschool2,elementary1,secondary],3,["Education"])
post_secondary1 = Nodes("Post-secondary1",[post_secondary],3,["Education"])
any_education = Nodes("Any_education",[without_post_secondary,post_secondary1],4,["Education"])

preschool.pointing_to.append(preschool1)
e1.pointing_to.append(elementary)
e2.pointing_to.append(elementary)
e3.pointing_to.append(elementary)
e4.pointing_to.append(junior_secondary)
e5.pointing_to.append(junior_secondary)
e6.pointing_to.append(senior_secondary)
e7.pointing_to.append(senior_secondary)
hs_grad.pointing_to.append(senior_secondary)
some_college.pointing_to.append(some_college1)
assoc_acdm.pointing_to.append(assoc)
assoc_voc.pointing_to.append(assoc)
bachelors.pointing_to.append(university)
prof_school.pointing_to.append(university)
masters.pointing_to.append(post_grad)
doctorate.pointing_to.append(post_grad)
preschool1.pointing_to.append(preschool2)
elementary.pointing_to.append(elementary1)
junior_secondary.pointing_to.append(secondary)
senior_secondary.pointing_to.append(secondary)
some_college1.pointing_to.append(post_secondary)
assoc.pointing_to.append(post_secondary)
university.pointing_to.append(post_secondary)
post_grad.pointing_to.append(post_secondary)
preschool2.pointing_to.append(without_post_secondary)
elementary1.pointing_to.append(without_post_secondary)
secondary.pointing_to.append(without_post_secondary)
post_secondary.pointing_to.append(post_secondary1)
without_post_secondary.pointing_to.append(any_education)
post_secondary1.pointing_to.append(any_education)

preschool.values.append(preschool)
e1.values.append(e1)
e2.values.append(e2)
e3.values.append(e3)
e4.values.append(e4)
e5.values.append(e5)
e6.values.append(e6)
e7.values.append(e7)
hs_grad.values.append(hs_grad)
some_college.values.append(some_college)
assoc_acdm.values.append(assoc_acdm)
assoc_voc.values.append(assoc_voc)
bachelors.values.append(bachelors)
prof_school.values.append(prof_school)
masters.values.append(masters)
doctorate.values.append(doctorate)
preschool1.values.append(preschool1)
elementary.values.append(elementary)
junior_secondary.values.append(junior_secondary)
senior_secondary.values.append(senior_secondary)
some_college1.values.append(some_college1)
assoc.values.append(assoc)
university.values.append(university)
post_grad.values.append(post_grad)
preschool2.values.append(preschool2)
elementary1.values.append(elementary1)
secondary.values.append(secondary)
post_secondary.values.append(post_secondary)
without_post_secondary.values.append(without_post_secondary)
post_secondary1.values.append(post_secondary1)
any_education.values.append(any_education)


#occupation
exec_managerial = Nodes("Exec-managerial",[],0,["Occupation"])
prof_specialty = Nodes("Prof-specialty",[],0,["Occupation"])
sales = Nodes("Sales",[],0,["Occupation"])
adm_clerical = Nodes("Adm-clerical",[],0,["Occupation"])
tech_support = Nodes("Tech-support",[],0,["Occupation"])
craft_repair = Nodes("Craft-repair",[],0,["Occupation"])
machine_op_inspct = Nodes("Machine-op-inspct",[],0,["Occupation"])
handlers_cleaners = Nodes("Handlers-cleaners",[],0,["Occupation"])
transport_moving = Nodes("Transport-moving",[],0,["Occupation"])
priv_house_serv = Nodes("Priv-house-serv",[],0,["Occupation"])
protective_serv = Nodes("Protective-serv",[],0,["Occupation"])
armed_forces = Nodes("Armed-Forces",[],0,["Occupation"])
farming_fishing = Nodes("Farming-fishing",[],0,["Occupation"])
other_service = Nodes("Other-service",[],0,["Occupation"])
white_collar = Nodes("White-collar",[exec_managerial,prof_specialty,sales,adm_clerical],1,["Occupation"])
blue_collar = Nodes("Blue-collar",[tech_support,craft_repair,machine_op_inspct,handlers_cleaners,transport_moving,priv_house_serv],1,["Occupation"])
other_occupation = Nodes("Other-occupation",[protective_serv,armed_forces,farming_fishing,other_service],1,["Occupation"])
any_occupation = Nodes("Any-occupation",[white_collar,blue_collar,other_occupation],2,["Occupation"])

exec_managerial.pointing_to.append(white_collar)
prof_specialty.pointing_to.append(white_collar)
sales.pointing_to.append(white_collar)
adm_clerical.pointing_to.append(white_collar)
tech_support.pointing_to.append(blue_collar)
craft_repair.pointing_to.append(blue_collar)
machine_op_inspct.pointing_to.append(blue_collar)
handlers_cleaners.pointing_to.append(blue_collar)
transport_moving.pointing_to.append(blue_collar)
priv_house_serv.pointing_to.append(blue_collar)
protective_serv.pointing_to.append(other_occupation)
armed_forces.pointing_to.append(other_occupation)
farming_fishing.pointing_to.append(other_occupation)
other_service.pointing_to.append(other_occupation)
white_collar.pointing_to.append(any_occupation)
blue_collar.pointing_to.append(any_occupation)
other_occupation.pointing_to.append(any_occupation)

exec_managerial.values.append(exec_managerial)
prof_specialty.values.append(prof_specialty)
sales.values.append(sales)
adm_clerical.values.append(adm_clerical)
tech_support.values.append(tech_support)
craft_repair.values.append(craft_repair)
machine_op_inspct.values.append(machine_op_inspct)
handlers_cleaners.values.append(handlers_cleaners)
transport_moving.values.append(transport_moving)
priv_house_serv.values.append(priv_house_serv)
protective_serv.values.append(protective_serv)
armed_forces.values.append(armed_forces)
farming_fishing.values.append(farming_fishing)
other_service.values.append(other_service)
white_collar.values.append(white_collar)
blue_collar.values.append(blue_collar)
other_occupation.values.append(other_occupation)
any_occupation.values.append(any_occupation)


#relationship
wife = Nodes("Wife",[],0,["Relationship"])
own_child = Nodes("Own-child",[],0,["Relationship"])
husband = Nodes("Husband",[],0,["Relationship"])
not_in_family = Nodes("Not-in-family",[],0,["Relationship"])
other_relative = Nodes("Other-relative",[],0,["Relationship"])
unmarried = Nodes("Unmarried",[],0,["Relationship"])
in_family = Nodes("In-family",[wife,own_child,husband],1,["Relationship"])
not_in_family1 = Nodes("Not in family1",[not_in_family],1,["Relationship"])
other_relative1 = Nodes("Other relative1",[other_relative],1,["Relationship"])
unmarried1 = Nodes("Unmarried1",[unmarried],1,["Relationship"])
any_relationship = Nodes("Any relationship",[in_family,not_in_family1,other_relative1,unmarried1],2,["Relationship"])

wife.pointing_to.append(in_family)
own_child.pointing_to.append(in_family)
husband.pointing_to.append(in_family)
not_in_family.pointing_to.append(not_in_family1)
other_relative.pointing_to.append(other_relative1)
unmarried.pointing_to.append(unmarried1)
in_family.pointing_to.append(any_relationship)
not_in_family1.pointing_to.append(any_relationship)
other_relative1.pointing_to.append(any_relationship)
unmarried1.pointing_to.append(any_relationship)

wife.values.append(wife)
own_child.values.append(own_child)
husband.values.append(husband)
not_in_family.values.append(not_in_family)
other_relative.values.append(other_relative)
unmarried.values.append(unmarried)
in_family.values.append(in_family)
not_in_family1.values.append(not_in_family1)
other_relative1.values.append(other_relative1)
unmarried1.values.append(unmarried1)
any_relationship.values.append(any_relationship)


#native country
united_states = Nodes("United-States",[],0,["Native_Country"])
outlying_us = Nodes("Outlying-US(Guam-USVI-etc)",[],0,["Native_Country"])
canada = Nodes("Canada",[],0,["Native_Country"])
mexico = Nodes("Mexico",[],0,["Native_Country"])
honduras = Nodes("Honduras",[],0,["Native_Country"])
guatemala = Nodes("Guatemala",[],0,["Native_Country"])
nicaragua = Nodes("Nicaragua",[],0,["Native_Country"])
el_salvador = Nodes("El-Salvador",[],0,["Native_Country"])
ecuador = Nodes("Ecuador",[],0,["Native_Country"])
peru = Nodes("Peru",[],0,["Native_Country"])
columbia = Nodes("Columbia",[],0,["Native_Country"])
puerto_rico = Nodes("Puerto-Rico",[],0,["Native_Country"])
dominican_republic = Nodes("Dominican-Republic",[],0,["Native_Country"])
jamaica = Nodes("Jamaica",[],0,["Native_Country"])
cuba = Nodes("Cuba",[],0,["Native_Country"])
haiti = Nodes("Haiti",[],0,["Native_Country"])
trinadad_tobago = Nodes("Trinadad&Tobago",[],0,["Native_Country"])
france = Nodes("France",[],0,["Native_Country"])
england = Nodes("England",[],0,["Native_Country"])
ireland = Nodes("Ireland",[],0,["Native_Country"])
scotland = Nodes("Scotland",[],0,["Native_Country"])
holand_netherlands = Nodes("Holand-Netherlands",[],0,["Native_Country"])
italy = Nodes("Italy",[],0,["Native_Country"])
greece = Nodes("Greece",[],0,["Native_Country"])
portugal = Nodes("Portugal",[],0,["Native_Country"])
yugoslavia = Nodes("Yugoslavia",[],0,["Native_Country"])
hungary = Nodes("Hungary",[],0,["Native_Country"])
germany = Nodes("Germany",[],0,["Native_Country"])
poland = Nodes("Poland",[],0,["Native_Country"])
philippines = Nodes("Philippines",[],0,["Native_Country"])
thailand = Nodes("Thailand",[],0,["Native_Country"])
cambodia = Nodes("Cambodia",[],0,["Native_Country"])
vietnam = Nodes("Vietnam",[],0,["Native_Country"])
laos = Nodes("Laos",[],0,["Native_Country"])
india = Nodes("India",[],0,["Native_Country"])
japan = Nodes("Japan",[],0,["Native_Country"])
china = Nodes("China",[],0,["Native_Country"])
hong = Nodes("Hong",[],0,["Native_Country"])
taiwan = Nodes("Taiwan",[],0,["Native_Country"])
south = Nodes("South",[],0,["Native_Country"])
iran = Nodes("Iran",[],0,["Native_Country"])
usa = Nodes("USA",[united_states,outlying_us],1,["Native_Country"])
north_america = Nodes("North-america",[canada],1,["Native_Country"])
middle_america = Nodes("Middle america",[mexico,honduras,guatemala,nicaragua,el_salvador],1,["Native_Country"])
western_south_america = Nodes("Western south america",[ecuador,peru],1,["Native_Country"])
northern_south_america = Nodes("Northern south america",[columbia],1,["Native_Country"])
caribbean = Nodes("Caribbean",[puerto_rico,dominican_republic,jamaica,cuba,haiti,trinadad_tobago],1,["Native_Country"])
western_europe = Nodes("Western Europe",[france,england,ireland,scotland,holand_netherlands],1,["Native_Country"])
southern_europe = Nodes("Southern-europe",[italy,greece],1,["Native_Country"])
southwestern_europe = Nodes("Southwestern europe",[portugal],1,["Native_Country"])
southeastern_europe = Nodes("Southeastern europe",[yugoslavia],1,["Native_Country"])
central_europe = Nodes("Central Europe",[hungary,germany,poland],1,["Native_Country"])
southeastern_asia = Nodes("Southeastern asia",[philippines,thailand,cambodia,vietnam,laos],1,["Native_Country"])
southern_asia = Nodes("Southern asia",[india],1,["Native_Country"])
eastern_asia = Nodes("Eastern asia",[japan,china,hong,taiwan,south],1,["Native_Country"])
middle_east = Nodes("Middle east",[iran],1,["Native_Country"])
north_america1 = Nodes("North america1",[usa,north_america,middle_america],2,["Native_Country"])
south_america = Nodes("South america",[western_south_america,northern_south_america,caribbean],2,["Native_Country"])
europe = Nodes("Europe",[western_europe,southern_europe, southwestern_europe,southeastern_europe,central_europe],2,["Native_Country"])
asia = Nodes("Asia",[southeastern_asia,southern_asia,eastern_asia,middle_east],2,["Native_Country"])
any_native_country = Nodes("Any native country",[north_america1,south_america,europe,asia],3,["Native_Country"])

united_states.pointing_to.append(usa)
outlying_us.pointing_to.append(usa)
canada.pointing_to.append(north_america)
mexico.pointing_to.append(middle_america)
honduras.pointing_to.append(middle_america)
guatemala.pointing_to.append(middle_america)
nicaragua.pointing_to.append(middle_america)
el_salvador.pointing_to.append(middle_america)
ecuador.pointing_to.append(western_south_america)
peru.pointing_to.append(western_south_america)
columbia.pointing_to.append(northern_south_america)
puerto_rico.pointing_to.append(caribbean)
dominican_republic.pointing_to.append(caribbean)
jamaica.pointing_to.append(caribbean)
cuba.pointing_to.append(caribbean)
haiti.pointing_to.append(caribbean)
trinadad_tobago.pointing_to.append(caribbean)
france.pointing_to.append(western_europe)
england.pointing_to.append(western_europe)
ireland.pointing_to.append(western_europe)
scotland.pointing_to.append(western_europe)
holand_netherlands.pointing_to.append(western_europe)
italy.pointing_to.append(southern_europe)
greece.pointing_to.append(southern_europe)
portugal.pointing_to.append(southwestern_europe)
yugoslavia.pointing_to.append(southeastern_europe)
hungary.pointing_to.append(central_europe)
germany.pointing_to.append(central_europe)
poland.pointing_to.append(central_europe)
philippines.pointing_to.append(southeastern_asia)
thailand.pointing_to.append(southeastern_asia)
cambodia.pointing_to.append(southeastern_asia)
vietnam.pointing_to.append(southeastern_asia)
laos.pointing_to.append(southeastern_asia)
india.pointing_to.append(southern_asia)
japan.pointing_to.append(eastern_asia)
china.pointing_to.append(eastern_asia)
hong.pointing_to.append(eastern_asia)
taiwan.pointing_to.append(eastern_asia)
south.pointing_to.append(eastern_asia)
iran.pointing_to.append(middle_east)
usa.pointing_to.append(north_america1)
north_america.pointing_to.append(north_america1)
middle_america.pointing_to.append(north_america1)
western_south_america.pointing_to.append(south_america)
northern_south_america.pointing_to.append(south_america)
caribbean.pointing_to.append(south_america)
western_europe.pointing_to.append(europe)
southern_europe.pointing_to.append(europe)
southwestern_europe.pointing_to.append(europe)
southeastern_europe.pointing_to.append(europe)
central_europe.pointing_to.append(europe)
southeastern_asia.pointing_to.append(asia)
southern_asia.pointing_to.append(asia)
eastern_asia.pointing_to.append(asia)
middle_east.pointing_to.append(asia)
north_america1.pointing_to.append(any_native_country)
south_america.pointing_to.append(any_native_country)
europe.pointing_to.append(any_native_country)
asia.pointing_to.append(any_native_country)

united_states.values.append(united_states)
outlying_us.values.append(outlying_us)
canada.values.append(canada)
mexico.values.append(mexico)
honduras.values.append(honduras)
guatemala.values.append(guatemala)
nicaragua.values.append(nicaragua)
el_salvador.values.append(el_salvador)
ecuador.values.append(ecuador)
peru.values.append(peru)
columbia.values.append(columbia)
puerto_rico.values.append(puerto_rico)
dominican_republic.values.append(dominican_republic)
jamaica.values.append(jamaica)
cuba.values.append(cuba)
haiti.values.append(haiti)
trinadad_tobago.values.append(trinadad_tobago)
france.values.append(france)
england.values.append(england)
ireland.values.append(ireland)
scotland.values.append(scotland)
holand_netherlands.values.append(holand_netherlands)
italy.values.append(italy)
greece.values.append(greece)
portugal.values.append(portugal)
yugoslavia.values.append(yugoslavia)
hungary.values.append(hungary)
germany.values.append(germany)
poland.values.append(poland)
philippines.values.append(philippines)
thailand.values.append(thailand)
cambodia.values.append(cambodia)
vietnam.values.append(vietnam)
laos.values.append(laos)
india.values.append(india)
japan.values.append(japan)
china.values.append(china)
hong.values.append(hong)
taiwan.values.append(taiwan)
south.values.append(south)
iran.values.append(iran)
usa.values.append(usa)
north_america.values.append(north_america)
middle_america.values.append(middle_america)
western_south_america.values.append(western_south_america)
northern_south_america.values.append(northern_south_america)
caribbean.values.append(caribbean)
western_europe.values.append(western_europe)
southern_europe.values.append(southern_europe)
southwestern_europe.values.append(southwestern_europe)
southeastern_europe.values.append(southeastern_europe)
central_europe.values.append(central_europe)
southeastern_asia.values.append(southeastern_asia)
southern_asia.values.append(southern_asia)
eastern_asia.values.append(eastern_asia)
middle_east.values.append(middle_east)
north_america1.values.append(north_america1)
south_america.values.append(south_america)
europe.values.append(europe)
asia.values.append(asia)
any_native_country.values.append(any_native_country)


#A dictionary for attributes and corresponding possible values
#This can be used to compute frequency set etc
attr_val = {
    "Sex": [[male,female],[any_sex]],
    "Race": [[white, black, asian_pacific_islander, amer_indian_eskimo,other_race],[white1,colored],[any_race]],
    "Marital_Status": [[never_married,divorced,separated,widowed,married_spouse_absent,married_af_spouse,married_civ_spouse],[never_married1,partner_absent,partner_present],[never_married2,married],[any_marital_status]],
    "Work_Class": [[work_pvt,self_emp_not_inc,self_emp_inc,federal_gov,local_gov,state_gov,without_pay,never_worked],[work_pvt1,self_emp,gov,without_pay1,never_worked1],[with_pay,without_pay2,never_worked2],[worked,never_worked3],[any_work_class]],
    "Education": [[preschool,e1,e2,e3,e4,e5,e6,e7,hs_grad,some_college,assoc_acdm,assoc_voc,bachelors,prof_school,masters,doctorate],[preschool1,elementary,junior_secondary,senior_secondary,some_college1,assoc,university,post_grad],[preschool2,elementary1,secondary,post_secondary],[without_post_secondary,post_secondary1],[any_education]],
    "Occupation": [[exec_managerial,prof_specialty,sales,adm_clerical,tech_support,craft_repair,machine_op_inspct,handlers_cleaners,transport_moving,priv_house_serv,protective_serv,armed_forces,farming_fishing,other_service],[white_collar,blue_collar,other_occupation],[any_occupation]],
    "Relationship": [[wife,own_child,husband,not_in_family,other_relative,unmarried],[in_family,not_in_family1,other_relative1,unmarried1],[any_relationship]],
    "Native_Country": [[united_states,outlying_us,canada,mexico,honduras,guatemala,nicaragua,el_salvador,ecuador,peru,columbia,puerto_rico,dominican_republic,jamaica,cuba,haiti,trinadad_tobago,france,england,ireland,scotland,holand_netherlands, italy, greece, portugal, yugoslavia,hungary,germany,poland,philippines,thailand,cambodia,vietnam,laos,india,japan,china,hong,taiwan,south,iran],[usa,north_america,middle_america,western_south_america,northern_south_america,caribbean,western_europe,southern_europe,southwestern_europe,southeastern_europe,central_europe,southeastern_asia,southern_asia,eastern_asia,middle_east],[north_america1,south_america,europe,asia],[any_native_country]],
    "Classifier": [yes,no]
    }


#creating Domi
dom = {
    0: [[male,female],[any_sex]],
    1: [[white, black, asian_pacific_islander, amer_indian_eskimo,other_race],[white1,colored],[any_race]],
    2: [[never_married,divorced,separated,widowed,married_spouse_absent,married_af_spouse,married_civ_spouse],[never_married1,partner_absent,partner_present],[never_married2,married],[any_marital_status]],
    3: [[work_pvt,self_emp_not_inc,self_emp_inc,federal_gov,local_gov,state_gov,without_pay,never_worked],[work_pvt1,self_emp,gov,without_pay1,never_worked1],[with_pay,without_pay2,never_worked2],[worked,never_worked3],[any_work_class]],
    4: [[preschool,e1,e2,e3,e4,e5,e6,e7,hs_grad,some_college,assoc_acdm,assoc_voc,bachelors,prof_school,masters,doctorate],[preschool1,elementary,junior_secondary,senior_secondary,some_college1,assoc,university,post_grad],[preschool2,elementary1,secondary,post_secondary],[without_post_secondary,post_secondary1],[any_education]],
    5: [[exec_managerial,prof_specialty,sales,adm_clerical,tech_support,craft_repair,machine_op_inspct,handlers_cleaners,transport_moving,priv_house_serv,protective_serv,armed_forces,farming_fishing,other_service],[white_collar,blue_collar,other_occupation],[any_occupation]],
    6: [[wife,own_child,husband,not_in_family,other_relative,unmarried],[in_family,not_in_family1,other_relative1,unmarried1],[any_relationship]],
    7: [[united_states,outlying_us,canada,mexico,honduras,guatemala,nicaragua,el_salvador,ecuador,peru,columbia,puerto_rico,dominican_republic,jamaica,cuba,haiti,trinadad_tobago,france,england,ireland,scotland,holand_netherlands, italy, greece, portugal, yugoslavia,hungary,germany,poland,philippines,thailand,cambodia,vietnam,laos,india,japan,china,hong,taiwan,south,iran],[usa,north_america,middle_america,western_south_america,northern_south_america,caribbean,western_europe,southern_europe,southwestern_europe,southeastern_europe,central_europe,southeastern_asia,southern_asia,eastern_asia,middle_east],[north_america1,south_america,europe,asia],[any_native_country]]
    }

print
print

#other parameters
alpha = 1.2 
k_anonymity = 5
ms = 5  #min support
tau = 1   #t is tau
f = 'elift'     #discrimination parameter

#Creating DB
for row in range(0,100):
    temp = F.readline().split("\t")
    #temp.remove(temp[0])
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

#Hard-coding values of Cpd
#step 2
'''Cpd = [male,female,any_sex,
    white, black, asian_pacific_islander, amer_indian_eskimo,other_race,white1,colored,any_race,
    never_married,divorced,separated,widowed,married_spouse_absent,married_af_spouse,married_civ_spouse,never_married1,partner_absent,partner_present,never_married2,married,any_marital_status,
    work_pvt,self_emp_not_inc,self_emp_inc,federal_gov,local_gov,state_gov,without_pay,never_worked,work_pvt1,self_emp,gov,without_pay1,never_worked1,with_pay,without_pay2,never_worked2,worked,never_worked3,any_work_class,
    preschool,e1,e2,e3,e4,e5,e6,e7,hs_grad,some_college,assoc_acdm,assoc_voc,bachelors,prof_school,masters,doctorate,preschool1,elementary,junior_secondary,senior_secondary,some_college1,assoc,university,post_grad,preschool2,elementary1,secondary,post_secondary,without_post_secondary,post_secondary1,any_education,
    exec_managerial,prof_specialty,sales,adm_clerical,tech_support,craft_repair,machine_op_inspct,handlers_cleaners,transport_moving,priv_house_serv,protective_serv,armed_forces,farming_fishing,other_service,white_collar,blue_collar,other_occupation,any_occupation,
    wife,own_child,husband,not_in_family,other_relative,unmarried,in_family,not_in_family1,other_relative1,unmarried1,any_relationship,
    united_states,outlying_us,canada,mexico,honduras,guatemala,nicaragua,el_salvador,ecuador,peru,columbia,puerto_rico,dominican_republic,jamaica,cuba,haiti,trinadad_tobago,france,england,ireland,scotland,holand_netherlands, italy, greece, portugal, yugoslavia,hungary,germany,poland,philippines,thailand,cambodia,vietnam,laos,india,japan,china,hong,taiwan,south,iran,usa,north_america,middle_america,western_south_america,northern_south_america,caribbean,western_europe,southern_europe,southwestern_europe,southeastern_europe,central_europe,southeastern_asia,southern_asia,eastern_asia,middle_east,north_america1,south_america,europe,asia,any_native_country
    ]'''
Cpd = [male,female,any_sex]

queue = []  #step 4
n = 8
roots = []
S = []
freq_set = []
freq_count = []

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
        print "Clock: %s" % (time.clock() - start_time)
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
            combi = list(itertools.product(*combi))     #because this itertools func does not return a list but sth a bit different on which we cannot perform the append function
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
                #k = 80               #k has been used as a variable somewhere ad its value is changing. Check where that is happening
                if c < k_anonymity:
                    anonymous = False

            #print "Anonymous: ", anonymous    
            if anonymous == True:   #if DB is k-anonymous step 19
                #print "Enter, ", node.name
                for item in node.pointing_to:
                    item.private = True         #marking all direct generalization
                                                #as k-anonymous
                flag = 0
                N = []
                for item in Cpd:       #step 21(1)
                    if item in node.values:
                        N.append(item)
                        flag = 1

                #print "test i: ", i
                if (flag == 1) and (i <= tau):    #step 21
                    if node.height == 0:
                        print "Enter"
                        MR = alpha_protection(i,node)   #step 23
                    else:
                        print "Enter"
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
            flag = 0
            N = []
            for item in Cpd:       #step 21(1)
                if item in node.values:
                    N.append(item)
                    flag = 1

            if flag == 1 and i <= tau:    #step 21
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
                        if item not in queue:
                            queue.append(item)  #insert direct gen into queue
                    queue = sorted(queue, key=attrgetter('height'))   #sorting by height
            
            else:
                for item in S[i]:
                    if node==item:      #delete node from Si step 31
                        S[i].remove(item)
                for item in node.pointing_to:
                    if item not in queue:
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
