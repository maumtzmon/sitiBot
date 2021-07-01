########################################################################
#
# Plantilla de mensajes basicos del bot de Telegram
# Ing. Mauricio Martinez Montero
# 
#
########################################################################

# Mensajes para responeder en kali bot
msg_uno="Ingresa por favor la direccion Ip que quieras revisar. \n\nPor ejemplo, puedes poner 8.8.8.8 o 192.168.1.100"

msg_dos='Ingresa un numero de puerto que quieras revisar en especifico, o escribe solo 80'

msg_tres="Checar nuevamente la IP ingresada previamente"

# Diccionario en el que vamos a asocioar los botones declarados en el main
# con  los mensajes que queremos que se desplieguen al ser accionados.

mensajes={'boton1':msg_uno,\
         'boton2':msg_dos,\
         'boton3':msg_tres}

# Funcion que devolvera el contenido del mensaje cuando se haya accionado un boton
def output_mensajes(boton):
    print('mensajes')
    return mensajes[boton]
