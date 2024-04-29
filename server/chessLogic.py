import chess
from FEN import FENS

class GameState():
    def __init__(self):
        self.fens = FENS
        self.current_fen_index = 0
        self.chessBoard = chess.Board(self.fens[self.current_fen_index])
        self.playerMove = True
        self.Elo = 2400

    def makeMove(self, move, chess_engine):
        try:
            chess_move = chess.Move.from_uci(move)
            if chess_move in self.chessBoard.legal_moves:
                self.chessBoard.push(chess_move)
                # print(self.getFEN())
                # print(move)
                print(f"Successful move: {move}")

                print("Thinking")
                bestMove = chess_engine.bestMove(self.getFEN(), self.Elo)
                chess_move = chess.Move.from_uci(bestMove)
                self.chessBoard.push(chess_move)
                print("Done")

                return True
            else:
                print(f"Illegal move: {move}")
                return False
        except ValueError as e:
            print(f"Error processing move {move}: {e}")
            return False
        
    def set_next_fen(self):
        self.current_fen_index = (self.current_fen_index + 1) % len(self.fens)
        new_fen = self.fens[self.current_fen_index]
        self.chessBoard.set_fen(new_fen)
        self.playerMove = True

    def get_board_position(self):
        position = {}
        for square in chess.SQUARES:
            piece = self.chessBoard.piece_at(square)
            if piece is not None:
                piece_type = piece.symbol()
                if piece.color == chess.WHITE:
                    piece_type = "w" + piece_type
                else:
                    piece_type = "b" + piece_type.upper()
                name = chess.square_name(square)
                position[self.chess_to_array_index(name)] = piece_type
        return position
    
    def chess_to_array_index(self, chess_notation):
        file_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        rank_map = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
        
        file_letter = chess_notation[0]
        rank_number = chess_notation[1]
        
        file_index = file_map[file_letter]
        rank_index = rank_map[rank_number]
        
        return str(rank_index) + str(file_index)
    
    def convert_to_algebraic(self,row, col):
        # Chess files run from 'a' to 'h', which correspond to 0-7 in your system
        file = chr(col + ord('a'))
        # Chess ranks run from '1' to '8', which are 7-0 in your system
        rank = str(8 - row)
        return file + rank
    
    def checkmate_color(self):
        if self.chessBoard.is_checkmate():
            # If it's white's turn, black is in checkmate, and vice versa
            return 'w' if self.chessBoard.turn == chess.WHITE else 'b'
        return None


    def setFEN(self, newFEN):
        self.getBoard().set_fen(newFEN)

    def getBoard(self):
        return self.chessBoard
    
    def getFEN(self):
        return self.getBoard().fen()