import chess
import chess.engine
import chess.pgn
import re
import chess
from termcolor import colored

def print_colored_board(board):
    board_str = str(board)  # tabuleiro em ASCII
    result = ""

    for char in board_str:
        if char in "PRNBQK":  # peças brancas
            result += colored(char, "white")
        elif char in "prnbqk":  # peças pretas
            result += colored(char, "red")  # pode trocar por "red", "green", etc.
        elif char == ".":
            result += colored(".", "grey")
        else:
            result += char

    print(result, "\n", "\n")


def carregar_movimentos_iniciais(board, movimentos):

   for move in movimentos:
        try:
            # Tentar fazer o movimento usando notação SAN
            san_move = board.parse_san(move)
            if san_move in board.legal_moves:
                board.push(san_move)
            else:
                print(f"Movimento inválido: {move}")
        except ValueError:
            print(f"Movimento não reconhecido: {move}")


def jogar_com_engine(board, engine_path, jogadas=10, tempo_por_jogada=1.0):
    with chess.engine.SimpleEngine.popen_uci(engine_path) as engine:
        for i in range(jogadas):
            jogador = "Brancas" if board.turn else "Pretas"
            resultado = engine.play(board, chess.engine.Limit(time=tempo_por_jogada))
            print(f"Jogada {i + 1} ({jogador}): {resultado.move}")
            board.push(resultado.move)  # já aceita objeto Move direto
            print_colored_board(board)


moves = """
1. d4 d5 2. Nf3 Nf6 3. Nc3 c5 4. Nb5 a6 5. Nc3 cxd4 6. Qxd4 Nc6 7. Qh4 d4 8. Ne4
Bf5 9. Nxf6+ exf6 10. e4 g5 11. Nxg5 fxg5 12. Bxg5 Qa5+
"""

moves = moves.replace("\n", " ")
historico_movimentos = re.sub(r"\d+\.", "", moves).split()

# Execução
board = chess.Board()

carregar_movimentos_iniciais(board, historico_movimentos)

print_colored_board(board)

jogar_com_engine(board, "/usr/bin/stockfish", jogadas=6, tempo_por_jogada=50)

game = chess.pgn.Game.from_board(board)

# Salvar para arquivo
with open("partida.pgn", "w", encoding="utf-8") as pgn_file:
    # Inicializa uma variável para armazenar as jogadas formatadas
    moves = []

    # Itera sobre as jogadas do jogo
    for i, move in enumerate(game.mainline_moves()):
        # Adiciona a jogada formatada à lista
        if i % 2 == 0:  # Jogada do branco
            moves.append(f"{(i // 2) + 1}. {move}")
        else:  # Jogada do preto
            moves[-1] += f" {move}"

    # Escreve as jogadas no arquivo, cada rodada em uma linha
    for move_line in moves:
        print(move_line, file=pgn_file)
