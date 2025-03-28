import csv
from base64 import b64decode
from datetime import UTC, datetime
from struct import unpack
from zlib import decompress
import os
import click
import numpy as np
import pylab
import requests



################################################ COMMAND PROCESSING ####################

def parse_params(machine, point, pmode, params):
    if params:
        machine, point, pmode = params.split(':')
    return machine, point, pmode

##################################################    LIST   ###########################

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

def obtain_spectras(ctx, machine, point, pmode):
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


##################################################  GET_WAVE  ##########################

def obtain_wave(ctx, machine, point, pmode, date):
    host = ctx.obj['HOST']
    user = ctx.obj['USER']
    password = ctx.obj['PASSWORD']
    # Convert to timestamp
    fecha_hora = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
    utc_time = fecha_hora.replace(tzinfo=UTC)
    timestamp = int(utc_time.timestamp())
    url = f"https://{host}/rest/waves/{machine}/{point}/{pmode}/{timestamp}"
    response = requests.get(url, auth=(user, password))
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def save_wave_to_csv(data, machine, point, pmode, datetime):
    safe_date = datetime.replace(':', '-')
    filename = os.path.join('output/reports', f"wave_{machine}_{point}_{pmode}_{safe_date}.csv")

    srate = float(data['sample_rate'])
    factor = float(data.get('factor', 1))
    raw = data['data']
    wave = decodificador['zint'](raw)

    wave *= factor

    t = np.linspace(0, len(wave) / srate, len(wave))

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['timestamp', 'value'])
        # Escribir datos
        for timestamp, value in zip(t, wave):
            writer.writerow([timestamp, value])


##################################################  GET_SPECTRA  #######################


def obtain_spectra(ctx, machine, point, pmode, date):
    host = ctx.obj['HOST']
    user = ctx.obj['USER']
    password = ctx.obj['PASSWORD']
    # Convertir la fecha a timestamp
    fecha_hora = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
    utc_time = fecha_hora.replace(tzinfo=UTC)
    timestamp = int(utc_time.timestamp())
    url = f"https://{host}/rest/spectra/{machine}/{point}/{pmode}/{timestamp}"
    response = requests.get(url, auth=(user, password))
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def save_spectra_to_csv(data, machine, point, pmode, datetime):
    safe_date = datetime.replace(':', '-')
    filename = os.path.join('output/reports',f"spectra_{machine}_{point}_{pmode}_{safe_date}.csv")

    fmin = data.get('min_freq', 0)
    fmax = data['max_freq']
    factor = data['factor']
    raw = data['data']
    sp = decodificador['zint'](raw)

    sp *= factor

    freq = np.linspace(fmin, fmax, len(sp))

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['timestamp', 'value'])
        # Escribir datos
        for timestamp, value in zip(freq, sp):
            writer.writerow([timestamp, value])


##################################################  PLOTS  #########################

def ploting_wave(data):
    srate = float(data['sample_rate'])
    factor = float(data.get('factor', 1))
    raw = data['data']
    wave = decodificador['zint'](raw)

    wave *= factor

    t = np.linspace(0, len(wave) / srate, len(wave))

    pylab.plot(t, wave)
    pylab.title('Waveform')
    pylab.grid(True)
    pylab.savefig('wavefig')
    pylab.show()


def ploting_spectra(data):
    fmin = data.get('min_freq', 0)
    fmax = data['max_freq']
    factor = data['factor']
    raw = data['data']
    sp = decodificador['zint'](raw)

    sp *= factor

    freq = np.linspace(fmin, fmax, len(sp))

    pylab.plot(freq, sp)
    pylab.title('Spectra')
    pylab.grid(True)
    pylab.savefig('spectrafig')
    pylab.show()










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
