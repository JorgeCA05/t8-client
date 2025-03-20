import os

import click
from dotenv import load_dotenv

from t8_client.api import obtain_spectra, obtain_waves

# Cargar variables de entorno desde el archivo .env
load_dotenv()

@click.group()
@click.option('-u', '--user', default=os.getenv('T8_USER'), help='User')
@click.option('-p', '--password', default=os.getenv('T8_PASSWORD'), help='Password')
@click.option('-h', '--host', default=os.getenv('T8_HOST'), help='Host')
@click.pass_context
def cli(ctx, user, password, host):
    if not user or not password or not host:
        raise click.UsageError("Usuario, contraseña y host deben ser especificados")
    ctx.ensure_object(dict)
    ctx.obj['USER'] = user
    ctx.obj['PASSWORD'] = password
    ctx.obj['HOST'] = host

@cli.command()
@click.option('-M', '--machine', required=True, help='Máquina')
@click.option('-p', '--point', required=True, help='Punto')
@click.option('-m', '--pmode', required=True, help='Modo de procesamiento')
@click.pass_context
def list_waves(ctx, machine, point, pmode):
    formas_de_onda = obtain_waves(ctx, machine, point, pmode)
    if formas_de_onda:
        for forma in formas_de_onda:
            click.echo(forma)
    else:
        click.echo('Error al obtener las formas de onda')

@cli.command()
@click.option('-M', '--machine', required=True, help='Máquina')
@click.option('-p', '--point', required=True, help='Punto')
@click.option('-m', '--pmode', required=True, help='Modo de procesamiento')
@click.pass_context
def list_spectra(ctx, machine, point, pmode):
    espectros = obtain_spectra(ctx, machine, point, pmode)
    if espectros:
        for espectro in espectros:
            click.echo(espectro)
    else:
        click.echo('Error al obtener los espectros')

if __name__ == '__main__':
    cli(obj={})

maq='LP_Turbine'
punt='MAD31CY005'
modoproc='AM1'
fecha='11-04-2019 18:25:54'