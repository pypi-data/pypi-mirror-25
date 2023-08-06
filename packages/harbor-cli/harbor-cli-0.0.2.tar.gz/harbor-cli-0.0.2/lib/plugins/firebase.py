'''
Firebase plugin module.
Writes to db/storage done from here
'''
import sys
from pyspin.spin import make_spin, Default

from lib.anchor import Anchor
from lib.plugins.hipchat import HipChatPlugin
from lib.utils.destructure import destructure
from lib.services.firebase_service import Firebase
from lib.utils.gradle import get_react_native_project_name
from lib.exceptions.FileNotFound import FileNotFoundException
from lib.utils.colorprinter import colorprint, print_with_spinner

EMAIL_EXISTS_ERROR_MESSAGE = 'An error occurred.\
        Please check your connection, credentials and try again.\n'
EXISTING_PACKAGE_ERROR = 'This package name is already registered.\
        If you want to update your details, please use the "--resync" flag\
        with admin credentials.'

class FirebasePlugin(Anchor):
    '''
    Handles firebase parts of any process.
    Generally, services will apply plugins which in turn apply their own.
    This is called somewhere down the tree.
    '''

    def __init__(self):
        super().__init__()
        super().apply(HipChatPlugin())

    def apply(self, compiler):
        compiler.plugin('register_user', self.register_user)
        compiler.plugin('add_user', self.add_user_to_project)
        compiler.plugin('deploy_project', self.deploy_project)
        compiler.plugin('register_project', self.register_project)

    def register_user(self, **kwargs):
        ''' Register a single user. '''
        def handle_error(error):
            '''
            Handle error when creating a user.
            The check we are interested in is EMAIL_EXISTS.
            '''
            error = eval(error.args[1])
            if error['error']['message'] == 'EMAIL_EXISTS':
                colorprint('RED')('\nThis email has already been registered. Please try another one.')
            else:
                colorprint('RED')(EMAIL_EXISTS_ERROR_MESSAGE)
            sys.exit(1)

        email, password = destructure(kwargs)('email', 'password')
        try:
            Firebase().signup_via_email(email, password)
            colorprint('GREEN')('\nSigned up successfully.\n')
            sys.exit(0)
        except Exception as error:
            handle_error(error)

    def register_project(self, **kwargs):
        '''
        Registers a project.
        Checks to see if there is a duplicate project with the same package name.
        Registers the current user as an admin.
        '''
        def project_output_path(proj_name):
            ''' Returns the database path  for projects. '''
            return ''.join(proj_name.split('.'))

        def members_output_path(user):
            ''' Returns the database path for members. '''
            return 'members/' + user['uid']

        name, package_name, icon_url = destructure(kwargs)('name', 'package_name', 'iconUrl')
        existing = Firebase().get_from_db('projects/' + project_output_path(package_name))
        if existing.val() is not None:
            colorprint('RED')(EXISTING_PACKAGE_ERROR)
            sys.exit(1)
        project_data = {
            'name': name,
            'uploads': {},
            'iconUrl': icon_url,
            'packageName': package_name,
        }
        member_admin_data = {
            'role': 'admin',
            'notificationLevel': 'all'
        }
        Firebase().write_to_db(
            'projects/' + project_output_path(package_name),
            project_data
        )
        Firebase().write_to_db(
            members_output_path(Firebase().get_current_user_details()) +
            '/' +
            project_output_path(package_name),
            member_admin_data,
            update=True
        )
        colorprint('GREEN')('Successfully registered.')


    def add_user_to_project(self, **kwargs):
        '''
        Add an entry to members/{uid}/{packageName}.
        '''
        def proj_path(proj_name):
            ''' Database path for projects. '''
            return ''.join(proj_name.split('.'))

        def members_output_path(user, proj_name):
            ''' Database path for members. '''
            return 'members/' + user['uid'] + '/' + proj_path(proj_name)

        target_email, role = destructure(kwargs)('email', 'role')
        try:
            project_name = get_react_native_project_name()
        except FileNotFoundException as error:
            colorprint('RED')(error.message)
            sys.exit(1)

        existing = Firebase().get_from_db('projects/' + proj_path(project_name))
        if existing.val() is None:
            colorprint('RED')('The project does not exist.')
            sys.exit(1)

        user = Firebase().get_details_for_user_by_email(target_email)()
        data = {
            'role': role,
            'notificationLevel': role
        }
        Firebase().write_to_db(
            members_output_path(user, project_name),
            data,
            update=True
        )
        colorprint('GREEN')('Invited "{0}" to "{1}" as "{2}"'.format(target_email, project_name, role))


    @print_with_spinner('GREEN', 'Deploying project.. Please be patient..')
    def deploy_project(self, **kwargs):
        ''' Firebase plugin hook for deploying a project. '''
        def timestamp():
            ''' Returns current timestamp. '''
            from datetime import datetime
            import calendar
            now = datetime.utcnow()
            return str(calendar.timegm(now.utctimetuple()))

        def storage_path(build_details, timestamp):
            ''' Returns storage path for APK. '''
            name = build_details['metainf']['name']
            return name + '/' + name + '_' +  timestamp + '.apk'

        def project_path(package_name, timestamp):
            ''' Returns the database path for new uploads to a project. '''
            return 'projects' + '/' + ''.join(package_name.split('.')) + '/uploads/' + timestamp

        def metadata_path(package_name):
            ''' Returns the database path for metadata. '''
            return 'projects' + '/' + ''.join(package_name.split('.')) + '/metadata'

        now = timestamp()
        build_details, release_type, changelog, branch, version, deployer_name = destructure(kwargs)(
            'build_details', 'release_type', 'changelog', 'branch', 'version', 'deployerName'
        )
        user = Firebase().get_current_user_details()
        self.apply_plugins(['deploy/will_upload', 'deploy/will_deploy'], {
            'user': user,
            'branch': branch,
            'version': version,
            'changelog': changelog,
            'release_type': release_type,
            'deployerName': deployer_name,
            'build_details': build_details,
        })
        url = Firebase().upload(
            storage_path(build_details, now),
            build_details['apk_path']
        )
        upload_data = {
            'branch': branch,
            'version': version,
            'releasedBy': user,
            'download_url': url,
            'changelog': changelog,
            'releaseType': release_type,
            'deployerName': deployer_name
        }
        metadata = {
            'lastReleasedOn': now,
            'lastReleasedBy': user,
            'currentVersion': version,
            'deployerName': deployer_name
        }
        compilation = {
            'url': url,
            'user':user,
            'branch': branch,
            'version': version,
            'metadata': metadata,
            'changelog': changelog,
            'release_type': release_type,
            'deployerName': deployer_name,
            'build_details': build_details,
        }
        package_name = build_details['metainf']['package_name']
        self.apply_plugins('deploy/did_upload', compilation)
        Firebase().write_to_db(
            project_path(package_name, now),
            upload_data,
            update=True
        )
        Firebase().write_to_db(
            metadata_path(package_name),
            metadata
        )
        self.apply_plugins('deploy/did_deploy', compilation)
        colorprint('GREEN')('\nUpload successful. APK was deployed.')
