import os

class PPMParser():
    def __init__(self, filePath, blocksize):
        self.filePath = filePath
        self.blocksize = blocksize
        self.filefd = os.open(filePath, os.O_RDONLY)
        self.metadata = self.parseMetaData()
        self.metaDataEnd = self.getMetaDataEnd()

    def getPixels(self, firstPixelPosition):
        pixels = []
        os.lseek(self.filefd, self.metaDataEnd+(firstPixelPosition*3), os.SEEK_SET)
        c = os.read(self.filefd, self.blocksize*3)
        for i in range(0, len(c), 3):
            try:
                pixels.append((c[i], c[i+1], c[i+2]))
            except:
                break
        os.lseek(self.filefd, 0, os.SEEK_SET)
        return pixels

    def parseMetaData(self):
        """Returns a list with the metadata.
        Index 0: file signature (P6).
        Index 1: width.
        Index 2: height.
        Index 3: depth."""
        image = open(self.filefd)
        metadata = []
        while len(metadata) < 4:
            line = str(self.getLine(), "utf-8")
            if (poundIndex := line.find("#")) != -1:
                continue
            line = line.split(" ")
            for data in line:
                metadata.append(data)
        image.close()
        self.filefd = os.open(self.filePath, os.O_RDONLY)
        os.lseek(self.filefd, 0, os.SEEK_SET)
        return [data.split().pop() for data in metadata]

    def getMetaDataEnd(self):
        fileSize = os.stat(self.filePath).st_size - 1
        return fileSize - int(self.metadata[1])*int(self.metadata[2])*3

    def getLine(self):
        c = b""
        while (newlineIndex := c.find(b"\n")) == -1:
            c += os.read(self.filefd, 10)
        os.lseek(self.filefd, newlineIndex - len(c) + 1, os.SEEK_CUR)
        return c[0:newlineIndex]
