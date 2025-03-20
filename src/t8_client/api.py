from base64 import b64decode
from datetime import UTC
from struct import unpack
from zlib import decompress

import numpy as np
import requests


def url_generator(direccion, dato, nombre, punto_de_med, modo_proc, fecha_hora):
    # Convertimos la fecha y hora a timestamp
    utc_time = fecha_hora.replace(tzinfo=UTC)
    timestamp = int(utc_time.timestamp())

    URL = f'https://{direccion}{dato}/{nombre}/{punto_de_med}/{modo_proc}/{timestamp}'

    return URL


def obtain_waves(ctx, machine, point, pmode):
    host = ctx.obj['HOST']
    user = ctx.obj['USER']
    password = ctx.obj['PASSWORD']
    url = f"https://{host}/rest/waves/{machine}/{point}/{pmode}"
    response = requests.get(url, auth=(user, password))
    if response.status_code == 200:
        data= response.json()
        return [item['_links']['self'] for item in data['_items']]
    else:
        return None
    
def obtain_spectra(ctx, machine, point, pmode):
    host = ctx.obj['HOST']
    user = ctx.obj['USER']
    password = ctx.obj['PASSWORD']
    url = f"https://{host}/rest/spectra/{machine}/{point}/{pmode}"
    response = requests.get(url, auth=(user, password))
    if response.status_code == 200:
        data= response.json()
        return [item['_links']['self'] for item in data['_items']]
    else:
        return None


def zint_to_float(raw):
    d = decompress(b64decode(raw.encode()))
    return np.array([unpack('h', d[i*2:(i+1)*2])[0] for i in range(int(len(d)/2))], 
                    dtype='f')

def zlib_to_float(raw):
    d = decompress(b64decode(raw.encode()))
    return np.array([unpack('f', d[i*4:(i+1)*4])[0] for i in range(int(len(d)/4))], 
                    dtype='f')

def b64_to_float(raw):
    return np.fromstring(b64decode(raw.encode()), dtype='f')

decodificador = {
    'zint': zint_to_float,
    'zlib': zlib_to_float,
    'b64': b64_to_float
}
