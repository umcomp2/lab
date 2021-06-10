import threading as th

RGB = {
    'R': 0,
    'G': 1,
    'B': 2
}

class Worker(th.Thread):
    def __init__(self, color, width, matrix):
        th.Thread.__init__(self)
        self.color = color
        self.global_index = 0
        self.width = width
        self.matrix = matrix

    def run(self):
        for i in range(self.color, len(buff), 3):
            col = int(global_index/self.width)
            row = self.width - global_index % self.width - 1
            self.matrix[row][col][self.color] = buff[i]
            global_index += 1


if __name__ == "__main__":
    pass