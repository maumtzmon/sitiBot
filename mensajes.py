########################################################################
#
# Plantilla de mensajes basicos del bot de Telegram
# Ing. Mauricio Martinez Montero
# 
#
########################################################################

user_name =''
user_chat = ''

# Mensajes para responeder en kali bot
msg_uno= 'A continuacion, ingresa la direccion Ip que quieras revisar. por ejemplo 192.168.100.1'

msg_dos='Ingresa el numero de puerto de la direccion Ip que deseas consultar'

msg_tres='mensaje tres'

# Diccionario en el que vamos a asocioar los botones declarados en el main
# con  los mensajes que queremos que se desplieguen al ser accionados.

mensajes={'boton1':msg_uno,\
         'boton2':msg_dos,\
         'boton3':msg_tres}

# Funcion que devolvera el contenido del mensaje cuando se haya accionado un boton
def output_mensajes(boton, chat_id='', name=''):
    user_name = name
    user_chat = chat_id
    print('mensajes, linea 30 siti_connection.py')
    return mensajes[boton]
