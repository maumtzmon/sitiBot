
########################################################################
#
# Bot de Telegram para prueba
# Ing. Mauricio Martinez Montero
# Para SITI mx
#
# Pequeña plantilla que incluye librerias basicas para el manejo de 
# un bot en Telegram utilizando Python 3 
#
#
########################################################################

# Librerias basicas de Telegram
#from SITI_bot.time_experiment import time_onServer
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram.ext.messagehandler import MessageHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, Message
from token_str import Token
from VPN_tools import Rasdial
# Librerias para uso de recursos de sistema
import logging, os, signal, time

# Librerias de archivos que se encuentran montados en el mismo directorio que el bot
from mensajes import output_mensajes
from funciones import  check_url, time_onServer# funcion_externa

# Token generado por el Bot Father, ver @BotFather en telegram
Token_Telegram=Token()

#Esto es para que el bot esté buscando constantemente en el servidor por mensajes nuevos.
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('Kalib Bot')

#Variables y archivos que va a utilizar para sus procesos
door = False
boton= 0 
checarIP=''
checarPuerto=''
interval = 30

######################################################################
# Definicion de funciones principales del bot

# Funcion para iniciar el bot
def start(update, context):
    logger.info('He recibido un comando start')
    name = update.effective_chat.first_name #Se obtiene el nombre del usario.
    chat_id = update.effective_chat.id #obtenemos el Chat ID a donde se andara el mensaje
    text = "Hola "+ name +" Vamos a verificar que una red tenga conexion \n" #  Chat Id="+str(chat_id)
    keyboard(chat_id, text, context) #Se envía el mensaje y sale el comando.
    return 0
    
# Funcion para generar botones permitidos en el teclado de Telegram
def keyboard(chat_id, text, context):
    kb = [[KeyboardButton("/ingresaIP")], \
         [KeyboardButton("/ingresaPuerto")], \
         [KeyboardButton("/checarConexion")], \
         #[KeyboardButton("/Boton_4a"), KeyboardButton("/Boton_4b")], \
         #[KeyboardButton("/Boton_5a"), KeyboardButton("/Boton_5b")], \
         #[KeyboardButton("/Boton_6")]]
        ]
    kb1 = ReplyKeyboardMarkup(kb, resize_keyboard=True, one_time_keyboard=True)
    context.bot.send_message(chat_id, text, reply_markup=kb1)
    return 0

# Funciones para los procesos del bot, funciones que realizan una accion
# al presionar cualquiera de los botones disponibles

def boton1(update, context):
    global door, boton  #variables globales para indicar que se apreto un boton
    door = True         #y que boton fue.
    boton = 1

    logger.info('He recibido un comando Boton IP, linea 74 siti_connection.py')
    text = output_mensajes('boton1')
    chat_id = update.effective_chat.id
    keyboard(chat_id, text, context)
    return 0

def boton2(update, context):
    global door, boton
    door = True
    boton = 2

    logger.info('He recibido un comando Boton Puerto, Linea 85 siti_conection.py')
    text = output_mensajes('boton2')
    chat_id = update.effective_chat.id
    keyboard(chat_id, text, context)
    return 0

def boton3(update, context):
    global door, boton   
    door = True
    boton = 3
    outputMessage = ''
    logger.info('He recibido un comando Boton Checa Periodicamente, linea 96 siti_connection.py')
    text = output_mensajes('boton3')
    chat_id = update.effective_chat.id
    keyboard(chat_id, text, context)
    if checarIP != '' and checarPuerto != '':
        checkURL=check_url(checarIP,checarPuerto)
        if checkURL != 200:
            outputMessage='error, no conexion! \n\n Alerta! \n \n Checa manualmente!'
        else:
            outputMessage = 'bien! \n\nEl link funciona!\n\n Revisare que este asi cada '+ str(interval) + ' seg'
            context.bot.send_message(chat_id,outputMessage)
            startAlert(update, context)
    else:
        msg_respuestaNoIP = 'debes ingresar antes los datos usando los botones /ingresaIP e /ingresaPuerto'
        context.bot.send_message(chat_id,msg_respuestaNoIP)

    return 0

    #query = update.callback_query
    #query.answer()

    #return 0

def startAlert(update, context):
    logger.info('He recibido comando alerta, linea 116 siti_connection.py')   #mensaje en la terminal
    text = "Alertas Activadas"                  #Mensaje Telegram al usuario
    chat_id = update.effective_chat.id          
    context.bot.send_message(chat_id, text)
    #calendarizacion de la rutina "Alerta" en el tiempo declarado previamente en "interval"= 60 seg
    new_job = context.job_queue.run_repeating(Alerta, interval = interval, first = 0, context=update.effective_chat.id, name='my_job')

def stopAlert(update, context):
    logger.info('He recibido comando Stop Alerta')
    chat_id = update.effective_chat.id
    text = 'Las alertas se han desactivado'
    context.bot.send_message(chat_id, text)
    jobs = context.job_queue.get_jobs_by_name('my_job')
    #jobs[0].stop()
    jobs[0].schedule_removal() #remosion de rutina de la agenda

def Alerta(context):
    logger.info('Estoy en Alerta, linea 133 siti_connection.py') 
    chat_id = context.job.context
    #Haz algo para revisar que esta en Alerta!
    date_time=time_onServer()
    text = 'Estoy en Alerta, checando si funciona!!!\n' + date_time
    context.bot.send_message(chat_id, text) #comentar cuando este listo el bot
    if checarIP != '' and checarPuerto != '':
        checkURL=check_url(checarIP,checarPuerto)
        if checkURL != 200:
            text = '\n\nAlgo no anda bien...\n\n RUN: COMMAND RISE VPN' #comentar cuando este listo el bot
            context.bot.send_message(chat_id, text)
            logFile=open('log_file.log','a')
            Rasdial_output=Rasdial()
            logger.info(Rasdial_output)#rise vpn
            if Rasdial_output=='VPN rised up':
                message= date_time+' -> ' + str(checkURL) + '\n'
                logFile.write(message)
                logFile.close()
            else:
                message= date_time+' -> ' + str(checkURL) + 'Rasdial error' + Rasdial_output + '\n'
                logFile.write(message)
                logFile.close()
                text = '\n\nAlgo no anda bien...\n\n\nALERTA:\nEL COMANDO RASDIAL NO FUNCIONO!!!\n\n VERIFICA MANUALMENTE\n'
                context.bot.send_message(chat_id, text)
            
        else:
            text = 'Todo bien'
            context.bot.send_message(chat_id, text) #comentar cuando este listo el bot
            return 0
    


# Funcion que maneja los mensajes de texto enviados por el usuario al bot
# sean o no solicitados por el bot

def Text(update,context):
    # 'global door' es una variable que indica si el mensaje se espera por la 
    # accion de un boton o si se recibio el mensaje sin haberlo esperado
    global door, boton, checarIP, checarPuerto 

    logger.info('recibí mensaje, estoy en text, linea 163 siti_connection.py')
    chat_id = update.effective_chat.id
    name = update.effective_chat.first_name
    try:
        link = update.effective_chat.link.split('/')[-1]
    except:
        link = 'no_tiene_link'
    print('usuario: '+link + '/' + name + ', linea 170 siti_connection.py' )
    
    if door == True:

        text = "Perfecto "+ name + ", recibi tu mensaje"
        context.bot.send_message(chat_id, text)
        
        if boton == 1:
            checarIP = update.message.text #ip
            msg_respuesta = "listo, ahora ingresa el puerto utilizando el boton /ingresaPuerto"
            context.bot.send_message(chat_id,msg_respuesta)
            boton = 0
        elif boton == 2:
            checarPuerto =  update.message.text #puerto
            context.bot.send_message(chat_id,'ok, listo, vamos a revisar el link')
            boton = 0
        elif boton == 3:
            messageRecived = update.message.text#ayuda
            boton = 0
        
        if checarIP != '' and checarPuerto != '':
            checkURL=check_url(checarIP,checarPuerto)
            logger.info(checkURL)
            if checkURL != 200:
                outPutmessage = 'Algo anda mal! \n\n ALERTA!\n\n Checa la conexion manualmente!!!'
                context.bot.send_message(chat_id,outPutmessage)
            elif checkURL == 200:
                outPutmessage = 'Bien, el link funciona!\n\nSi deseas que revise periodicamente el link presiona /checarConexion'
                context.bot.send_message(chat_id,outPutmessage)
      
        # chat_id_to_Mau = 18616105 #este chat_id es mio, me enviara un mensaje para indicar que alguien esta usando el bot
        # text_to_Mau = 'el usuario: ' + name + '/ @'+ link + ', hizo una sugerencia para implementar: \n'+ messageRecived
        # context.bot.send_message(chat_id_to_Mau,text_to_Mau)
        
        door = False
    
    else:

        text = "Que gusto " + name + ", Soy el bot Siti!"
        context.bot.send_message(chat_id, text)
        
        
        chat_id_to_Mau = 18616105 #este chat_id es mio, me enviara un mensaje para indicar que alguien esta usando el bot
        messageRecived = update.message.text
        text_to_Mau = 'el usuario: @' + link + ' / ' + name + ', mando un mensaje a kaliBot: \n'+ messageRecived + '\n '
        context.bot.send_message(chat_id_to_Mau,text_to_Mau)
        


######################################################################
# Main del programa

if __name__ == '__main__':


    updater = Updater(Token_Telegram, use_context=True)
    dispatcher = updater.dispatcher

    #comandos y conexion de cada uno a su respectiva funcion
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('ingresaIP', boton1))
    dispatcher.add_handler(CommandHandler('ingresaPuerto', boton2))
    dispatcher.add_handler(CommandHandler('checarConexion', boton3))
    dispatcher.add_handler(CommandHandler('stopAlert', stopAlert))
    # dispatcher.add_handler(CommandHandler())
    # dispatcher.add_handler(CommandHandler())
    
    #maneja la recepcion de texto por parte de un remitente y Text() maneja ese mensaje
    dispatcher.add_handler(MessageHandler(Filters.text, Text))

    #inicia el bot y se mantiene a la espera de la interaccion con un usuario
    updater.start_polling()
    updater.idle()

