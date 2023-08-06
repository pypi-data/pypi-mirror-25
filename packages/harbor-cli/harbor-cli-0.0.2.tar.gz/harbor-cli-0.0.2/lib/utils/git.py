from subprocess import Popen, PIPE

def branch():
    '''
    Get current git branch.
    # git name-rev --name-only HEAD
    '''
    with Popen(['git', 'name-rev', '--name-only', 'HEAD'],
               bufsize=-1,
               stdout=PIPE,
               stderr=PIPE,
               universal_newlines=True
              ) as process:

        retval = None
        for line in process.stdout:
            retval = line

        return retval.rstrip()

def whoami():
    '''
    Get git user
    '''
    with Popen(['git', 'config', 'user.name'],
               bufsize=-1,
               stdout=PIPE,
               stderr=PIPE,
               universal_newlines=True
              ) as process:

        retval = None
        for line in process.stdout:
            retval = line

        return retval.rstrip()
