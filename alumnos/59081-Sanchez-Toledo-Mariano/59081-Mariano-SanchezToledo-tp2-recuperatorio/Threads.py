from threading import Thread

def createThread(target=None, name=None, args=()):
    return Thread(target, name, args())
