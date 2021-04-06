import os
import time


def comando_ls_hijo():
    print(f"soy el hijo {os.getpid()}")
    os.execlp("ls", "user/bin/ls", "-l")

def esperaHijo():
    os.wait()
    print("soy el padre")


if __name__ == "__main__":
    print(f"soy el proceso padre {os.getpid()}")
    pid = os.fork()
    if pid > 0:
        esperaHijo()
    else:
        time.sleep(3)
        comando_ls_hijo()
