from __future__ import print_function
import click

@click.command()
def cli():
    click.echo("Hello, World!")

def hello():
    return("Hello, Fang")

def say_hello():
    return(hello())

if __name__ == '__main__':
    cli()
