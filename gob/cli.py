# cli.py
import os
import click
import shutil
from .cx import cx
from .tx import tx

@click.group()
def main():
    pass

main.add_command(cx)
main.add_command(tx)

if __name__ == '__main__':
    main()