"""
En este archivo estan definidos los errores que pueden
surgir durante la ejecucion de main.py
"""
class InvalidFileExtension(Exception):
    """Extension del archivo no valida"""
    pass

class FormatIdentifierNotFound(Exception):
    """Al leer el header del archivo no se encontro"""
    """el identificador del formato PPM            """
    pass