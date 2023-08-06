"""
    gease
    ~~~~~~~~~~~~~~~~~~~

    Make github release at command line

    :copyright: (c) 2017 by Onni Software Ltd.
    :license: MIT License, see LICENSE for more details

"""

import os
import sys
import json
import crayons
from gease._version import __version__, __description__
from gease.release import EndPoint
import gease.exceptions as exceptions
try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

HELP = """%s. version %s

Usage: %s

where:

   release message is optional. It could be a quoted string or space separate
   string

Examples:

   gs gease v0.0.1 first great release
   gs gease v0.0.2 "second great release"
""" % (
    crayons.yellow('gease ' + __description__),
    crayons.magenta(__version__, bold=True),
    crayons.yellow('gs repo tag [release message]', bold=True),
)
DEFAULT_GEASE_FILE_NAME = '.gease'
DEFAULT_RELEASE_MESSAGE = "A new release via gease."
NOT_ENOUGH_ARGS = 'Not enough arguments'
KEY_GEASE_USER = 'user'
KEY_GEASE_TOKEN = 'personal_access_token'
MESSAGE_FMT_RELEASED = 'Release is created at: %s'


def main():
    if len(sys.argv) < 3:
        if len(sys.argv) == 2:
            error(NOT_ENOUGH_ARGS)
        print(HELP)
        sys.exit(-1)
    try:
        user, token = get_token()
    except exceptions.NoGeaseConfigFound as e:
        fatal(str(e))
    except KeyError as e:
        fatal("Key %s is not found" % str(e))

    repo = sys.argv[1]
    tag = sys.argv[2]
    msg = " ".join(sys.argv[3:])
    if len(msg) == 0:
        msg = DEFAULT_RELEASE_MESSAGE
    release = EndPoint(token, user, repo)
    try:
        url = release.publish(tag_name=tag, name=tag, body=msg)
        print(MESSAGE_FMT_RELEASED % crayons.green(url))
    except exceptions.AbnormalGithubResponse as e:
        error(str(e))


def get_token():
    """
    Find geasefile from user's home folder
    """
    home_dir = os.path.expanduser('~')
    geasefile = os.path.join(home_dir, DEFAULT_GEASE_FILE_NAME)
    try:
        with open(geasefile, 'r') as config:
            gease = json.load(config)
            return gease[KEY_GEASE_USER], gease[KEY_GEASE_TOKEN]
    except FileNotFoundError:
        raise exceptions.NoGeaseConfigFound(
            'Cannot find %s' % geasefile)


def error(message):
    print('Error: %s' % crayons.red(message))


def fatal(message):
    error(message)
    sys.exit(-1)


if __name__ == '__main__':
    main()
