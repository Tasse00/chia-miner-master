import click
from pprint import pprint
from dataclasses import dataclass


from .env import env
from .device import device
from .miner import miner

@click.group(invoke_without_command=True)
def cli():
    pass

cli.add_command(env)
cli.add_command(device)
cli.add_command(miner)

