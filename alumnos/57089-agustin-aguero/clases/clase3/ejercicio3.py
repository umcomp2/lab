import time, sys,signal,os 

class Signal():
    def __init__(self):
        self.time = 1
        self.number = 0
    
    def handler(self,signal_number,frame): # what does frame do?
        if signal_number == 10:         #sigusr1
            self.time = self.time *2
        
        if signal_number == 12:      #sigusr2
            self.time = self.time /2
            if self.time < 1:
                print("time less that 1 sec, exit")
                sys.exit()


    def printeable(self): #this will show the consecutive numbers and apply a sleep
        while True:
            print(self.number)
            self.number +=1
            time.sleep(self.time)

if __name__ == "__main__":

    def recibir_señal(signal_number,frame): #why do i need a frame?
        inst.handler(signal_number,frame)
    
    signal.signal(signal.SIGUSR1,recibir_señal)
    signal.signal(signal.SIGUSR2,recibir_señal)

    inst= Signal()
    print(f"WITH THIS PID: {os.getpid()} if we send in another terminal [kill - 10(SIGUSR1) or -12(SIGUSR2) {os.getpid()}],it will initialize the logic ")
    inst.printeable()
    #signal.pause()


