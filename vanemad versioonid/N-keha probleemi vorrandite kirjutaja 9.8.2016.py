# coding=utf-8
print("kirjutaja 9.8.2016")
__author__ = 'Olger'
from tkinter import *
from tkinter import ttk
from tkinter import tix
from math import log#vaja energia arvutamiseks
#panna progressbar näitama, et kui palju aega on jäänud ligikaudsete tulemuste täpsustuseni (töötades täpsustab tulemusi kuni kasutaja pausi nuppu vajutab)
#teha algmoisted valitavaks tabelist checkbuttoni abil

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
    pass
def lisa_PML_massi_info(N_1,m_voi_q,mq_1):
    if m_voi_q.get()=="mass":
        m_voi_q="m"
    else:
        m_voi_q="q"
    seoste_lahter.insert(END,m_voi_q+"("+N_1+")="+mq_1+"\n")
luhikirjedused = {"--puudub--":"PMLe pole" ,'klassikaline': '(klassikalise füüsika kirjeldus)', 'QM': 7, 'SR': 'In physics, special relativity (SR, also known as the special theory of relativity or STR) is the generally accepted and experimentally well confirmed physical theory regarding the relationship between space and time. In Albert Einsteins original pedagogical treatment, it is based on two postulates:'}

raam = Tk()
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
ttk.Label(mudeli_frame, text="mitu korda diferentseerida:").grid(row=3, column=0,sticky=(N, W))
kordusi_sisend=ttk.Entry(mudeli_frame)
kordusi_sisend.grid(row=3,column=1,sticky=(W, E))
ttk.Label(mudeli_frame, text="toimus Suur Pauk:").grid(row=4, column=0,sticky=(N, W))
SP_sisend=Checkbutton(mudeli_frame)
SP_sisend.grid(row=4,column=1,sticky=(N,W))
ttk.Label(mudeli_frame, text="mateeria mudel:").grid(row=5, column=0, sticky=(N, W))
mateeria_mudel=StringVar()
mateeria_mudeli_valik=ttk.OptionMenu(mudeli_frame, mateeria_mudel,"klassikaline","--puudub--","klassikaline","SR erirelatiivsus","QM kvantfüüsika")
mateeria_mudeli_valik.grid(row=5, column=1, sticky=(N, W))
ttk.Label(mudeli_frame, text="Vastastikmõjude mudel:").grid(row=6, column=0)
ttk.Label(mudeli_frame, text="gravitatsioon:").grid(row=7, column=0, sticky=(N, W))
G_mudel=StringVar()
G_mudeli_valik=ttk.OptionMenu(mudeli_frame, G_mudel,"klassikaline","--puudub--","klassikaline","GM gravitomagnetism","GR üldrelatiivsus")
G_mudeli_valik.grid(row=7, column=1, sticky=(N, W))
ttk.Label(mudeli_frame, text="elekter:").grid(column=0, row=8,sticky=(N, W))
E_mudel=StringVar()
E_mudeli_valik=ttk.OptionMenu(mudeli_frame, E_mudel,"klassikaline","--puudub--","klassikaline","EM elektromagnetism","EW elektronõrk")
E_mudeli_valik.grid(row=8, column=1, sticky=(N, W))
ttk.Label(mudeli_frame, text="nõrk:").grid(column=0, row=9,sticky=(N, W))
W_mudel=StringVar()
W_mudeli_valik=ttk.OptionMenu(mudeli_frame, W_mudel,"--puudub--","--puudub--","Yukawa","EW")
W_mudeli_valik.grid(row=9, column=1, sticky=(N, W))
ttk.Label(mudeli_frame, text="tugev:").grid(column=0, row=10,sticky=(N, W))
S_mudel=StringVar()
S_mudeli_valik=ttk.OptionMenu(mudeli_frame, S_mudel,"--puudub--","--puudub--")
S_mudeli_valik.grid(row=10, column=1, sticky=(N, W))
mudeli_frame.grid(row=0,column=0,sticky=(N,W))


olukorra_frame=LabelFrame(raam)
ttk.Label(olukorra_frame, text="OLUKORRA SISESTAMINE:").grid(row=0, column=0, columnspan=2)#teha võimalus kasutajal mugavalt sisestada erinevat süsteemi kohta
Button(olukorra_frame, text="laadi olukord failist").grid(row=1,column=0,sticky=(N,W))

vormi_frame1=Frame(olukorra_frame)
ttk.Label(vormi_frame1, text="PML nimega").grid(column=0, row=0)
N_sisend=ttk.Entry(vormi_frame1, width=8)
N_sisend.insert(0,"N_1")
N_sisend.grid(row=0,column=1)
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
N_sisend=ttk.Entry(vormi_frame1, width=3)
N_sisend.insert(0,"N_1")
N_sisend.grid(row=0,column=1)
ttk.Label(vormi_frame1, text="asub alati PML nimega").grid(column=2, row=0)
N_sisend=ttk.Entry(vormi_frame1, width=3)
N_sisend.insert(0,"N_2")
N_sisend.grid(row=0,column=3)
ttk.Label(vormi_frame1, text="kaugusel").grid(column=4, row=0)
N_sisend=ttk.Entry(vormi_frame1, width=3)
N_sisend.insert(0,"r")
N_sisend.grid(row=0,column=5)
Button(vormi_frame1, text="lisa").grid(row=0, column=6)
vormi_frame1.grid(row=4, column=0, columnspan=2,sticky=(N,W))

vormi_frame1=Frame(olukorra_frame)
ttk.Label(vormi_frame1, text="PML nimega").grid(column=0, row=0)
N_sisend=ttk.Entry(vormi_frame1, width=3)
N_sisend.insert(0,"N_1")
N_sisend.grid(row=0,column=1)
tuletis=StringVar()
tuletise_valik=ttk.OptionMenu(vormi_frame1,tuletis,"mass","mass","elektrilaeng")
tuletise_valik.grid(row=0, column=2, sticky=(N, W))
ttk.Label(vormi_frame1, text="on").grid(column=3, row=0)
mq_sisend=ttk.Entry(vormi_frame1, width=3)
mq_sisend.insert(0,"m_1")
mq_sisend.grid(row=0,column=4)
ttk.Label(vormi_frame1, text=".").grid(column=5, row=0)
Button(vormi_frame1, text="lisa", command=lambda:lisa_PML_massi_info(N_sisend.get(),tuletis,mq_sisend.get())).grid(row=0, column=6)
vormi_frame1.grid(row=5, column=0, columnspan=2,sticky=(N,W))
olukorra_frame.grid(row=0,column=1,sticky=(N,W))


valjundi_frame=LabelFrame(raam)
ttk.Label(valjundi_frame, text="VÄLJUNDITE VALIKUD:").grid(row=0, column=0, columnspan=2)
Button(valjundi_frame, text="salvesta sisend faili").grid(row=1, column=0, sticky=(N, W))
Button(valjundi_frame, text="salvesta väljund faili").grid(row=1, column=1, sticky=(N, E))
ttk.Label(valjundi_frame, text="Graafiku valikud:").grid(column=0, row=2)
ttk.Label(valjundi_frame, text="vali kasutatavad algmõisted:").grid(row=2, column=0,columnspan=2)
moistete_frame=Frame(valjundi_frame)
moistete_loend=ttk.Treeview(moistete_frame,height=7)
moistete_loend.column("#0",width=128)
moistete_loend.insert('', 0, 'Eukleidiline ruum', text='Eukleidiline ruum')
moistete_loend.insert('', 0, 'Aegruum', text='Aegruum')
moistete_loend.insert('Eukleidiline ruum', 0, 'sirgjoon', text='sirgjoon')
moistete_loend.insert('Eukleidiline ruum', 0, 'tasand', text='tasand')
moistete_loend.insert('Eukleidiline ruum', 0, 'punkt', text='punkt')
moistete_loend.insert('', 0, 'aeg', text='aeg')
moistete_loend.insert('', 0, 'jõud', text='jõud')
moistete_loend.insert('', 0, 'mass', text='mass')
moistete_loend.insert('', 0, 'elektrilaeng', text='elektrilaeng')
moistete_loend.insert('', 0, 'kiirus', text='kiirus')
moistete_loend.insert('', 0, 'kiirendus', text='kiirendus')
moistete_loend.insert('', 0, 'punktmasslaeng', text='punktmasslaeng')
moistete_loend.insert('', 0, 'konstandid', text='konstandid')
moistete_loend.insert('konstandid', 0, 'c valguskiirus', text='c valguskiirus')
moistete_loend.insert('konstandid', 0, 'ε_E vaakumi dielektriline labitavus', text='ε_E vaakumi dielektriline läbitavust')
moistete_loend.insert('konstandid', 0, 'ε_G vaakumi digravitatsiooniline labitavus', text='ε_G vaakumi digravitatsiooniline läbitavus')
moistete_loend.insert('konstandid', 0, 'k_E koulombi', text='k_E koulombi')
moistete_loend.insert('konstandid', 0, 'k_G gravitatsiooni', text='k_G gravitatsiooni')
moistete_loend.insert('konstandid', 0, 'elektrimagnetiline', text='elektrimagnetiline')
moistete_loend.insert('konstandid', 0, 'gravitimagnetiline', text='gravitimagnetiline')
uuenda_algmoistete_loend()
scrollbar2=Scrollbar(moistete_frame, command=moistete_loend.yview)
scrollbar2.pack(side=RIGHT, fill=Y)
moistete_loend.config(yscrollcommand=scrollbar2.set)
moistete_loend.pack(side=LEFT)
moistete_frame.grid(row=3, column=0, columnspan=2,sticky=(N,W))
valjundi_frame.grid(row=0, column=2, sticky=(N, W))


seoste_frame=Frame(raam)
seoste_lahter=Text(seoste_frame, height=8, width=153, wrap=NONE)
yscrollbar=Scrollbar(seoste_frame,command=seoste_lahter.yview)
xscrollbar=Scrollbar(seoste_frame,command=seoste_lahter.xview, orient=HORIZONTAL)
yscrollbar.pack(side=RIGHT, fill=Y)
xscrollbar.pack(side=BOTTOM, fill=X)
seoste_lahter.pack(fill=BOTH, expand=TRUE)
seoste_lahter.config(yscrollcommand=yscrollbar.set)
seoste_lahter.config(xscrollcommand=xscrollbar.set)
seoste_frame.grid(row=1,column=0,columnspan=4,sticky=(N,E))


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
mudeli_info_frame.grid(row=2,column=0)
ttk.Label(mudeli_info_frame, text="huvitavaid omadusi valitud mudeli kohta:").grid(row=4, column=0,columnspan=2)
ttk.Label(mudeli_info_frame, text="sisemisi vabadusastmeid:").grid(row=6, column=0, sticky=(N,W))
ttk.Label(mudeli_info_frame, text="3", relief=SUNKEN).grid(row=6, column=1)
ttk.Label(mudeli_info_frame, text="vabadusastmeid valitud algmõistetes kirjeldades:").grid(row=7, column=0, sticky=(N,W))
ttk.Label(mudeli_info_frame, text="3", relief=SUNKEN).grid(row=7, column=1)

visualiseerimise_frame=LabelFrame(raam)
ttk.Label(visualiseerimise_frame, text="VISUALISEERITUD VÄLJUND:").grid(row=0, column=0, columnspan=2)
visualiseerimise_frame.grid(row=2,column=2,sticky=(N,E))

#ttk.Label(raam, text="Iga mitmes asukoht faili kirjutada:").grid(column=0, row=5,sticky=(N, W))
#iga_mitmes_samm_kirja_sisend=ttk.Entry(raam)
#iga_mitmes_samm_kirja_sisend.grid(row=5,column=1,sticky=(W, E))

mainloop()