import os

class PPMParser():
    def __init__(self, filePath, blocksize):
        self.filePath = filePath
        self.blocksize = blocksize
        self.filefd = os.open(filePath, os.O_RDONLY)
        # self.dimensions = self.parseDimensions()
        # self.bytesStart = self.parseBytesStart()
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
                pixels.append((None, None, None))
        os.lseek(self.filefd, 0, os.SEEK_SET)
        return pixels

    def parseMetaData(self):
        image = open(self.filefd)
        metadata = []
        while len(metadata) < 4:
            # line = image.readline()
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
        return fileSize - int(self.metadata[1])*int(self.metadata[2])*3 - 1

    def getLine(self):
        c = b""
        while (newlineIndex := c.find(b"\n")) == -1:
            c += os.read(self.filefd, 10)
        os.lseek(self.filefd, newlineIndex - len(c) + 1, os.SEEK_CUR)
        #print(newlineIndex - len(c))
        return c[0:newlineIndex]

    def parseDimensions(self):
        c = os.read(self.filefd, 20)
        c = c.split(b"\n")
        for i in range(len(c)):
            if c[i][0] == "#":
                c.pop(i)
        print(c)
        c = c[1]
        c = c.decode().split(" ")
        os.lseek(self.filefd, 0, os.SEEK_SET) 
        return (c[0], c[1])

    def parseBytesStart(self):
        """
        c = os.read(self.filefd, 40)
        for i in range(len(c)):
            if c[i] not in [10, 32, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 80, 35]:
                break

        
        c = str(c[0:i], "ascii")
        print(c)
        """
        return 0

        """
        blankspaces = 0
        blankSpacePosition = 0
        found = False
        while found is not True:
            c = os.read(self.filefd, 20)
            for i in range(len(c)):
                if c[i] in (10, 32):
                    blankspaces += 1
                    blankSpacePosition = i
            if blankspaces == 4:
                found = True 
        return blankSpacePosition+1
        """

