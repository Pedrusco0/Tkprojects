from tkinter import *
from pytube import YouTube

class Downloader():
    def __init__(self):
        root = Tk()
        self.root = root
        self.tela()
        self.frames()
        self.widgets()
        root.mainloop()
    def tela(self):
        self.root.title("Downloader")
        self.root.geometry("600x300")
        self.root.resizable(False, False)
    def frames(self):
        self.frameTitle = Frame(self.root, bd=4, bg='#C0C0C0')
        self.frameTitle.place(relx= 0.02, rely=0.02, relwidth=0.96, relheight=0.12)

        self.frameButtons = Frame(self.root, bd=4, bg='#C0C0C0')
        self.frameButtons.place(relx= 0.02, rely=0.20, relwidth=0.96, relheight=0.75)

    def widgets(self):
        self.lbTitle = Label(self.frameTitle, text="Cocoloader")        
        self.lbTitle.place(relx= 0.40, rely=0.30, relwidth=0.20, relheight=0.5)
Downloader()
