from tkinter import font
from tkinter import *
raam=Tk()
tekst=Text(raam, height=5, width=55)
tekst.pack()
tekst.insert(END,"\\vec{R}=\\frac{m_1 \\vec{r}_1 + m_2 \\vec{r}_2}{m_1+m_2}")
pilt = PhotoImage(file="naite pilt.gif")
font = font.Font(family="Helvetica",size=12)
Label(raam,image=pilt,text="SIIA   PEAB   TULEMA   VÕRRAND\nVASTAVALT   LATEX   KOODILE",compound=CENTER,font=font,fg="red").pack()
mainloop()