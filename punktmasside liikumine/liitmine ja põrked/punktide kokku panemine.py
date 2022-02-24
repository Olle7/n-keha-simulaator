l=["F","F","F","F","F","F","am","aq","a1","a2","a3","a4","F","F","F","F","F","F","bm","bq","b1","b2","b3","b4","cm","cq","c1","c2","c3","c4","dm","dq","d1","d2","d3","d4"]
liit=[(6,18),(18,24)]#a+b;c+d
samm=6
#6;1,3,4,5
print(l)
def plastiline_põrge_stringina(l,liit):
    for a in liit:
        r=samm//2-1
        p=len(l)#-p kui on lisatud/kustutatud enne otsitavat
        while r != 0:#
            r+=-1
            l[a[1]+3]+="+"+l[a[0]+3]+"+"+l[a[0]]+"+"+l[a[1]-p]
            del l[a[0]+2],l[a[0]+2]
        l[a[1]-p]+="+"+l[a[0]]
        l[a[1]-p+1]+="+"+l[a[0]+1]
        del l[a[0]],l[a[0]]
    liit=[]
    return(l)
def liida_punktid_stringi_tehetena(l,liit):
    for a in liit:
        r=samm//2-1
        p=len(l)#-p kui on lisatud/kustutatud enne otsitavat
        while r != 0:#
            r+=-1
            l[a[1]+3]+="+"+l[a[0]+3]+"+"+l[a[0]]+"+"+l[a[1]-p]
            del l[a[0]+2],l[a[0]+2]
        l[a[1]-p]+="+"+l[a[0]]
        l[a[1]-p+1]+="+"+l[a[0]+1]
        del l[a[0]],l[a[0]]
    liit=[]
    return(l)
print(plastiline_põrge_stringina(l,liit))#muudab kahjuks li ära
#print("l=",l)
#print(liida_punktid_stringi_tehetena(l,liit))
