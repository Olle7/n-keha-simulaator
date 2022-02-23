print("cb proov 2")

stri="qertfhywQWASDws"
print(stri[stri.index("w")+1:])


from tkinter import tix,Button
raam=tix.Tk()

#def gs():
#    print(loend_linnukesega.focus())
#b=Button(command=gs)
#b.pack()


def si(a):
    print(a)


loend_linnukesega=tix.CheckList(browsecmd=si)
loend_linnukesega.hlist.add("T",text="aeg")
loend_linnukesega.hlist.add("A",text="elektromagnetväli")
loend_linnukesega.hlist.add("A.E",text="elektriväli")
loend_linnukesega.setstatus("T","on")
loend_linnukesega.setstatus("A.E","off")
loend_linnukesega.getmode("A.E")

loend_linnukesega.autosetmode()
loend_linnukesega.pack()
raam.mainloop()


"""
    moistete_loend.hlist.add('Eukleidiline ruum', text='Eukleidiline ruum')
    moistete_loend.hlist.add('Aegruum', text='Aegruum')
    moistete_loend.hlist.add("Aegruum.aegruumi_algmoiste", text="aegruumi_algmoiste")
    moistete_loend.setstatus("Aegruum.aegruumi_algmoiste", "off")
    moistete_loend.hlist.add('Eukleidiline ruum.sirgjoon', text='sirgjoon')
    moistete_loend.setstatus("Eukleidiline ruum.sirgjoon", "off")
    moistete_loend.hlist.add('Eukleidiline ruum.tasand', text='tasand')
    moistete_loend.setstatus("Eukleidiline ruum.tasand", "off")
    moistete_loend.hlist.add('Eukleidiline ruum.punkt', text='punkt')
    moistete_loend.setstatus("Eukleidiline ruum.punkt", "on")
    moistete_loend.hlist.add('aeg', text='aeg')
    moistete_loend.setstatus("aeg", "on")
    moistete_loend.hlist.add('jõud', text='jõud')
    moistete_loend.setstatus("jõud", "on")
    moistete_loend.hlist.add('mass', text='mass')
    moistete_loend.setstatus("mass", "on")
    moistete_loend.hlist.add('elektrilaeng', text='elektrilaeng')
    moistete_loend.setstatus("elektrilaeng", "on")
    moistete_loend.hlist.add('kiirus', text='kiirus')
    moistete_loend.setstatus("kiirus", "off")
    moistete_loend.hlist.add('kiirendus', text='kiirendus')
    moistete_loend.setstatus("kiirendus", "off")
    moistete_loend.hlist.add('punktmasslaeng', text='punktmasslaeng')
    moistete_loend.setstatus("punktmasslaeng", "on")
    moistete_loend.hlist.add('konstandid', text='konstandid')
    moistete_loend.hlist.add('konstandid.c valguskiirus', text='c valguskiirus')
    moistete_loend.setstatus("konstandid.c valguskiirus", "on")
    moistete_loend.hlist.add('konstandid.ε_E vaakumi dielektriline labitavus',text='ε_E vaakumi dielektriline läbitavust')
    moistete_loend.setstatus("konstandid.ε_E vaakumi dielektriline labitavus", "off")
    moistete_loend.hlist.add('konstandid.ε_G vaakumi digravitatsiooniline labitavus',text='ε_G vaakumi digravitatsiooniline läbitavus')
    moistete_loend.setstatus("konstandid.ε_G vaakumi digravitatsiooniline labitavus", "on")
    moistete_loend.hlist.add('konstandid.k_E koulombi', text='k_E koulombi')
    moistete_loend.setstatus("konstandid.k_E koulombi", "on")
    moistete_loend.hlist.add('konstandid.k_G gravitatsiooni', text='k_G gravitatsiooni')
    moistete_loend.setstatus("konstandid.k_G gravitatsiooni", "on")
    moistete_loend.hlist.add('konstandid.elektrimagnetiline', text='elektrimagnetiline')
    moistete_loend.setstatus("konstandid.elektrimagnetiline", "on")
    moistete_loend.hlist.add('konstandid.gravitimagnetiline', text='gravitimagnetiline')
    moistete_loend.setstatus("konstandid.gravitimagnetiline", "on")"""