'''
Handle registration of users/projects from here.
'''
import sys

from lib.anchor import Anchor
from lib.constants.paths import PATHS
from lib.services.stdio_service import get_login_credentials, login_with_email
from lib.services.firebase_service import Firebase
from lib.utils.gradle import get_react_native_project_name
from lib.utils.json_parser import json_parse
from lib.exceptions.FileNotFound import FileNotFoundException
from lib.plugins.firebase import FirebasePlugin
from lib.utils.decorators import requires_presence_of_file
from lib.utils.colorprinter import colorprint


class RegistrationService(Anchor):
    '''
    An Anchor class to register a user or project.
    While the bulk of the work is done by the plugins, this class
    does supplementary work.
    '''

    def __init__(self):
        super().__init__()
        self.apply(FirebasePlugin())

    def delegate(self, is_user_registration=False):
        ''' Delegate for the CLI. The only public method. '''
        if is_user_registration:
            email, password = get_login_credentials()
            self.apply_plugins('register_user', email=email, password=password)

        login_with_email(Firebase().login_with_email)
        self.__register_project__()

    def __register_project__(self):
        ''' Register a project on the server. '''
        try:
            package_name = get_react_native_project_name()
            package_json = json_parse('package.json')
            package_json_name = package_json['name']
        except FileNotFoundException as error:
            colorprint('RED')(error.message)
            sys.exit(1)

        try:
            find_icons()
            icon_path = Firebase().upload(package_json_name + '/icon.png', PATHS['ICONS_XXHDPI'])
        except FileNotFoundException:
            icon_path = None
            print('Could not find icons.. ignoring.')

        self.apply_plugins('register_project',
                           name=package_json_name,
                           package_name=package_name,
                           iconUrl=icon_path
                          )


@requires_presence_of_file(
    PATHS['ICONS_XXHDPI'],
    'Cannot find icons in path {0}. Skipping..'.format
)
def find_icons():
    '''
    Return which icon sets were found
    Currently only returns True, and icon is hardcoded to xxhdpi
    '''
    return True
