#l=[X,Y,Z,x,y,z,m,q,X,Y,Z,x,y,z, m,q,X, Y,Z,x,y,z,m,q,X,Y,Z,x,y,z,m,q]#a on kiirendus;v on kiirus;m on mass;q on laeng.
#l= [1,2,3,0,1,0,1,0,0,5,6,7,0,7,20,0,0,-7,2,0,2,3,3,5,0,0,0,0,0,0,4,0]#4 gruppi ehk 32 elementi;[X,Y,Z,vx,vy,vz,m,q]
#kunagi võiks teha ka muu arvu dimensiioonidega töötavaks!
#l=[0,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0]
#l=[0,-25,0,0,0,0,1,0,0,6372805,0,0,0,0,5973600000000000000000000,0]#õun ja maa
def küsi_punkt():
    return([float(input("kordinaadid:\nX:")),float(input("Y:")),float(input("Z:")),float(input("kiiruste projektsioonid:\nx:")),float(input("y:")),float(input("z:")),float(input("\nmass:")),float(input("laeng:"))])
    print("")
def küsi_punkte():#teha võimalus sisestada määratud kehi...
    l=küsi_punkt()
    l+=küsi_punkt()
    while input("kas sisestada punktmasslaeng?") in ["jah","1","ja","sisestada"]:#teha eri ühikud
        l+=küsi_punkt()
    return(l)
def küsi_ühikutega_punkte(l=[]):#konstandiga vordelise (muutuja) muutmine q puhul ainult
    l2=[]
    while input("kas sisestada punktmasslaeng?") in ["jah","1","ja","sisestada"]:
        u=["X","Y","Z","x-kiirus","y-kiirus","z-kiirus","mass","laeng"]#järjekorda saab vahetada lastes skripti korra teisest texti töötlus skriptist läbi.
        print("Sisesta: \"SUURUS*ÜHIK\"")
        for i in range(0,8):
            p=input(u[i]).split("*")
#        if len(p)==1:
    l+=l2
l=küsi_punkte()
print("kehasi on:",len(l)/8)
liit=[]
#import Turtle
druut=float(input("Sisesta ajadiferentsiaali suurus:"))**2
G=10**-11*6.67384*druut#kas skript saaks kasutada ainult konstandite suhet?
k=10**9*8.9875517873681764*druut#kui korrutada kõik laegud läbi ruutjuurega k´st?-laengutel olex rohkem komasi
n=int(input("Iga mitmes diferentseerimine printida:"))
korduste_limiit=int(input("Mitu korda diferentseerida(kui tahate kuni kõik punktid on ,ilma piiranguta, samas kohas jätke lahter tühjaks:"))
i=0
while len(l)>=8 and i != korduste_limiit:#korduste arv
    b=i%n==0
    if b:
        print("t=",i*druut)
    i+=1
    for j1 in range(0,len(l),8):
        for j2 in range(j1+8,len(l),8):#j2 on alati suurem kui
            if l[j1]==l[j2] and l[1+j1]==l[1+j2] and l[2+j1]==l[2+j2]:#kui kaks keha asuvad samal kohal #aga kui on ligilähedased?
                print("Paneb liitmiseks kirja",j1,j2)
                liit+=[j1,j2]
            else:
                I_toorik=(l[7+j1]*l[7+j2]*k+G*l[6+j1]*l[6+j2])/(((l[j1]-l[j2])**2+(l[1+j1]-l[1+j2])**2+(l[2+j1]-l[2+j2])**2)**1.5)#(q1*q2*k+G*m1*m2)/r**3 ; kui kordinaadid on samad tekib 0iga jagamine! võiks hoopis punktid liita!#8ne
                II_toorik=I_toorik/l[6+j1]#See POLE resunalt kiirus , ega kiiruse absoluutväärtus.
                l[3+j1]+=II_toorik*(l[j2]-l[j1])#esimese punktmasslaengu kiiruse muutmine x-teljel
                l[4+j1]+=II_toorik*(l[1+j2]-l[1+j1])#esimese punktmasslaengu kiiruse muutmine y-teljel
                l[5+j1]+=II_toorik*(l[2+j2]-l[2+j1])#esimese punktmasslaengu kiiruse muutmine z-teljel
                II_toorik=I_toorik/l[6+j2]#(q1*q2*k+G*m1*m2)/(r**3*m2)
                l[3+j2]+=II_toorik*(l[j1]-l[j2])#teise punktmasslaengu kiiruse muutmine x-teljel
                l[4+j2]+=II_toorik*(l[1+j1]-l[1+j2])#teise punktmasslaengu kiiruse muutmine y-teljel
                l[5+j2]+=II_toorik*(l[2+j1]-l[2+j2])#teise punktmasslaengu kiiruse muutmine z-teljel
        l[j1]+=l[3+j1]#s_x=v_x*dt
        l[1+j1]+=l[4+j1]
        l[2+j1]+=l[5+j1]#vaja ainult j1ga
        if b:
            print("X:"+str(l[j1]),"Y:"+str(l[1+j1]),"Z:"+str(l[2+j1]),"vx:"+str(l[3+j1]),"vy:"+str(l[4+j1]),"vz:"+str(l[5+j1]),"m:"+str(l[6+j1]),"q:"+str(l[7+j1]))
    if b:
        print("")
    while len(liit) != 0:#liidab punkte
        l[6+liit[0]]+=l[6+liit[1]]#m_uus=m1+m2 OK
        l[3+liit[0]]=(l[3+liit[0]]*l[6+liit[0]]+l[6+liit[1]]*l[3+liit[1]])/l[6+liit[0]]#v_x_uus=(m1*v1_x+m2*v2_x)/m_uus
        l[4+liit[0]]=(l[4+liit[0]]*l[6+liit[0]]+l[6+liit[1]]*l[4+liit[1]])/l[6+liit[0]]#v_y_uus=(m1*v1_y+m2*v2_y)/m_uus
        l[5+liit[0]]=(l[5+liit[0]]*l[6+liit[0]]+l[6+liit[1]]*l[5+liit[1]])/l[6+liit[0]]#v_z_uus=(m1*v1_z+m2*v2_z)/m_uus
        l[7+liit[0]]+=l[7+liit[1]]#q_uus=q1+q2
        del l[liit[1]],l[liit[1]],l[liit[1]],l[liit[1]],l[liit[1]],l[liit[1]],l[liit[1]],l[liit[1]],liit[0],liit[1]#kustutab punkti,mis liideti teisele ja liitmiste järjendi 2esimest.
