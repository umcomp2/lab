
import os


#Check EoF.
def is_eof(fileHandle):
        cur = fileHandle.tell()
        fileHandle.seek(0, os.SEEK_END)
        end = fileHandle.tell()
        fileHandle.seek(cur, os.SEEK_SET)
        return cur == end


# Se le da un archivo ppm y separa ecabezado y cuerpo.
class Input():
    def __init__(self, filename, mode='rb'):
        self.filename = filename
        self.fileHandle = open(filename, mode)
        self.header = b''

    def getHeader(self):
        while True:
            line = self.fileHandle.readline()
            self.header += line
            if line == b'255\n':
                break
        print('Header Done')
        return self.header

    def getBody(self):
        tempFile = open('temp.tmp', 'wb')
        while True:
            tempData = self.fileHandle.readline()
            tempFile.write(tempData)
            if is_eof(self.fileHandle):
                break
        print('Body Done')
