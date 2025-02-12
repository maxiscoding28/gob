# cli.py
import click
from .cx import cx
from .tx import tx
from .wu import wu
import os
import datetime
from .utils import get_gob_dir


@click.group()
def main():
    """Manage customers, health checks, and tickets."""
    pass

main.add_command(cx)
main.add_command(tx)
main.add_command(wu)

@main.command('tree')
def list_tree():
    """List directories"""
    gob_dir = get_gob_dir()
    for root, dirs, _ in os.walk(gob_dir):
        level = root.replace(gob_dir, '').count(os.sep)
        if level == 0:
            for dir_name in dirs:
                if dir_name == 'health-check':
                    list_health_checks(root, dir_name)
                else:
                    list_other_directories(root, dir_name)
        break

def list_health_checks(root, dir_name):
    sub_dir_path = os.path.join(root, dir_name, 'premium', 'health-checks')
    if os.path.exists(sub_dir_path):
        current_year = str(datetime.datetime.now().year)
        sub_level = 1
        indent = ' ' * 4 * sub_level
        click.echo(f"{indent}health-checks/")
        for sub_root, sub_dirs, sub_files in os.walk(sub_dir_path):
            if sub_root == sub_dir_path:
                for sub_dir in sub_dirs:
                    if sub_dir == current_year:
                        click.echo(f"{indent}    {sub_dir}/")
                        current_year_path = os.path.join(sub_root, sub_dir)
                        list_markdown_files(current_year_path, indent)

def list_markdown_files(current_year_path, indent):
    for _, _, files in os.walk(current_year_path):
        for file in files:
            if file.endswith('.md'):
                click.echo(f"{indent}        {file}")

def list_other_directories(root, dir_name):
    sub_dir_path = os.path.join(root, dir_name)
    sub_level = 1
    indent = ' ' * 4 * sub_level
    click.echo(f"{indent}{dir_name}/")
    for sub_root, sub_dirs, _ in os.walk(sub_dir_path):
        if sub_root == sub_dir_path:
            for sub_dir in sub_dirs:
                click.echo(f"{indent}    {sub_dir}/")
                if sub_dir == 'tickets':
                    list_tickets(sub_root, sub_dir, indent)

def list_tickets(sub_root, sub_dir, indent):
    tickets_path = os.path.join(sub_root, sub_dir)
    for ticket_root, ticket_dirs, _ in os.walk(tickets_path):
        if ticket_root == tickets_path:
            for ticket_dir in ticket_dirs:
                click.echo(f"{indent}        {ticket_dir}/")

if __name__ == '__main__':
    main()