# -*- coding: utf-8 -*-
import os
import logging
from react import jsx
from .config import JS_DIR, JSX_DIR
from tornado.autoreload import watch

log = logging.getLogger('seahorse.jsx')


# JSX
def rename_jsx(jsx_file):
    """Renames a .jsx filename to .js"""
    return str(jsx_file)[:-3]+'js'


def jsx_filepath(filename):
    """Returns filepath: static/jsx/filename"""
    return os.path.join(JSX_DIR, filename)


def js_filepath(filename):
    """Returns filepath: static/js/filename"""
    return os.path.join(JS_DIR, filename)


def jsx_compile():
    """Compiles .jsx files in static/jsx into .js files in static/js"""
    print('INFO:seahorse.jsx:Compiling JSX static files into plain Javascript')
    transformer = jsx.JSXTransformer()
    jsx_files = os.listdir(JSX_DIR)
    for jsx_file in jsx_files:
        transformer.transform(
                jsx_filepath(jsx_file),
                js_path=js_filepath(rename_jsx(jsx_file)))


def watch_directory(directory):
    """Adds a given directory to the autoreload watch list."""
    for filename in os.listdir(directory):
        watch(os.path.join(directory, filename))


def watch_jsx_files():
    """Adds the JSX_DIR to the autoreload watch list."""
    log.info('Adding JSX directory to autoreload watch list')
    watch_directory(JSX_DIR)
