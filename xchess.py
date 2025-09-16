import chess
import chess.engine

board = chess.Board()


moves_uci = [
    "e2e4", "d7d5", #1
    "f2f3", "g8f6", #2
    "d2d4", "e7e6", #3
    "b1c3", "b8c6", #4
    "a2a3", "f8e7", #5
    "c1e3", "a7a6", #6
    "d1d2", "b7b5", #7
    "e1c1", "e7d6", #8
    "g2g4", "h7h6", #9
    "e4e5", "c6e5", #1
    "d4e5", "d6e5", #11
    "g4g5", "h6g5", #12
    "e3g5", "c8b7", #13
    "f3f4", "e5d6", #14
    "d1e1", "d5d4", #15
    "c3e4", "f6e4", #16
    "d2d4", "d6f4", #17
    "g5f4", "d8d4", #18
    "g1f3", "d4f6", #19
    ""
]

for move in moves_uci:
    board.push_uci(move)

# Inicie o motor Stockfish
with chess.engine.SimpleEngine.popen_uci("/usr/bin/stockfish") as engine:
    for i in range(3):  # Para as próximas 3 jogadas
        result = engine.play(board, chess.engine.Limit(time=60.0))  # Limite de tempo de 60 segundos
        print(f"Melhor jogada {i + 1} para as pretas:", result.move)

        # Aplique a jogada ao tabuleiro
        board.push_uci(result.move.uci())
        print(board)
        print (f"/n/t")
