from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from pytubefix import YouTube

class Funcs:

    def limpa_tela(self):
        self.entrylink.delete(0, END)
    
    def conecta_bd(self):
        self.conn = sqlite3.connect("POO.db")
        self.cursor = self.conn.cursor()
        print("Conectando ao banco de dados")
    
    def desconecta_bd(self):
        self.conn.close()
        print("Desconectando do banco de dados")
    
    def monta_tabela(self):
        self.conecta_bd()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS registro(
                link CHAR(150) PRIMARY KEY NOT NULL,
                type CHAR(40),
                name CHAR(100)
                );
            """)
        self.conn.commit()
        print("Banco de dados criado")
        self.desconecta_bd()

    def add_link(self, url, url_type, video_name):
        if url == "":
            msg = "Atenção! Digite um URL"
            messagebox.showinfo("Aviso", msg)
        else:
            self.conecta_bd()
            self.cursor.execute("""INSERT OR REPLACE INTO registro (link, type, name)
                VALUES(?, ?, ?)""", (url, url_type, video_name))
            self.conn.commit()
            self.desconecta_bd()
            self.select_lista()
            self.limpa_tela()

    def get_url_type(self, url):
        if "youtube.com" in url or "youtu.be" in url:
            return "YouTube"
        elif "tiktok.com" in url:
            return "TikTok"
        elif "twitter.com" in url:
            return "Twitter"
        else:
            return "Desconhecido"

    def get_video_name(self, url):
        if "youtube.com" in url or "youtu.be" in url:
            try:
                yt = YouTube(url)
                return yt.title
            except Exception as e:
                print(f"Erro ao obter título do vídeo: {e}")
                return "Desconhecido"
        else:
            return "Desconhecido"

    def select_lista(self):
        if hasattr(self, 'listalink'):  # Verifica se o listalink existe
            self.listalink.delete(*self.listalink.get_children())
            self.conecta_bd()
            lista = self.cursor.execute("""SELECT link, type, name FROM registro
                ORDER BY link ASC;""")
            for i in lista:
                self.listalink.insert("", END, values=i)
            self.desconecta_bd()
    
    def onDoubleClick(self, event):
        self.limpa_tela()
        self.listalink.selection()
        for n in self.listalink.selection():
            col1 = self.listalink.item(n, 'values')
            self.entrylink.insert(END, col1[0])
    
    def deleta_cliente(self):
        self.link = self.entrylink.get()
        if self.link == "":
            messagebox.showinfo("Aviso", "Selecione um link para apagar.")
            return

        self.conecta_bd()
        self.cursor.execute("""DELETE FROM registro WHERE link = ? """, (self.link,))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela()
        self.select_lista()

    def altera_cliente(self):
        self.link_novo = self.entrylink.get()
        if self.link_novo == "":
            messagebox.showinfo("Aviso", "Selecione um link para alterar.")
            return

        selecionado = self.listalink.selection()
        if not selecionado:
            messagebox.showinfo("Aviso", "Selecione um link na lista para alterar.")
            return

        selecionado = selecionado[0]
        self.link_antigo = self.listalink.item(selecionado, 'values')[0] 
        self.conecta_bd()
        self.cursor.execute("""UPDATE registro SET link = ? WHERE 
                            link = ? """, (self.link_novo, self.link_antigo))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela()  
        self.select_lista()
          
    def busca_cliente(self):
        termo_busca = self.entrylink.get()  # Obtém o termo de busca do entry
        if termo_busca == "":
            messagebox.showinfo("Aviso", "Digite um termo para buscar.")
            return

        self.conecta_bd()
        self.listalink.delete(*self.listalink.get_children())

        # Busca no campo 'link', 'type' ou 'name'
        self.cursor.execute(
            """ SELECT link, type, name FROM registro
            WHERE link LIKE ? OR type LIKE ? OR name LIKE ? ORDER BY link ASC""", 
            (f"%{termo_busca}%", f"%{termo_busca}%", f"%{termo_busca}%"))
        buscanomeCli = self.cursor.fetchall()
        for i in buscanomeCli:
            self.listalink.insert("", END, values=i)
        self.desconecta_bd()

class Downloader(Funcs):
    def __init__(self):
        root = Tk()
        self.root = root
        self.tela()
        self.frames()
        self.widgets()
        self.menus()
        self.monta_tabela()
        root.mainloop()

    def tela(self):
        self.root.title("COCOLoader")
        self.root.geometry("600x300")
        self.root.resizable(False, False)
        self.root.config(background='#cc232a')

    def frames(self):
        self.frameTitle = Frame(self.root, bd=4, bg='#ececec')
        self.frameTitle.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.12)

        self.frameButtons = Frame(self.root, bd=4, bg='#ececec')
        self.frameButtons.place(relx=0.02, rely=0.20, relwidth=0.96, relheight=0.75)

    def widgets(self):
        self.lbTitle = Label(self.frameTitle, text="COCOloader", bg='#ececec')
        self.lbTitle.place(relx=0.40, rely=0.30, relwidth=0.20, relheight=0.5)

        self.lbURL = Label(self.frameButtons, text="Insira o URL:", bg='#ececec')
        self.lbURL.place(relx=0.10, rely=0.1, relwidth=0.20, relheight=0.1)

        self.entrylink = Entry(self.frameButtons)
        self.entrylink.place(relx=0.15, rely=0.2, relwidth=0.7, relheight=0.1)

        self.ytbutton = Button(self.frameButtons, text="YouTube", command=self.handle_youtube)
        self.ytbutton.place(relx=0.1, rely=0.4, relwidth=0.2, relheight=0.2)

        self.twtbutton = Button(self.frameButtons, text="Twitter", command=self.handle_twitter)
        self.twtbutton.place(relx=0.4, rely=0.4, relwidth=0.2, relheight=0.2)

        self.tktbutton = Button(self.frameButtons, text="TikTok", command=self.handle_tiktok)
        self.tktbutton.place(relx=0.7, rely=0.4, relwidth=0.2, relheight=0.2)

    def handle_youtube(self):
        url = self.entrylink.get()
        url_type = self.get_url_type(url)
        video_name = self.get_video_name(url)
        self.add_link(url, url_type, video_name)
        self.YtDownloader()

    def handle_twitter(self):
        url = self.entrylink.get()
        url_type = self.get_url_type(url)
        video_name = "Desconhecido"  # Twitter não tem uma API fácil para obter o nome do vídeo
        self.add_link(url, url_type, video_name)
        messagebox.showinfo("Twitter", "URL do Twitter adicionado ao banco de dados.")

    def handle_tiktok(self):
        url = self.entrylink.get()
        url_type = self.get_url_type(url)
        video_name = "Desconhecido"  # TikTok requer uma API para obter o nome do vídeo
        self.add_link(url, url_type, video_name)
        messagebox.showinfo("TikTok", "URL do TikTok adicionado ao banco de dados.")

    def menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def quit(): self.root.destroy()
        
        menubar.add_cascade(label="Opções", menu=filemenu)
        menubar.add_cascade(label="Histórico", menu=filemenu2)
        
        filemenu.add_command(label="Sair", command=quit)

        filemenu2.add_command(label="Ver", command=self.Historico)
        filemenu2.add_command(label="Limpar", command=self.limpa_tela)

    def Historico(self):
        histroot = Tk()
        self.histroot = histroot
        self.histroot.title("COCOloader")
        self.histroot.geometry("600x300")
        self.histroot.resizable(False, False)
        self.histroot.config(background='#cc232a')
        self.framesHist()
        self.cria_lista()  # Cria a lista na janela de histórico
        self.HistWidgets()
        self.select_lista()  # Carrega os dados na lista
        self.histroot.mainloop()

    def framesHist(self):
        self.frameHistButtons = Frame(self.histroot, bd=4, bg='#ececec')
        self.frameHistButtons.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.12)

        self.frameHist = Frame(self.histroot, bd=4, bg='#ececec')
        self.frameHist.place(relx=0.02, rely=0.20, relwidth=0.96, relheight=0.75)
    
    def cria_lista(self):
        # Cria a lista na janela de histórico
        self.listalink = ttk.Treeview(self.frameHist, height=3, columns=("link", "type", "name"))
        self.listalink.heading("#0", text="id")
        self.listalink.heading("link", text="link")
        self.listalink.heading("type", text="linktype")
        self.listalink.heading("name", text="nome")

        self.listalink.column("#0", width=10)
        self.listalink.column("link", width=250)
        self.listalink.column("type", width=40)
        self.listalink.column("name", width=200)

        self.listalink.place(relx=0.01, rely=0.01, relwidth=0.95, relheight=0.85)

        self.scrollList = Scrollbar(self.frameHist, orient='vertical')
        self.listalink.configure(yscroll=self.scrollList.set)
        self.scrollList.place(relx=0.96, rely=0.01, relwidth=0.04, relheight=0.85)
        self.listalink.bind("<Double-1>", self.onDoubleClick)

    def HistWidgets(self):
        # Entry para inserir o termo de busca
        self.entrylink_hist = Entry(self.frameHistButtons)
        self.entrylink_hist.place(relx=0.02, rely=0.3, relwidth=0.5, relheight=0.65)

        # Botões para as funções
        self.btLimpar = Button(self.frameHistButtons, text="Limpar", command=self.limpa_tela)
        self.btLimpar.place(relx=0.55, rely=0.3, relwidth=0.1, relheight=0.65)
        
        self.btBuscar = Button(self.frameHistButtons, text="Buscar", command=self.busca_cliente)
        self.btBuscar.place(relx=0.65, rely=0.3, relwidth=0.1, relheight=0.65)

        self.btNovo = Button(self.frameHistButtons, text="Novo", command=lambda: self.add_link(self.entrylink_hist.get(), self.get_url_type(self.entrylink_hist.get()), self.get_video_name(self.entrylink_hist.get())))
        self.btNovo.place(relx=0.75, rely=0.3, relwidth=0.1, relheight=0.65)

        self.btAlterar = Button(self.frameHistButtons, text="Alterar", command=self.altera_cliente)
        self.btAlterar.place(relx=0.85, rely=0.3, relwidth=0.1, relheight=0.65)

        self.btApagar = Button(self.frameHistButtons, text="Apagar", command=self.deleta_cliente)
        self.btApagar.place(relx=0.95, rely=0.3, relwidth=0.1, relheight=0.65)

    def YtDownloader(self):
        self.linkyt = self.entrylink.get()
        try:
            self.yt = YouTube(self.linkyt)
            ytroot = Tk()
            self.rootyt = ytroot        
            self.rootyt.title("COCOloader")
            self.rootyt.geometry("400x200")
            self.rootyt.resizable(False, False)
            self.yttitle = self.yt.title
            
            self.lbTitle = Label(self.rootyt, text=self.yttitle)
            self.lbTitle.grid(row=0, column=0)

            self.ytqualitybox = ttk.Combobox(self.rootyt)
            self.ytqualitybox['values'] = ('-----','Qualidade mais Alta', 'Qualidade mais Baixa', 'Apenas Video', 'Apenas Audio')
            self.ytqualitybox.current(0)
            self.ytqualitybox.place(relx=0.2, rely=0.4, relwidth=0.6, relheight=0.1)
            
            self.ytconfirm = Button(self.rootyt, text="Confirmar", command=self.YtConfirm)
            self.ytconfirm.place(relx=0.2, rely=0.7, relwidth=0.2, relheight=0.2)
            
            self.rootyt.mainloop()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar vídeo: {e}")

    def YtConfirm(self):
        ytconfig = self.ytqualitybox.get()
        msg = "Downloaded"
        
        try:
            if ytconfig == "Qualidade mais Alta":
                ytvideohigh = self.yt.streams.get_highest_resolution()
                ytvideohigh.download()
                messagebox.showinfo("COCOloader", msg)

            elif ytconfig == "Qualidade mais Baixa":
                ytvideo = self.yt.streams.get_lowest_resolution()
                ytvideo.download()
                messagebox.showinfo("COCOloader", msg)

            elif ytconfig == "Apenas Video":
                ytvideomp3 = self.yt.streams.filter(only_video=True)[0]
                ytvideomp3.download()
                messagebox.showinfo("COCOloader", msg)
                
            elif ytconfig == "Apenas Audio":
                ytaudio = self.yt.streams.filter(only_audio=True)[0]
                ytaudio.download()
                messagebox.showinfo("COCOloader", msg)
            else:
                messagebox.showerror("COCOloader", "Selecione uma opção válida")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao baixar vídeo: {e}")
            
Downloader()