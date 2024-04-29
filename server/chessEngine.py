from lczero.backends import Weights, Backend, GameState
import chess
from stockfish import Stockfish

class ChessEngine:
    def __init__(self):
        self.large_net_size = Backend(weights=Weights('./Lc0_networks/768x15x24h-t82-2-swa-5230000.pb'), backend='eigen')
        self.medium_net_size = Backend(weights=Weights('./Lc0_networks/t1-smolgen-512x15x8h-distilled-swa-3395000.pb'), backend='eigen')
        self.small_net_size = Backend(weights=Weights('./Lc0_networks/t1-256x10-distilled-swa-2432500.pb'), backend='eigen')

        self.stockfish = Stockfish('/opt/homebrew/bin/stockfish')
        
        self.move_qualities = {}
        self.fen_evaluations_cache = {"large": {}, "medium": {}, "small": {}}

    
    def bestMove(self, fen, Elo):
        self.stockfish.set_fen_position(fen)
        self.stockfish.set_elo_rating(Elo)

        # Get best move
        bestMove = self.stockfish.get_best_move()

        return bestMove

    def LCZERO_Eval_with_cache(self, fen, name, network):
        # Check if the FEN has already been evaluated
        if fen in self.fen_evaluations_cache[name]:
            return self.fen_evaluations_cache[name][fen]

        # If not in cache, evaluate the position and store the result in the cache
        input_data = GameState(fen=fen).as_input(network)
        evaluation = network.evaluate(input_data)[0].q()
        self.fen_evaluations_cache[name][fen] = evaluation

        return evaluation

    def move_quality_with_cache(self, fen_before, move):
        move_qualities = {}
        position_evaluation = {}

        for name, network in [("large", self.large_net_size), ("medium", self.medium_net_size), ("small", self.small_net_size)]:
            # Evaluate the position before the move, using the caching version of LCZERO_Eval
            pre_move_evaluation = self.LCZERO_Eval_with_cache(fen_before, name, network)
            position_evaluation[name] = pre_move_evaluation

            # Play move
            board = chess.Board(fen_before)
            board.push(move)
            fen_after = board.fen()

            # Evaluate the new position after the move
            post_move_evaluation = self.LCZERO_Eval_with_cache(fen_after, name, network)

            # Calculate the quality of the move
            move_quality =  - post_move_evaluation - pre_move_evaluation

            move_qualities[name] = move_quality

        return move_qualities, position_evaluation
    
    def piece_count_encoded(self, piece_count):
        Q1 = 17 #quantile(0.25)
        Q3 = 30 #quantile(0.75)
        if piece_count <= Q1:
            return 0
        elif piece_count <= Q3:
            return 1
        else:
            return 2

    def transform_data(self, FEN, move):
        fen = FEN # FEN String

        turn = fen.split(' ')[1]

        material_balance, piece_count, num_of_legal_move = self.piece_count_and_balance(fen)
        double_pawns, isolated_pawns, passed_pawns = self.calculate_pawn_structure(fen)

        piece_count_encoded = self.piece_count_encoded(piece_count)

        chess_move = chess.Move.from_uci(move)

        move_quality, position_evaluation = self.move_quality_with_cache(fen, chess_move)

        #ELO
        if turn == 'w':
            my_double_pawns, opponent_double_pawns = double_pawns['white'], double_pawns['black']
            my_isolated_pawns, opponent_isolated_pawns = isolated_pawns['white'], isolated_pawns['black']
            my_passed_pawns, opponent_passed_pawns = passed_pawns['white'], passed_pawns['black']
        else:
            material_balance = - material_balance

            my_double_pawns, opponent_double_pawns = double_pawns['black'], double_pawns['white']
            my_isolated_pawns, opponent_isolated_pawns = isolated_pawns['black'], isolated_pawns['white']
            my_passed_pawns, opponent_passed_pawns = passed_pawns['black'], passed_pawns['white']

        data = [material_balance, 
                num_of_legal_move, 
                my_double_pawns, 
                opponent_double_pawns, 
                my_isolated_pawns, 
                opponent_isolated_pawns, 
                my_passed_pawns, 
                opponent_passed_pawns, 
                move_quality['small'], 
                move_quality['medium'], 
                move_quality['large'], 
                position_evaluation['small'], 
                position_evaluation['medium'], 
                position_evaluation['large'], 
                piece_count_encoded
        ]
        

        return data

    def piece_count_and_balance(self, fen):
        piece_values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9,
                        'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9}

        board = chess.Board(fen)
        num_of_legal_move = len(list(board.legal_moves))

        # Extract the board placement part from the FEN string
        board_part = fen.split(' ')[0]

        # Calculate the material balance
        balance = 0
        piece_count = 2 #2 kings
        for piece in board_part:
            if piece in piece_values:
                piece_count += 1
                balance += piece_values[piece]

        return balance, piece_count, num_of_legal_move
    
    def calculate_pawn_structure(self, fen):
        board = chess.Board(fen)
        pawns = {'white': {}, 'black': {}}

        double_pawns = {'white': 0, 'black': 0}
        isolated_pawns = {'white': 0, 'black': 0}
        passed_pawns = {'white': 0, 'black': 0}

        # Initialize pawn files
        for file in range(8):
            pawns['white'][file] = []
            pawns['black'][file] = []

        # Count pawns on each file
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.piece_type == chess.PAWN:
                color = 'white' if piece.color else 'black'
                file = chess.square_file(square)
                rank = chess.square_rank(square)
                pawns[color][file].append(rank)

        #print('white: ', pawns['white'])
        #print('black: ', pawns['black'])

        # Identify double and isolated pawns
        for color in ['white', 'black']:
            for file in range(8):

                file_count = len(pawns[color][file])

                # Double pawns
                if file_count > 1:
                    double_pawns[color] += file_count - 1

                # Isolated pawns
                if file_count > 0:
                    left_has_pawn = len(pawns[color][file - 1]) > 0 if file > 0 else False
                    right_has_pawn = len(pawns[color][file + 1]) > 0 if file < 7 else False
                    if not left_has_pawn and not right_has_pawn:
                        isolated_pawns[color] += file_count

                # Passed pawns
                for rank in pawns[color][file]:
                    is_passed = True
                    for f in [file - 1, file, file + 1]:
                        if f < 0 or f > 7:
                            continue
                        opposing_color = 'black' if color == 'white' else 'white'
                        for opposing_rank in range(rank + 1, 8) if color == 'white' else range(0, rank):
                            if opposing_rank in pawns[opposing_color][f]:
                                is_passed = False
                                break
                        if not is_passed:
                            break
                    if is_passed:
                        passed_pawns[color] += 1

        return double_pawns, isolated_pawns, passed_pawns
    