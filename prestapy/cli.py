import click
import requests

from prestapy.prestashop_ep.brands import get_manufacturers


@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    click.echo(f"Debug mode is {'on' if debug else 'off'}")


@cli.command()  # @cli, not @click!
@click.option('--url', type=str, required=True)
@click.option('--api_key', type=str, required=True)
def brand(url, api_key):
    click.echo(get_manufacturers(url, api_key))


if __name__ == "__main__":
    cli()
