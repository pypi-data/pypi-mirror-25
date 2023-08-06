'''
Helpers for standard I/O work.
'''
import sys
import getpass
import click

from lib.utils import git
from lib.utils.validators import is_valid_email
from lib.utils.colorprinter import colorprint

RELEASE_LOG_TEXT = '''
# Please enter a change log for this release. Everything below this line is ignored, and an
# empty message aborts the release.

# On branch {0}
'''

ASK_EMAIL = 'Enter your email address: '
INVALID_EMAIL = 'You entered an invalid email.'
LOGIN_SUCCESS = '[✓] Logged in successfully.'
LOGIN_FAILURE = ''' n[✘] An error occurred.
Please check your connection, credentials and try again.\n
'''

def get_login_credentials():
    ''' Get login creds from user. Also includes some validation. '''
    while True:
        email = input(ASK_EMAIL)
        if is_valid_email(email):
            break
        colorprint('RED')(INVALID_EMAIL)

    password = getpass.getpass()
    return (email, password)

def login_with_email(login):
    ''' Login a user with email via auth service. '''
    email, password = get_login_credentials()
    try:
        login(email, password)
        colorprint('GREEN')(LOGIN_SUCCESS)
    except Exception:  #pylint: disable=broad-except
        colorprint('RED')(LOGIN_FAILURE)
        sys.exit(1)

def get_version():
    ''' Get the version number for this release from user. '''
    version = input('Enter a version number for this release: ')

    return version

def get_changelog():
    '''
    Opens up EDITOR, and allows user to enter changelog.
    Splits by the boilerplate text and returns user input
    '''
    current_branch = git.branch()

    data = click.edit(
        text=RELEASE_LOG_TEXT.format(current_branch),
        require_save=True
    )
    try:
        serialized = data.split(RELEASE_LOG_TEXT.format(current_branch))
        return serialized[0]
    except Exception: #pylint: disable=broad-except
        return ''
