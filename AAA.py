import tkinter as tk
from tkinter import Menu, ttk, messagebox, END
import sqlite3

#mimatei
class Funcs:
    def limpa_tela(self):
        self.nome_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.senha_entry.delete(0, END)
        self.cidade_entry.delete(0, END)

    def conecta_bd(self):
        self.conn = sqlite3.connect("clientes.db")
        self.cursor = self.conn.cursor()
        print("Conectando ao banco de dados")

    def desconecta_bd(self):
        self.conn.close()
        print("Desconectando do banco de dados")

    def monta_tabela(self):
        self.conecta_bd()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                nome_cliente CHAR(40) NOT NULL,
                email CHAR(40) NOT NULL,
                senha CHAR(40) NOT NULL,
                cidade CHAR(40) NOT NULL
            );
        """)
        self.conn.commit()
        print("Banco de dados criado")
        self.desconecta_bd()

    def add_cliente(self):
        self.nome = self.nome_entry.get()
        self.email = self.email_entry.get()
        self.senha = self.senha_entry.get()
        self.cidade = self.cidade_entry.get()

        if self.nome == "" or self.email == "" or self.senha == "" or self.cidade == "":
            msg = "Atenção! Preencha todos os campos."
            messagebox.showinfo("Aviso", msg)
        else:
            self.conecta_bd()
            self.cursor.execute("""
                INSERT INTO clientes (nome_cliente, email, senha, cidade)
                VALUES (?, ?, ?, ?)
            """, (self.nome, self.email, self.senha, self.cidade))
            self.conn.commit()
            self.desconecta_bd()
            self.select_lista()
            self.limpa_tela()
#parte extremamente chata abaixo
    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute("""
            SELECT nome_cliente, email, cidade FROM clientes ORDER BY nome_cliente ASC;
        """)
        for i in lista:
            self.listaCli.insert("", END, values=i)
        self.desconecta_bd()

    def onDoubleClick(self, event):
        self.limpa_tela()
        self.listaCli.selection()
        for n in self.listaCli.selection():
            col1, col2, col3 = self.listaCli.item(n, 'values')
            self.nome_entry.insert(END, col1)
            self.email_entry.insert(END, col2)
            self.cidade_entry.insert(END, col3)

    def deleta_cliente(self):
        self.nome = self.nome_entry.get()
        self.conecta_bd()
        self.cursor.execute("""
            DELETE FROM clientes WHERE nome_cliente = ?
        """, (self.nome,))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela()
        self.select_lista()
#me mata de uma vez
    def altera_cliente(self):
        self.nome_novo = self.nome_entry.get()
        self.email_novo = self.email_entry.get()
        self.senha_nova = self.senha_entry.get()
        self.cidade_nova = self.cidade_entry.get()

        selecionado = self.listaCli.selection()[0]
        self.nome_antigo = self.listaCli.item(selecionado, 'values')[0]

        self.conecta_bd()
        self.cursor.execute("""
            UPDATE clientes SET nome_cliente = ?, email = ?, senha = ?, cidade = ?
            WHERE nome_cliente = ?
        """, (self.nome_novo, self.email_novo, self.senha_nova, self.cidade_nova, self.nome_antigo))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela()
        self.select_lista()

    def busca_cliente(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())

        nome = self.nome_entry.get()
        self.cursor.execute("""
            SELECT nome_cliente, email, cidade FROM clientes
            WHERE nome_cliente LIKE ? ORDER BY nome_cliente ASC
        """, (f"%{nome}%",))
        buscanomeCli = self.cursor.fetchall()
        for i in buscanomeCli:
            self.listaCli.insert("", END, values=i)
        self.limpa_tela()
        self.desconecta_bd()


class Application(Funcs):
    def __init__(self, root):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.monta_tabela()
        self.select_lista()
        self.menus()
        self.listaCli.bind("<Double-1>", self.onDoubleClick)

    def tela(self):
        self.root.title("Cadastro Coco")
        self.root.configure(background="#1e4738")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        self.root.maxsize(width=900, height=700)
        self.root.minsize(width=500, height=400)

    def frames_da_tela(self):
        self.frame_1 = tk.Frame(self.root, bd=4, bg="#dfe3ee",
                                highlightbackground="#af373c", highlightthickness=3)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)

        self.frame_2 = tk.Frame(self.root, bd=4, bg="#dfe3ee",
                                highlightbackground="#af373c", highlightthickness=3)
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

    def widgets_frame1(self):
#aiai amo meus amigoes cocolhoes
        self.lb_titulo = tk.Label(self.frame_1, text="Cadastro Cocolhão >:)", bg="#dfe3ee", fg="#ab0d2f", font=('Nexa', 12, 'bold'))
        self.lb_titulo.place(relx=0.36, rely=0.02)

#BUTOES!!!!!!
        self.bt_limpar = tk.Button(self.frame_1, text="Limpar", bd=2, bg="#ab0d2f", fg="white",
                                   font=('verdana', 8, 'bold'), command=self.limpa_tela)
        self.bt_limpar.place(relx=0.02, rely=0.7, relwidth=0.15, relheight=0.15)


        self.bt_buscar = tk.Button(self.frame_1, text="Buscar", bd=2, bg="#ab0d2f", fg="white",
                                   font=('verdana', 8, 'bold'), command=self.busca_cliente)
        self.bt_buscar.place(relx=0.23, rely=0.7, relwidth=0.15, relheight=0.15)


        self.bt_novo = tk.Button(self.frame_1, text="Novo", bd=2, bg="#ab0d2f", fg="white",
                                 font=('verdana', 8, 'bold'), command=self.add_cliente)
        self.bt_novo.place(relx=0.43, rely=0.7, relwidth=0.15, relheight=0.15)


        self.bt_alterar = tk.Button(self.frame_1, text="Alterar", bd=2, bg="#ab0d2f", fg="white",
                                    font=('verdana', 8, 'bold'), command=self.altera_cliente)
        self.bt_alterar.place(relx=0.63, rely=0.7, relwidth=0.15, relheight=0.15)


        self.bt_apagar = tk.Button(self.frame_1, text="Apagar", bd=2, bg="#ab0d2f", fg="white",
                                   font=('verdana', 8, 'bold'), command=self.deleta_cliente)
        self.bt_apagar.place(relx=0.83, rely=0.7, relwidth=0.15, relheight=0.15)

#campos aqui ó
        self.lb_nome = tk.Label(self.frame_1, text="Nome:", bg="#dfe3ee", fg="#ab0d2f")
        self.lb_nome.place(relx=0.15, rely=0.15)

        self.nome_entry = tk.Entry(self.frame_1)
        self.nome_entry.place(relx=0.15, rely=0.25, relwidth=0.3)


        self.lb_email = tk.Label(self.frame_1, text="Email:", bg="#dfe3ee", fg="#ab0d2f")
        self.lb_email.place(relx=0.15, rely=0.35)

        self.email_entry = tk.Entry(self.frame_1)
        self.email_entry.place(relx=0.15, rely=0.45, relwidth=0.3)


        self.lb_senha = tk.Label(self.frame_1, text="Senha:", bg="#dfe3ee", fg="#ab0d2f")
        self.lb_senha.place(relx=0.55, rely=0.15)

        self.senha_entry = tk.Entry(self.frame_1, show="*")
        self.senha_entry.place(relx=0.55, rely=0.25, relwidth=0.3)


        self.lb_cidade = tk.Label(self.frame_1, text="Cidade:", bg="#dfe3ee", fg="#ab0d2f")
        self.lb_cidade.place(relx=0.55, rely=0.35)

        self.cidade_entry = tk.Entry(self.frame_1)
        self.cidade_entry.place(relx=0.55, rely=0.45, relwidth=0.3)

    def lista_frame2(self):
        self.listaCli = ttk.Treeview(self.frame_2, height=3, columns=("col1", "col2", "col3")) #eu ODEIO ESSA BUCETA DE LISTA PQP, morre praga
        self.listaCli.heading("#0", text="")
        self.listaCli.heading("#1", text="Nome")
        self.listaCli.heading("#2", text="Email")
        self.listaCli.heading("#3", text="Cidade")

        self.listaCli.column("#0", width=1)
        self.listaCli.column("#1", width=100)
        self.listaCli.column("#2", width=150)
        self.listaCli.column("#3", width=100)

        self.listaCli.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scroolLista = tk.Scrollbar(self.frame_2, orient="vertical")
        self.listaCli.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)

    def menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        
        filemenu = Menu(menubar)

        def quit(): self.root.destroy()
        
        menubar.add_cascade(label="Opções", menu=filemenu)
        
        filemenu.add_command(label="Opções", command=quit)
        filemenu.add_command(label="Sair", command=quit)


#inicia essa desgraça >:(
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()