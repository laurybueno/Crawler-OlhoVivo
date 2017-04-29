# coding: utf-8
import requests
import csv
import os
import time
import datetime
import threading
import sys

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


def get_data(cod_linhas):
    print("Getting data on thread " + str(threading.currentThread().threadID))
    for linha in cod_linhas:
        dir_path = '/data/' + str(datetime.date.today().year) + '/' + str(datetime.date.today().month) + '/' + str(datetime.date.today().day) + '/'
        file_name = str(linha) + '-' + str(time.time()) + '.json'
        complete_path = dir_path + file_name

        os.makedirs(os.path.dirname(complete_path), exist_ok=True)
        with open(complete_path, 'w') as f:
            f.write(get_posicao(linha))
    print("Finished getting data on thread " + str(threading.currentThread().threadID))


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


# Prepare the threading system
class myThread (threading.Thread):
    def __init__(self, cod_linhas, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.cod_linhas = cod_linhas

    def run(self):
        get_data(self.cod_linhas)


print("Getting first token...")
renew_token()

print("Getting cod_linhas...")
all_cod_linhas = []
with open('/data/gtfs/routes.txt', 'r') as f:
    routes = csv.reader(f)
    next(routes, None)  # ignore header
    for line in routes:
        for cod in get_cod_linha(line[0]):
            all_cod_linhas.append(cod)


all_cod_linhas = list(set(all_cod_linhas))  # remove duplicate entries
# Split all_cod_linhas into five groups
# Each one will be given to a diferent thread
chunks_of_cod_linhas = []
for chunk in chunks(all_cod_linhas, 100):
    chunks_of_cod_linhas.append(chunk)

id = 1
while True:
    renew_token()
    for chunk in chunks_of_cod_linhas:
        myThread(chunk, id).start()
        id += 1

    active_threads = threading.activeCount()
    print("There are " + str(active_threads) + " threads running.")
    # Ten rogue threads must trigger a full stop to prevent service overload
    if active_threads > (len(chunks_of_cod_linhas) + 10):
        sys.exit("Thread limit of " + str(len(chunks_of_cod_linhas) + 10) + " exceeded: " + str(active_threads))

    print("Sleep main thread for 60 seconds...")
    time.sleep(60)
