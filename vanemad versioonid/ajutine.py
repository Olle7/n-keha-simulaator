a="""["Eukleidiline ruum.sirgjoon", "mass", "jõud", "elektrilaeng", "kiirus", "kiirendus", "punktmasslaeng",
"konstandid.c valguskiirus", "konstandid.ε_E vaakumi dielektriline labitavus",
"konstandid.ε_G vaakumi digravitatsiooniline labitavus", "konstandid.k_E koulombi",
"konstandid.k_G gravitatsiooni", "konstandid.elektrimagnetiline läbitavus", "konstandid.gravitimagnetiline läbitavus",
"Aegruum.aegruumi_algmoiste", "ühikud.SI"]"""
b=""
q=True
for i in range(0,len(a)):
    #print(a[i])
    if a[i]=="\"":
        if q:
            b+="("
            b+=a[i]
            q=False
        else:
            b+=a[i]
            b+=",\"PROOV1\",\"PROOV2\")"
            q=True
    else:
         b+=a[i]
print(b)