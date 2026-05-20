"""
Oi! Este é o arquivo pincipal da nossa implementação do MENACE - desenvolvido
utilizando a biblioteca pygame.

:)
"""


def main():
    import argparse
    import sys

    import pygame as pg

    from menace_jogo.files.gui import (
        DISPLAY_H,
        DISPLAY_W,
        Caixinhas,
        Menace,
        Player,
        Probabilidades,
        Simulacao,
        display_center,
        get_string,
        # computer_starts,
        konami,
        mixer,
        reset_game,
        scale_factor,
    )

    RUNNING = True
    FPS = 60
    PAUSADO = [False, False]
    LOADING = False  # serve para carregar arquivo brain

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

    TREINO = args.treino

    if args.nivel:
        if args.nivel in ["facil", "Facil", "fácil", "Fácil"]:
            TREINO = 500
        elif args.nivel in ["medio", "Medio", "médio", "Médio"]:
            TREINO = 1000
        elif args.nivel in ["dificil", "Dificil", "difícil", "Difícil"]:
            TREINO = 5000
        elif args.nivel in ["impossivel", "Impossivel", "impossível", "Impossível"]:
            TREINO = 10000
        else:
            TREINO = 0

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

    ###############################################################################
    #                            Configurações iniciais                           #
    ###############################################################################

    pg.init()
    clock = pg.time.Clock()
    pg.event.set_allowed([pg.KEYDOWN, pg.QUIT, pg.MOUSEBUTTONDOWN])
    font = pg.font.Font("files/assets/basis33.ttf", 50)
    lista_konami = ["0" for _ in range(10)]

    # Janela:
    screen = pg.display.set_mode((DISPLAY_W, DISPLAY_H), pg.FULLSCREEN | pg.SCALED)
    pg.display.set_caption("MENACE")
    icon = pg.image.load("files/assets/icon.png")
    pg.display.set_icon(icon)
    background = pg.image.load("files/assets/sprites/bg_colorido.png")
    background = pg.transform.scale_by(background, scale_factor)
    pg.mouse.set_visible(False)

    # Placar:
    vitorias_jogador = [0]
    vitorias_menace = [0]
    empates = [0]
    lista_de_listas = [vitorias_jogador, vitorias_menace, empates]

    ###############################################################################
    #                             Instâncias e objetos                            #
    ###############################################################################

    # Jogador:
    Player_group = pg.sprite.Group()

    player = Player(computer_starts, (100, 100))
    Player_group.add(player)

    # Menace:
    menace = Menace(not computer_starts)

    if LOADING:
        menace.load_pickles(lista_de_listas)

    # Animação:
    animacao_group = pg.sprite.Group()
    proximo_group = pg.sprite.GroupSingle()

    proximo = pg.sprite.Sprite()
    proximo.image = pg.image.load(
        "files/assets/sprites/spr_proximo.png"
    ).convert_alpha()
    proximo.image = pg.transform.scale_by(proximo.image, scale_factor)
    proximo.rect = proximo.image.get_rect()
    proximo.rect.center = display_center
    proximo_group.add(proximo)

    # Caixinhas:
    caixinhas_group = pg.sprite.Group()

    for i in range(9):
        caixinha_nova = Caixinhas(player, i + 1)
        caixinhas_group.add(caixinha_nova)

    # Probabilidades:
    prob_group = pg.sprite.Group()

    for i in range(9):
        prob_nova = Probabilidades("0%", i + 1, screen, font)
        prob_group.add(prob_nova)

    # Simulação:
    simulacao = Simulacao(screen, font, menace.menace)

    ###############################################################################
    #                                 Loop do jogo                                #
    ###############################################################################

    while RUNNING:
        events = pg.event.get()

        lista_konami = konami(events, lista_konami)
        if lista_konami == True:
            menace.save_pickles(lista_de_listas)
            RUNNING = False

        # Checagem de eventos:
        for event in events:
            if event.type == pg.KEYDOWN:
                # Print brain (P)
                if event.key == pg.K_p:
                    print(menace.menace.brain)

                # Print histórico (H)
                if event.key == pg.K_h:
                    print(
                        f"------------------------ \
    \n Vitórias do jogador: {lista_de_listas[0][-1]} \n \
    \n Vitórias do MENACE: {lista_de_listas[1][-1]} \n \
    \n Empates: {lista_de_listas[2][-1]} \n \
    ------------------------"
                    )

                # Recomeçar partida atual (R)
                if event.key == pg.K_r and not PAUSADO[0]:
                    animacao_group.empty()
                    PAUSADO[0] = True
                    reset_game(caixinhas_group)
                    menace.menace.jogadas = []
                    mixer.stop()

                # Continuar depois do final de uma partida (Enter)
                if PAUSADO and event.key == pg.K_RETURN:
                    animacao_group.empty()
                    PAUSADO[0] = False
                    if PAUSADO[1]:
                        PAUSADO[0] = True
                        PAUSADO[1] = False
                        reset_game(caixinhas_group)
                    mixer.stop()

        # Simula os jogos caso ainda precise treinar
        if simulacao.contagem_treino < TREINO:
            screen.fill((0, 0, 0))
            simulacao.simula_partida(100)
            simulacao.render()
            pg.display.update()
            clock.tick(FPS)
            continue

        if PAUSADO[1]:
            PAUSADO[1] -= 1
            if not PAUSADO[1]:
                reset_game(caixinhas_group)

        if (
            (player.isX)
            and (get_string(caixinhas_group) == "000000000")
            and (not PAUSADO[0])
        ):
            menace.jogada(
                caixinhas_group,
                lista_de_listas,
                animacao_group,
                PAUSADO,
                prob_group,
            )

        # Updates:
        if (not PAUSADO[0]) or (PAUSADO[1]):
            screen.blit(background, (0, 0))

            caixinhas_group.draw(screen)
            caixinhas_group.update(
                events,
                menace,
                caixinhas_group,
                lista_de_listas,
                animacao_group,
                PAUSADO,
                prob_group,
            )

        if ((len(animacao_group) != 0) or (PAUSADO[0])) and (not PAUSADO[1]):
            screen.fill((0, 0, 0))
        if ((len(animacao_group) == 0) and (PAUSADO[0])) and (not PAUSADO[1]):
            proximo_group.draw(screen)

        if (not PAUSADO[0]) or (PAUSADO[1]):
            prob_group.draw(screen)
            prob_group.update()

            if len(animacao_group) == 0:
                Player_group.draw(screen)
                Player_group.update()

        animacao_group.draw(screen)
        animacao_group.update()

        pg.display.update()
        clock.tick(FPS)

    # Fecha loop do jogo:
    pg.quit()
    sys.exit()
