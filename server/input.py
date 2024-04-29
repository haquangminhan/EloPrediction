import numpy as np
class Input:
    def __init__(self):
        self.move_count = 0
        self.data = []

    def append(self, newData):
        self.move_count += 1
        self.data.append([self.move_count] + newData)

    def toNumpyArray(self):
        return np.array(self.data)

    def reset(self):
        self.move_count = 0
        self.data = []
    
