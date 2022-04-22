#!/usr/bin/env python
# -*- coding: utf-8 -*-
import config
from threading import Lock, Thread
from time import sleep,time
import requests
import urllib3
import os
import sys
import json
from datetime import datetime


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

'''
Variaveis Globais
'''

# headers_api = {
#     "Content-Type": "application/x-www-form-urlencoded",
#     "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59",
#     "content-length":None
# }
headers_api = {
    "accept": "application/json;charset=utf-8",
    "Content-Type": "application/json; charset=UTF-8",
    'Accept-Charset': 'UTF-8',
}
url_api = 'https://dadosabertos.camara.leg.br/api/v2/deputados'
url_api_get = 'https://dadosabertos.camara.leg.br/api/v2/deputados'
url_api_get_full = 'https://dadosabertos.camara.leg.br/api/v2/deputados/{}'
url_api_get_frente = 'https://dadosabertos.camara.leg.br/api/v2/deputados/{}/frentes'

numero_instancia = 0

documentos_list=[]
documentos_dados = None

def process():
    s = inicializarRequest()
    c = get_cookies(s)
    response = getDeputados(s,c)
    if not os.path.exists("./finalizado/"):
        os.makedirs("./finalizado/")    
    with open('./finalizado/{}.json'.format(datetime.now().strftime("%d-%m-%Y %H-%M-%S")), 'w',encoding='utf8') as outfile:
        outfile.write(json.dumps(response,ensure_ascii=False))#,ensure_ascii=True
    return True

'''
Funcao Que acessa a pagina da api para a captura do cookie
'''
def get_cookies(s):
    cookies_api = None
    try:
        with s.get(url = url_api, headers=headers_api,verify=False,timeout=30) as r:
            cookies_api = r.cookies
    except Exception as e:
        print("Erro ao Acessa a API! Erro: "+str(e))
    return cookies_api

def inicializarRequest():
    s = requests.Session()
    s.headers.update(headers_api)
    return s

def getDeputados(s,cookies_api):
    global dep_full
    resultado = None
    dep_raw = []
    dep_full = []
    print('Preparando para pegar deputados...')
    try:
        with s.get(url = url_api_get,headers=headers_api,verify=False,allow_redirects=True,cookies=cookies_api,timeout=30) as r:
            if r.status_code == 200:
                resultado = r.json()
                for dep in resultado['dados']:
                    dep_raw.append({'id':dep['id'],'nome':dep['nome']})
    except Exception as e:
        print("Erro ao Capturar os dados na API! Erro: "+str(e))
    print('{} deputados cadastrado!'.format(len(dep_raw)))
    print('Pegando informações adcionais...')
    
    gerenciar_threads(dep_raw,getDepFull,(s,cookies_api))
    #for dep_temp in dep_raw:

    print('{} deputados completos!'.format(len(dep_full)))
    print('Pegando Frentes de deputados...')
    gerenciar_threads([{'id':dep['id']} for dep in dep_full],getDepFrente,(s,cookies_api))
    print('{} deputados completos com frentes atualizadas!'.format(len(dep_full)))
    return dep_full

def getDepFull(dep_temp,s,cookies_api,key):    
    response = None
    try:
        with s.get(url = url_api_get_full.format(dep_temp),headers=headers_api,verify=False,allow_redirects=True,cookies=cookies_api,timeout=30) as r:
            if r.status_code == 200:
                resultado = r.json()
                response =resultado['dados']
    except Exception as e:
        print("Erro ao Capturar os dados na API! Erro: "+str(e))
    with Lock():    
        global documentos_list
        if response != None:
            documentos_list[key][0] = ""
            global dep_full
            dep_full.append(response)
            atualizar_contagem()
        else:
            documentos_list[key][2]+= 1
            if documentos_list[key][2] == config.TENTATIVA_MAX:
                dep_full.append({'id':dep_temp})
        global numero_instancia
        numero_instancia-= 1

def getDepFrente(idDep,s,cookies_api,key):    
    response = None
    try:
        with s.get(url = url_api_get_frente.format(idDep),headers=headers_api,verify=False,allow_redirects=True,cookies=cookies_api,timeout=30) as r:
            if r.status_code == 200:
                    resultado = r.json()
                    response = resultado['dados']
    except Exception as e:
        print("Erro ao Capturar os dados na API! Erro: "+str(e))
    with Lock():    
        global documentos_list
        global dep_full
        if response != None and True in [True if y['id'] == idDep else False for y in dep_full]:
            documentos_list[key][0] = ""            
            for dep in dep_full:
                if dep['id'] == idDep:
                    dep['frentes'] = response
            atualizar_contagem()
        else:
            documentos_list[key][2]+= 1
            if documentos_list[key][2] == config.TENTATIVA_MAX:
                for dep in dep_full:
                    if dep['id'] == idDep:
                        dep['frentes'] = ['Erro']
        global numero_instancia
        numero_instancia-= 1

def gerenciar_threads(array=[],func=None,variaveis=()):
    #colocar um for para adicionar um espaço no array de cada documento como None q ser usado para o tempo
    # verificar se o tempo é none ou se ja faz 1 min com o lock para verificao e lock para adicao de tempo no array tmb
    #global INSTANCIAS_MAX 
    global documentos_list
    global documentos_dados

    documentos_dados = None
    documentos_list=[]

    for inf in array:
        documentos_list.append([inf['id'],None,0])

    atualizar_contagem()

    while (True in [True if y[0]!="" and y[2]< config.TENTATIVA_MAX else False for y in documentos_list]):
        for i,documento in enumerate(documentos_list):
            with Lock():
                global numero_instancia            
                if (numero_instancia < config.INSTANCIAS_MAX):
                    if ((documento[1] == None or time() -documento[1]>= config.TEMPO_ESPERA) and documento[0]!="" and documento[2]< config.TENTATIVA_MAX):
                        documentos_list[i][1] = time()
                        numero_instancia+= 1
                        Thread(target=func,name="doc"+str(documento)+' key:'+str(i), args=(documentos_list[i][0],*variaveis,i)).start()
                else:
                    sleep(5)
        if not(True in [True if y[0]!="" and y[2]< config.TENTATIVA_MAX else False for y in documentos_list]):
            break

        if not(False in [True if y[1] != None and time() -y[1]>= config.TEMPO_ESPERA and numero_instancia < config.INSTANCIAS_MAX else False for y in documentos_list]):
            sleep(5)
        elif numero_instancia >= config.INSTANCIAS_MAX:
            sleep(1)
    return documentos_dados

def atualizar_contagem():
    processados = sum([True if y[0]=="" or y[2]>=(config.TENTATIVA_MAX-1) else False for y in documentos_list])
    sys.stdout.write ("Documentos Processados %s/%s \r" % (str(processados),str(len(documentos_list))))
    sys.stdout.flush()



