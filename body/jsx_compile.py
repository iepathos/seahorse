import os
from react import jsx
from .config import STATIC_DIR


def rename_jsx(jsx_file):
    """Renames a .jsx filename to .js"""
    return str(jsx_file)[:-3]+'js'


def jsx_filepath(filename):
    """Returns filepath: static/jsx/filename"""
    return os.path.join('body/static/jsx', filename)


def js_filepath(filename):
    """Returns filepath: static/js/filename"""
    return os.path.join('body/static/js', filename)


def jsx_compile():
    """Compiles .jsx files in static/jsx into .js files in static/js"""
    print('Compiling JSX static files into plain Javascript')
    transformer = jsx.JSXTransformer()
    jsx_files = os.listdir('body/static/jsx')
    for jsx_file in jsx_files:
        transformer.transform(
                jsx_filepath(jsx_file),
                js_path=js_filepath(rename_jsx(jsx_file)))
