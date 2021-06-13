def writePPM(file, img):
    """
    """
    file.write(bytearray('P6\n'+
                         str(len(img[0]))+
                         ' '+str(len(img))
                         +'\n255\n'
                         , 'ascii'))
    for row in img:
        for rgb in row:
            file.write(bytes(rgb))
    return None



    