import configparser
config = configparser.ConfigParser()
config['conexion'] = {}
config['conexion']['port'] = "1234"
config['conexion']['ip'] = '127.0.0.1'
config['datos_personales'] = {}
config['datos_personales']['nombre'] = "Nahuel"
config['datos_personales']['directorio'] = "/home/nahuel/facultad/computacion/lab/tps/direc1"
config['datos_imagen'] = {}
config['datos_imagen']['imagen'] = "dog.jpg"
config['datos_imagen']['edicion'] = "invertir_colores"
config['parametros_imagen'] = {}
config['parametros_imagen']['n1'] = ""
config['parametros_imagen']['n2'] = ""
config['parametros_imagen']['n3'] = ""
config['parametros_imagen']['n4'] = ""
config['parametros_imagen']['texto'] = ""

with open('cliente.ini', 'w+') as configfile:
  config.write(configfile)
