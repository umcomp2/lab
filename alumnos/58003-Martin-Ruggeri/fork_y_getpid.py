import os

print(f"hola mundo {os.getpid()}")
os.fork()
print(f"soy el proceso nuevo{os.getpid()}")
os.fork()
print(f"soy el ultimo proceso {os.getpid()}")
