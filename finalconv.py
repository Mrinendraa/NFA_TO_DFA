import graphviz

def printtransitiontable(sets,alphabets):
    sts = list(sets.keys())
    max=0
    for i in sts:
        if len(i) > max:
            max=len(i)
    if max < 5:
        max=5# for alignment purposes
    print(f" {'_' * (max+2 )}{'_' * (max+ 3) * len(alphabets)}")
    print(f"| State{' ' * (max - 5)} | ",end="")#for alignment purposes

    for inp in alphabets:  
        print(""+"".join(inp.ljust(max)),end=" | ")
    print("")
    print("|"+("-"*(max+2)+"|")*(len(alphabets)+1))
    for i in sts:
        next=sets[i]
        print(f"| {i.ljust(max)} | ",end="" )
        for inp in alphabets:
            print(""+ ",".join(next.get(inp, [])).ljust(max),end=" | ")
        print("")
    print(f" {'‾' * (max+2 )}{'‾' * (max+ 3) * len(alphabets)}")


# to draw graph
def drawdfa(dfa,fstate):
    dot = graphviz.Digraph()
    final_states=set()
    for state, transitions in dfa.items():
        if fstate in state:
            final_states.add(state)  # Add the state to final states set if state is present
        for next_states in transitions.values():
            for next_state in next_states:
                if fstate in next_state:
                    final_states.add(next_state)  # Add the next state to final states set if fstate is present

    # Add the states
    for state in dfa:
        if state in final_states:
            dot.node(state, state, shape='doublecircle')  # Mark as final state
        else:
            dot.node(state, state)

    # Add the transitions
    for state, transitions in dfa.items():
        for symbol, next_states in transitions.items():
            next_state_label=""
            t1=next_states
            next_state_label=",".join(t1)
            dot.edge(state, next_state_label, label=symbol)

    # Render and save the graph as a PNG file
    dot.render('dfa_graph', format='png', cleanup=True)
    print("Graph rendering completed.")


#to get input of alphabets set from user
str=input("Enter Alphabet set:")
alphabets=str.split()
inputs=alphabets.copy()
alphabets.append("*") #for epsilon transition
print(inputs)
print(alphabets)
dfa={}
nfa={}
states=[]#to have set of all states
closure={}#to have closure of individual states
lam1=[]#list for lambda transition
l=0#to know whether lambda transitions present or not
#to get input from user for nfa
while(1):
    temp=input("Enter State,input,next state: ")
    if temp=="end":
        break
    a=temp.split()
    if a[1]=="*":
        l=1
    if a[0] not in states:#to append to states if not present
        states.append(a[0])
    if a[2] not in states:#to append to states if not present
        states.append(a[2])
    if a[0] not in nfa:
        nfa[a[0]]={}#to initialize during first call
        
    if a[1] not in nfa[a[0]] and a[1] in alphabets:#to check if the input is in alphabet set or not and proceed only if present in alphabet set
        nfa[a[0]][a[1]]=[]
    nfa[a[0]][a[1]].append(a[2])
print("")

for i in states:#if the final state has no more transitions, initialize them as void
    if i not in nfa.keys():
        nfa[i]={}

#to initial non defined alphabets transtions as empty list
for i in nfa.keys():
   for x in alphabets:
      if x not in nfa[i]:
         nfa[i][x]=[]

initial=input("Enter initial state:")
final=input("Enter final state:")
if l==0:
    printtransitiontable(nfa,inputs)
    dfa[initial]={}
    for i in inputs:
        dfa[initial][i]=nfa[initial][i] 

    for x in inputs:
        t1=dfa[initial][x]
        new=",".join(t1)
        if new=="":
            dfa[initial][x]=["trap"]#to have "trap" state assigned for not defined  transitions
            continue
        if new not in dfa:
            dfa[new]={}

    nfa["trap"]={}
    for x in inputs:
        nfa["trap"][x]=["trap"]
    print("")
    #conversion part from non-lambda nfa to dfa
    c=1 #counter variable that determines when the loop should stop,i.e,when all states are converted
    while c==1:
        c=0
        key=list(dfa.keys())
        for initial in key:
            if dfa[initial]=={}:
                temp=initial.split(",")
                for x in inputs:
                    if x not in dfa[initial]:
                            dfa[initial][x]=[]
                    s=0 # counter variable that determines the addition of trap state
                    for i in temp:
                        z=nfa[i][x].copy()
                        for q in z :
                            if q not in dfa[initial][x]:
                                dfa[initial][x].append(q)
                                s=1
                    if s==0:
                        dfa[initial][x].append("trap") #if next state transition is defined  then it will be added otherwise "trap"
                        dfa["trap"]={}
                        c=1
                    else:    
                        t1=dfa[initial][x]
                        new=""
                        new=",".join(t1)
                        if new not in dfa:
                            dfa[new]={}
                            c=1

    printtransitiontable(dfa,inputs)





else:
    printtransitiontable(nfa,alphabets)
    # to initial closure

    for i in states:
        closure[i]=[]

    #to seperate out lambda transitions
    for i in states:
        if nfa[i]["*"]!=[]:
            t=",".join(nfa[i]["*"])
            lam1.append(f"{i} * {t}")
    
    #to initialize closure
    for i in states:
            closure[i].append(i)


    # to find epsilon_closure
    def epsilon_closure(i,lam,t):
        for j in lam:
            temp=j.split()
            if t==temp[0]:
                temptemp=temp[2].split(",")
                for k in temptemp:
                    if k not in closure[i]:
                        closure[i].append(k)
                        t=k
                        epsilon_closure(i,lam,t)    
                
    keys=closure.keys()
    for i in keys:
        epsilon_closure(i,lam1,i)
    
    print(closure)
    
    
    t=",".join(closure[initial])
    print("")
    dfa[t]={}

    nfa["trap"]={}
    for x in alphabets:
        nfa["trap"][x]=["trap"]


    b=0
    c=1 #counter variable that determines when the loop should stop,i.e,when all states are converted
    while c==1:
        c=0
        key=list(dfa.keys())
        for initial in key:
            if dfa[initial]=={}:
                temp=initial.split(",")
                for x in inputs:
                    if x not in dfa[initial]:
                        dfa[initial][x]=[]
                    s=0 # counter variable that determines the addition of trap state
                    for i in temp:
                        z=nfa[i][x].copy()
                        for q in z :
                            k=closure[q].copy()
                            for p in k:
                                if p not in dfa[initial][x]:
                                    dfa[initial][x].append(p)
                                    s=1
                    if s==0:
                        dfa[initial][x].append("trap") #if next state transition is defined  then it will be added otherwise "trap"
                        b=1
                        c=1
                    else:    
                        t1=dfa[initial][x]
                        new=",".join(t1)
                        if new not in dfa:
                            dfa[new]={}
                            c=1
    if b==1:
        dfa["trap"]={}
        for i in inputs:
            dfa["trap"][i]=["trap"]
    

    printtransitiontable(dfa,inputs)

drawdfa(dfa,final)