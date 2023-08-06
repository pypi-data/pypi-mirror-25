'''
Handle invitations to other users from here.
'''
from lib.anchor import Anchor
from lib.plugins.firebase import FirebasePlugin
from lib.services.firebase_service import Firebase
from lib.services.stdio_service import login_with_email


class InvitationService(Anchor):
    '''
    An Anchor class to invite people to a project.
    While the bulk of the work is done by the plugin, this class
    does supplementary work.
    '''

    def __init__(self, role, email):
        super().__init__()
        self.apply(FirebasePlugin())
        self.role = role
        self.target_email = email

    def delegate(self):
        ''' Public method used as the CLI hook. '''
        login_with_email(Firebase().login_with_email)
        self.apply_plugins('add_user', email=self.target_email, role=self.role)
