import csv
import os
from datetime import UTC, datetime, timezone

import click
from dotenv import load_dotenv

from t8_client.api import (
    obtain_spectra,
    obtain_spectras,
    obtain_wave,
    obtain_waves,
    parse_params,
    save_spectra_to_csv,
    save_wave_to_csv,
)

load_dotenv()

@click.group()
@click.option("-u", "--user", default=os.getenv("T8_USER"), help="User")
@click.option("-p", "--password", default=os.getenv("T8_PASSWORD"), help="Password")
@click.option("-h", "--host", default=os.getenv("T8_HOST"), help="Host")
@click.pass_context
def cli(ctx, user, password, host):
    if not user or not password or not host:
        raise click.UsageError("User, password and host must be specified")
    ctx.ensure_object(dict)
    ctx.obj["USER"] = user
    ctx.obj["PASSWORD"] = password
    ctx.obj["HOST"] = host

##################################################    LIST   ###########################

@cli.command()
@click.option('-M', '--machine', default=None, help='Machine')
@click.option('-p', '--point', default=None, help='Point')
@click.option('-m', '--pmode', default=None, help='Processing mode')
@click.option('-P', '--params', default=None, help='Parameters in format -> M:P:PM')
@click.pass_context
def list_waves(ctx, machine, point, pmode, params)->None:
    machine, point, pmode = parse_params(machine, point, pmode, params)
    formas_de_onda = obtain_waves(ctx, machine, point, pmode)
    if formas_de_onda:
        for forma in formas_de_onda:
            timestamp = int(forma.split('/')[-1])
            date = datetime.fromtimestamp(timestamp, UTC).isoformat()
            click.echo(date)
    else:
        click.echo('Error getting all the waveforms')

@cli.command()
@click.option('-M', '--machine', default=None, help='Machine')
@click.option('-p', '--point', default=None, help='Point')
@click.option('-m', '--pmode', default=None, help='Processing mode')
@click.option('-P', '--params', default=None, help='Parameters in format -> M:P:PM')
@click.pass_context
def list_spectra(ctx, machine, point, pmode, params):
    machine, point, pmode = parse_params(machine, point, pmode, params)
    espectros = obtain_spectras(ctx, machine, point, pmode)
    if espectros:
        for espectro in espectros:
            timestamp = int(espectro.split('/')[-1])
            date = datetime.fromtimestamp(timestamp, UTC).isoformat()
            click.echo(date)
    else:
        click.echo('Error listing all the spectras')

##################################################    GET  ############################

@cli.command()
@click.option('-M', '--machine', default=None, help='Machine')
@click.option('-p', '--point', default=None, help='Point')
@click.option('-m', '--pmode', default=None, help='Processing mode')
@click.option('-P', '--params', default=None, help='Parameters in format -> M:P:PM')
@click.option('-t', '--time', required=True, help='YYYY-MM-DDTHH:MM:SS')
@click.pass_context
def get_wave(ctx, machine, point, pmode, params, time):
    machine, point, pmode = parse_params(machine, point, pmode, params)
    forma_de_onda = obtain_wave(ctx, machine, point, pmode, time)
    if forma_de_onda:
        save_wave_to_csv(forma_de_onda, machine, point, pmode, time)
        click.echo(f'Waveform saved as wave_{machine}_{point}_{pmode}_{time.replace(":", "-")}.csv')  # noqa: E501
    else:
        click.echo('Error getting that waveform')


@cli.command()
@click.option('-M', '--machine', default=None, help='Machine')
@click.option('-p', '--point', default=None, help='Point')
@click.option('-m', '--pmode', default=None, help='Processing mode')
@click.option('-P', '--params', default=None, help='Parameters in format -> M:P:PM')
@click.option('-t', '--time', required=True, help='YYYY-MM-DDTHH:MM:SS')
@click.pass_context
def get_spectra(ctx, machine, point, pmode, params, time):
    machine, point, pmode = parse_params(machine, point, pmode, params)
    forma_de_onda = obtain_spectra(ctx, machine, point, pmode, time)
    if forma_de_onda:
        save_spectra_to_csv(forma_de_onda, machine, point, pmode, time)
        click.echo(f'Espectra saved as spectra_{machine}_{point}_{pmode}_{time.replace(":", "-")}.csv')  # noqa: E501
    else:
        click.echo('Error getting that spectra')


###################################################   PLOT   ###########################










if __name__ == '__main__':
    cli(obj={})





maq='LP_Turbine'
punt='MAD31CY005'
modoproc='AM1'
fecha='11-04-2019 18:25:54'