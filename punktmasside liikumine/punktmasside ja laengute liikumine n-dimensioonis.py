#l=[m,q,X,x,Y,y,m,q,X,x,Y,y,m,q,X,x,Y,y,m,q,X,x,Y,y,m,q,X,x,Y,y,m,q,X,x,Y,y,m,q,X,x,Y,y]#a on kiirendus;v on kiirus;m on mass;q on laeng.
#l= [1,2,3,0,1,0,1,0,0,5,6,0,5,7,2,0,0,7,2,0,2,3,3,5,0,0,0,0,0,7]#5 gruppi ehk 30 elementi;[X,Y,Z,vx,vy,vz,m,q]
#l=[1,0,-25,0,5973600000000000000000000,0,-6372805,0]#õun ja maa
#l=[1,0,-1,0,1,0,0,0,1,0,1,0]#!-probleem ?-küsimus $-idee
def küsi_punkt():
    lugeja=0
    l=[float(input("sisesta mass:"))]
    while l[0]==0:
        print("Kui punkmassi mass=0 ,siis ei mõjuta keha teisi kehi ja keha asukoht ajahetkel on määramatu  või algne,seega pole tarvis selle keha muid omadusi sisestada.\n")
        l=[float(input("sisesta mass:"))]
    l.append(float(input("sisesta laeng:")))
    while samm != lugeja:
        l+=[(float(input(("sisesta ")+str(lugeja+1)+(".dimensiooni kordinaat:")))),(float(input(("sisesta kiirus ")+str(lugeja+1)+".dimensiooni projektsioonis:")))]
        lugeja+=1
    print("")
    return(l)
def küsi_punkte():#$teha võimalus sisestada määratud kehi
    print("")
    l=küsi_punkt()
    l+=küsi_punkt()
    while input("kas sisestada veel üks punktmasslaeng?") in ["jah","1","ja","sisestada","Y"]:#teha eri ühikud
        l+=küsi_punkt()
    print("")
    return(l)
liit=[]
#import Turtle#$#KÜSIDA MIHKELSONILT KUIDAS SAAB LUUA n KILPKONNA
samm=int(input("Sisesta dimensioonide arv:"))#(s-2)/2=s/2-1
l=küsi_punkte()
samm+=samm+2
print("kehasi on:",(len(l))/samm)
druut=float(input("Sisesta ajadiferentsiaali suurus:"))**2
G=10**-11*6.67384*druut#kas skript saaks kasutada ainult konstandite suhet$?
k=10**9*8.9875517873681764*druut#kui korrutada kõik laegud läbi ruutjuurega k´st?-laengutel olex rohkem komasi
druut=druut**0.5
n=int(input("Iga mitmes diferentseerimine printida:"))
korduste_limiit="0"
korduste_limiit+=input("Mitu korda diferentseerida(kui tahate kuni kõik punktid on samas kohas jätke lahter tühjaks):")
korduste_limiit=int(korduste_limiit)+1
print("")
i=1
while len(l)>=samm and i != korduste_limiit:#korduste arv
    b=(i-1)%n==0#ütleb et, kas on vaja printida.
    if b:
        print("t=",i*druut)
    i+=1
    for j1 in range(0,len(l),samm):
        for j2 in range(j1+samm,len(l),samm):#j2 on alati suurem kui j1
            for mõõde in range(2,samm,2):
                if l[j1+mõõde] != l[j2+mõõde]:#kolmes kohas on kordinaatide projektsioonide erinevusi vaja
                    I_toorik=0
                    for mõõde in range(2,samm,2):#salvestab eelmise mõõtme andja poolt antud mõõtme üle,nagu peabki
                        I_toorik+=(l[j1+mõõde]-l[j2+mõõde])**2
                    I_toorik=(l[j1]*l[j2]*G-l[1+j1]*l[1+j2]*k)/I_toorik**1.5
                    II_toorik=I_toorik/l[j1]
                    I_toorik=I_toorik/l[j2]
                    for mõõde in range(2,samm,2):#muudab kiirusi #kirjutab punkti liitmis kontrolli mõõtmeandja mõõtmed üle, nagu peabki#kas oleks kiirem kui võta muutuja samm-2?
                        l[1+j1+mõõde]+=II_toorik*(l[j2+mõõde]-l[j1+mõõde])
                        l[1+j2+mõõde]+=I_toorik*(l[j1+mõõde]-l[j2+mõõde])
                    break
                elif mõõde == samm-2 and l[1+j1]==l[1+j2]:#vahet pole kas if või elif#kui kõik kordinaadid on samad siis määratakse punktid liitmisele#ei toimi
                    print("LIIDAB PUNKTID:\nm:"+str(l[j1]),"; q:"+str(l[1+j1]),end=" ;")
                    print("m:"+str(l[j1]),";q:"+str(l[1+j1]),end=" ;  ")
                    for mõõde in range(2,samm,2):
                        print(str(mõõde//2)+".ds="+str(l[j1+mõõde])+";",str(mõõde//2)+".dv="+str(l[j1+mõõde+1]),end="; ")# v*d peax olema?!
                    print("")
                    liit+=[j1,j2]
        for mõõde in range(2,samm,2):
            l[mõõde+j1]+=l[1+j1+mõõde] #s_l=v_l*dt #vaja ainult j1ga
        if b:
            print("m:"+str(l[j1]),"q:;"+str(l[1+j1]),end=" ;  ")
            for mõõde in range(2,samm,2):
                print(str(mõõde//2)+".ds="+str(l[j1+mõõde])+";",str(mõõde//2)+".dv="+str(l[j1+mõõde+1]),end="; ")# v*d peax olema?!
            print("")
    if b:
        print("")
    while len(liit) != 0:#liidab punkte
        I_toorik=0
        while I_toorik!=samm:
            l[3+liit[0]]=(l[liit[0]]*l[3+liit[0]]+l[liit[1]]*l[3+liit[1]])/(l[liit[0]]+l[liit[1]])#v_x_uus=(m1*v1_x+m2*v2_x)/(m_1+m_2)#?!
            del l[liit[0]+2],l[liit[0]+3]#l_keha1,v_keha1
            I_toorik+=2
        l[liit[0]]+=l[liit[1]]#m_uus=m1+m2 OK
        del liit[0],liit[1]#kustutab punkti,mis liideti teisele ja liitmiste järjendi 2esimest.
