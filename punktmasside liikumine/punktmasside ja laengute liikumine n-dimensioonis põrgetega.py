#l=[m,q,X,x,Y,y,m,q,X,x,Y,y,m,q,X,x,Y,y,m,q,X,x,Y,y,m,q,X,x,Y,y,m,q,X,x,Y,y,m,q,X,x,Y,y]#v on kiirus;m on mass;q on laeng.
#l=[1,0,-25,0,5973600000000000000000000,0,-6372805,0]#õun ja maa
#l=[1,0,-1,0,1,0,0,0,1,0,1,0]#!-probleem ?-küsimus $-idee
#l=[1,2,3,4,5,2,3,4]
def küsi_punkt():
    lugeja=0
    l=[float(input("sisesta mass:"))]
    while l[0]==0:
        print("Kui punkmassi mass=0 ,siis ei mõjuta punkt teisi punkte ja keha asukoht ajahetkel on määramatu või algne,seega pole tarvis selle keha muid omadusi sisestada.\n")
        l=[float(input("sisesta mass:"))]
    l.append(float(input("sisesta laeng:")))
    while samm != lugeja:
        l+=[(float(input(("sisesta ")+str(lugeja+1)+(".dimensiooni kordinaat:")))),(float(input(("sisesta kiirus ")+str(lugeja+1)+".dimensiooni projektsioonis:")))]
        lugeja+=1
    print("")
    return(l)
def küsi_punkte():
    print("")
    l=küsi_punkt()
    l+=küsi_punkt()
    while input("kas sisestada veel üks punktmasslaeng?") in ["jah","1","ja","sisestada","Y"]:#teha eri ühikud#$teha võimalus sisestada määratud punkte
        l+=küsi_punkt()
    print("")
    return(l)
liit=[]
#import Turtle#Lisada kilpkonni listi$
samm=int(input("Sisesta dimensioonide arv:"))
l=küsi_punkte()
samm+=samm+2
print("kehasi on:",(len(l))/samm)
dif=float(input("Sisesta ajadiferentsiaali suurus:"))#saab iga uute punktide leidmise järel muuta#$muuta pöördvõrdeliseks kiireima keha kiirusega.
G=10**-11*6.67384*dif**2#kas skript saaks kasutada ainult konstandite suhet$?
k=10**9*8.9875517873681764*dif**2#kui korrutada kõik laegud läbi ruutjuurega k´st?-laengutel olex rohkem komasi
n=int(input("Iga mitmes diferentseerimine printida:"))
I_toorik=input("Mitu korda diferentseerida(kui tahate kuni kõik punktid on samas kohas jätke lahter tühjaks):")
if I_toorik.isdigit():
    korduste_limiit=int(I_toorik)+1
else:
    korduste_limiit=False
print("")
i=1
ep1=True
while len(l)>samm-1 and i != korduste_limiit:#korduste arv
    b=i%n==0#ütleb et, kas on vaja printida.
    if b:
        print("t=",i*dif)
    i+=1
    for p1 in range(0,len(l),samm):
        for p2 in range(p1+samm,len(l),samm):#p2 on alati suurem kui p1
            I_toorik=0
            for mõõde in range(2,samm,2):#kehade kaugus
                I_toorik+=(l[p1+mõõde]-l[p2+mõõde])**2
            if I_toorik==0:#kui asuvad samas kohas
                if l[1+p1]==l[1+p2] and ep1!=p1:#on sama laeguga  ,aga ei ole sama p1 mis eelmisel.#kas mass peaks ka sama olema?$
                    ep1=p1
                    liit+=[p1,p2]#pole vajalik ega võimalik omavahelist mõju määrata#loendi liit lisatakse õigeid asju
            else:#leiab punktide kiirenduste ja aja diferentsiaalide ruutude korrutised.
                I_toorik=(l[p1]*l[p2]*G-l[1+p1]*l[1+p2]*k)/I_toorik**1.5
                II_toorik=I_toorik/l[p1]
                I_toorik=I_toorik/l[p2]
                for mõõde in range(2,samm,2):#muudab kiirusi
                    l[1+p1+mõõde]+=II_toorik*(l[p2+mõõde]-l[p1+mõõde])#v1+=v1+a*dt**2
                    l[1+p2+mõõde]+=I_toorik*(l[p1+mõõde]-l[p2+mõõde])
        for mõõde in range(2,samm,2):
            l[mõõde+p1]+=l[1+p1+mõõde] #s_l=v_l*dt #vaja ainult p1´ga.
        if b:
            print("m:"+str(l[p1])+"; q:"+str(l[1+p1]),end=" ;  ")
            for mõõde in range(2,samm,2):
                print(str(mõõde//2)+".s="+str(l[p1+mõõde])+";",str(mõõde//2)+".v="+str(l[p1+mõõde+1]),end="; ")# v/d peax olema?!
            print("")
    if b:
        print("")
    for b in range(0,len(liit),2):#liidab#kus liidetud punkt kustutada?#$võib WHILE ja DELiga ka teha
        l[liit[1+b]+1]+=l[liit[b]+1]#q=q1+q2=2*q1=2*q2
        for mõõde in range(3,samm,2):#iga mõõtme jaoks kiirus
            l[liit[1+b]+mõõde]=(l[liit[b]]*l[liit[b]+mõõde]+l[liit[1+b]]*l[liit[1+b]+mõõde])/(l[liit[b]]+l[liit[1+b]])#v_l=(m1*vl1+m2*vl2)/(m1+m2)
        l[liit[1+b]]+=l[liit[b]]#m=m1+m2
        del liit[b+1]
    while len(liit)!=0:
        b=0
        while b!=samm:#kustutab 1.punkti mis teisele liideti
            del l[liit[0]]#kustutab 1.punkti konkreetse atribuudi
            b+=1
        del liit[0]
