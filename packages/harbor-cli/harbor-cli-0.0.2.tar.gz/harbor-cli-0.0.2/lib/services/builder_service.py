'''
Module for getting an instance that builds the project
for a given build platform.
'''
import sys

from lib.constants.build_platforms import BuildPlatforms
from lib.services.build_strategies import build_strategies
from lib.exceptions.DirNotFound import DirNotFoundException
from lib.exceptions.FileNotFound import FileNotFoundException
from lib.utils.colorprinter import colorprint


def builder(build_platform=BuildPlatforms.REACT_NATIVE):
    ''' Returns a builder class for a specific platform '''
    def build():
        '''
        Call the build strategy for the platform.
        Handle exceptions
        '''
        red_printer = colorprint('RED')
        try:
            return build_strategies()[build_platform]()
        except DirNotFoundException as error:
            red_printer(error.message)
            sys.exit(1)
        except FileNotFoundException as error:
            red_printer(error.message)
            sys.exit(0)

    return build
