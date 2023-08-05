#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The bot script runs a simple chatbot that will respond to greetings on the command line.

To install this bot run `python setup.py install` which will install the command `bot`

A typical interaction with this bot would be:

$ bot Hi
Hi hobs, how are you?
$ bot Hey
Hi hobs, how are you?
$ bot Inspire me!
Failure is part of the process. Each time you fail you are one step closer to success.


"""
from __future__ import division, print_function, absolute_import

import argparse
import sys
import logging
import os
import requests

from labeler_site import __version__  # noqa

__author__ = "Hobson Lane"
__copyright__ = "Hobson Lane"
__license__ = "mit"

_logger = logging.getLogger(__name__)

WALLPAPER_PATH = os.path.join(os.path.expanduser('~'), 'Pictures', 'wallpaper')


def change_wallpaper(new_path=WALLPAPER_PATH, wallpaper_path=WALLPAPER_PATH, backup=False):
    new_path, wallpaper_path = os.path.abspath(new_path), os.path.abspath(wallpaper_path)
    with open(new_path, 'rb') as fin:
        newimage = fin.read()
    if new_path != wallpaper_path:
        with open(wallpaper_path, 'rb') as fin:
            oldimage = fin.read()
        if newimage != oldimage:
            with open(wallpaper_path, 'wb') as fout:
                fout.write(newimage)
            return newimage


def recognize_greeting(statement):
    """Recognizes if string statement starts with Hi or Hey or any other greeting.

    Args:
      statement (str): a string from the commandline from the user

    Returns:
      bool: True if statement is a greeting. False otherwise.

    >>> recognize_greeting('hi')
    True
    """
    statement = statement.lower()
    if statement.startswith('hi') or statement.startswith('hey'):
        return True
    return False


def is_greeting(statement):
    """Recognizes if string statement starts with Hi or Hey or any other greeting.

    Args:
      statement (str): a string from the commandline from the user

    Returns:
      bool: True if statement is a greeting. False otherwise.

    >>> is_greeting('hi')
    True
    """
    statement = statement.lower()
    if statement.startswith('hi') or statement.startswith('hey'):
        return True
    return False


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser()  # description="Just a greeting recognizer.")
    parser.add_argument(
        '--version',
        action='version',
        version='labeler_site {ver}'.format(ver=__version__))
    parser.add_argument(
        '--upload',
        dest="upload",
        help="Path to image file for upload to labler API",
        type=str)
    parser.add_argument(
        '-v',
        '--verbose',
        dest="loglevel",
        help="set loglevel to INFO",
        action='store_const',
        const=logging.INFO)
    parser.add_argument(
        '-vv',
        '--very-verbose',
        dest="loglevel",
        help="set loglevel to DEBUG",
        action='store_const',
        const=logging.DEBUG)
    return parser.parse_known_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


# class Match:

#     ___init__(self, groups):
#         self.group_list = groups or []

#     def groups():
#         return self.group_list

# class Matcher:
#     """A pseudo-regex object with only a match method, and a hard-coded decision tree (FSM)."""

#     def match(statement):
#         """ Return a Match object with a 1-len list of "groups" containing the name that the user addressed """
#         words = statement.lower().strip().split()
#         if not len(words):
#             return Match([])
#         w0 = words[0]
#         if len(w0) > 1 and w0[0] == 'h':
#             if w0[1] == 'i':
#                 return Match(words[1] if len(words) > 1 else [''])
#             if len(w0) > 2 and w0[1] == 'e' and w0[2] == 'y':
#                 return Match(words[1] if len(words) > 1 else [''])
#         return []


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args, unknown = parse_args(args)
    # setup_logging(args.loglevel)
    # _logger.debug("Starting crazy calculations...")
    if is_greeting(' '.join(unknown)):
        print("Hi {}, would you like to play a game?".format(os.getenv('USER', 'Boss')))
    if args.upload:
        upload(args.upload)
    # _logger.info("Script ends here")


def upload(filepath):
    # POST request to your API with "files" key in requests data dict

    # base_dir = os.path.join(os.getenv('HOME'), 'Pictures')
    base_dir = os.path.expanduser(os.path.dirname(filepath))
    url = 'http://localhost:8000/api/'
    filename = os.path.basename(filepath)
    with open(os.path.join(base_dir, filename), 'rb') as fin:
        print(fin.name)
        POST_data = {'caption': 'bot upload'}
        files = {'file': (filename, fin),
                 'file_name': filename}
        resp = requests.post(url, data=POST_data, files=files)
        print(resp)


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    print('sys.args:')
    print(sys.args)
    run()
