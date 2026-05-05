from api import Jogador, simulacao, plot
from pprint import pprint

if __name__ == "__main__":

    num_jogos = 2000

    # playerO = Jogador(1)
    playerO = Jogador(1, reforco_vitoria=0, reforco_derrota=0)

    # playerX = Jogador(2, reforco_vitoria=0, reforco_derrota=0)
    playerX = Jogador(2)

    playerO, playerX, vitoriasO, vitoriasX, empates = simulacao(
        playerO,
        playerX,
        num_jogos,
    )

    print()
    pprint(playerO.brain)
    print("---")
    pprint(playerX.brain)

    plot_name = "simulacao"
    plot(vitoriasO, vitoriasX, empates, plot_name, show=True)
