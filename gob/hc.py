import os
import click
import subprocess
import re
from datetime import datetime
from .utils import open_directory

def prompt_user(message):
    return input(message)

GOB_DIR = os.path.expanduser("~/.gob")
HEALTH_CHECK_DIR = os.path.join(GOB_DIR, "health-check")
REPO_URL = "https://github.com/github/helphub-knowledge-base.git"

@click.group()
def cli():
    pass

@click.group()
def hc():
    pass

@hc.command()
def clone():
    """Clone the health-check repository."""
    click.echo("Running gob hc clone...")
    if not os.path.exists(HEALTH_CHECK_DIR) or not os.listdir(HEALTH_CHECK_DIR) or not os.path.exists(os.path.join(HEALTH_CHECK_DIR, ".git")):
        clone_repo = prompt_user("The health-check directory does not exist or is not a valid git repository. Do you want to clone it? (y/n): ")
        if clone_repo.lower() == 'y':
            clone_health_check_repo()
        else:
            click.echo("Aborted cloning the repository.")
    else:
        click.echo("The health-check directory already exists and is a valid git repository.")

@hc.command()
def cd():
    """Change directory to the health-check directory."""
    click.echo("Running gob hc cd...")
    os.chdir(HEALTH_CHECK_DIR)
    click.echo(f"Changed directory to {HEALTH_CHECK_DIR}")

@hc.command()
@click.option('-c', '--customer', required=True, help='Customer name')
@click.option('-o', '--open', 'open_flag', is_flag=True, help='Open the file in VSCode')
def add(customer, open_flag):
    """Add a new health-check file for a customer."""
    click.echo("Running gob hc add...")
    current_date = datetime.now()
    year = current_date.year
    month = current_date.strftime("%m")
    file_name = f"{customer}-{year}-{month}.md"
    branch_name = file_name.replace(".md", "")
    directory_path = os.path.join(HEALTH_CHECK_DIR, "premium", "health-checks", str(year))
    file_path = os.path.join(directory_path, file_name)
    
    # Ensure we are on the main branch before creating a new branch
    try:
        subprocess.run(["git", "-C", HEALTH_CHECK_DIR, "checkout", "main"], check=True)
        click.echo("Switched to main branch.")
    except subprocess.CalledProcessError as e:
        click.echo(f"Failed to switch to main branch: {e}")
        return
    
    # Create a new git branch off of the main branch
    try:
        subprocess.run(["git", "-C", HEALTH_CHECK_DIR, "checkout", "-b", branch_name], check=True)
        click.echo(f"Created and switched to new branch: {branch_name}")
    except subprocess.CalledProcessError as e:
        click.echo(f"Failed to create new branch: {e}")
        return
    
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    
    with open(file_path, 'w') as file:
        file.write(f"# Health Check for {customer}\n\nDate: {current_date.strftime('%Y-%m-%d')}\n")
    
    click.echo(f"Created file: {file_path}")
    
    if open_flag:
        open_directory(file_path)

def clone_health_check_repo():
    try:
        subprocess.run(["git", "clone", REPO_URL, HEALTH_CHECK_DIR], check=True)
        click.echo("Repository cloned successfully.")
    except subprocess.CalledProcessError as e:
        click.echo(f"Failed to clone the repository: {e}")

@hc.command('push')
def push_command():
    """Push the current working branch in the health-check repo to the remote origin."""
    click.echo("Running gob hc push...")
    try:
        current_branch = subprocess.check_output(
            ["git", "-C", HEALTH_CHECK_DIR, "rev-parse", "--abbrev-ref", "HEAD"],
            text=True
        ).strip()
        subprocess.run(["git", "-C", HEALTH_CHECK_DIR, "push", "-u", "origin", current_branch], check=True)
        click.echo(f"Pushed branch {current_branch} to remote origin.")
    except subprocess.CalledProcessError as e:
        click.echo(f"Failed to push the branch: {e}")

cli.add_command(hc)
