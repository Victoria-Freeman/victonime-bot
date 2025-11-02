import click
import config as Config

@click.command()
def setup():
    Config.generateRcloneConfig()