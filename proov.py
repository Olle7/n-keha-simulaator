import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *

def graph():
    tmptext = "$"+entry.get("1.0","end")[:-1]+"$"

    fig.clear()
    fig.text(0, 0, tmptext, fontsize = 20)
    canvas.draw()


root = Tk()

mainframe = Frame(root)
mainframe.pack()
text = StringVar()
entry = Text(mainframe)
entry.pack()
label = Label(mainframe)
label.pack()
b=Button(text="kuva LaTeX",command=graph)
b.pack()

fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
fig.text(0.2,0.6,r"$\begin{cases}&\forall(T_1;(T_1\in\mathbb{R})\to\forall(N_1;(N_1\in\mathbb{N})\wedge (N_1<N)\to\forall(D_1;(D_1\in\mathbb{N})\wedge (D_1<D)\to\frac{X(T_1+2\cdot d;N_1;D_1)-2\cdot X(T_1+d;N_1;D_1)+X(T_1+d;N_1;D_1)}{d^2}=\frac{1}{c\cdot m(N_1)\cdot (c^2-(\sum_{j=1}^{D_e}(\frac{X(T_1+d;N_1;j)-X(T_1;N_1;j)}{d}))^2)^{1/2}}\cdot\sum_{i=1}^N(\frac{((X(T_1;i;D_1)-X(T_1;N_1;D_1))\cdot c^2+\frac{X(T_1+d;N_1;D_1)-X(T_1;N_1;D_1)}{d^2}\cdot\sum_{j=1}^{D_e}((X(T_1;N_1;D_1)-X(T_1;i;D_1))\cdot(X(T_1+d;N_1;i)+X(T_1;N_1;i)))\cdot (m(N_1)\cdot m(i)\cdot k_G-q(N_1)\cdot q(i)\cdot k_E)}{(\sum_{j=1}^{D_e}((X(T_1;N_1;j)-X(T_1;i;j))^2))^{D_j/2}}))))\\&D_e=3\\&D_j=3\\\end{cases}$",fontsize=19)

canvas = FigureCanvasTkAgg(fig, master=label)
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

root.mainloop()