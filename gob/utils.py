# utils.py
import os
import click
import shutil

def get_gob_dir():
    return os.path.join(os.path.expanduser('~'), '.gob')

def get_customer_dir(customer_name):
    return os.path.join(get_gob_dir(), customer_name.capitalize())

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    return False

def remove_directory(path):
    if os.path.exists(path):
        shutil.rmtree(path)
        return True
    return False

def list_directories(path):
    if os.path.exists(path):
        return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    return []

def open_directory(path):
    editor = os.getenv('EDITOR', 'open')
    os.system(f'{editor} {path}')