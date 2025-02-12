import click
import os
import shutil
from .utils import get_customer_dir, create_directory, remove_directory, list_directories, open_directory, get_gob_dir

@click.group()
def tx():
    """Manage tickets."""
    pass

@tx.command('add')
@click.option('-c', '--customer_name', required=True, help='Name of the customer')
@click.argument('ticket_id')
def add_ticket(customer_name, ticket_id):
    """Add a new ticket."""
    click.echo("Running gob tx add...")
    customer_dir = get_customer_dir(customer_name)
    if not os.path.exists(customer_dir):
        click.secho(f'🔴 Error: Customer directory {customer_name} does not exist.', fg='red')
        return
    ticket_path = os.path.join(customer_dir, 'tickets', ticket_id)
    if create_directory(ticket_path):
        # Create notes.sh and notes.md files within the ticket directory
        notes_sh_path = os.path.join(ticket_path, 'notes.sh')
        notes_md_path = os.path.join(ticket_path, 'notes.md')
        with open(notes_sh_path, 'w') as notes_sh_file:
            notes_sh_file.write('#!/bin/bash\n\n# Notes for ticket\n')
        with open(notes_md_path, 'w') as notes_md_file:
            notes_md_file.write('# Notes\n\n')
        click.secho(f'🟢 Ticket {ticket_id} created for customer {customer_name}.', fg='green')
    else:
        click.secho(f'🔴 Ticket {ticket_id} already exists for customer {customer_name}.', fg='red')

@tx.command('solve')
@click.option('-c', '--customer_name', required=True, help='Name of the customer')
@click.argument('ticket_id')
def solve_ticket(customer_name, ticket_id):
    """Mark a ticket as solved."""
    click.echo("Running gob tx solve...")
    customer_dir = get_customer_dir(customer_name)
    ticket_dir = os.path.join(customer_dir, 'tickets')
    ticket_path = os.path.join(ticket_dir, ticket_id)
    if not os.path.exists(ticket_path):
        click.secho(f'🔴 Error: Ticket {ticket_id} does not exist for customer {customer_name}.', fg='red')
        return
    if click.confirm(f'Are you sure you want to mark ticket {ticket_id} as solved?', default=False):
        solved_dir = os.path.join(get_gob_dir(), '.solved')
        create_directory(solved_dir)
        shutil.move(ticket_path, os.path.join(solved_dir, ticket_id))
        click.secho(f'🟢 Ticket {ticket_id} marked as solved and moved to {solved_dir}.', fg='green')
    else:
        click.echo('Operation cancelled.')

@tx.command('reopen')
@click.option('-c', '--customer_name', required=True, help='Name of the customer')
@click.argument('ticket_id')
def reopen_ticket(customer_name, ticket_id):
    """Reopen a solved ticket."""
    click.echo("Running gob tx reopen...")
    customer_dir = get_customer_dir(customer_name)
    solved_dir = os.path.join(get_gob_dir(), '.solved')
    ticket_path = os.path.join(solved_dir, ticket_id)
    if not os.path.exists(ticket_path):
        click.secho(f'🔴 Error: Ticket {ticket_id} does not exist in the solved tickets.', fg='red')
        return
    ticket_dir = os.path.join(customer_dir, 'tickets')
    create_directory(ticket_dir)
    shutil.move(ticket_path, os.path.join(ticket_dir, ticket_id))
    click.secho(f'🟢 Ticket {ticket_id} reopened and moved back to customer {customer_name}.', fg='green')

@tx.command('rm')
@click.option('-c', '--customer_name', required=False, help='Name of the customer')
@click.option('-s', '--solved', is_flag=True, help='Remove solved ticket')
@click.argument('ticket_id')
def remove_ticket(customer_name, solved, ticket_id):
    """Remove a ticket."""
    click.echo("Running gob tx rm...")
    gob_dir = get_gob_dir()
    if solved:
        solved_dir = os.path.join(gob_dir, '.solved')
        ticket_path = os.path.join(solved_dir, ticket_id)
        if not os.path.exists(ticket_path):
            click.secho(f'🔴 Error: Solved ticket {ticket_id} does not exist.', fg='red')
            return
        if click.confirm(f'Are you sure you want to remove solved ticket {ticket_id}?', default=False):
            remove_directory(ticket_path)
            click.secho(f'🟢 Solved ticket {ticket_id} removed.', fg='green')
        else:
            click.echo('Operation cancelled.')
    else:
        if not customer_name:
            click.secho('🔴 Error: Customer name is required if not removing solved tickets.', fg='red')
            return
        customer_dir = get_customer_dir(customer_name)
        ticket_dir = os.path.join(customer_dir, 'tickets')
        ticket_path = os.path.join(ticket_dir, ticket_id)
        if not os.path.exists(ticket_path):
            click.secho(f'🔴 Error: Ticket {ticket_id} does not exist for customer {customer_name}.', fg='red')
            return
        if click.confirm(f'Are you sure you want to remove ticket {ticket_id} for customer {customer_name}?', default=False):
            remove_directory(ticket_path)
            click.secho(f'🟢 Ticket {ticket_id} for customer {customer_name} removed.', fg='green')
        else:
            click.echo('Operation cancelled.')

@tx.command('ls')
@click.option('-c', '--customer_name', required=False, help='Name of the customer')
@click.option('-s', '--solved', is_flag=True, help='List solved tickets')
def list_tickets(customer_name, solved):
    """List all tickets for a customer."""
    click.echo("Running gob tx ls...")
    gob_dir = get_gob_dir()
    if solved:
        solved_dir = os.path.join(gob_dir, '.solved')
        tickets = list_directories(solved_dir)
        if not tickets:
            click.secho('🔴 No solved tickets found.', fg='red')
        else:
            click.secho('🟢 Solved tickets:', fg='green')
            for ticket in tickets:
                click.echo(f'  {ticket}')
    else:
        if not customer_name:
            click.secho('🔴 Error: Customer name is required if not listing solved tickets.', fg='red')
            return
        customer_dir = get_customer_dir(customer_name)
        ticket_dir = os.path.join(customer_dir, 'tickets')
        tickets = list_directories(ticket_dir)
        if not tickets:
            click.secho(f'🔴 No tickets found for customer {customer_name}.', fg='red')
        else:
            click.secho(f'🟢 Tickets for customer {customer_name}:', fg='green')
            for ticket in tickets:
                click.echo(f'  {ticket}')

@tx.command('open')
@click.option('-c', '--customer_name', required=True, help='Name of the customer')
@click.argument('ticket_id')
def open_ticket(customer_name, ticket_id):
    """Open a ticket directory with the default editor or 'open' command."""
    click.echo("Running gob tx open...")
    customer_dir = get_customer_dir(customer_name)
    ticket_dir = os.path.join(customer_dir, 'tickets')
    ticket_path = os.path.join(ticket_dir, ticket_id)
    if not os.path.exists(ticket_path):
        click.secho(f'🔴 Error: Ticket {ticket_id} does not exist for customer {customer_name}.', fg='red')
        return
    open_directory(ticket_path)

@tx.command('mv')
@click.option('-c', '--customer_name', required=True, help='Name of the customer')
@click.option('-p', '--path', required=True, help='Path of the file or directory to move')
@click.argument('ticket_id')
def move_to_ticket(customer_name, path, ticket_id):
    """Move a file or directory to a ticket directory."""
    click.echo("Running gob tx mv...")
    customer_dir = get_customer_dir(customer_name)
    ticket_dir = os.path.join(customer_dir, 'tickets')
    ticket_path = os.path.join(ticket_dir, ticket_id)
    if not os.path.exists(ticket_path):
        click.secho(f'🔴 Error: Ticket {ticket_id} does not exist for customer {customer_name}.', fg='red')
        return
    if not os.path.exists(path):
        click.secho(f'🔴 Error: Path {path} does not exist.', fg='red')
        return
    shutil.move(path, ticket_path)
    click.secho(f'🟢 Moved {path} to ticket {ticket_id} for customer {customer_name}.', fg='green')