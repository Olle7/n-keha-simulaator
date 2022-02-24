#l=[m,q,X,x,Y,y,m,q,X,x,Y,y,m,q,X,x,Y,y,m,q,X,x,Y,y,m,q,X,x,Y,y,m,q,X,x,Y,y,m,q,X,x,Y,y]#v on kiirus;m on mass;q on laeng.
#l=[1,0,-25,0,5973600000000000000000000,0,-6372805,0]#õun ja maa
l=[1989000000000000000000000000000,0,0,0,0,0,5973600000000000000000000,0,0,29783,149600000000,0]#!-probleem ?-küsimus $-idee #päike ja maa
mõõtkava=10
import time
def küsi_punkt():
    l=[float(input("sisesta mass:"))]
    while l[0]==0:
        print("Kui punkmassi mass=0 ,siis ei mõjuta punkt teisi punkte ja keha asukoht ajahetkel on määramatu või algne,seega pole tarvis selle keha muid omadusi sisestada.\n")
        l=[float(input("sisesta mass:"))]
    l.append(float(input("sisesta laeng:")))
    if graaf:
        l.append(turtle.Turtle())
    if põ!="0":
        l.append(float(input("sisesta põrkeks vajalik kaugus:")))#kaugus m ja q´st (järjendis) sõltub kas graaf==True
    p1=0
    while samm != p1:
        l+=[(float(input(("sisesta ")+str(p1+1)+(".dimensiooni kordinaat:")))),(float(input(("sisesta kiirus ")+str(p1+1)+".dimensiooni projektsioonis:")))]
        p1+=1
    if graaf:#paneb punkti algsesse asukohta. toimib.
        l[-samm*2-1].penup()
        if samm > 0:
            l[-samm*2-1].setx(l[-samm*2]*mõõtkava)
        if samm > 1:
            l[-samm*2-1].sety(l[2-samm*2]*mõõtkava)
        l[-samm*2-1].pendown()
    print("")
    return(l)
def küsi_punkte():
    print("")
    l=küsi_punkt()+küsi_punkt()
    while input("kas sisestada veel üks punktmasslaeng?") in ["jah","1","ja","sisestada","Y"]:#teha eri ühikud#$teha võimalus sisestada määratud punkte
        l+=küsi_punkt()
    print("")
    return(l)
import turtle
samm=int(input("Sisesta dimensioonide arv:"))
while samm<=0:
    print("dimensioone ei saa olla 0 või vähem.")
    samm=int(input("Sisesta dimensioonide arv:"))
if input("kas kasutada turteli graafikat:") in ["jah","1","ja","sisestada","Y"]:
    graaf=True
else:
    graaf=False
põ=input("kuidas põrkeid arvestada?(1-elastsena;2-plastilisena;0-üldse mitte):")
while põ not in["0","1","2"]:
    põ=input("kuidas põrkeid arvestada?(1-elastsena;2-plastilisena;0-üldse mitte):")
#l=küsi_punkte()
a=2
samm+=samm+2
if graaf==True:
    samm+=1
    a=3
if põ!="0":
    samm+=1
    a+=1
liit=[]
i=1
ep1=True
korduste_limiit=1
t=0
while len(l)>samm:#korduste arv
    if i==korduste_limiit:
        i=1
        G=0
        for p1 in range(0,len(l),samm):
            G+=l[p1]
        print("kehade süsteemi kui terviku:\nm_res=",G,"kilogrammi")
        G=0
        for p1 in range(1,len(l),samm):
            G+=l[p1]
        print("q_res=",G,"kulonit")#impulss ,energia(ka pot kui on määratud põrkeks vajalik kaugus)
        G=0
        for p1 in range(0,len(l),samm):
            k=0
            for p2 in range(a+1+p1,samm+p1,2):#i võib ümber nimetada$
                k+=l[p2]**2#k=v**2 on kiiruse ruut
            G+=l[p1]*k#m*v**2
        print("E_kin_res=(Σm_n*v_n_dim**2)/2=",G/2,"džauli)")
        for mõõde in range(a,samm,2):#valib mõõtme
            G=0
            for p1 in range(0,len(l),samm):#valib keha
                G+=l[p1]*l[p1+mõõde+1]
            print(str(mõõde//2)+".mv_res=",G,end=(" ;"))
        print("\n")
        dif=float(input("Sisesta ajadiferentsiaali suurus:"))#saab iga uute punktide leidmise järel muuta#$muuta pöördvõrdeliseks kiireima keha kiirusega.
        G=10**-11*6.67384*dif**2#kas skript saaks kasutada ainult konstandite suhet$?
        k=10**9*8.551787368*dif**2#kui korrutada kõik laegud läbi ruutjuurega k´st?-laengutel olex rohkem komasi;ON 2 KORDA VÄIKSEM konstandist ,SEST s=(a*t**2)/2
        I_toorik=input("Mitu korda diferentseerida(kui tahate kuni kõik punktid on samas kohas jätke lahter tühjaks):")#I_tooriku asemel võiks olla korduste_limiit!?
        n=int(input("Iga mitmes diferentseerimine printida:"))
#        if input("kas kirjutada tulemused txt faili")=="1":
            #
        print("")
        if I_toorik.isdigit():#korrutab kiirused aja diferentsiaalidega läbi.
            korduste_limiit=int(I_toorik)+1
        print("t=",t)
        for p1 in range(0,len(l),samm):
            print("m="+str(l[p1])+"; q="+str(l[1+p1]),end=" ;  ")#jäävad tühikud lõppu
            for mõõde in range(a,samm,2):
                print(str(mõõde//2)+".s="+str(l[p1+mõõde])+";",str(mõõde//2)+".v="+str(l[p1+mõõde+1]),end="; ")# v*dif peax olema?! #Kas kuvada keskmine või lõpukiirus aja dt jooksul
            print("")
            for p2 in range(a+1,samm+1,2):#TEHA ALATI LÄBI PEALE dif´i MUUTMIST.
                l[p1+p2]=l[p1+p2]*dif
        print("")
    b=i%n==0#ütleb et, kas on vaja printida.
    t+=dif
    if b:
        print("t=",t)
    i+=1
    for p1 in range(0,len(l),samm):#võtab järjest punktmassi alguse indekseid
        for p2 in range(p1+samm,len(l),samm):#p2 on alati suurem kui p1
            I_toorik=0
            for mõõde in range(a,samm,2):#kehade vahelise kauguse ruut = r**2
                I_toorik+=(l[p1+mõõde]-l[p2+mõõde])**2
            if I_toorik==0:#kui asuvad samas kohas # PEAX OLEMA ET KUI KAUGUS ON VÄIKSEM KUI PÕRKEKS VAJALIK KAUGUS
                print("punktid kattuvad")
                if ep1!=p1:#ei ole sama p1 mis eelmisel.
                    ep1=p1#eelmine p1 tuleb määrata,nagu ongi,võrdluse ja väätustamise vahel
                    liit+=[p1,p2]#pole vajalik ega võimalik omavahelist mõju määrata#loendi liit lisatakse õigeid asju
            else:#leiab punktide kiirenduste ja aja diferentsiaali ruudu korrutised.
                I_toorik=(l[p1]*l[p2]*G-l[1+p1]*l[1+p2]*k)/I_toorik**1.5#(m1*m2*G-q1*q2*k)*dt**2/(r**3)
                II_toorik=I_toorik/l[p1]#(m2*G-q1*q2*k/m1)*dt**2/r**3=a1*dt**2/(r*2)
                I_toorik=I_toorik/l[p2]#(m1*G-q1*q2*k/m2)*dt**2/r**3=a2*dt**2/(r*2)
                for mõõde in range(a,samm,2):#muudab kiirusi
                    l[1+p1+mõõde]+=II_toorik*(l[p2+mõõde]-l[p1+mõõde])#v1=v_10+a*dt**2=(m2*G-q1*q2*k/m1)*dt**2*l/r**3=a1*dt**2*l/(r*2)
                    l[1+p2+mõõde]+=I_toorik*(l[p1+mõõde]-l[p2+mõõde])#v2=v_20+a*dt**2
        for mõõde in range(a+p1,samm+p1,2):#muudab asukohti
            l[mõõde]+=l[1+mõõde]#s_l=s_l0+v_l*dt#vaja ainult p1´ga.  #algiiruse nihe ei sõltu aja diferentsiaali suurusest!!!
        if graaf:#turtle graafika.
            if samm-a==2:#kui on üks dimensioon
                l[p1+2].goto(0,l[a+p1]*mõõtkava)#näitab nagu oleks õiges kohas aga turtle ekraanil on vales kohas!
                input("peaks olema kohas:"+str(l[a+p1]*mõõtkava))#
            elif samm-a>=4:#kui on 2 dimensioooni
                print(l[p1+2],".goto",(l[a+p1]*mõõtkava,",",l[a+p1+2]*mõõtkava))#
                l[p1+2].goto(l[a+p1]*mõõtkava,l[a+p1+2]*mõõtkava)
        if b:
            print("m="+str(l[p1])+"; q="+str(l[1+p1]),end=" ;  ")#jäävad tühikud lõppu
            for mõõde in range(a,samm,2):
                print(str(mõõde//2)+".s="+str(l[p1+mõõde])+";",str(mõõde//2)+".v="+str(l[p1+mõõde+1]/dif),end="; ")# v*dif peax olema?! #Kas kuvada keskmine või lõpukiirus aja dt jooksul
            print("")
    if b:
        print("")
    #siia teha punktide liitmine
    liit=[]
