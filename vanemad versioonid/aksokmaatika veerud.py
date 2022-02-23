tahestik="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
N=int(input("N:"))
K=1#int(input("K:"))

def tee_read(veerud):#ei tee esimest rida
    q=[]
    for rea_nr in range(1,2**len(veerud)):
        q2="any_x("
        for veeru_nr in range(0,len(veerud)):
            if rea_nr%2==0:
                q2+="NOT"
            q2+="("+veerud[veeru_nr]+") and "
            rea_nr=rea_nr//2
        q.append(q2[:-5]+")")#[:-5],et and lopust ära votta.
    return(q)
veerud=[]
for hulk1 in range(0,N):
    for hulk2 in range(0,N):
        veerud.append(tahestik[hulk1]+r" in "+tahestik[hulk2])
m=[]
for hulk1 in range(0,N):
    m.append(tahestik[hulk1]+r" in x")
m.append("x in x")
for hulk1 in range(0,N):
    m.append(r"x in " + tahestik[hulk1])
veerud=veerud+tee_read(m)
print(veerud)
print(len(veerud),"veergu.")
print(2**len(veerud),"bitti.")
#print(2**(2**len(veerud)),"kombinatsiooni.")