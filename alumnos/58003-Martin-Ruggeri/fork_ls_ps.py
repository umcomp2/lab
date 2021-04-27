import os
import time


def comando_ls_or_ps(proceso):
    if proceso == "ls":
        os.execlp("ls", "user/bin/ls", "-l")
    elif proceso == "ps":
        os.execlp("ps", "user/bin/ps", "-f")


def esperaHijo():
    os.wait()
    print("soy el padre")


def forkear_con_espera(tiempo_de_espera, comando):
    print(f"soy el proceso padre {os.getpid()}")
    pid = os.fork()
    if pid > 0:
        esperaHijo()
    else:
        time.sleep(tiempo_de_espera)
        print(f"soy el hijo {os.getpid()} de {os.getppid()}")
        comando_ls_or_ps(comando)


if __name__ == "__main__":
    forkear_con_espera(3, "ls")
