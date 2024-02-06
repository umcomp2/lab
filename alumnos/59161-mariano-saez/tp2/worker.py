import threading as th


class Worker(th.Thread):
    def __init__(self, color, width, high, matrix, buff, barrier1, size, sentido):
        th.Thread.__init__(self)
        self.color = color
        self.global_index = 0
        self.width = width
        self.high = high
        self.matrix = matrix
        self.buff = buff
        self.barrier1 = barrier1
        self.size = size
        self.sentido = sentido

    def run(self):
        # Este if hace que no tenga que comprobar en cada iter.
        # del while que sentido se selecciono, sino que solo
        # guardo el id. de la funcion en una variable que apunte
        # a la funcion a ejecutar segun corresponda
        if self.sentido == 90:
            rotate = self.rotate_right
        else:
            rotate = self.rotate_left

        while True:
            # Esperar que el buffer tenga nuevo contenido
            self.barrier1.wait()

            # Algoritmo de ubicacion izq. o der.
            rotate()

            # Control para terminar iteraciones
            if len(self.buff[0]) < self.size:
                break

            # Esperar a que todos terminen de leer
            self.barrier1.wait()


    def rotate_left(self):
        for i in range(self.color, len(self.buff[0]), 3):
                col = int(self.global_index/self.width)
                row = self.width - self.global_index % self.width - 1
                self.matrix[row][col][self.color] = self.buff[0][i]
                self.global_index += 1


    def rotate_right(self):
        for i in range(self.color, len(self.buff[0]), 3):
                row = self.global_index % self.width
                col = self.high - int(self.global_index/self.width) - 1
                self.matrix[row][col][self.color] = self.buff[0][i]
                self.global_index += 1


if __name__ == "__main__":
    pass
