#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sys import argv
from time import sleep
import threading
import requests
from main import get_Threads
# import config
from controller.manageRequest import process
#import traceback
import sys

'''Variavel que armazena o estado da conexao internet'''
'''INTERNET = False'''

'''
    Funçao que é inicializada com o inicio da aplicação para instânciar toda a macro.
    @return ? Bolean: apenas representa se a função foi terminada de forma saúdavel ou não.
'''


def initialize():
    #global PROGRAM_PATH
    global INTERNET
    '''Argumento opcional que muda o local do programa alvo padrão'''
    if len(argv) > 1:
       #config.PROGRAM_PATH = argv[1]
       pass

    print('Verificando Acesso a Internet...')
    INTERNET = False

    '''Inicializa a thread que verifica conexao com internet'''
    get_Threads().append(threading.Thread(target=internet,name="internet"))
    get_Threads()[len(get_Threads())-1].start()
    while not INTERNET:
        print('sem acesso a internet...')
        sleep(0.20)
    
    if not work():
        return shutdownThreads(False)

    return shutdownThreads(True)

def work():
    while True:
        try:
            if INTERNET:
                # if True:                    
                process()
                break
                # else:
                #     sleep(10)
                #     print('Sem processos para executar...')
                #break
            sleep(5)
        except Exception as e:
            # linhaerro = None
            # try:
            #     for stack in reversed(traceback.extract_stack(limit=9)):
            #         if linhaerro == None:
            #             linhaerro = '*Erro na Linha:* {} ({} - {})'.format(stack.lineno,stack.filename,stack.name)
            #         else:
            #             linhaerro += ', {} ({} - {})'.format(stack.lineno,stack.filename,stack.name)
            # except:
            #     if linhaerro == None:
            #         linhaerro = 'Não foi possivel informar a Linha!'
            # teste = sys.exc_info()[-1]
            try:
                lineError = 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
            except:
                lineError = 'Error without line'
            print("{} linha erro: {}".format(e,lineError))
            return False
    return True


'''
    Funçao que verifica se tem internet
    @params : Todos os parametros sao padrões para checagem
'''


def internet(url="https://www.google.com.br/", timeout=5):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    TIME_DELAY = 2

    global INTERNET

    while True:
        try:
            requests.get(url=url, timeout=timeout)
            INTERNET = True
        except:
            INTERNET = False
            pass

        if getattr(threading.currentThread(), "stop", False):
            break

        sleep(TIME_DELAY)

def shutdownThreads(return_tmp = None):
    #global THREADS
    for thread in get_Threads():
        thread.stop = True
    if return_tmp == None:
        pass
    else:
        return return_tmp