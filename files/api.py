import numpy as np
from itertools import product
from functools import partial
from random import choices, choice
from matplotlib import pyplot as plt


ALL_SYMMETRY_OP = {
    "id": lambda x: x,
    "rot90": partial(np.rot90, k=1),
    "rot180": partial(np.rot90, k=2),
    "rot270": partial(np.rot90, k=3),
    "flipv": np.fliplr,
    "fliph": np.flipud,
    "flipds": lambda x: np.fliplr(np.rot90(x)),
    "flipdp": lambda x: np.flipud(np.rot90(x)),
}

# Operaçãos inversas
ALL_SYMMETRY_OP_INV = {
    "id": lambda x: x,
    "rot90": partial(np.rot90, k=-1),
    "rot180": partial(np.rot90, k=-2),
    "rot270": partial(np.rot90, k=-3),
    "flipv": np.fliplr,
    "fliph": np.flipud,
    "flipds": lambda x: np.fliplr(np.rot90(x)),
    "flipdp": lambda x: np.flipud(np.rot90(x)),
}


def testa_simetrias():
    """Para testar se as operações são válidas. Se der print, tem algo errado."""
    for jogo in map(Configuracao, product([0, 1, 2], repeat=9)):
        conf = jogo.config
        for name in ALL_SYMMETRY_OP:
            op = ALL_SYMMETRY_OP[name](conf)
            treat = ALL_SYMMETRY_OP_INV[name](op)
            if not np.all(np.equal(conf, treat)):
                print(name)
                print(conf)
                print()
                print(treat)
                print()
                return


class Configuracao:
    """Classe para representar uma configuração do jogo da velha.

    Args:
      representacao:
        Numpy array de representando o jogo. Pode ser a representação em grade
        3x3 ou em vetor linha, tanto faz. Pode ser também a representação em
        string da configuração.
    """

    def __init__(self, representacao="000000000"):
        if isinstance(representacao, str):
            self.config = np.array(list(representacao), dtype=int)
        else:
            self.config = np.array(representacao, dtype=int)

        msg = "Tua configuração deve ter 9 posições"
        assert len(self.config.ravel() == 9), msg
        self.config = self.config.reshape(3, 3)
        self.esta_encolhido = False
        self.lista = list(self.config.ravel())

    def __repr__(self):
        return self.config.reshape(3, 3).__str__()

    def encolhe(self):
        """Faz com que a representação da configuração fique encolhida."""
        self.esta_encolhido = True
        self.config = self.config.ravel()
        return self.config

    def desencolhe(self):
        """Faz com que a representação da configuração fique desencolhida."""
        self.esta_encolhido = False
        self.config = self.config.reshape(3, 3)
        return self.config

    def symmetry_dict(self):
        """Gera o conjunto de simetrias."""
        if not hasattr(self, "symmetries"):
            symmetries = {}
            self.desencolhe()
            for name, op in ALL_SYMMETRY_OP.items():
                id_ = "".join(str(num) for num in op(self.config).ravel())
                symmetries[name] = id_
            self.symmetries = symmetries
        return self.symmetries

    def get_symmetry_id(self):
        """O ID oficial da config. é a string da primeira posição do sorted."""
        self.symmetry_dict()
        self.id_ = sorted(self.symmetries.values())[0]
        self.op_name = [
            name
            for name in self.symmetries
            if self.symmetries[name] == self.id_
        ][0]
        return self.id_

    def symmetry_map(self):
        """Computa o mapa de simetria. Números iguais representam mesma jogada."""
        self.symmetry_dict()
        mapa = (np.arange(9) + 1).reshape(3, 3)

        base = self.symmetries["id"]

        if base == self.symmetries["fliph"]:
            mapa[2, :] = mapa[0, :]
        if base == self.symmetries["flipv"]:
            mapa[:, 2] = mapa[:, 0]
        if base == self.symmetries["flipdp"]:
            mapa[1, 0] = mapa[0, 1]
            mapa[2, 0] = mapa[0, 2]
            mapa[2, 1] = mapa[1, 2]
        if base == self.symmetries["flipds"]:
            mapa[1, 2] = mapa[0, 1]
            mapa[2, 2] = mapa[0, 0]
            mapa[2, 1] = mapa[1, 0]
        if base in [self.symmetries["rot90"], self.symmetries["rot270"]]:
            mapa[0, 0] = mapa[0, 2] = mapa[2, 0] = mapa[2, 2] = 1
            mapa[0, 1] = mapa[1, 0] = mapa[1, 2] = mapa[2, 1] = 2
        if base == self.symmetries["rot180"]:
            mapa[2, 1] = mapa[0, 1]
            mapa[1, 2] = mapa[1, 0]
            mapa[2, 2] = mapa[0, 0]
            mapa[2, 0] = mapa[0, 2]

        # jogadas proibidas tem número -1
        logic = self.config > 0
        mapa[logic] = -1

        return mapa

    def create_choice_dict(self, initial_value=8, decay=2):
        """Cria dicionário com todas as as jogadas iniciadas com o mesmo valor.

        Args:
          initial_value:
            Inteiro que será o número de beads de cada posição permitida na
            primeira rodada.
          decay:
            Taxa de perda de beads a cada rodada.

        Returns:
          Dicionário com posições como chaves e número de beads como valores.
        """

        self.get_symmetry_id()

        # computa o número de beads desta rodada usando decay
        num_empty = self.id_.count("0")
        num_beads = 0
        if num_empty >= 8:
            # primeira jogada do jogador 1 ou 2
            num_beads = initial_value
        elif num_empty >= 6:
            # segunda jogada do jogador 1 ou 2
            num_beads = initial_value / decay
        elif num_empty >= 4:
            # terceira jogada do jogador 1 ou 2
            num_beads = (initial_value / decay) / decay
        elif num_empty >= 2:
            # quarta jogada do jogador 1 ou 2
            num_beads = ((initial_value / decay) / decay) / decay

        num_beads = int(round(num_beads))
        num_beads = num_beads if num_beads > 0 else 1

        # tem que converter para a posição padrão antes
        conf = Configuracao(self.id_)
        mapa = conf.symmetry_map()

        # preenche dicionário
        choice_dict = {v: num_beads for v in set(mapa[mapa > 0])}

        return choice_dict

    def check_vitoria(self, jogador):
        """Checa se jogador ganhou."""
        self.desencolhe()
        logic = self.config == jogador
        if (
            3 in logic.sum(axis=0)
            or 3 in logic.sum(axis=1)
            or np.trace(logic) == 3
            or np.trace(np.fliplr(logic)) == 3
        ):
            return True
        else:
            return False


class Jogador:
    """Cria um agente jogador de jogo da velha.

    Args:
      player_num : int
        Valor 1 representa jogador que faz primeiro movimento e valor 2
        representa o outro jogador.
      valor_inicial : int
        Quantidade de missangas de cada cor distribuidas inicialmente nas caixas
        de fósforo.
      reforco_vitoria : int
        Quantidade de missangas adicionadas quando se ganha.
      reforco_derrota : int
        Quantidade de missangas adicionadas quando se perde.
      reforco_empate : int
        Quantidade de missangas adicionadas quando se empata.
    """

    def __init__(
        self,
        player_num=1,
        valor_inicial=8,
        reforco_vitoria=3,
        reforco_derrota=-1,
        reforco_empate=0,
        decay_do_valor_inicial=2,
    ):
        assert valor_inicial > 0
        self.player_num = player_num
        self.valor_inicial = valor_inicial
        self.decay_do_valor_inicial = decay_do_valor_inicial
        self.cria_dicionario_jogadas()
        self.reforco_vitoria = reforco_vitoria
        self.reforco_derrota = reforco_derrota
        self.reforco_empate = reforco_empate
        self.jogadas = []
        self.num_jogos = 0

    def cria_dicionario_jogadas(self):
        """Cria dicionário de todas as jogadas possíveis do jogador.

        Lista apenas jogos onde mais de uma escolha pode ser feita.

        Condições:
        + Jogador 1 é quem começa a jogar
        + Jogos já ganhos não são listados
        + jogos com apenas um movimento possível não são listados
        + jogos sem um movimento possível não são listados
        """

        if self.player_num == 1:
            diff = 0
        else:
            diff = 1

        jogos = {
            jogo.get_symmetry_id(): jogo.create_choice_dict(
                self.valor_inicial, self.decay_do_valor_inicial
            )
            for jogo in map(Configuracao, product([0, 1, 2], repeat=9))
            if jogo.lista.count(1) - jogo.lista.count(2) == diff
            and not (jogo.check_vitoria(1) or jogo.check_vitoria(2))
            and not jogo.lista.count(0) in [0, 1]
        }

        self.brain = jogos

    def realizar_jogada(self, config, verbose=False, return_prob=False):
        """Recebe uma configuração e retorna a configuração com jogada realizada.

        Args:
          config:
            Configuração atual do tabuleiro. Pode ser string ou instancia de
            Configuracao.
          verbose:
            Se `True`, então printa informações da jogada. Para ser usado no
            debug.
          return_prob:
            Se `True`, então além da jogada realizada, retorna um array com as
            probabilidades que cada casa tinha de ser sorteada. Probabilidades
            representadas em um número entre zero e um.

        Return:
          Se `return_prob=False` então retorna uma instância de Configuração com
          a jogada já realizada. Se `return_prob=True`, então retorna
          adicionalmente um array com as probabilidade de cada casa ser jogada
          (probabilidades antes da jogada ser realizada).
        """

        config = Configuracao(config) if isinstance(config, str) else config
        id_ = config.get_symmetry_id()

        if id_.count("0") == 1:
            # apenas uma jogada a ser feita, não temos escolha
            array = config.desencolhe()
            logic = array == 0
            array[logic] = self.player_num
            config_up = Configuracao(array)

            if return_prob:
                prob_cada_casa = np.zeros((3, 3))
                prob_cada_casa[logic] = 1
                return config_up, prob_cada_casa
            else:
                return config_up

        else:
            dicionario = self.brain[id_]
            posicoes = list(dicionario.keys())
            chance = list(dicionario.values())

            # escolhe jogada
            casa_escolhida = choices(posicoes, weights=chance)[0]

            config_up = Configuracao(id_)
            mapa = config_up.symmetry_map()

            if verbose:
                print(config)
                print(ALL_SYMMETRY_OP_INV[config.op_name](mapa))
                print(casa_escolhida)
                print(dicionario)
                print(config.op_name)
                print()

            index = choice(np.where(mapa.ravel() == casa_escolhida)[0])

            lista = config_up.lista.copy()
            lista[index] = self.player_num
            array = np.array(lista).reshape(3, 3)
            array = ALL_SYMMETRY_OP_INV[config.op_name](array)
            config_up = Configuracao(array)

            # registra jogo feito
            self.jogadas.append([dicionario, casa_escolhida])

            if return_prob:
                # computa as chances de cada casa ser jogada
                prob_cada_casa = np.zeros(9)

                for i in range(9):
                    pos = mapa.ravel()[i]
                    prob_cada_casa[i] = dicionario[pos] if pos > 0 else 0

                prob_cada_casa /= prob_cada_casa.sum()
                prob_cada_casa = prob_cada_casa.reshape(3, 3)
                prob_cada_casa = ALL_SYMMETRY_OP_INV[config.op_name](
                    prob_cada_casa
                )

                return config_up, prob_cada_casa
            else:
                return config_up

    def atualizar_vitoria(self):
        """Atualiza os dicionários de escolha em caso de vitória."""

        for dicionario, casa_escolhida in self.jogadas:
            dicionario[casa_escolhida] += self.reforco_vitoria

            if dicionario[casa_escolhida] < 0:
                dicionario[casa_escolhida] = 0

            # se uma caixa está sem missangas, temos que resetá-la
            if sum(list(dicionario.values())) <= 0:
                for k in dicionario:
                    dicionario[k] = self.valor_inicial

        self.jogadas = []
        self.num_jogos += 1

    def atualizar_derrota(self):
        """Atualiza os dicionários de escolha em caso de derrota."""

        for dicionario, casa_escolhida in self.jogadas:
            dicionario[casa_escolhida] += self.reforco_derrota

            if dicionario[casa_escolhida] < 0:
                dicionario[casa_escolhida] = 0

            # se uma caixa está sem missangas, temos que resetá-la
            if sum(list(dicionario.values())) <= 0:
                for k in dicionario:
                    dicionario[k] = self.valor_inicial

        self.jogadas = []
        self.num_jogos += 1

    def atualizar_empate(self):
        """Atualiza os dicionários de escolha em caso de empate."""

        for dicionario, casa_escolhida in self.jogadas:
            dicionario[casa_escolhida] += self.reforco_empate

            if dicionario[casa_escolhida] < 0:
                dicionario[casa_escolhida] = 0

            # se uma caixa está sem missangas, temos que resetá-la
            if sum(list(dicionario.values())) <= 0:
                for k in dicionario:
                    dicionario[k] = self.valor_inicial

        self.jogadas = []
        self.num_jogos += 1


def simulacao(player1, player2, num_jogos=100):
    jogadores = [player1, player2]
    vitorias1 = [0]
    vitorias2 = [0]
    empates = [0]

    for _ in range(num_jogos):
        config = Configuracao()
        jogador_da_vez = False

        while (
            (not config.check_vitoria(1))
            and (not config.check_vitoria(2))
            and (config.get_symmetry_id().count("0") > 0)
        ):
            config = jogadores[jogador_da_vez].realizar_jogada(config, False)
            jogador_da_vez = not jogador_da_vez

        if config.check_vitoria(1):
            jogadores[0].atualizar_vitoria()
            jogadores[1].atualizar_derrota()
            vitorias1.append(vitorias1[-1] + 1)
            vitorias2.append(vitorias2[-1])
            empates.append(empates[-1])

        elif config.check_vitoria(2):
            jogadores[1].atualizar_vitoria()
            jogadores[0].atualizar_derrota()
            vitorias2.append(vitorias2[-1] + 1)
            vitorias1.append(vitorias1[-1])
            empates.append(empates[-1])

        else:
            jogadores[1].atualizar_empate()
            jogadores[0].atualizar_empate()
            vitorias1.append(vitorias1[-1])
            vitorias2.append(vitorias2[-1])
            empates.append(empates[-1] + 1)

    return player1, player2, vitorias1, vitorias2, empates


def plot(
    vitorias1,
    vitorias2,
    empates,
    plot_name="",
    show=False,
    label1="Vitórias 1",
    label2="Vitórias 2",
):
    fig, axe = plt.subplots(
        ncols=1,
        nrows=1,
        figsize=(5, 5),
        dpi=150,
    )

    x = list(range(1, len(vitorias1)))

    axe.plot(x, vitorias1[1:], label=label1)
    axe.plot(x, vitorias2[1:], label=label2)
    axe.plot(x, empates[1:], label="Empates")

    axe.set_xlabel("Jogo")
    axe.set_ylabel("Quantidade")

    fig.legend()

    if plot_name:
        fig.savefig(
            f"{plot_name}.png",
            dpi=150,
            bbox_inches="tight",
            pad_inches=2e-2,
        )

    if show:
        plt.show()

    plt.close(fig)
