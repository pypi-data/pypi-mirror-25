'''
Strategy for building different project types.
'''
from lib.utils import gradle
from lib.constants.paths import PATHS
from lib.utils.json_parser import json_parse
from lib.constants.build_platforms import BuildPlatforms
from lib.utils.decorators import requires_presence_of_dir, requires_presence_of_file

FILE_NOT_FOUND = 'Cannot find {0}.\
        Please make sure you are in the root of a valid React Native Project.'
DIR_NOT_FOUND = 'Cannot find the Android directory ({0}).\
        Please make sure you are in the root of a valid React Native Project.'


def build_strategies():
    ''' Build strategies for different platforms.  '''
    return {
        BuildPlatforms.REACT_NATIVE: strategy_react_native
    }


@requires_presence_of_file(
    PATHS['REACT_NATIVE_PACKAGE_JSON'],
    FILE_NOT_FOUND.format
)
@requires_presence_of_dir(
    PATHS['REACT_NATIVE_ANDROID_DIR'],
    DIR_NOT_FOUND.format
)
def strategy_react_native():
    '''
    Build strategy for react_native projects.
    '''
    gradle.clean_project()
    build_details = gradle.build_react_native()

    if build_details['returncode'] == 0:
        project_data = json_parse(PATHS['REACT_NATIVE_PACKAGE_JSON'])

        build_details.update({
            'metainf': {
                'name': project_data['name'],
                'package_name': gradle.get_react_native_project_name()
            }
        })

        return build_details

    else:
        raise Exception('Build clean/build failed.')
