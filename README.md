# Extracao-de-Deputados
Extração de Deputados e suas Frentes utilizando a API Dados Abertos da Câmera
# Extração de Deputados

## Extração de Deputados e suas Frentes

Esse projeto foi projetado para ser responsável para alimentar uma aplicação de um Projeto do meu período da faculdade, mas que no final não foi necessário e então foi adaptada e reformulado neste projeto! A aplicação realiza consultas para obter informações em tempo reais de deputados, consumindo a API do Dados Abertos neste processo.

## O que o projeto contém
- Request em Python
- Integração com a API do [Dados Abertos](https://dadosabertos.camara.leg.br)
- Gerenciamento de Multithreading para executar simultâneos Requests

## Instalação
Para rodar o projeto faça essas configurações:
- Clone o projeto (utilizando comando git ou baixando em zip)
- Instale o Python (recomendado versão 3.8)
- Instale a biblioteca que se encontra em requirements
```
python -m pip install -U pip setuptools
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Resultados & O que é esperado
Arquivo com a lista de deputados e suas frentes em JSON! Os arquivos gerados se encontram na pasta **Finalizado** com o nome da data e hora extraídos.<br>
![image](https://user-images.githubusercontent.com/19514153/164598810-a5367900-4edf-413b-9aa8-a085b50ff709.png)
<br>
**No Console irar imprimir a situação do processo da execução da aplicação!**
<br>![console](https://user-images.githubusercontent.com/19514153/164596217-048c12bd-8612-4ee1-b0e4-632f71992f84.png)
