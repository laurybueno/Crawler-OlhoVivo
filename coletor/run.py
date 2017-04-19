# coding: utf-8
import requests
import csv
import os
import schedule
import time

url = 'http://api.olhovivo.sptrans.com.br/v0'
s = requests.session()


def renew_token():
    s.post(url + '/Login/Autenticar?token=' + os.getenv('API_KEY'), timeout=3)


def get_cod_linha(linha):
    res = s.get(url + '/Linha/Buscar?termosBusca=' + linha)
    ret = []
    for linha in res.json():
        ret.append(linha['CodigoLinha'])

    return ret


# Returns json text ready to be saved as file
def get_posicao(cod_linha):
    try:
        res = s.get(url + '/Posicao?codigoLinha=' + str(cod_linha), timeout=3)
        return res.text
    except Exception:
        return ''


def get_data():
    print("Getting data...")
    renew_token()
    for linha in cod_linhas:
        with open('/data/' + str(linha) + '-' + str(time.time()) + '.json', 'w') as f:
            f.write(get_posicao(linha))


print("Getting first token...")
renew_token()

print("Getting cod_linhas...")
cod_linhas = []
with open('/data/gtfs/routes.txt', 'r') as f:
    routes = csv.reader(f)
    next(routes, None)  # ignore header
    for line in routes:
        for cod in get_cod_linha(line[0]):
            cod_linhas.append(cod)


cod_linhas = set(cod_linhas)  # remove duplicate entries
schedule.every(1).minutes.do(get_data)

while True:
    schedule.run_pending()

    print("Sleep for a second...")
    time.sleep(1)
