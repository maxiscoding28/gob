# cx.py
import click
from .utils import get_customer_dir, create_directory, remove_directory, list_directories, open_directory, get_gob_dir
import os

@click.group()
def cx():
    pass

@cx.command('add')
@click.option('-c', '--customer_name', required=True, help='Name of the customer')
def create_customer(customer_name):
    """Create a directory for a customer."""
    click.echo("Running gob cx add...")
    customer_dir = get_customer_dir(customer_name)
    if create_directory(customer_dir):
        click.secho(f'🟢 Customer directory {customer_name} created.', fg='green')
    else:
        click.secho(f'🔴 Customer directory {customer_name} already exists.', fg='red')

@cx.command('rm')
@click.option('-c', '--customer_name', required=True, help='Name of the customer')
def remove_customer(customer_name):
    """Remove a customer directory."""
    click.echo("Running gob cx rm...")
    customer_dir = get_customer_dir(customer_name)
    if not os.path.exists(customer_dir):
        click.secho(f'🔴 Error: Customer directory {customer_name} does not exist.', fg='red')
        return
    click.echo(f'Contents of {customer_name} directory:')
    for item in os.listdir(customer_dir):
        click.echo(item)
    if click.confirm('Are you sure you want to delete this directory?', default=False):
        if remove_directory(customer_dir):
            click.secho(f'🟢 Customer directory {customer_name} has been removed.', fg='green')
        else:
            click.secho(f'🔴 Error: Failed to remove customer directory {customer_name}.', fg='red')
    else:
        click.echo('Operation cancelled.')

@cx.command('ls')
def list_customers():
    """List all customer directories except the .solved directory."""
    click.echo("Running gob cx ls...")
    customers = list_directories(get_gob_dir())
    if not customers:
        click.secho('🔴 No customer directories found.', fg='red')
    else:
        click.secho('🟢 Customers:', fg='green')
        for customer in customers:
            if customer != '.solved':
                click.echo(f'\t{customer}')

@cx.command('open')
@click.option('-c', '--customer_name', required=True, help='Name of the customer')
def open_customer(customer_name):
    """Open a customer directory with the default editor or 'open' command."""
    click.echo("Running gob cx open...")
    customer_dir = get_customer_dir(customer_name)
    if not os.path.exists(customer_dir):
        click.secho(f'🔴 Error: Customer directory {customer_name} does not exist.', fg='red')
        return
    open_directory(customer_dir)