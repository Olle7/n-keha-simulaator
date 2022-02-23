# coding=utf-8

print("värskeim kirjutaja")#
__author__ = 'Olger Männik'
from tkinter import *
from tkinter import ttk, tix
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from math import log#vaja energia arvutamiseks
#panna progressbar näitama, et kui palju aega on jäänud ligikaudsete tulemuste täpsustuseni (töötades täpsustab tulemusi kuni kasutaja pausi nuppu vajutab)

class HidingScrollBar(ttk.Scrollbar):#selle klassi kirjutas Andres Mikelson
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
class Table(ttk.Frame):#selle klassi kirjutas Andres Mihkelson
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
def analuutiline_lahend():
    return(False)
def uuenda_luhikirjeldus():
    luhikirjeldus.config(state=NORMAL)
    luhikirjeldus.insert(END,"Mudeli üldkirjeldus: "+luhikirjedused[mateeria_mudel.get()])
    luhikirjeldus.config(state=DISABLED)# ajutiselt kommentaar
def uuenda_algmoistete_loend():#siin muuta, mõisted mida antud mudeli puhul valida ei saa halliks.
    moistete_loend.hlist.add("matemaatiline algmoiste", text="matemaatiline algmoiste")
    hargnevad_algmoisted = ["PML","Eukleidiline ruum", "konstandid", 'Aegruum', "ühikud"]
    moistete_loend.hlist.add("füüsikaline algmoiste",text="füüsikaline algmoiste")
    for hargnev_algmoiste in hargnevad_algmoisted:
        moistete_loend.hlist.add("füüsikaline algmoiste."+hargnev_algmoiste, text=hargnev_algmoiste)
    for algmoiste in fuusikalised_algmoisted:
        moistete_loend.hlist.add("füüsikaline algmoiste."+algmoiste[0]+"."+algmoiste[1], text=(algmoiste[1]+" "+algmoiste[2]))
        moistete_loend.setstatus("füüsikaline algmoiste."+algmoiste[0]+"."+algmoiste[1], "off")
    for algmoiste in matemaatilised_algmoisted:
        moistete_loend.hlist.add("matemaatiline algmoiste."+algmoiste, text=algmoiste)
        moistete_loend.setstatus("matemaatiline algmoiste."+algmoiste, "off")
def lisa_PML_massi_info(N_1,m_voi_q,mq_1):
    if m_voi_q.get()=="mass":
        m_voi_q="m"
    else:
        m_voi_q="q"
    seoste_sisendi_lahter.insert(END, m_voi_q + "(" + N_1 + ")=" + mq_1 + "\n")
def kuva_algmoiste_info(algmoiste):
    vaadatava_algmoiste_kirjeldus.config(state=NORMAL)
    vaadatava_algmoiste_kirjeldus.delete('1.0', END)
    print(algmoiste)
    vaadatava_algmoiste_kirjeldus.insert(END,(algmoiste[algmoiste.find(".")+1:])+"\n\n")
    vaadatava_algmoiste_kirjeldus.config(state=DISABLED)
    vaheta_algmoisteid()
def kirjuta_mudeli_valiku_vorrandid(*args):
    seoste_sisendi_lahter.delete(1.0, "end")
    if G_mudel.get()=="--puudub--":
        k_G="0"
    else:
        k_G="k_G"
    if E_mudel.get()=="--puudub--":
        k_E="0"
    else:
        k_E="k_E"
    if mateeria_mudel.get()=="klassikaline":
        inertsus1=r"\frac{1}{m(N_1)}"
        inertsus2=""
        inertsus3=""
    elif mateeria_mudel.get()=="SR erirelatiivsus":
        inertsus1=r"\frac{1}{c\cdot m(N_1)\cdot (c^2-v^2)^{1/2}}"
        inertsus2="("
        inertsus3=r"-v \cdot \sum(y))"
    seoste_sisendi_lahter.insert(END, r"\forall(T_1;(T_1\in\mathbb{R})\to\forall(N_1;(N_1\in\mathbb{N})\to\forall(D_1;(D_1\in\mathbb{N})\to\frac{X(T_1+2\cdot d;N_1;D_1)-2\cdot X(T_1+d;N_1;D_1)+X(T_1+d;N_1;D_1)}{d^2}=" + inertsus1 + r"\cdot\sum_{i=1}^" + N_sisend.get() + r"(\frac{" + inertsus2 + r"(X(T_1;i;D_1)-X(T_1;N_1;D_1))" + inertsus3 + r"\cdot (m(N_1)\cdot m(i)\cdot " + k_G + r"-q(N_1)\cdot q(i)\cdot " + k_E + r")}{(\sum_{j=1}^" + eraldi_mootmete_sisend.get() + "((X(T_1;N_1;j)-X(T_1;i;j))^2))^{" + jou_mootmete_sisend.get() + r"/2}}))))" + "\n")
    mudeli_frame.config(relief=FLAT)
def kirjuta_mudeli_valiku_vorrandid(*args):
    seoste_sisendi_lahter.delete(1.0, "end")
    seoste_sisendi_lahter.insert(END, "\\begin{cases}\n" + r"&\forall(T_1;(T_1\in\mathbb{R})\to\forall(N_1;(N_1\in\mathbb{N})\wedge (N_1<N)\to\forall(D_1;(D_1\in\mathbb{N})\wedge (D_1<D)\to\frac{X(T_1+2\cdot d;N_1;D_1)-2\cdot X(T_1+d;N_1;D_1)+X(T_1+d;N_1;D_1)}{d^2}=\frac{1}{c\cdot m(N_1)\cdot (c^2-(\sum_{j=1}^{D_e}(\frac{X(T_1+d;N_1;j)-X(T_1;N_1;j)}{d}))^2)^{1/2}}\cdot\sum_{i=1}^N(\frac{((X(T_1;i;D_1)-X(T_1;N_1;D_1))\cdot c^2+\frac{X(T_1+d;N_1;D_1)-X(T_1;N_1;D_1)}{d^2}\cdot\sum_{j=1}^{D_e}((X(T_1;N_1;D_1)-X(T_1;i;D_1))\cdot(X(T_1+d;N_1;i)+X(T_1;N_1;i)))\cdot (m(N_1)\cdot m(i)\cdot k_G-q(N_1)\cdot q(i)\cdot k_E)}{(\sum_{j=1}^{D_e}((X(T_1;N_1;j)-X(T_1;i;j))^2))^{D_j/2}}))))\\" + "\n" + "&D_e=" + eraldi_mootmete_sisend.get() + r"\\" + "\n&D_j=" + jou_mootmete_sisend.get() + r"\\" + "\n&N=" + N_sisend.get() + r"\\" + "\n")
    if SR.get():
        seoste_sisendi_lahter.insert(END, "&c=299792458 \\\\\n")
    else:
        seoste_sisendi_lahter.insert(END, "&\\lim_{c \\to \infty}\\\\\n")
    if QM.get():
        seoste_sisendi_lahter.insert(END, "&\\hbar\\approx 6.62606957\\cdot 10^{-34} \\\\\n")
    else:
        seoste_sisendi_lahter.insert(END, "&\\lim_{\\hbar \\to 0}\\\\\n")
    if G_mudel.get()=="--puudub--":
        seoste_sisendi_lahter.insert(END, "&k_G=0\n")
    else:
        seoste_sisendi_lahter.insert(END, "&k_G \\approx 0.0000000000667384\\\\\n")
    if E_mudel.get()=="--puudub--":
        seoste_sisendi_lahter.insert(END, "&k_E=0\n")
    else:
        seoste_sisendi_lahter.insert(END, "&k_E \\approx 8900000000\\\\\n")
    seoste_sisendi_lahter.insert(END, r"\end{cases}")
def sisendi_lahter_muudeti(*args):
    mudeli_frame.config(relief=RAISED)
    fig.clear()
    fig.text(0, 0.2, "$"+seoste_sisendi_lahter.get("1.0","end")[:-1]+"$", fontsize=14)
    canvas.draw()
def vaheta_algmoisteid(*args):
    seosed_LaTeXina=seoste_sisendi_lahter.get("1.0", "end")
    for algmoiste in fuusikalised_algmoisted:
        #print("algmoiste on",algmoiste[1])
        for jargmine_mark in ("+","-","\\"," ","^","{","(",")","}","\n","&"):
            for eelmine_mark in ("+","-","\\"," ","^","{","(",")","}","\n","&"):
                seosed_LaTeXina=seosed_LaTeXina.replace(eelmine_mark+algmoiste[1]+jargmine_mark,eelmine_mark+"("+algmoiste[3]+")"+jargmine_mark)
    seoste_sisendi_lahter.delete(0.0, "end")
    seoste_sisendi_lahter.insert(END, seosed_LaTeXina)
luhikirjedused = {"--puudub--":"PMLe pole" ,'klassikaline': '(klassikalise füüsika kirjeldus)', 'QM': 7, 'SR': 'In physics, special relativity (SR, also known as the special theory of relativity or STR) is the generally accepted and experimentally well confirmed physical theory regarding the relationship between space and time. In Albert Einsteins original pedagogical treatment, it is based on two postulates:'}
fuusikalised_algmoisted=[("PML", "m", "mass", "m", "PROOV2"), ("PML", "F", "jõud", "PROOV1", "PROOV2"), ("PML", "q", "elektrilaeng", "q", "PROOV2"), ("PML", "v", "kiirus", "PROOV1", "PROOV2"), ("PML", "a", "kiirendus", "PROOV1", "PROOV2"), ("PML", "PML", "punktmasslaeng", "PROOV1", "PROOV2"),
                         ("konstandid","c","valguskiirus","c","PROOV2"), ("konstandid","ε_E","vaakumi dielektriline labitavus",r"1/(4\cdot \pi \cdot k_E)",r"1/(4\cdot \pi \cdot ε_G)"),
                         ("konstandid","ε_G","vaakumi digravitatsiooniline labitavus",r"1/(4\cdot \pi \cdot k_G)",r"1/(4\cdot \pi \cdot ε_G)"), ("konstandid","k_E","koulombi","k_E","PROOV2"),
                         ("konstandid","k_G","gravitatsiooni","k_G","PROOV2"), ("konstandid","μ_E","elektrimagnetiline läbitavus","PROOV1","PROOV2"), ("konstandid","μ_G","gravitimagnetiline läbitavus","PROOV1","PROOV2"),
                         ("Aegruum","A","aegruumi_algmoiste","PROOV1","PROOV2"), ("ühikud","SI","","PROOV1","PROOV2")]
matemaatilised_algmoisted=["JA","VÕI","EGA","SIIS_KUI","TÕENE","VÄÄR","universaalsuskvantor","eksistentsiaal kvantor","hulk","hulka kuuluvus"]

raam = tix.Tk()
raam.title("N-keha simulaator D-mootmelise ruumiga")


mudeli_frame=LabelFrame(raam)
ttk.Label(mudeli_frame, text="FÜÜSIKALISE MUDELI VALIK:").grid(row=0, column=0, columnspan=2)
ttk.Label(mudeli_frame, text="eradi arvestatavaid mootmeid:").grid(row=1, column=0, sticky=(N, W))
eraldi_mootmete_sisend=ttk.Entry(mudeli_frame)
eraldi_mootmete_sisend.grid(row=1,column=1,sticky=(W, E))
eraldi_mootmete_sisend.insert(0,"3")
ttk.Label(mudeli_frame, text="jou soltuvuse kaugusest mootmeid:").grid(row=2, column=0,sticky=(N, W))
jou_mootmete_sisend=ttk.Entry(mudeli_frame)#muuta laiust väiksemaks
jou_mootmete_sisend.grid(row=2,column=1,sticky=(W, E))
jou_mootmete_sisend.insert(0,"3")
ttk.Label(mudeli_frame, text="mitu osakest on süsteemis:").grid(row=3, column=0,sticky=(N, W))
N_sisend=ttk.Entry(mudeli_frame)
N_sisend.grid(row=3, column=1, sticky=(W, E))
N_sisend.insert(0,"N")
ttk.Label(mudeli_frame, text="toimus Suur Pauk:").grid(row=4, column=0,sticky=(N, W))
SP_sisend=Checkbutton(mudeli_frame,command=kirjuta_mudeli_valiku_vorrandid)
SP_sisend.grid(row=4,column=1,sticky=(N,W))
ttk.Label(mudeli_frame, text="SR erirelatiivsus:").grid(row=5, column=0,sticky=(N, W))
SR=IntVar()
SR_sisend=Checkbutton(mudeli_frame,variable=SR,command=kirjuta_mudeli_valiku_vorrandid)
SR_sisend.grid(row=5,column=1,sticky=(N,W))
ttk.Label(mudeli_frame, text="QM kvantfüüsika:").grid(row=6, column=0,sticky=(N, W))
QM=IntVar()
QM_sisend=Checkbutton(mudeli_frame,variable=QM,command=kirjuta_mudeli_valiku_vorrandid)
QM_sisend.grid(row=6,column=1,sticky=(N,W))
mateeria_mudel=StringVar()
mateeria_mudeli_valik=ttk.OptionMenu(mudeli_frame, mateeria_mudel,"klassikaline","--puudub--","klassikaline","SR erirelatiivsus","QM kvantfüüsika")
mateeria_mudeli_valik["menu"].entryconfigure(3,state="disable")
mateeria_mudel.trace("w",kirjuta_mudeli_valiku_vorrandid)
#mateeria_mudeli_valik.grid(row=5, column=1, sticky=(N, W))
ttk.Label(mudeli_frame, text="Vastastikmõjude mudel:").grid(row=7, column=0)
ttk.Label(mudeli_frame, text="gravitatsioon:").grid(row=8, column=0, sticky=(N, W))
G_mudel=StringVar()
G_mudeli_valik=ttk.OptionMenu(mudeli_frame, G_mudel,"klassikaline","--puudub--","klassikaline","GM gravitomagnetism","GR üldrelatiivsus")
G_mudeli_valik['menu'].entryconfigure(2, state = "disabled")
G_mudeli_valik['menu'].entryconfigure(3, state = "disabled")
G_mudel.trace("w",kirjuta_mudeli_valiku_vorrandid)
G_mudeli_valik.grid(row=8, column=1, sticky=(N, W))
ttk.Label(mudeli_frame, text="elekter:").grid(column=0, row=9,sticky=(N, W))
E_mudel=StringVar()
E_mudeli_valik=ttk.OptionMenu(mudeli_frame, E_mudel,"klassikaline","--puudub--","klassikaline","EM elektromagnetism","EW elektronõrk")
E_mudeli_valik['menu'].entryconfigure(2, state = "disabled")
E_mudeli_valik['menu'].entryconfigure(3, state = "disabled")
E_mudel.trace("w",kirjuta_mudeli_valiku_vorrandid)
E_mudeli_valik.grid(row=9, column=1, sticky=(N, W))
ttk.Label(mudeli_frame, text="nõrk:").grid(column=0, row=10,sticky=(N, W))
W_mudel=StringVar()
W_mudeli_valik=ttk.OptionMenu(mudeli_frame, W_mudel,"--puudub--","--puudub--","Yukawa","EW")
W_mudeli_valik['menu'].entryconfigure(1, state = "disabled")
W_mudeli_valik['menu'].entryconfigure(2, state = "disabled")
W_mudel.trace("w",kirjuta_mudeli_valiku_vorrandid)
W_mudeli_valik.grid(row=10, column=1, sticky=(N, W))
ttk.Label(mudeli_frame, text="tugev:").grid(column=0, row=11,sticky=(N, W))
S_mudel=StringVar()
S_mudeli_valik=ttk.OptionMenu(mudeli_frame, S_mudel,"--puudub--","--puudub--")
S_mudel.trace("w",kirjuta_mudeli_valiku_vorrandid)
S_mudeli_valik.grid(row=11, column=1, sticky=(N, W))
mudeli_frame.grid(row=0,column=0,sticky=(N,W))


olukorra_frame=LabelFrame(raam)
ttk.Label(olukorra_frame, text="OLUKORRA SISESTAMINE:").grid(row=0, column=0, columnspan=2)#teha võimalus kasutajal mugavalt sisestada erinevat süsteemi kohta
Button(olukorra_frame, text="laadi olukord failist").grid(row=1,column=0,sticky=(N,W))

vormi_frame1=Frame(olukorra_frame)
ttk.Label(vormi_frame1, text="PML nimega").grid(column=0, row=0)
n_sisend=ttk.Entry(vormi_frame1, width=8)
n_sisend.insert(0, "N_1")
n_sisend.grid(row=0, column=1)
ttk.Label(vormi_frame1, text="kordinaadi nimega").grid(row=0, column=2)
t_0_sisend=ttk.Entry(vormi_frame1, width=4)
t_0_sisend.insert(0,"D_1")
t_0_sisend.grid(row=0,column=3)
vormi_frame1.grid(row=2, column=0, columnspan=2,sticky=(N,W))
vormi_frame1=Frame(olukorra_frame)
sisend=ttk.Entry(vormi_frame1, width=3)
sisend.grid(row=1,column=0)
tuletis=StringVar()
tuletise_valik=ttk.OptionMenu(vormi_frame1,tuletis,"väärtus","väärtus","suunaline kiirus",". ajakaudse tuletise väärtus")
tuletise_valik.grid(row=1, column=1, sticky=(N, W))
ttk.Label(vormi_frame1, text="ajahetkel").grid(row=1, column=2)
t_0_sisend=ttk.Entry(vormi_frame1, width=5)
t_0_sisend.insert(0,"T_1")
t_0_sisend.grid(row=1,column=3)
ttk.Label(vormi_frame1, text="on").grid(row=1, column=4)
t_0_sisend=ttk.Entry(vormi_frame1, width=5)
t_0_sisend.insert(0,"x_1")
t_0_sisend.grid(row=1,column=5)
ttk.Label(vormi_frame1, text=".").grid(row=1, column=6)
Button(vormi_frame1, text="lisa").grid(row=1, column=7)
vormi_frame1.grid(row=3, column=0, columnspan=2,sticky=(N,W))

vormi_frame1=Frame(olukorra_frame)
ttk.Label(vormi_frame1, text="PML nimega").grid(column=0, row=0)
n_sisend=ttk.Entry(vormi_frame1, width=3)
n_sisend.insert(0, "N_1")
n_sisend.grid(row=0, column=1)
ttk.Label(vormi_frame1, text="asub alati PML nimega").grid(column=2, row=0)
n_sisend=ttk.Entry(vormi_frame1, width=3)
n_sisend.insert(0, "N_2")
n_sisend.grid(row=0, column=3)
ttk.Label(vormi_frame1, text="kaugusel").grid(column=4, row=0)
n_sisend=ttk.Entry(vormi_frame1, width=3)
n_sisend.insert(0, "r")
n_sisend.grid(row=0, column=5)
Button(vormi_frame1, text="lisa").grid(row=0, column=6)
vormi_frame1.grid(row=4, column=0, columnspan=2,sticky=(N,W))

vormi_frame1=Frame(olukorra_frame)
ttk.Label(vormi_frame1, text="PML nimega").grid(column=0, row=0)
n_sisend=ttk.Entry(vormi_frame1, width=3)
n_sisend.insert(0, "N_1")
n_sisend.grid(row=0, column=1)
tuletis=StringVar()
ttk.OptionMenu(vormi_frame1,tuletis,"mass","mass","elektrilaeng").grid(row=0, column=2, sticky=(N, W))
ttk.Label(vormi_frame1, text="on").grid(column=3, row=0)
mq_sisend=ttk.Entry(vormi_frame1, width=3)
mq_sisend.insert(0,"m_1")
mq_sisend.grid(row=0,column=4)
ttk.Label(vormi_frame1, text=".").grid(column=5, row=0)
Button(vormi_frame1, text="lisa", command=lambda:lisa_PML_massi_info(n_sisend.get(), tuletis, mq_sisend.get())).grid(row=0, column=6)
vormi_frame1.grid(row=5, column=0, columnspan=2,sticky=(N,W))

vormi_frame1=Frame(olukorra_frame)
tuntud_objekt=StringVar()
ttk.OptionMenu(vormi_frame1,tuntud_objekt,"Maa","Maa","Päike","Kuu","Saturn","elektron","prooton").grid(row=0, column=0, sticky=(N, W))
ttk.Label(vormi_frame1, text="asub punktis").grid(column=1, row=0)
X_sisend=ttk.Entry(vormi_frame1, width=3)
X_sisend.insert(0,"(x_1;x_2;x_3...)")#teha vaikeseade vastavaks sisestatud fuusikalise susteem mootmete arvule
X_sisend.grid(row=0,column=2)
Button(vormi_frame1, text="lisa", command=lambda:lisa_PML_massi_info()).grid(row=0, column=3)
vormi_frame1.grid(row=6,column=0,sticky=(N,W))
olukorra_frame.grid(row=0,column=1,sticky=(N,W))


valjundi_frame=LabelFrame(raam)
ttk.Label(valjundi_frame, text="VÄLJUNDITE VALIKUD:").grid(row=0, column=0, columnspan=2)
Button(valjundi_frame, text="salvesta sisend faili").grid(row=1, column=0, sticky=(N, W))
Button(valjundi_frame, text="salvesta väljund faili").grid(row=1, column=1, sticky=(N, E))
ttk.Label(valjundi_frame, text="Graafiku valikud:").grid(column=0, row=2)
ttk.Label(valjundi_frame, text="vali kasutatavad algmõisted:").grid(row=2, column=0)
moistete_frame=Frame(valjundi_frame)
moistete_loend=tix.CheckList(moistete_frame,browsecmd=kuva_algmoiste_info,command=vaheta_algmoisteid)#height=7 !!!!!
#moistete_loend.column("#0",width=128)
moistete_loend.autosetmode()#POLE KINDEL, ET MIDA SEE KÄSK TEEB.
uuenda_algmoistete_loend()
moistete_loend.pack(side=LEFT)
moistete_frame.grid(row=3, column=0, columnspan=2,sticky=(N,W))
moistete_loend.setstatus("füüsikaline algmoiste."+"konstandid.c","on")
moistete_loend.setstatus("füüsikaline algmoiste."+"konstandid.k_G","on")
moistete_loend.setstatus("füüsikaline algmoiste."+"konstandid.k_E","on")
vaadatava_algmoiste_kirjeldus=Text(valjundi_frame,height=10,width=21,wrap=WORD,state=DISABLED)#panna sellele scrollbar
vaadatava_algmoiste_kirjeldus.grid(row=2,column=1,rowspan=2,sticky=(W,S))
valjundi_frame.grid(row=0, column=2, sticky=(N, W))


seoste_sisendi_frame=Frame(raam)
seoste_sisendi_lahter=Text(seoste_sisendi_frame, height=8, width=157, wrap=NONE)
kirjuta_mudeli_valiku_vorrandid()
seoste_sisendi_lahter.bind("<Key>", sisendi_lahter_muudeti)
# punktmasslaengute arv ainult siis kui PMLid on eraldi parameetrite abil kirjeldatud.
yscrollbar=Scrollbar(seoste_sisendi_frame, command=seoste_sisendi_lahter.yview)
xscrollbar=Scrollbar(seoste_sisendi_frame, command=seoste_sisendi_lahter.xview, orient=HORIZONTAL)
yscrollbar.pack(side=RIGHT, fill=Y)
xscrollbar.pack(side=BOTTOM, fill=X)
seoste_sisendi_lahter.pack(fill=BOTH, expand=TRUE)
seoste_sisendi_lahter.config(yscrollcommand=yscrollbar.set)
seoste_sisendi_lahter.config(xscrollcommand=xscrollbar.set)
seoste_sisendi_frame.grid(row=1, column=0, columnspan=4, sticky=(N, E))


latex_valjundi_frame=Frame(raam)
fig=matplotlib.figure.Figure(figsize=(11, 4), dpi=100)
fig.text(0, 0.2, "$"+seoste_sisendi_lahter.get("1.0","end")[:-1]+"$", fontsize=14)
#print("$"+seoste_sisendi_lahter.get("1.0","end")[:-1]+"$")
label=Label(latex_valjundi_frame)
label.pack()
canvas = FigureCanvasTkAgg(fig, master=label)
canvas.draw()
canvas.get_tk_widget().pack()
latex_valjundi_frame.grid(row=2, column=0, columnspan=4, sticky=(N, E))


mudeli_info_frame=LabelFrame(raam)
ttk.Label(mudeli_info_frame, text="FÜÜSIKALISE MUDELI INFO:").grid(row=0, column=0, columnspan=2)
luhikirjelduse_frame=Frame(mudeli_info_frame)
luhikirjeldus=Text(luhikirjelduse_frame, height=4, width=51, wrap=WORD)
uuenda_luhikirjeldus()
luhikirjeldus.pack(side=LEFT)
scrollbar=Scrollbar(luhikirjelduse_frame,command=luhikirjeldus.yview)
scrollbar.pack(side=RIGHT, fill=Y)
luhikirjeldus.config(yscrollcommand=scrollbar.set)
luhikirjelduse_frame.grid(row=1,column=0,columnspan=2)
mudeli_info_frame.grid(row=3,column=0)
ttk.Label(mudeli_info_frame, text="huvitavaid omadusi valitud mudeli kohta:").grid(row=4, column=0,columnspan=2)
ttk.Label(mudeli_info_frame, text="sisemisi vabadusastmeid:").grid(row=6, column=0, sticky=(N,W))
ttk.Label(mudeli_info_frame, text="3", relief=SUNKEN).grid(row=6, column=1)
ttk.Label(mudeli_info_frame, text="vabadusastmeid valitud algmõistetes kirjeldades:").grid(row=7, column=0, sticky=(N,W))
ttk.Label(mudeli_info_frame, text="3", relief=SUNKEN).grid(row=7, column=1)


visualiseerimise_frame=LabelFrame(raam)
ttk.Label(visualiseerimise_frame, text="VISUALISEERITUD VÄLJUND:").grid(row=0, column=0, columnspan=2)
visualiseerimise_frame.grid(row=3,column=2,sticky=(N,E))

#ttk.Label(raam, text="Iga mitmes asukoht faili kirjutada:").grid(column=0, row=5,sticky=(N, W))
#iga_mitmes_samm_kirja_sisend=ttk.Entry(raam)
#iga_mitmes_samm_kirja_sisend.grid(row=5,column=1,sticky=(W, E))

mainloop()