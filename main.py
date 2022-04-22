#!/usr/bin/env python
# -*- coding: utf-8 -*-
from controller import base
import config 
import sys


'''Declaração de Variavel Global'''
THREADS=[]

def main():
    global THREADS
    THREADS=[]

    config.initialize()
    print('Iniciando Macro Automatizada...')
    if base.initialize():
        print('Finalizando...')
    else:
        print('Finalizando devido a algum erro!')
    sys.exit()

def get_Threads():
    global THREADS
    return THREADS

if __name__ == '__main__':
    main()