from flask import Flask, request, jsonify
from chessLogic import GameState
from predict import Predict
from input import Input
from chessEngine import ChessEngine
# import os

app = Flask(__name__)
game_state = GameState()
elo_predict = Predict()
input_to_model = Input()
chess_engine = ChessEngine()


@app.route("/board", methods=['GET'])
def board():
    # Send the current board state to the frontend
    board_array = game_state.get_board_position()
    return jsonify({
        "board": board_array, 
        "checkmateColor": game_state.checkmate_color()
    })

@app.route("/next_fen", methods=['GET'])
def set_fen():
    game_state.set_next_fen()
    input_to_model.reset()
    return jsonify({
        "status": "success",
        "board": game_state.get_board_position(),
        "currentFen": game_state.getFEN(),
    })

@app.route("/move", methods=['POST'])
def move():
    # Receive and process a move request
    data = request.json
    start_position = data['start']
    end_position = data['end']
    promotion = data.get('promotion', '')

    # Convert the positions from 2D array format to algebraic notation
    start_position_algebraic = game_state.convert_to_algebraic(int(start_position[0]), int(start_position[1]))
    end_position_algebraic = game_state.convert_to_algebraic(int(end_position[0]), int(end_position[1]))
    
    # Translate positions to the format expected by the chess library
    move = start_position_algebraic + end_position_algebraic

    if promotion:
        move += promotion.lower()
    
    # Attempt to make the move and respond based on its legality
    fen = game_state.getFEN()
    if game_state.makeMove(move, chess_engine):
        predict = elo_predict.predict(fen, move, input_to_model, chess_engine)
        # print(predict)
        return jsonify({"status": "success",
                        "board": game_state.get_board_position(), 
                        "checkmateColor": game_state.checkmate_color(),
                        "prediction": predict
                        })
    else:
        return jsonify({"status": "failure", 
                        "board": game_state.get_board_position(),  
                        "checkmateColor": game_state.checkmate_color()
                        })

if __name__ == "__main__":
    app.run(debug=True)
    # port = int(os.environ.get("PORT", 5000))  # Default to 5000 if no PORT variable is set
    # app.run(host='0.0.0.0', port=port, debug=False)