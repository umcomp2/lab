class NoPPMfile(Exception):
    """El archivo no es un archivo PPM"""
    pass

class EscalaNoNegativa(Exception):
    """La escala q otorgamos para cada color no puede ser negativa"""
    pass

class SizeNoNegativo(Exception):
    """Size no puede ser negativo"""
    pass
