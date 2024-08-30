import os

import click

from prestapy.prestashop_ep.brands import Brand


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)

    ctx.obj['DEBUG'] = debug


@cli.group()  # @cli, not @click!
@click.pass_context
def brand(ctx):
    ctx.ensure_object(dict)

    ctx.obj['URL'] = os.environ.get("URL", "")
    ctx.obj['API_KEY'] = os.environ.get("API_KEY", "")


@brand.command()
@click.pass_context
def brand_list(ctx):
    url = ctx.obj.get('URL')
    api_key = ctx.obj.get('API_KEY')
    br = Brand(url, api_key)
    click.echo(br.get_all())


if __name__ == "__main__":
    cli()
