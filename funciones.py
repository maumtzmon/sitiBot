########################################################################
#
# Plantilla de funciones basicas adicionales del bot de Telegram
# Ing. Mauricio Martinez Montero
# LabDet, Criogenia. Instituto de Ciencias Nucleares, UNAM.
#
# Pequeña plantilla que contiene funciones de analisis y procesos
# en ella podemos programar lo que sea y devolver el resultado en 
# formato string para desplegarla como un mensaje en la interfaz de 
# Telegram
#
#
########################################################################


import urllib.request
from urllib.error import URLError
import sched, time

s = sched.scheduler(time.time, time.sleep)



def check_url(checarIP, checarPuerto):
    url='http://'+ checarIP + ':' + checarPuerto + '/'
    try:
        error_code=urllib.request.urlopen(url).getcode()
        return error_code
    except URLError as e:
        error_code= str(e)
        return error_code

def time_onServer():
    time_server=time.localtime()
    time_dict= { 'year': str(time_server.tm_year), 'month':str(time_server.tm_mon), \
        'day':str(time_server.tm_mday), 'hour':str(time_server.tm_hour), \
        'min':str(time_server.tm_min), 'sec':str(time_server.tm_sec), 'tzone':str(time_server.tm_zone)}
    
    date_time = time_dict['year']+'-'+time_dict['month']+'-'+time_dict['day']+' '\
        + time_dict['hour']+':'+time_dict['min']+':'+time_dict['sec']

    return date_time

def print_time(a='default'):
    print("From print_time", time.time(), a)

def print_some_times():
    print(time.time())
    s.enter(10, 1, print_time)
    s.enter(5, 2, print_time, argument=('positional',))
    s.enter(5, 1, print_time, kwargs={'a': 'keyword'})
    s.run()
    print(time.time())



        
    