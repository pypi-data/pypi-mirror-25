import json

import click
import requests
import crayons


@click.group()
def cli():
    """ NGROK TOOLKIT """
    pass

@click.command()
@click.option('-p', default=4040,
              help="Port number the ngrok web server is configured to run on \
              (additional processes will increment their port by 1) (default: 4040)")
@click.option('--one/--not-one', default=False,
              help='Only print a single url of the default web service')
@click.option('--pretty/--not-pretty', default=False,
              help="Print with lines and corresponding web service port numbers")
def url(p, one, pretty):
    for url in get_urls_on_port(p):
        if pretty:
            click.echo(crayons.yellow("------------------------"))
            p_num = crayons.yellow(p)
            msg = "Port number of web service: {}".format(p_num)
            click.echo(msg)
        msg = crayons.green(url)
        click.echo(msg)
        if one:
            break


cli.add_command(url)




def get_urls_on_port(port):
    """ Get the urls of active ngrok tunnels at the given port.

    Args:
        port (int): The port number to get urls of

    Returns:
        list: urls of active ngrok tunnels at port
    """
    try:
        tunnels_url = "http://localhost:{}/api/tunnels".format(port)
        req = requests.get(tunnels_url)
        urls = []
        tunnels = req.json()['tunnels']
        for tunnel in tunnels:
            urls.append(tunnel['public_url'])
        return urls
    except requests.exceptions.RequestException as error:
        raise ValueError("Error: {}".format(error))


if __name__ == '__main__':
    cli()
