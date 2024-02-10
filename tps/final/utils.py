def agregar_evento(self):
        # Aquí haces las preguntas necesarias para agregar un evento
        self.request.sendall(b"Ingrese el nombre del evento: ")
        nombre_evento = self.request.recv(1024).strip()

        self.request.sendall(bytes("Ingrese el número de sectores: ", 'utf-8'))
        num_sectores = int(self.request.recv(1024).strip())

        sectores = []
        for i in range(num_sectores):
            self.request.sendall(f"Ingrese el nombre del sector {i + 1}: ".encode())
            nombre_sector = self.request.recv(1024).strip().decode()
            self.request.sendall(f"Ingrese la capacidad del sector {i + 1}: ".encode())
            capacidad_sector = int(self.request.recv(1024).strip())
            sectores.append({"nombre": nombre_sector, "capacidad": capacidad_sector})

        # Llama a la tarea de Celery para agregar el evento
        agregar_evento.delay(nombre_evento, sectores)