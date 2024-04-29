# from joblib import load
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.losses import MeanSquaredError
import pandas as pd

class Predict:
    def __init__(self):
        # self.model = load_model('./model/gru_model.h5')
        self.model = load_model('./model/model_final_chess_Q1_Q3')

    def predict(self, FEN, move, input_to_model, LeelaZero):
        data = LeelaZero.transform_data(FEN, move)

        input_to_model.append(data)
        X_new = input_to_model.toNumpyArray()
        print(X_new)

        X_newnew = self.prepare_sequences(X_new)
        print(X_newnew[0][0][-1])

        y_pred = self.model.predict(X_newnew)
        print("---------------------------------", y_pred[0][0])

        predict_and_evaluation = data[8:14] + [str(y_pred[0][0])]

        return predict_and_evaluation
    
    def prepare_sequences(self, sequences):
        # Determine the maximum sequence length
        max_len = 43

        # Pad the sequences
        X_padded = pad_sequences([sequences], maxlen=max_len, padding='post', dtype='float32')

        return X_padded