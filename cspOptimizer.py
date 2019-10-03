import sys
from collections import defaultdict
from cspProblem import CSP, Constraint  
from cspSearch import Search_from_CSP
from searchGeneric import AStarSearcher


day=['mon','tue','wed','thu','fri']
time=['9am','10am','11am','12pm','1pm','2pm','3pm','4pm']

constraints=[]

cost=defaultdict(int)
domains={}
# m1 m2 m3

def before(m1,m2):
   
    if m1//8 < m2//8:
        return True
    elif m1//8== m2//8 and m1%8 < m2%8:
        return True
    return False
def one_day_between(m1,m2):
    if abs(m1//8-m2//8)==2:
        return True
    return False
def one_hour_between(m1,m2):
    if m1//8==m2//8 and abs(m1%8-m2%8)==2:
        return True
    return False
def same_day(m1,m2):
    if m1//8==m2//8 :
        return True
    return False

def domain_num(dt,dlen,tlen):    
    if dt in day:
        return [(day.index(dt)*tlen+i) for i in range(tlen)]
    elif dt in time:
        return [(i*tlen+time.index(dt)) for i in range(dlen)]
    elif dt =='morning':
        return [(i*tlen+j) for j in range(tlen/2) for i in range(dlen)]
    elif dt=='afternoon':
        return [(i*tlen+j) for j in range(tlen/2,tlen) for i in range(dlen)]
    elif '-' in dt:
        fr,to=list(map(lambda x:x.split(),l.split('-')))
        return [x for x in range(day.index(fr[0])*tlen+time.index(fr[1]),day.index(to[0])*tlen+time.index(to[1])+1)]                 
    else:
        dt=list(dt.split())
        if dt[0]=='before':
            if len(dt)==2:
                if dt[1] in day:
                    return [(i*tlen+j) for j in range(tlen) for i in range(day.index(dt[1]))]
                else:
                    return [(i*tlen+j) for j in range(time.index(dt[1])) for i in range(dlen)]
            else:
                   return [x for x in range(day.index(dt[1])*tlen+time.index(dt[2]))]
        else:
            if len(dt)==2:
                if dt[1] in day:
                    return [(i*tlen+j) for j in range(tlen) for i in range(day.index(dt[1]+1,dlen))]
                else:
                    return [(i*tlen+j) for j in range(time.index(dt[1])+1,tlen) for i in range(dlen)]
            else:
                   return [x for x in range(day.index(dt[1])*tlen+time.index(dt[2])+1,dlen*tlen)]

def soft_cost(m,dt,s):
    if s=='early-week':
        cost[(m,dt)]+=(dt//8)
    elif s=='late-week':
        cost[(m,dt)]+=(4-dt//8)
    elif s=='early-morning':
        cost[(m,dt)]+=(dt%8)
    elif s=='midday':
        cost[(m,dt)]+=abs(3-dt%8)
    elif s=='late-afternoon':
        cost[(m,dt)]+=(7-dt%8)

f = open(sys.argv[1], "r")
for l in f:
    if '#' in l:
        l=l[:l.index('#')] 
    l=list(map(lambda x:x.strip(),l.split(',')))
    if l[0]=="meeting":
        domains[l[1]]=set(range(len(day)*len(time)))
    elif l[0]=="constraint":
        m1,c,m2=l[1].split()
        c.replace('-','_')
        constraints.append(Constraint((m1.strip(),m2.strip()),eval(c)))
    elif l[0]=="domain":
        m=l[1]
        if l[-1] == "hard":               
            domains[m]=domains[m]&set(domain_num(l[2],len(day),len(time)))
        if l[-1]== "soft":
            for dt in domains[m]:
                soft_cost(m,dt,l[2])
f.close()

csp=CSP(domains,constraints,cost)
search_from_csp=Search_from_CSP(csp)
path=AStarSearcher(search_from_csp).search()

if path !=None:
    cost=path.end().cost
    path=path.end().to_node
    for v in path:
        print(v,':',day[path[v]//8],' ',time[path[v]%8],sep='')
    print('cost:',cost,sep='')
else:
    print('No Solution')


