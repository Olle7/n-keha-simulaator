p=[2,1]#[m,q]
oskesed=[0,8,1,p,10,-15,1,p]#[x,y,z,tüüp]
G=10**-11*6.67384
def leiakiirendus(o1,o2):
    r=((o1[0]-o2[0])**2+(o1[1]-o2[1])**2+(o1[2]-o2[2])**2)**0.5
    global G
    m1=o1[3][0]
    m2=o2[3][0]
    F=G*m1*m2/r**2
    a=G*m2/r**2
    print(str("F=")+F)
    print(str("a=")+a)
leiakiirendus([0,10,0,p],[0,0,0,p])
