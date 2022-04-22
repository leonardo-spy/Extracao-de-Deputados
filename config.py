#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser
import sys
import platform

def initialize():
    global INSTANCIAS_MAX,TENTATIVA_MAX,TEMPO_ESPERA,OS_PLATAFORM,OS_VERSION,IS_EXE
    OS_PLATAFORM = sys.platform
    OS_VERSION =(platform.machine().endswith('64') == True)
    if getattr(sys, 'frozen', False):        
        IS_EXE = True
    else:
        IS_EXE = False

    config = configparser.RawConfigParser()
    config.read('config')
    sections = config.sections()
    if not sections or not 'CONFIG' in sections:
        ''' Quantidade maxima de requisicoes de documentos no site da camera '''
        INSTANCIAS_MAX = 30
        ''' numero de tentativas maxima em um documento que falhou '''
        TENTATIVA_MAX = 3
        ''' segundos que espera para poder processar o documento denovo '''
        TEMPO_ESPERA = 90
        print('Inicializando com váriaveis padrão...')
    else:
        details_dict = dict(config.items('CONFIG'))
        INSTANCIAS_MAX=int(details_dict['instancias_max'])
        TENTATIVA_MAX=int(details_dict['tentativa_max'])
        TEMPO_ESPERA=int(details_dict['tempo_espera'])
        print('Arquivo de configuração carregado...')