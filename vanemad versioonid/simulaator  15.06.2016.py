# coding=utf-8
__author__ = 'Olger'
from tkinter import *
from tkinter import ttk
from  math import log#vaja energia arvutamiseks
#lisada N-keha probleemi vorrandite valjastamise voimalus
#panna progressbar tööle
#praegune ajahetk teha automaatselt muutuvaks
#leida mingi austsüsteem millesse konvetrides viga võimalikult väike tuleks, näiteks selline kus resimpulss ja massikese on 0. Teha arvutused alles selles süsteemis ja lõpuks ümber konvertida kuvamiseks.
#Kui pöörata graafilist liidese vaadet nii, et aeg on üks ruumi koordinaatidest tuleb arvestada, et kaugus ei aegruumis ega eukleuidilises spatial ruumis ei ole võrdeline kaugusega ekraanil.
#Graafilise liidese puhul SRis arvestada, et uues taustsüsteemis muutub ka ajasammu pikkus
ll=[]
#ll=[1.989e+30, 0.0,"Paike", 0.0, 0.0, 0.0, 0.0, 5.9736e+24, 0.0, "Maa", 152097701000.0, 0.0, 0.0,29291]
a=3#a naitab ,et kui palju arve on punktmasslaengu kirjeldamiseks kasutatud enne asukohti ja kiiruseid.
graaf=False
p2=False
liit=[]
dif_0=1
dif=1

class HidingScrollBar(ttk.Scrollbar):
    """
    Kerimisriba, mis end ise ära peidab, kui seda ei vajata
    """
    def set(self, lo, hi, *args):
        """
        Kerimisriba parameetrite seadmine koos vajadusel riba peitmise või näitamisega
        """
        # Kui element on juba piisavalt suur terve sisu mahutamiseks
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # ... eemaldame kerimisriba
            self.grid_remove()
        else:
            # Vastasel juhul taastame selle
            self.grid()

        super().set(lo, hi, *args)
class Table(ttk.Frame):
    def createCell(self, row, column, data,r="solid"):
        """
        Tabelis uue lahtri loomine
        """
        label = ttk.Label(self.frame, text=str(data), borderwidth=1, relief=r)
        label.grid(row=row, column=column, sticky=N+S+W+E, ipadx=5, ipady=1)
        self.labels[row][column] = label
    def onFrameConfigure(self, event):
        """
        Kui sisemise raami suurus (tabeli elementide arv või kõrgus-laius) muutub,
        peame Canvasele kerimise toimimiseks andma teada uue ala suuruse
        """
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
    def __init__(self, master, data=None, *args, **kwargs):
        """
        Tabeli loomiseks vajalike elementide algseadistamine
        """
        super().__init__(master, **kwargs)

        # Loome Canvas'e, sest see toetab kerimisribasid
        self.canvas = Canvas(self)
        # Canvas võtab tema ümber oleva raami suuruse (sellesama raami, millele ehitame üles oma klassi)
        self.canvas.grid(row=0, column=0, padx=4, pady=4, sticky=N+S+W+E)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Canvase sisse omakorda loome uue raami, et hakata sellesse paigutama tabelilahtreid
        self.frame = ttk.Frame(self.canvas)
        self.canvas.create_window(0, 0, anchor=N+W, window=self.frame)
        # Kui raami suurus peaks muutuma, anname sellest teada ka Canvasele, et uuendataks kerimisribadega seonduvat
        self.frame.bind('<Configure>', self.onFrameConfigure)

        # Kerimisribad ning nendega seotud käskude sidumine Canvasega
        self.verticalScrollbar = HidingScrollBar(self, orient='vertical', command=self.canvas.yview)
        self.horizontalScrollbar = HidingScrollBar(self, orient='horizontal', command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.verticalScrollbar.set, xscrollcommand=self.horizontalScrollbar.set)

        # Kerimisribade paigutus välimise raami sees
        self.verticalScrollbar.grid(row=0, column=1, sticky=N+S)
        self.horizontalScrollbar.grid(row=1, column=0, sticky=W+E)
        self.columnconfigure(1, weight=0)
        self.rowconfigure(1, weight=0)

        # List, mis hoiab lahtreid kujutavaid Label'eid
        self.labels = []

        # Kui konstruktor sai andmeid, joonistame nende põhjal tabeli välja
        if data:
            self.drawTable(data)
    def addRow(self, rowData, r="solid"):
        """
        Lisab tabeli lõppu uue rea
        """
        self.labels.append([])
        for colIndex in range(len(rowData)):
            self.labels[-1].append(None)
            self.createCell(len(self.labels) - 1, colIndex, rowData[colIndex], r=r)
    def clearTable(self):
        """
        Tühjendab tabeli andmetest (kustutades lahtreid kujutavad Label elemendid)
        """
        for row in self.labels:
            for label in row:
                label.destroy()
        self.labels = []
def uuenda_ja_lisa(mass, laeng, nimi, sisendid, l, samm, punkte, res_mass, res_laeng, res_massikese, res_impulsid, res_energia, res_momendid, tabel):
    global ll
    lisatav=[mass,laeng,nimi]
    for sisend in range(0,int(eraldi_mootmete_sisend.get())*2,2):
        lisatav+=[float(sisendid[sisend].get()),float(sisendid[sisend+1].get())]
    lisa(lisatav)
    print(ll)
    tabel.addRow([lisatav.pop(2)] + lisatav)
    uuenda_omadused(ll,samm,1,punkte,res_mass,res_laeng,res_massikese,res_impulsid,res_energia,res_momendid)
def leia_jou_tegurid(dim,GEM,G=(6.67384*10**-11),epsilon_0=(8.85418781762*10**-12),c_valguskiirus=299792458):
    from math import gamma,pi
    A_sfaar=2*pi**(dim/2)/gamma(dim/2)#dim-1 mootmelise sfaari suurus ilma raadiust arvestmata
    del gamma
    G=G*4*pi/A_sfaar
    k=1/(A_sfaar*epsilon_0)#Sfaari suuruse ja elektrilise konstandi korrutise pöördvaartus#Kolme mootme puhul 8,9875517873681764*10**9 #8.854187817620*10**-12=vaakumi dielektriline labistatavus
    if GEM:
        G=G/c_valguskiirus**2
        k=k/c_valguskiirus**2
    return (G,k)
def uuenda_omadused(l,samm,dif,punkte,res_mass,res_laeng,res_massikese,res_impulsid,res_energia,res_momendid):
    punkte.set(str(len(l)//samm))
    res_mass.set(str(resunalt_mass(l,samm)))
    res_laeng.set(str(resunalt_laeng(l,samm)))
    arvuta_res_impulsid(l,samm,dif,res_impulsid)
    #res_energia.set(arvuta_energia(ll,samm,dif,float(jou_mootmete_sisend.get())))
    arvuta_impulsimomedid(l,samm,arvuta_massikese(ll,samm,res_mass,res_massikese),dif,res_momendid)
def arvuta_energia(l,samm,dif,dim):
    if dim==2:
        from math import log
    E=0
    for punktmass1 in range(0,len(l),samm):
        for moode in range(a,samm,2):
            E+=l[punktmass1]*l[punktmass1+moode+1]**2/2
        for punktmass2 in range(0,punktmass1,samm):
            r=0
            for moode in range(a,samm,2):
                r+=(l[punktmass1+moode]-l[punktmass2+moode])**2
            if dim==2:
                E+=(G*l[punktmass1]*l[punktmass2]-k*l[punktmass1+1]*l[punktmass2+1])*math.log(r)/2
            else:
                E+=(1-r**(2-dim*2))*(G*l[punktmass1]*l[punktmass2]-k*l[punktmass1+1]*l[punktmass2+1])/(dim-2)
    return(E)
def arvuta_massikese(l,samm,res_mass,res_massikese):
    if res_mass.get()!="0.0":
        massikeskme_jarjend=[]
        for moode in range(a,samm,2):#Selle saab panna ehk kokku impulsi leidmise tsukliga$
            mr=0
            for p1 in range(0,len(l),samm):
                mr+=l[p1+moode]*l[p1]
            mr=mr/float(res_mass.get())
            massikeskme_jarjend.append(mr)#jarjendisse liit pannakse massikeskme asukoht koigis dimensioonides
        return(massikeskme_jarjend)
    else:
        for lunk in res_massikese:
            lunk.set("maaramatu")
        return(False)
def arvuta_res_impulsid(l,samm,dif,res_impulsid):
    for moode in range(a,samm,2):
        impulss=0
        for p1 in range(0,len(l),samm):
            impulss+=l[p1+moode+1]*l[p1]
        res_impulsid[moode//2-1].set(str(impulss/dif))
def arvuta_impulsimomedid(l,samm,massikeskme_jarjend,dif,res_momendid):
    i=0
    if massikeskme_jarjend:
        for moode1 in range(a,samm,2):
            for moode2 in range(moode1+2,samm,2):
                impulsimoment=0
                for punktmass in range(0,len(l),samm):
                    impulsimoment+=((massikeskme_jarjend[moode2//2-1]-l[punktmass+moode2])*l[punktmass+moode1+1]-(massikeskme_jarjend[moode1//2-1]-l[punktmass+moode1])*l[punktmass+moode2+1])*l[punktmass]
                    #print("-(",massikeskme_jarjend[moode1//2-1],"-",l[punktmass+moode1],")*",l[punktmass+moode2+1],"+(",massikeskme_jarjend[moode2//2-1],"-",l[punktmass+moode2],")*",l[punktmass+moode1+1],"))*",l[punktmass])
                res_momendid[i].set(str(impulsimoment/dif))
                i+=1
    else:
        for moment in res_momendid:
            moment.set("maaramatus")
def resunalt_mass(l,samm):
    mass=0
    for massi_indeks in range(0,len(l),samm):
        mass+=l[massi_indeks]
    return (mass)
def resunalt_laeng(l,samm):
    laeng=0
    for laengu_indeks in range(1,len(l)+1,samm):
        laeng+=l[laengu_indeks]
    return (laeng)
def uuenda_loend(l,samm,dif):
    tabel.clearTable()
    tabel.addRow(veergude_nimed,r="raised")#lisab veergude nimed
    for punktmasslaeng in range(0,len(l),samm):
        rida_loendis=l[punktmasslaeng:][:(a-1)]
        for v in range(a+punktmasslaeng,samm+punktmasslaeng,2):
            rida_loendis.append(l[v])
            rida_loendis.append(l[v+1]/dif)
        tabel.addRow([l[punktmasslaeng+a-1]]+rida_loendis)
def muuda_kasutajaliidest_simuleeri():
    simuleeri(ll,int(eraldi_mootmete_sisend.get()),float(jou_mootmete_sisend.get()),int(GEM_sisend.get()),gravitatsiooniline_sisend.get(),elektriline_sisend.get(),int(kordusi_sisend.get()),float(t_0_sisend.get()),float(t_1_sisend.get()),iga_mitmes_samm_kirja_sisend.get())
def loo_sisestamis_GUI(B):
    global ll
    sisendid=[]
    eraldi_mootmete_sisend.configure(state="readonly")
    samm=int(eraldi_mootmete_sisend.get())
    Button(raam,command=muuda_kasutajaliidest_simuleeri,text="kaivita simulatsioon").grid(row=16+samm*2,sticky=(W))
    pb = ttk.Progressbar(raam, orient="horizontal", length=200, mode="determinate")
    pb.grid(column=0,row=16+samm*2,sticky=(N,E),columnspan=2)
    ttk.Label(raam, text="nimi:").grid(column=0, row=12,sticky=(N, W))
    nime_sisend=ttk.Entry(raam)
    nime_sisend.grid(row=12,column=1,sticky=(W, E))
    ttk.Label(raam, text="mass:").grid(column=0, row=13,sticky=(N, W))
    massi_sisend=ttk.Entry(raam)
    massi_sisend.grid(row=13,column=1,sticky=(W, E))
    ttk.Label(raam, text="laeng:").grid(column=0, row=14,sticky=(N, W))
    laengu_sisend=ttk.Entry(raam,text="")
    laengu_sisend.grid(row=14,column=1,sticky=(W, E))
    laengu_sisend.insert(0,"0")
    global tabel,veergude_nimed
    tabel = Table(raam)
    res_massikese=[]
    res_impulsid=[]
    res_momendid=[]
    veergude_nimed=["Nimi","mass","laeng"]
    for moode in range(0,samm):
        sisendid.append(ttk.Entry(raam))
        sisendid[moode*2].grid(row=15+moode*2,column=1)
        sisendid[moode*2].insert(0,"0")
        ttk.Label(raam, text=(str(1+moode)+". s:")).grid(column=0, row=15+moode*2,sticky=(N, W))
        sisendid.append(ttk.Entry(raam))
        sisendid[moode*2+1].grid(row=16+moode*2,column=1)
        sisendid[moode*2+1].insert(0,"0")
        ttk.Label(raam, text=(str(1+moode)+". v:")).grid(column=0, row=16+moode*2,sticky=(N, W))
        veergude_nimed.append(str(1+moode)+".s")
        veergude_nimed.append(str(1+moode)+".v")
        ttk.Label(raam, text=(str(1+moode)+". mootme impulss=")).grid(column=3, row=15+moode,sticky=(N, W))
        res_impulsid.append(StringVar())
        Label( raam, textvariable=res_impulsid[moode], relief=SUNKEN ).grid(row=15+moode,column=4, sticky=(N, W))
        res_impulsid[moode].set("0")
        for moode2 in range(moode+1,samm,1):
            ttk.Label(raam, text=(str(moode+1)+"&"+str(moode2+1)+"mootme impulsimoment=")).grid(row=12+len(res_momendid),column=5,sticky=(N, E))
            res_momendid.append(StringVar())
            Label( raam, textvariable=res_momendid[len(res_momendid)-1], relief=SUNKEN ).grid(row=(11+len(res_momendid)),column=6,sticky=(N, E))
            res_momendid[len(res_momendid)-1].set("maaramatu")
    uuenda_loend(ll,samm*2+a,1)
    Button(raam,text="kustuta punktmass").grid(row=11,column=1,padx=0,sticky=(N,E))#TODO teha punktmasside kustutamise nupp toimivaks
    B.config(command=lambda:uuenda_ja_lisa(float(massi_sisend.get()), float(laengu_sisend.get()), nime_sisend.get(), sisendid, ll, samm * 2 + a, punkte, res_mass, res_laeng, res_massikese, res_impulsid, res_energia, res_momendid, tabel))
    if samm>1:
        Button (raam, text="uuenda(muutused ajas arvutusveast)", command=lambda:uuenda_omadused(ll,samm*2+a,dif,punkte,res_mass,res_laeng,res_massikese,res_impulsid,res_energia,res_momendid)).grid(row=11,column=5,padx=0,columnspan=2,sticky=(N,E))
    else:
        Button(raam,text="uuenda\n(muutused ajas\narvutusveast)",command=lambda:uuenda_omadused(ll,samm*2+a,dif,punkte,res_mass,res_laeng,res_massikese,res_impulsid,res_energia,res_momendid)).grid(row=11,column=5,padx=0,columnspan=2,rowspan=2,sticky=(N,E))
    tabel.grid(columnspan=5, column=3, rowspan=11, row=0, sticky=(N, W))
    ttk.Label(raam, text="Susteemi konstantsed suurused:").grid(column=3, row=11, padx=5, pady=0,columnspan=2)
    ttk.Label(raam, text="punktmasslaengute arv=").grid(column=3, row=12, pady=0, sticky=(N, W))
    punkte = StringVar()
    Label( raam, textvariable=punkte, relief=SUNKEN ).grid(row=12,column=4, sticky=(N, W))
    punkte.set("0")
    ttk.Label(raam, text="resunalt mass=Σ(m_i)=").grid(column=3, row=13, pady=0, sticky=(N, W))
    res_mass = StringVar()
    Label( raam, textvariable=res_mass, relief=SUNKEN ).grid(row=13,column=4, sticky=(N, W))
    res_mass.set("0")
    ttk.Label(raam, text="resunalt laeng=Σ(q_i)=").grid(column=3, row=14, sticky=(N, W))
    res_laeng = StringVar()
    Label( raam, textvariable=res_laeng, relief=SUNKEN ).grid(row=14,column=4, sticky=(N, W))
    res_laeng.set("0")
    ttk.Label(raam, text="energia=Σ(E_i)=").grid(column=3, row=16+samm*2, pady=0, sticky=(N, W))
    res_energia=StringVar()
    Label( raam, textvariable=res_energia, relief=SUNKEN ).grid(row=16+samm*2,column=4, sticky=(N, W))
    res_energia.set("0")
    nullnivoo=StringVar()
    Epot1="punktmasslaengud uksteisest lopmatult kaugel"
    Epot2="punktmasslaengud uksteisest kaugusel 0"
    Epot3="maksimaalne kineetiline ,mis susteemil voib energia jaavuse seaduse poolest olla"
    Epot4="punktmasslaengud uksteisest kaugusel:"
    if samm>2:
        nullnivoo_menuu=ttk.OptionMenu(raam,nullnivoo,Epot1,Epot1,Epot2,Epot3,Epot4)
        nullnivoo_menuu.grid(column=5,columnspan=2, row=16+samm*2, sticky=(N))
        nullnivoo_menuu.config(width=22)
        ttk.Label(raam, text="pot. energia 0-nivooga").grid(column=5, row=16+samm*2, sticky=(N, W))
    else:
        nullnivoo_menuu=ttk.OptionMenu(raam,nullnivoo,"Potensiaalse energia nullnivooga "+Epot1,"Potensiaalse energia nullnivooga "+Epot1,"Potensiaalse energia nullnivooga "+Epot2,"Potensiaalse energia nullnivooga "+Epot3,"Potensiaalse energia nullnivooga "+Epot4)
        nullnivoo_menuu.grid(column=5,columnspan=2 ,row=16+samm*2,sticky=(W,N))
        if samm==2:
            nullnivoo_menuu.config(width=28)
        elif samm<2:
            nullnivoo_menuu.config(width=4)
    nullnivoo_sisend=ttk.Entry()
    nullnivoo_sisend.config(width=5)
    nullnivoo_sisend.grid(column=6, row=16+samm*2, sticky=(N, E))
def lisa(lisatav):
    global ll
    if int(eraldi_mootmete_sisend.get())*2+a==len(lisatav):
        ll+=lisatav
    else:
        quit("lisatava pikkus ei klapi eraldia arvestavate mootmete arvuga")
def analuutiline_lahend():
    return(False)
def simuleeri(l,eraldi_mootmeid,dim,mudel,gravitatsiooniline,elektriline,kordusi,t,t_1,data):
    global dif_0
    samm=eraldi_mootmeid*2+a
    dim=dim/2
    G,k=leia_jou_tegurid(dim*2,mudel)
    dif=(t_1-t)/kordusi
    if mudel:
        c_valguskiirus=299792458#valguskiirus "SI" susteemis
    Gt2=G*dif**2
    kt2=k*dif**2
    l=korruta_aja_difertentsaaliga_ajakudsed_tuletised(l,samm,dif/dif_0)
    dif_0=dif
    if analuutiline_lahend():
        pass#ajutine
    else:
        t+=float(t_0_sisend.get())
        if gravitatsiooniline:
            if elektriline:
                if mudel==1:
                    def muuda_v(l,p1,p2,siht):
                        c2_miinus_v2=c_valguskiirus**2
                        vXx=0
                        for moode in range(a,samm,2):
                            delta_v=l[1+p2+moode]-l[1+p1+moode]#kiiruste vahe
                            c2_miinus_v2+=delta_v**2#vektor v pikkuse ruut
                            vXx+=delta_v*(l[p2+moode]-l[p1+moode])#v ja x skalaar korrutis
                        tegur_jagatud_kaugus_astmes=(l[1+p1]*l[1+p2]*kt2-l[p1]*l[p2]*Gt2)/siht**dim
                        c2_miinus_v2=c2_miinus_v2*tegur_jagatud_kaugus_astmes
                        vXx=vXx*tegur_jagatud_kaugus_astmes
                        for moode in range(a,samm,2):
                            a_p1=vXx*(l[1+p2+moode]-l[1+p1+moode])-c2_miinus_v2*(l[p2+moode]-l[p1+moode])#(l[p2+moode]-l[p1+moode]) on deltaX_D ehk punktide vahelise vektori projektsioon kindlal mootmel
                            a_p2=-a_p1/l[p2]
                            a_p1=a_p1/l[p1]
                            l[1+p1+moode]+=a_p1#v1=v_10+a*dt**2=(m2*G-q1*q2*k/m1)*dt**2*l/r**3=a1*dt**2*l/(r**2)
                            l[1+p2+moode]+=a_p2#v2=v_20+a*dt**2
                        return(l)
                elif mudel==0:
                    def muuda_v(l,p1,p2,siht):
                        a_p1=(l[p1]*l[p2]*Gt2-l[1+p1]*l[1+p2]*kt2)/siht**(dim)#(m1*m2*G-q1*q2*k)*dt**2/(r**3)
                        a_p2=a_p1/l[p1]#(m2*G-q1*q2*k/m1)*dt**2/r**3=a1*dt**2/(r**2)
                        a_p1=a_p1/l[p2]#(m1*G-q1*q2*k/m2)*dt**2/r**3=a2*dt**2/(r**2)
                        for moode in range(a,samm,2):#muudab kiirusi
                            l[1+p1+moode]+=a_p2*(l[p2+moode]-l[p1+moode])#v1=v_10+a*dt**2=(m2*G-q1*q2*k/m1)*dt**2*l/r**3=a1*dt**2*l/(r**2)
                            l[1+p2+moode]+=a_p1*(l[p1+moode]-l[p2+moode])#v2=v_20+a*dt**2
                        return (l)
            else:
                if mudel==1:
                    def muuda_v(l,p1,p2,siht):
                        c2_miinus_v2=c_valguskiirus**2
                        vXx=0
                        for moode in range(a,samm,2):
                            delta_v=l[1+p2+moode]-l[1+p1+moode]#kiiruste vahe
                            c2_miinus_v2+=delta_v**2#vektor v pikkuse ruut
                            vXx+=delta_v*(l[p2+moode]-l[p1+moode])#v ja x skalaar korrutis
                        tegur_jagatud_kaugus_astmes=(l[p1]*l[p2]*Gt2)/siht**dim
                        c2_miinus_v2=c2_miinus_v2*tegur_jagatud_kaugus_astmes
                        vXx=vXx*tegur_jagatud_kaugus_astmes
                        for moode in range(a,samm,2):
                            a_p1=vXx*(l[1+p2+moode]-l[1+p1+moode])-c2_miinus_v2*(l[p2+moode]-l[p1+moode])#(l[p2+moode]-l[p1+moode]) on deltaX_D ehk punktide vahelise vektori projektsioon kindlal mootmel
                            a_p2=-a_p1/l[p2]
                            a_p1=a_p1/l[p1]
                            l[1+p1+moode]+=a_p1#v1=v_10+a*dt**2=(m2*G-q1*q2*k/m1)*dt**2*l/r**3=a1*dt**2*l/(r**2)
                            l[1+p2+moode]+=a_p2#v2=v_20+a*dt**2
                        return(l)
                elif mudel==0:
                    def muuda_v(l,p1,p2,siht):
                        a_p1=Gt2/siht**dim#ainult gravitatsiooni seadus
                        a_p2=-l[p1]*a_p1
                        a_p1=l[p2]*a_p1
                        for moode in range(a,samm,2):
                            siht=(l[p2+moode]-l[p1+moode])#l ehk punktide vahleine kaugus kindla dimensioooni projektsioonis
                            l[1+p1+moode]+=a_p1*siht#v1=v_10+a*dt**2=m2*G*dt**2*l/r**3=a1*dt**2*l/(r**2)
                            l[1+p2+moode]+=a_p2*siht#v2=v_20+a*dt**2
                        return(l)
        elif elektriline:
            if mudel==1:
                def muuda_v(l,p1,p2,siht):
                    c2_miinus_v2=c_valguskiirus**2
                    vXx=0
                    for moode in range(a,samm,2):
                        delta_v=l[1+p2+moode]-l[1+p1+moode]#kiiruste vahe
                        c2_miinus_v2+=delta_v**2#vektor v pikkuse ruut
                        vXx+=delta_v*(l[p2+moode]-l[p1+moode])#v ja x skalaar korrutis
                    tegur_jagatud_kaugus_astmes=(l[1+p1]*l[1+p2]*kt2)/siht**dim
                    c2_miinus_v2=c2_miinus_v2*tegur_jagatud_kaugus_astmes
                    vXx=vXx*tegur_jagatud_kaugus_astmes
                    for moode in range(a,samm,2):
                        a_p1=vXx*(l[1+p2+moode]-l[1+p1+moode])-c2_miinus_v2*(l[p2+moode]-l[p1+moode])#(l[p2+moode]-l[p1+moode]) on deltaX_D ehk punktide vahelise vektori projektsioon kindlal mootmel
                        a_p2=-a_p1/l[p2]
                        a_p1=a_p1/l[p1]
                        l[1+p1+moode]+=a_p1#v1=v_10+a*dt**2=(m2*G-q1*q2*k/m1)*dt**2*l/r**3=a1*dt**2*l/(r**2)
                        l[1+p2+moode]+=a_p2#v2=v_20+a*dt**2
                    return(l)
            elif mudel==0:
                def muuda_v(l,p1,p2,siht):
                    a_p1=(l[1+p1]*l[1+p2]*kt2)/siht**(dim)#(m1*m2*G-q1*q2*k)*dt**2/(r**3)
                    a_p2=a_p1/l[p1]#(m2*G-q1*q2*k/m1)*dt**2/r**3=a1*dt**2/(r**2)
                    a_p1=a_p1/l[p2]#(m1*G-q1*q2*k/m2)*dt**2/r**3=a2*dt**2/(r**2)
                    for moode in range(a,samm,2):#muudab kiirusi
                        l[1+p1+moode]+=a_p2*(l[p2+moode]-l[p1+moode])#v1=v_10+a*dt**2=(m2*G-q1*q2*k/m1)*dt**2*l/r**3=a1*dt**2*l/(r**2)
                        l[1+p2+moode]+=a_p1*(l[p1+moode]-l[p2+moode])#v2=v_20+a*dt**2
                    return (l)
        else:
            def muuda_v(l,p1,p2,siht):
                return(l)
    #l=N_ajasammu(l,samm,muuda_v,kordusi%data)
    if data!="":
        kordusi2=kordusi//int(data)
        data=""
    else:
        kordusi2=1
    N=kordusi//kordusi2-1
    i=0
    if mudel==0 or mudel==1:
        while i<kordusi2:
            i+=1
            g=osakeste_paaritamisega_ajasamm_kirjutamisega(l,samm,muuda_v)
            data+=g[1]
            l=N_ajasammu_osakeste_paaritamisega(g[0],samm,muuda_v,N)
        uuenda_loend(l,samm,dif)
    else:
        print("mudel2")
        while i < kordusi2:
            i+=1
            g=osakeste_ja_valjaga_ajasamm_kirjutamisega(l)
            data += g[1]
            l=N_ajasammu_osakeste_ja_valjaga(l,v,samm,N)
    if data!="":
        fail=open("N-keha simulaatori valjund.txt","w")
        fail.write(data)
        fail.close()
def korruta_aja_difertentsaaliga_ajakudsed_tuletised(l,samm,dif):
    for p1 in range(0,len(l),samm):
        for p2 in range(a+1,samm,2):#korrutab koik kiirused ja kiirendused aja diferentsiaaliga labi.
            l[p1+p2]=dif*l[p1+p2]
    return (l)
def N_ajasammu_osakeste_paaritamisega(l,samm,muuda_v,kordusi):
    i=0
    ep1=-1#on, et kui sama indeksiga 1. punkt liitmiseks kirja on juba pandud ,ei paneks script seda uuesti kirja.
    liit=[]
    while i<kordusi:
        i+=1
        for p1 in range(0,len(l),samm):#votab jarjest punktmassi alguse indekseid
            for moode in range(a+p1,samm+p1,2):#muudab asukohti#oige on muuta enne asukohti juhul ,kui tombejoud on ulekaalus.
                l[moode]+=l[1+moode]#s_l=s_l0+v_l*dt+a*dt**2/2#vaja ainult p1´ga.
            for p2 in range(0,p1,samm):#p2 on alati vaiksem kui p1#muuta range argumente nii ,et indexite saamiseks peaks vahem tehteid tegema.
                siht=0
                for moode in range(a,samm,2):#kehade vahelise kauguse ruut = r**2
                    siht+=(l[p1+moode]-l[p2+moode])**2#esimese punkti selle dimensiooni kordinaadi ja teise punkti selle dimensiooni kordinaadi vahe ruut
                if siht:#  leiab punktide kiirenduste ja aja diferentsiaali ruudu korrutised.
                    l=muuda_v(l,p1,p2,siht)
                else:#kui asuvad samas kohas#peaks olema ,et kui kaugus on vaiksem ,kui porkeks vajalike kauguste summa.
                    print("Punktid kattuvad")
                    if ep1!=p1:#ei ole sama p1 mis eelmisel.
                        ep1=p1#eelmine p1 tuleb maarata,nagu ongi,peale vordlust,
                        liit+=[p1,p2]#pole vajalik ega voimalik omavahelist moju maarata#loendi liit lisatakse oigeid asju
        # siia see, mis juhtub punktmass-laengute samma kohta sattumisel.
        liit=[]
    return (l)
def osakeste_paaritamisega_ajasamm_kirjutamisega(l,samm,muuda_v):
    ep1=-1#on et sama indeksiga 1. punkt liitmiseks kirja on juba pandud ,ei paneks script seda uuesti kirja.
    liit=[]
    data=""
    for p1 in range(0,len(l),samm):#votab jarjest punktmassi alguse indekseid
        for moode in range(a+p1,samm+p1,2):#muudab asukohti#oige on muuta enne asukohti juhul ,kui tombejoud on ulekaalus.
            data+=(str(l[moode])+";")
            l[moode]+=l[1+moode]#s_l=s_l0+v_l*dt+a*dt**2/2#vaja ainult p1´ga.
        for p2 in range(0,p1,samm):#p2 on alati vaiksem kui p1#muuta range argumente nii ,et indexite saamiseks peaks vahem tehteid tegema.
            siht=0
            for moode in range(a,samm,2):#kehade vahelise kauguse ruut = r**2
                siht+=(l[p1+moode]-l[p2+moode])**2#esimese punkti selle dimensiooni kordinaadi ja teise punkti selle dimensiooni kordinaadi vahe ruut
            if siht:#leiab punktide kiirenduste ja aja diferentsiaali ruudu korrutised.
                l=muuda_v(l,p1,p2,siht)
            else:#kui asuvad samas kohas#peaks olema ,et kui kaugus on vaiksem ,kui porkeks vajalike kauguste summa.
                print("Punktid kattuvad")
                if ep1!=p1:#ei ole sama p1 mis eelmisel.
                    ep1=p1#eelmine p1 tuleb maarata,nagu ongi,peale vordlust,
                    liit+=[p1,p2]#pole vajalik ega voimalik omavahelist moju maarata#loendi liit lisatakse oigeid asju
    data+="\n"
    #punktide liitmine
    return (l,data)
def N_ajasammu_osakeste_ja_valjaga(l,v,samm,kordusi):
    i=0
    while i<kordusi:
        for moode in range(a + p1, samm + p1, 2):
            pass

        i+=1
        for p1 in range(0,len(l),samm):#votab jarjest punktmassi alguse indekseid
            for moode in range(a+p1,samm+p1,2):#muudab asukohti#oige on muuta enne asukohti juhul ,kui tombejoud on ulekaalus.
                l[moode]+=l[1+moode]#s_l=s_l0+v_l*dt+a*dt**2/2#vaja ainult p1´ga.

        #siia punktmass-laengute kiiruste muutmine samas kohas asuvate valjade tottu.

        #siia see, mis juhtub punktmass-laengute samma kohta sattumisel.
        liit=[]
    return (l)

raam = Tk()
raam.title("N-keha simulaator D-mootmelise ruumiga")

ttk.Label(raam, text="eradi arvestatavaid mootmeid:").grid(column=0, row=0,sticky=(N, W))
eraldi_mootmete_sisend=ttk.Entry(raam)
eraldi_mootmete_sisend.grid(row=0,column=1,sticky=(W, E))
ttk.Label(raam, text="jou soltuvuse kaugusest mootmeid:").grid(column=0, row=1,sticky=(N, W))
jou_mootmete_sisend=ttk.Entry(raam)
jou_mootmete_sisend.grid(row=1,column=1,sticky=(W, E))
jou_mootmete_sisend.insert(0,"3")
ttk.Label(raam, text="ajahetk:").grid(column=0, row=2,sticky=(N, W))
t_0_sisend=ttk.Entry(raam)
t_0_sisend.insert(0,"0")
t_0_sisend.grid(row=2,column=1,sticky=(W, E))
ttk.Label(raam, text="simuleerida ajahetkeni:").grid(column=0, row=3,sticky=(N, W))
t_1_sisend=ttk.Entry(raam)
t_1_sisend.grid(row=3,column=1,sticky=(W, E))
ttk.Label(raam, text="Mitu korda diferentseerida:").grid(column=0, row=4,sticky=(N, W))
kordusi_sisend=ttk.Entry(raam)
kordusi_sisend.grid(row=4,column=1,sticky=(W, E))
ttk.Label(raam, text="Iga mitmes asukoht faili kirjutada:").grid(column=0, row=5,sticky=(N, W))
iga_mitmes_samm_kirja_sisend=ttk.Entry(raam)
iga_mitmes_samm_kirja_sisend.grid(row=5,column=1,sticky=(W, E))

GEM_sisend = IntVar()
Radiobutton(raam, text="GEM", variable=GEM_sisend, value=2, state=DISABLED).grid(row=7, sticky=W)
Radiobutton(raam, text="GEM c=∞", variable=GEM_sisend, value=1).grid(column=0,row=7, columnspan=2)
G=Radiobutton(raam, text="klassikaline fuusika", variable=GEM_sisend, value=0).grid(row=7, sticky=E,column=1)
ttk.Label(raam, text="arvestatavad vastastikmojud:").grid(column=0, row=8, padx=5, pady=5, sticky=(N, W))
gravitatsiooniline_sisend = IntVar()
Checkbutton(raam, text="gravitatsiooniline", variable=gravitatsiooniline_sisend).grid(row=9, sticky=W)
gravitatsiooniline_sisend.set(1)
elektriline_sisend = IntVar()
Checkbutton(raam, text="elektriline", variable=elektriline_sisend).grid(row=10, sticky=W)
elektriline_sisend.set(1)
ttk.Label(raam, text="Lisa punktmass:").grid(column=0, row=11, padx=5, pady=5, sticky=(N, W))
lisamis_nupp=Button(raam,text="lisa punktmass",command=lambda:loo_sisestamis_GUI(lisamis_nupp))
lisamis_nupp.grid(row=11,column=0,columnspan=2)

mainloop()