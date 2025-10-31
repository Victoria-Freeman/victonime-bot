#!/usr/bin/env python3

import click
from dotenv import load_dotenv
import rclone as Rclone
import couchdrop as Couchdrop
import anilibria as Anilibria
import wasabi as Wasabi
import bunny as Bunny

load_dotenv()

@click.group()
def cli(): pass

@cli.group()
def wasabi(): pass

@cli.group()
def anilibria(): pass

@cli.group
def couchdrop(): pass

@cli.group
def rclone(): pass

@cli.group
def bunny(): pass

rclone.add_command(Rclone.setup)

couchdrop.add_command(Couchdrop.setup)
couchdrop.add_command(Couchdrop.automate)
couchdrop.add_command(Couchdrop.cleanup)

anilibria.add_command(Anilibria.parse_season)
anilibria.add_command(Anilibria.new_anime)
anilibria.add_command(Anilibria.update)

wasabi.add_command(Wasabi.setup)
wasabi.add_command(Wasabi.upload)
wasabi.add_command(Wasabi.cleanup)

bunny.add_command(Bunny.setup)


if __name__ == "__main__":
    cli()
