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
        try:
            self.filename = filename
            self.fileHandle = open(filename, mode)
            self.header = b''
        except:
            raise ValueError('Imagen no encontrada, verifique la ruta e intentelo nuevamente')

    def processImage(self):
        try:
            while True:
                line = self.fileHandle.readline()
                if line.find(b'#') != -1:
                    continue
                self.header += line
                if line == b'255\n':
                    break
            headerList = self.header.split()
            column, row = headerList[1], headerList[2]
            print('Header Done')
            self.getBody()
            print('Body saved in tmp')
            return self.header, int(column), int(row)
        except:
            raise RuntimeError('Error al extraer header')

    def getBody(self):
        try:
            tempFile = open('body.tmp', 'wb')
            while True:
                tempData = self.fileHandle.readline()
                tempFile.write(tempData)
                if is_eof(self.fileHandle):
                    break
            print('Body Done')
        except:
            raise RuntimeError('Error al extraer body')
