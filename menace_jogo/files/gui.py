"""
Este é o arquivo responsável por guardar todas as classes e funções utilizadas
na implementação da interface gráfica do MENACE!

:)
"""

import argparse
import pickle

import pygame as pg
from pygame import mixer

from menace_jogo.files.api import Configuracao, Jogador

parser = argparse.ArgumentParser()

parser.add_argument(
    "-t",
    "--treino",
    type=int,
    default=0,
    help="Quantidade de jogos para treinar o MENACE",
)

parser.add_argument(
    "-n",
    "--nivel",
    type=str,
    default="",
    help="Nível de desafio: fácil, médio, difícil ou impossível",
)

parser.add_argument(
    "-p",
    "--primeiro",
    type=str,
    default="MENACE",
    help="O primeiro jogador será o MENACE ou o humano?",
)

args = parser.parse_args()

if args.primeiro:
    if args.primeiro in [
        "menace",
        "MENACE",
        "Menace",
        "máquina",
        "Máquina",
        "maquina",
        "Maquina",
    ]:
        computer_starts = True
    elif args.primeiro in ["humano", "Humano", "eu", "Eu"]:
        computer_starts = False
    else:
        computer_starts = True


# -------------------------------- Config: ------------------------------- #
brain_save_path = "files/assets/brain.pickle"
history_save_path = "files/assets/history.pickle"
# computer_starts = True

# -------------------------------- Display: ------------------------------- #
scale_factor = 10  # para os sprites
DISPLAY_W, DISPLAY_H = 1280, 960
display_center = (DISPLAY_W / 2, DISPLAY_H / 2)

# ---------------------------- Carregando os sons: --------------------------- #
mixer.init()
snd_bead = mixer.Sound("files/assets/audios/bead.mp3")
snd_win = mixer.Sound("files/assets/audios/win.mp3")
snd_lose = mixer.Sound("files/assets/audios/lose.mp3")
snd_draw = mixer.Sound("files/assets/audios/draw.mp3")


def get_string(grupo_caixas):
    """
    Devolve a configuração atual do tabuleiro em forma de string.

    Args:
        grupo_caixas (pg.sprite.Group): grupo de caixas (objetos da classe
        Caixinhas, do tipo pg.sprite.Sprite) que descrevem o tabuleiro

    Returns:
        saida (str): string contendo a configuração atual do tabuleiro

    """
    saida = ""
    for caixa in grupo_caixas:
        saida += str(int(caixa.value))
    return saida


###############################################################################
#                          Funções interface gráfica                          #
###############################################################################


def get_sprites(size, file):
    """
    Transforma uma imagem de spritesheet numa lista de sprites do pygame individuais.

    Args:
        size (tup): (width, height) de cada sprite individual
        file (str): local do arquivo da spritesheet

    Returns:
        sprites (list): lista de superfícies/sprites do pygame

    """
    w, h = size
    x, y = (0, 0)
    sheet = pg.image.load(file).convert_alpha()
    sheet_rect = sheet.get_rect()
    sprites = []
    for _ in range(0, sheet_rect.width - w + 1, w):
        sheet.set_clip(pg.Rect(x, y, w, h))
        sprite = sheet.subsurface(sheet.get_clip())
        sprite = pg.transform.scale_by(sprite, scale_factor)
        sprites.append(sprite)
        x += w
    return sprites


def get_bead(num):
    """
    Devolve o sprite de uma miçanga a partir do seu número de identificação:
        (1) = vermelho; (2) = laranja; (3) = amarelo; (4) = verde;
        (5) = azul claro; (6) = azul escuro; (7) = roxo; (8) = rosa;
        (9) = branco.

    Args:
        num (int): número de 1 a 9 para descrever a cor da miçanga

    Returns:
        sprite (pg.Surface): superfície/sprite do pygame da miçanga

    """
    w, h = (6, 4)
    x, y = ((num - 1) * w, 0)
    sheet = pg.image.load("files/assets/sprites/spr_bead.png").convert_alpha()
    sheet.set_clip(pg.Rect(x, y, w, h))
    sprite = sheet.subsurface(sheet.get_clip())
    sprite = pg.transform.scale_by(sprite, scale_factor)
    return sprite


def atualizar_tela(grupo_caixas, jogada_antiga, jogada_atual, prob, grupo_probs):
    """
    Atualiza os valores das probabilidades e os valores das caixinhas (tabuleiro).

    Args:
        grupo_caixas (pg.sprite.Group): grupo de caixas (objetos da classe Caixinhas,
    do tipo pg.sprite.Sprite) que descrevem o tabuleiro
        jogada_antiga (str): string representando a jogada anterior à atual.
        jogada_atual (api.Configuracao): instância de Configuracao representando a
    jogada atual
        prob (arr): array com as probabilidades de cada casa ser jogada (antes da jogada)
    ser realizada
        grupo_probs (pg.sprite.Group): grupo das probabilidades (instâncias da classe
    Probabilidades; as quais incluem tanto os dados das probabilidades quanto os sprites
    das miçangas)
    """
    for n, sprite in enumerate(grupo_probs):
        probabilidade = prob[n]
        sprite.text = sprite.font.render(
            f"{probabilidade*100:.2f}%", True, (255, 255, 255)
        )

    for caixa, valor_antigo, valor_atual in zip(
        grupo_caixas, jogada_antiga, jogada_atual.lista
    ):
        if valor_antigo != str(valor_atual):
            caixa.change_value(valor_atual)


def reset_game(grupo_caixas):
    """
    Reseta o jogo, "zerando" as caixinhas do tabuleiro.

    Args:
        grupo_caixas (pg.sprite.Group): grupo de caixas (objetos da classe Caixinhas,
    do tipo pg.sprite.Sprite) que descrevem o tabuleiro

    """
    for caixa in grupo_caixas:
        caixa.change_value(0)


def konami(events, current):
    """
    Checa pelo input do Konami code.

    Args:
        events (list): lista de eventos intrínseca da biblioteca pygame
        current (list): lista atual de progresso do konami code case o mesmo esteja sendo
    digitado

    Returns:
        True, caso o código tenha sido digitado completa e corretamente;
        a lista atual de progresso current atualizada, caso contrário
    """
    exit = ["u", "u", "d", "d", "l", "r", "l", "r", "b", "a"]

    for e in events:
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_UP:
                del current[0]
                current.append("u")
            elif e.key == pg.K_DOWN:
                del current[0]
                current.append("d")
            elif e.key == pg.K_LEFT:
                del current[0]
                current.append("l")
            elif e.key == pg.K_RIGHT:
                del current[0]
                current.append("r")
            elif e.key == pg.K_b:
                del current[0]
                current.append("b")
            elif e.key == pg.K_a:
                del current[0]
                current.append("a")

    if "".join(exit) == "".join(current):
        return True

    else:
        return current


def vitoria(quem_ganhou, lista_de_listas, anim_grupo, pausado, menace=None):
    """
    Função ativada quando alguém ganha; atualiza dados do menace e anima a cena
    correspondente.

    Args:
        quem_ganhou:
          string 'p' caso o jogador tenha ganhado; instância do menace caso
          omenace tenha ganhado
        lista_de_listas (list):
          lista contendo as listas de vitória, derrota e empate
        anim_grupo (pg.sprite.Group):
          grupo de cenas animadas (instâncias da classe CenaAnimada)
        pausado (list):
          lista com os valores booleanos de pausa utilizados para animações
        menace (gui.Menace.menace, optional):
          instância do menace necessária caso o ganhador seja o jogador; caso
          contrário, None

    """
    global snd_win, snd_lose

    lista_jogador, lista_menace, lista_empates = lista_de_listas

    if quem_ganhou == "p":
        menace.atualizar_derrota()
        lista_jogador.append(lista_jogador[-1] + 1)
        lista_menace.append(lista_menace[-1])
        # Animação:
        cena_voce_ganhou = CenaAnimada(
            display_center,
            (80, 22),
            "spr_voceVenceu.png",
        )
        anim_grupo.add(cena_voce_ganhou)
        cena_voce_ganhou.animando = 60
        print("Você ganhou!")
        snd_win.play()

    else:
        quem_ganhou.atualizar_vitoria()
        lista_jogador.append(lista_jogador[-1])
        lista_menace.append(lista_menace[-1] + 1)
        # Animação:
        cena_voce_perdeu = CenaAnimada(
            display_center,
            (80, 22),
            "spr_vocePerdeu.png",
        )
        anim_grupo.add(cena_voce_perdeu)
        cena_voce_perdeu.animando = 60
        print("MENACE ganhou!")
        snd_lose.play()

    lista_empates.append(lista_empates[-1])
    pausado[0] = True
    pausado[1] = 300


def empate(lista_de_listas, anim_grupo, pausado):
    """
    Função ativada quando o jogo empata; atualiza dados do menace e anima a cena.

    Args:
        lista_de_listas (list):
          lista contendo as listas de vitória, derrota e empate
        anim_grupo (pg.sprite.Group):
          grupo de cenas animadas (instâncias da classe CenaAnimada)
        pausado (list):
          lista com os valores booleanos de pausa utilizados para animações

    """
    lista_jogador, lista_menace, lista_empates = lista_de_listas
    lista_jogador.append(lista_jogador[-1])
    lista_menace.append(lista_menace[-1])
    lista_empates.append(lista_empates[-1] + 1)

    # Animação:
    cena_empate = CenaAnimada(display_center, (80, 22), "spr_empate.png")
    anim_grupo.add(cena_empate)
    cena_empate.animando = 60
    print("Empate!")
    pausado[0] = True
    pausado[1] = 300
    snd_draw.play()


###############################################################################
#                                   Classes                                   #
###############################################################################


class Caixinhas(pg.sprite.Sprite):
    """
    Representa cada casa/posição no tabuleiro do jogo. Seu valor é alterado
    quando um jogador interage com uma instância da mesma.

    """

    def __init__(self, mouse, num):
        super().__init__()
        self.value = 0
        self.sprites = get_sprites(
            (19, 19),
            "files/assets/sprites/spr_caixinha.png",
        )
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.mouse = mouse
        self.num = num
        delta = 220
        centerX, centerY = (455, 525)
        caixinhaDict = {
            1: (centerX - delta, centerY - delta),
            2: (centerX, centerY - delta),
            3: (centerX + delta, centerY - delta),
            4: (centerX - delta, centerY),
            5: (centerX, centerY),
            6: (centerX + delta, centerY),
            7: (centerX - delta, centerY + delta),
            8: (centerX, centerY + delta),
            9: (centerX + delta, centerY + delta),
        }
        self.rect.center = caixinhaDict[self.num]

    def update(
        self,
        events,
        menace,
        grupo_caixas,
        lista_de_listas,
        anim_grupo,
        pausado,
        grupo_probs,
    ):
        if self.image == self.sprites[2] or self.image == self.sprites[3]:
            return
        mouse_pos = pg.mouse.get_pos()
        hover = self.rect.collidepoint(mouse_pos)
        self.image = self.sprites[1] if hover else self.sprites[0]

        # Checa jogada:
        for event in events:
            if (
                event.type == pg.MOUSEBUTTONDOWN
                and hover
                and (not pausado[0])
                and (not pausado[1])
                and (len(anim_grupo) == 0)
            ):
                self.change_value(computer_starts + 1)
                menace.jogada(
                    grupo_caixas,
                    lista_de_listas,
                    anim_grupo,
                    pausado,
                    grupo_probs,
                )

    def change_value(self, valor):
        if valor == 0:
            self.image = self.sprites[0]
        else:
            self.image = self.sprites[valor + 1]
        self.value = valor


class OsAndXs(pg.sprite.Sprite):
    """
    Utilizada para objetos de X ou O no jogo.

    """

    def __init__(self, isX, xy=None):
        super().__init__()

        self.isX = isX

        if xy is None:
            return

        self.sprites = get_sprites(
            (19, 19),
            "files/assets/sprites/spr_OsAndXs.png",
        )
        self.image = self.sprites[isX]
        self.rect = self.image.get_rect()
        self.rect.center = list(xy)


class Player(OsAndXs):
    """
    Subclasse de OsAndXs utilizada que representa o jogador na tela.

    """

    def __init__(self, isX, xy=None):
        super().__init__(isX, xy)

    def update(self):
        self.rect.center = pg.mouse.get_pos()


class Menace(OsAndXs):
    """
    Subclasse de OsAndXs utilizada que representa o MENACE.

    """

    def __init__(self, isX, xy=None, verbose=False):
        super().__init__(isX, xy)
        self.verbose = verbose
        self.menace = Jogador(isX + 1)

    def jogada(
        self,
        grupo_caixas,
        lista_de_listas,
        anim_grupo,
        pausado,
        grupo_probs,
    ):
        # Jogada:
        estado_jogo = get_string(grupo_caixas)
        config = Configuracao(estado_jogo)

        if (
            (not config.check_vitoria(1))
            and (not config.check_vitoria(2))
            and (config.get_symmetry_id().count("0") > 0)
        ):
            config, prob = self.menace.realizar_jogada(
                estado_jogo,
                self.verbose,
                True,
            )
            prob = prob.ravel()
            temp = estado_jogo
            atualizar_tela(grupo_caixas, estado_jogo, config, prob, grupo_probs)
            self.casa_mudada = list(
                i != j for i, j in zip(get_string(grupo_caixas), temp)
            )
            self.casa_mudada = self.casa_mudada.index(True) + 1

        # Check vitória, empate, etc.:
        if config.check_vitoria(self.isX + 1):
            vitoria(self.menace, lista_de_listas, anim_grupo, pausado)

        elif config.check_vitoria((not self.isX) + 1):
            vitoria("p", lista_de_listas, anim_grupo, pausado, self.menace)

        elif config.get_symmetry_id().count("0") == 0:
            empate(lista_de_listas, anim_grupo, pausado)

        else:
            # Animação:
            num = self.casa_mudada
            cena_embaralhando = CenaAnimada(
                (2 / 5 * DISPLAY_W - 50, DISPLAY_H / 2 + 50),
                (100, 100),
                "spr_embaralhando.png",
            )
            cena_embaralhando.sprites.extend(
                get_sprites(
                    (100, 100),
                    f"files/assets/sprites/spr_opening_{num}.png",
                )
            )
            cena_embaralhando.sprites.extend([cena_embaralhando.sprites[-1]] * 5)
            anim_grupo.add(cena_embaralhando)
            cena_embaralhando.animando = len(cena_embaralhando.sprites)
            return True

    def save_pickles(self, lista_de_listas):
        with open(brain_save_path, "wb") as handle:
            pickle.dump(
                self.menace.brain,
                handle,
                protocol=pickle.HIGHEST_PROTOCOL,
            )

        with open(history_save_path, "wb") as handle:
            pickle.dump(
                lista_de_listas,
                handle,
                protocol=pickle.HIGHEST_PROTOCOL,
            )

    def load_pickles(self, lista_de_listas):
        with open(brain_save_path, "rb") as handle:
            loaded_brain = pickle.load(handle)
            self.menace.brain = loaded_brain

        with open(history_save_path, "rb") as handle:
            loaded_history = pickle.load(handle)
            lista_de_listas.clear()
            lista_de_listas.extend(loaded_history)


class CenaAnimada(pg.sprite.Sprite):
    """
    Classe especial para cenas animadas utilizadas durante o jogo.

    """

    def __init__(self, xy, size, file):
        super().__init__()
        self.sprites = get_sprites(size, "files/assets/sprites/" + file)
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.rect.center = xy
        self.count = 0
        self.animando = 0

    def update(self):
        if (len(self.sprites) == 56) and (round(self.animando, 1) == 11.0):
            snd_bead.play()
        if self.animando >= 0:
            buff = 0.2
            self.count += buff
            self.animando -= buff
        else:
            self.kill()
        if self.count >= len(self.sprites):
            self.count = 0
        self.image = self.sprites[int(self.count)]


class Probabilidades(pg.sprite.Sprite):
    """
    Utilizada para plotar as probabilidades de cada jogada possível em determinada
    configuração do tabuleiro.

    """

    def __init__(self, text, num, display, font):
        super().__init__()
        self.font = font
        self.display = display
        self.num = num
        self.text = self.font.render(text, True, (255, 255, 255))
        self.prob_rect = self.text.get_rect()
        self.prob_rect.center = (4 / 5 * DISPLAY_W, DISPLAY_H / 10 * num)
        self.image = get_bead(num)
        self.rect = self.image.get_rect()
        self.rect.center = (4 / 5 * DISPLAY_W - 70, DISPLAY_H / 10 * num)

    def update(self):
        self.display.blit(self.text, self.prob_rect)


class Simulacao(pg.sprite.Sprite):
    """
    Classe para armazenar, processar e renderizar as informações durante o
    treinamento.

    """

    def __init__(self, display, font, jogador):
        super().__init__()

        self.jogador = jogador

        self.font = font
        self.display = display

        self.contagem_treino = 0
        self.contagem_vitorias = 0
        self.contagem_derrotas = 0
        self.contagem_empates = 0

        # Texto de vitórias, derrotas e empate
        self.text = self.font.render("", True, (255, 255, 255))
        self.text_rect = self.text.get_rect()
        self.text_rect.midbottom = (DISPLAY_W / 2, DISPLAY_H - 70)

        # Contagem de partidas simuladas
        self.text_contagem = self.font.render(
            "NRO DE PARTIDAS: 0", True, (255, 255, 255)
        )
        self.text_contagem_rect = self.text_contagem.get_rect()
        self.text_contagem_rect.midbottom = (DISPLAY_W / 2, DISPLAY_H - 70)

        # Retângulo da borda
        self.retangulo_borda = pg.Rect(0, 0, 900, 160)
        self.retangulo_borda.center = (DISPLAY_W / 2, DISPLAY_H / 2)

        # Retângulo de vitórias
        self.retangulo_vitorias = pg.Rect(0, 0, 880, 140)
        self.retangulo_vitorias.center = (DISPLAY_W / 2, DISPLAY_H / 2)

        # Retângulo de empates
        self.retangulo_empates = pg.Rect(0, 0, 880, 140)
        self.retangulo_empates.center = (DISPLAY_W / 2, DISPLAY_H / 2)

        # Retângulo de derrotas
        self.retangulo_derrotas = pg.Rect(0, 0, 880, 140)
        self.retangulo_derrotas.center = (DISPLAY_W / 2, DISPLAY_H / 2)

    def render(self):
        # Texto de vitórias, derrotas e empate
        self.text = self.font.render(
            f"Vitórias: {self.contagem_vitorias} | "
            f"Empates: {self.contagem_empates} | "
            f"Derrotas: {self.contagem_derrotas}",
            True,
            (255, 255, 255),
        )
        self.text_rect = self.text.get_rect()
        self.text_rect.midbottom = (DISPLAY_W / 2, DISPLAY_H - 70)
        self.display.blit(self.text, self.text_rect)

        # Contagem de partidas simuladas
        self.text_contagem = self.font.render(
            f"NRO DE PARTIDAS: {self.contagem_treino}", True, (255, 255, 255)
        )
        self.text_contagem_rect = self.text_contagem.get_rect()
        self.text_contagem_rect.midtop = (DISPLAY_W / 2, 70)
        self.display.blit(self.text_contagem, self.text_contagem_rect)

        # Retângulo da borda
        pg.draw.rect(self.display, (50, 50, 50), self.retangulo_borda)

        # Retângulo de vitórias
        self.retangulo_vitorias.width = 880 * (
            self.contagem_vitorias / self.contagem_treino
        )
        self.retangulo_vitorias.midleft = ((DISPLAY_W / 2) - 440, DISPLAY_H / 2)
        pg.draw.rect(self.display, (50, 230, 50), self.retangulo_vitorias)

        # Retângulo de empates
        self.retangulo_empates.width = (
            880 * (self.contagem_empates / self.contagem_treino)
        ) + 10
        self.retangulo_empates.midleft = self.retangulo_vitorias.midright
        pg.draw.rect(self.display, (230, 230, 50), self.retangulo_empates)

        # Retângulo de derrotas
        self.retangulo_derrotas.width = 880 * (
            self.contagem_derrotas / self.contagem_treino
        )
        self.retangulo_derrotas.midright = ((DISPLAY_W / 2) + 440, DISPLAY_H / 2)
        pg.draw.rect(self.display, (230, 50, 50), self.retangulo_derrotas)

    def simula_partida(self, nro_partidas=1, strategy="slow learner"):
        vitorias, derrotas, empates, _ = self.jogador.self_train(nro_partidas, strategy)

        self.contagem_empates += empates[-1]
        self.contagem_treino += nro_partidas

        # POG para mostrar corretamente quando o primeiro jogador é humano
        if self.jogador.player_num != 2:
            self.contagem_vitorias += vitorias[-1]
            self.contagem_derrotas += derrotas[-1]
        else:
            self.contagem_vitorias += derrotas[-1]
            self.contagem_derrotas += vitorias[-1]
