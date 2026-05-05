# MENACE: Caixas de fósforo que aprendem </h1>

Estamos em busca dos melhores jogadores de Jogo da Velha que possam desafiar o nosso **grande campeão**, o MENACE, uma caixinha de fósforo com habilidades super especiais de **aprendizado de máquina**. Queremos competir com os mais diversos jogadores e aprimorar cada vez mais as habilidades do MENACE!!! E aí?

<p align='center' style='font-size:120%'> VOCÊ ACHA QUE CONSEGUE GANHAR JOGANDO CONTRA UMA CAIXINHA DE FÓSFORO? </p>

<p align="center"><img src="https://github.com/alicevk/MENACE/assets/106678040/f52ddf3b-f538-4edc-816c-7ae54e6d9732" height="300"></p>


## O que é o MENACE e como ele funciona?

O MENACE (Matchbox Educable Noughts and Crosses Engine) consiste em um conjunto de caixas de fósforo, no qual cada uma representa uma possível configuração do tabuleiro do jogo da velha. Dentro de cada caixa há um conjunto de miçangas coloridas, representando todos possíveis movimentos que o MENACE pode realizar.

Inicialmente, as caixas de fósforo são preenchidas com número igual das miçangas que  correspondem a cada jogada. Cada vez que o MENACE joga uma partida de jogo da velha, ele consulta a caixa  correspondente à configuração atual do tabuleiro e seleciona aleatoriamente uma miçanga  dessa caixa. A miçanga selecionada determina a jogada que ele irá realizar. Isso ocorre sucessivamente até o final da partida.

Após o final do jogo, o  MENACE recebe um feedback na forma de vitória, derrota ou empate. Dependendo desse feedback, em cada caixinha o MENACE recebe mais miçangas iguais à que foi sorteada (caso suas jogadas tenham sido boas o suficiente), ou então perde algumas miçangas dessa cor (caso ele não tenha um bom desempenho).

Essa capacidade de receber um feedback demonstra a super habilidade do MENACE: o aprendizado de máquina. Por meio do resultado do seu confronto com o MENACE, conseguimos atribuir valores positivos, negativos ou neutros que comutam em um processo de aprendizado para que o MENACE fique cada vez mais estrategista quando você joga com ele.

**E aí, está preparado para enfrentar esse desafio?**


## Como rodar o MENACE?

A forma mais fácil de rodar o MENACE é usando o `uv`. Para instalar o `uv`, siga o guia na página oficial: https://docs.astral.sh/uv/getting-started/installation/.

Tendo instalado o `uv`, basta rodar o comando abaixo no terminal.

```sh
uvx --from git+https://github.com/drcassar/MENACE menace
```

O comando acima inicia um agente MENACE do zero, sem nenhum treinamento, ideal para observar o processo de aprendizado desde o início. Você pode configurar a dificuldade do MENACE escolhendo um dos 4 comandos abaixo.

```sh
uvx --from git+https://github.com/drcassar/MENACE menace --nivel facil
```

```sh
uvx --from git+https://github.com/drcassar/MENACE menace --nivel medio
```

```sh
uvx --from git+https://github.com/drcassar/MENACE menace --nivel dificil
```

```sh
uvx --from git+https://github.com/drcassar/MENACE menace --nivel impossivel
```

Se você desejar ser o primeiro a jogar, adicione um `--primeiro humano` ao comando.

```sh
uvx --from git+https://github.com/drcassar/MENACE menace --nivel dificil --primeiro humano
```

## Alguns cuidados antes de rodar o MENACE:
	
* Foi implementada uma trava para o jogo não ser fechado sem querer/fora de hora por jogadores em eventos! Por isso, a combinação Alt + F4 não vai fechar a tela! Tome cuidado com isso! O único jeito de sair da tela fullscreen e fechar a janela é digitando o Konami code!!!! ( ↑ ↑ ↓ ↓ ← → ← → B A )

**OBS:** A interface gráfica não foi otimizada para o sistema Windows, por isso tome cuidado extra nessa plataforma! Caso o código acima não funcione, utilize o Gerenciador de Tarefas do Windows.
