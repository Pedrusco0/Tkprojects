from tkinter import *
from functools import partial

class Calculadora():
    def __init__(self):
        root = Tk()
        self.root = root
        self.tela()
        self.frames()
        self.result()
        self.botoes()
        root.mainloop()

    def tela(self):
        self.root.title("Calculadora")
        self.root.geometry("352x380")
        self.root.resizable(False, False)
    def frames(self):
        self.frameResult = Frame(self.root, bd=4, bg='#C0C0C0')
        self.frameResult.place(relx= 0.02, rely=0.02, relwidth=0.96, relheight=0.12)

        self.frameNum = Frame(self.root, bd=4, bg='#C0C0C0')
        self.frameNum.place(relx= 0.02, rely=0.19, relwidth=0.96, relheight=0.770)

    def result(self):
        self.result_valor1 = Label(self.frameResult, bg='#C0C0C0')
        self.result_valor1.place(relx=0.02, rely=0, relheight=0.95, relwidth=0.40)

        self.result_operacao = Label(self.frameResult, bg='#C0C0C0')
        self.result_operacao.place(relx=0.40, rely=0, relheight=0.95, relwidth=0.20)

        self.result_valor2 = Label(self.frameResult, bg='#C0C0C0')
        self.result_valor2.place(relx=0.60, rely=0, relheight=0.95, relwidth=0.40)

    def numero(self):
        self.result_valor1.config(text=self.calc_num7['text'])
        print(self.calc_num7['text'])

    def botoes(self):
        #grid cima
        self.calc_num7 = Button(self.frameNum, text="7", width=8, height=4, command=self.numero)
        self.calc_num7.grid(row=0, column=0)

        self.calc_num8 = Button(self.frameNum, text="8", width=8, height=4, command=self.numero)
        self.calc_num8.grid(row=0, column=1)

        self.calc_num9 = Button(self.frameNum, text="9", width=8, height=4, command=partial(self.numero))
        self.calc_num9.grid(row=0, column=2)

        self.calc_divisao = Button(self.frameNum, text="/", width=8, height=4)
        self.calc_divisao.grid(row=0, column=3)

        self.calc_voltar = Button(self.frameNum, text="<-", width=8, height=4)
        self.calc_voltar.grid(row=0, column=4)

        #grid meio
        self.calc_num4 = Button(self.frameNum, text="4", width=8, height=4)
        self.calc_num4.grid(row=1, column=0)

        self.calc_num5 = Button(self.frameNum, text="5", width=8, height=4)
        self.calc_num5.grid(row=1, column=1)

        self.calc_num6 = Button(self.frameNum, text="6", width=8, height=4)
        self.calc_num6.grid(row=1, column=2)

        self.calc_vezes = Button(self.frameNum, text="*", width=8, height=4)
        self.calc_vezes.grid(row=1, column=3)

        self.calc_pesquisa = Button(self.frameNum, text="⌕", width=8, height=4)
        self.calc_pesquisa.grid(row=1, column=4)
    
        #grid baixo
        self.calc_num1 = Button(self.frameNum, text="1", width=8, height=4)
        self.calc_num1.grid(row=2, column=0)

        self.calc_num2 = Button(self.frameNum, text="2", width=8, height=4)
        self.calc_num2.grid(row=2, column=1)

        self.calc_num3 = Button(self.frameNum, text="3", width=8, height=4)
        self.calc_num3.grid(row=2, column=2)

        self.calc_menos = Button(self.frameNum, text="-", width=8, height=4)
        self.calc_menos.grid(row=2, column=3)

        self.calc_memoria = Button(self.frameNum, text="✎", width=8, height=4)
        self.calc_memoria.grid(row=2, column=4)

        #grid baixo²
        self.calc_num0 = Button(self.frameNum, text="0", width=8, height=4)
        self.calc_num0.grid(row=3, column=0)

        self.calc_ponto = Button(self.frameNum, text=".", width=8, height=4)
        self.calc_ponto.grid(row=3, column=1)

        self.calc_igual = Button(self.frameNum, text="=", width=8, height=4)
        self.calc_igual.grid(row=3, column=2)

        self.calc_mais = Button(self.frameNum, text="+", width=8, height=4)
        self.calc_mais.grid(row=3, column=3)

        self.calc_felizinho = Button(self.frameNum, text=":)", width=8, height=4)
        self.calc_felizinho.grid(row=3, column=4)



Calculadora()
