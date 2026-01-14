from tkinter import *
from tkinter import ttk
import sys 
import os
import subprocess

dificuldade = 0   # valor inicial
jogador = "--menace"
botoes_dificuldade = []  # lista para armazenar os botões e resetar cor
botoes_jogador = []

DEFAULT_COLOR = "SystemButtonFace"
SELECTED_COLOR = "lightblue"


def criar_botao_dificuldade(frame, texto, dificuldade_valor, linha):
    botao = Button(frame, text=texto, width=20, bg=DEFAULT_COLOR)
    botao.grid(column=0, row=linha, pady=2)

    botao.config(
        command=lambda val=dificuldade_valor, btn=botao: selecionar_dificuldade(val, btn)
    )

    botoes_dificuldade.append(botao)

def criar_botao_jogador(frame,texto,jogador,linha):
    botao = Button(frame, text = texto, width=20,bg=DEFAULT_COLOR)
    botao.grid(column=2, row=linha, pady=2)

    botao.config(
        command=lambda val=jogador, btn=botao: selecionar_jogador(val, btn)
    )

    botoes_jogador.append(botao)


def selecionar_dificuldade(valor, botao_clicado):
    global dificuldade
    dificuldade = valor

    for btn in botoes_dificuldade:
        if btn == botao_clicado:
            btn.config(bg=SELECTED_COLOR)
        else:
            btn.config(bg=DEFAULT_COLOR)

def selecionar_jogador(valor, botao_clicado):
    global jogador
    jogador = valor

    for btn in botoes_jogador:
        if btn == botao_clicado:
            btn.config(bg=SELECTED_COLOR)
        else:
            btn.config(bg=DEFAULT_COLOR)



def run_game():
    if dificuldade == 0:
        subprocess.Popen(["main.exe"])
    else:
        subprocess.Popen(["main.exe", "--nivel", dificuldade])

'''
def run_game():
    if dificuldade == 0:
        os.system("python main.py")
    else:
        os.system(f"python main.py --nivel {dificuldade}")
'''


root = Tk()
root.title("MENACE")
root.iconbitmap("icon.ico")

frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Selecione Sua Dificuldade").grid(column=0, row=0)

criar_botao_dificuldade(frm, "Sem Treino", 0, 1)
criar_botao_dificuldade(frm, "Nível Fácil", "facil", 2)
criar_botao_dificuldade(frm, "Nível Médio", "medio", 3)
criar_botao_dificuldade(frm, "Nível Difícil", "dificil", 4)
criar_botao_dificuldade(frm, "Nível IMPOSSÍVEL", "impossivel", 5)

player = ttk.Label(frm, text="Primeiro Jogador")
player.grid(column=2, row=0)
criar_botao_jogador(frm,"O Jogador", "--player",2)
criar_botao_jogador(frm, "O MENACE", "--menace",3)
Button(frm, text="JOGAR", command=run_game,width=20, pady=15).grid(column=1, row=6)


root.mainloop()
