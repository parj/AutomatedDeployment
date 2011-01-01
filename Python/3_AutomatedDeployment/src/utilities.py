'''
Created on Dec 31, 2010

@author: parj
'''

from fabric.api import env
import os.path
from fabric.state import output
from fabric.operations import local,prompt

def rsync(fromDirectory, toDirectory, toServer=env.host, toUser=env.user):
    """
    Rsyncs from localhost to a remote directory
    
    :type fromDirectory: String
    :param fromDirectory: The directory which is to copied from localhost
    :type toDirectory: String
    :param toDirectory: The directory to which to rsync remotely
    :type toServer: String
    :param toServer: The remote server to which the file is to copied [Optional].
    :type toUser: String
    :param toUser: The remote user to be used which the remote server [Optional].
        
    
    >>> fab -H test.uk rsync:fromDirectory=/tmp/licence.jar,toDirectory=/tmp
    >>> fab dev_server rsync:fromDirectory=/tmp/licence.jar,toDirectory=/tmp
    >>> fab -H test.uk rsync:fromDirectory=/tmp/licence.jar,toDirectory=/tmp,toServer=test2.uk,toUser=user2
        
    """
    
    if (toServer == None):
        toServer = env.host
        
    rsync = _rsyncCommand_() + fromDirectory + ' ' + toUser + '@' + toServer + ':' + toDirectory
    local(rsync)
    
def _getLocationOfFile_(message):
    """
    Used for taking an input from a user for a path and checking if the file exists on the localhost.
    Returns the filepath supplied by the user. If the filepath does not exist, the function loops
    and asks the user again.
    
    :type message: String
    :param message: The command to be executed by the user  
    
    .. warning:
        Internal function not to be called directly from command line
    
    
    >>> licenceFile = getLocationOfFile("What is the location of the licence file on the localhost?")
    """
    
    fileExists = False
    iFile = None    #: holds the input filepath from the user
    
    while (not(fileExists)):
        iFile = prompt(message)
        fileExists = os.path.isfile(iFile)
        
        if (not(fileExists)):
            print(iFile + " does not exist. Please provide absolute path on the localhost")
        else:
            local('echo "File found"; ls -lrt ' + iFile, capture=False)
        
    return iFile

def _tarCommand_():
    """
    Used for returning tar command. If output.debug set to true, tar will be verbose
    """
    tarCommand = ''
    
    if (output.debug):
        tarCommand = 'tar v'
    else:
        tarCommand = 'tar '
        
    return tarCommand

def _jarCommand_():
    """
    Used for returning jar command. If output.debug set to true, jar will be verbose
    """
    jarCommand = ''
    
    if (output.debug):
        jarCommand = 'jar v'
    else:
        jarCommand = 'jar '
        
    return jarCommand

def _rsyncCommand_():
    """
    Used for returning rsync command. If output.debug set to true, rsync will be verbose
    """
    rsyncCommand = ''
    
    if (output.debug):
        rsyncCommand = 'rsync -av '
    else:
        rsyncCommand = 'rsync -aq '
        
    return rsyncCommand

def _zipCommand_():
    """
    Used for returning zip command. If output.debug set to true, zip will be verbose
    """
    zipCommand = ''
    
    if (output.debug): #If debugging is on, be more verbose
        zipCommand = 'zip -rv '
    else:
        zipCommand = 'zip -rq '
    
    return zipCommand