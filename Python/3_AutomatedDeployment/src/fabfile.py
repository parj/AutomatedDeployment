'''
Created on Dec 23, 2010

@author: Parjanya Mudunuri <parjanya@gmail.com>

To ensure this runs, Fabric should be deployed on the gold server
The gold server's public key should be in all server's ~/.ssh/authorized_keys
'''

from fabric.api import run, env
from fabric.operations import local,prompt
from fabric.state import output
from fabric.contrib.console import confirm
import time, os.path
from datetime import datetime
from environments import *
    
def host_info():
    print 'Checking lsb_release of host: ',  env.host
    run('lsb_release -a')

def uptime():
    run('uptime')

def vmstat():
    run('vmstat')

def rsync(fromDirectory, toDirectory, toServer=env.host, toUser=env.user):
    """
    Rsyncs from localhost to a remote directory
    
    @type fromDirectory: String
    @param fromDirectory: The directory which is to copied from localhost
    @type toDirectory: String
    @param toDirectory: The directory to which to rsync remotely
    @type toServer: String
    @param toServer: The remote server to which the file is to copied [Optional].
    @type toUser: String
    @param toUser: The remote user to be used which the remote server [Optional].
        
    Example: 
    1. fab -H test.uk rsync:fromDirectory=/tmp/licence.jar,toDirectory=/tmp
    2. fab dev_server rsync:fromDirectory=/tmp/licence.jar,toDirectory=/tmp
    3. fab -H test.uk rsync:fromDirectory=/tmp/licence.jar,toDirectory=/tmp,toServer=test2.uk,toUser=user2
    """
    
    if (toServer == None):
        toServer = env.host
        
    rsync = 'rsync -av ' + fromDirectory + ' ' + toUser + '@' + toServer + ':' + toDirectory
    local(rsync)

def murex_deployLicence(licenceFile=None):
    """
    Used for deploying the licence of Murex. 
    1. It backups the path specified in the variable folderToBackup
    2. The backup is named backup_2010_11_12_12_30_59.zip [Year_Month_Date_Hour_Min_Sec]
    3. The backup zip is stored in the path specified in the variable archiveFolder
    4. The licence jar file is rsync'ed from the localhost to the remote server
    5. The licence is exploded and the orginal file removed
    
    @type licenceFile: String
    @param licenceFile: The path of the licence file on the localhost machine. If this is not supplied
    the user will be asked  
    
    Specify the full path of the licence directory of the remote server in the variable folderToBackup 
    Example: 
    1. fab -H test.uk rsync    In this situation you will be asked for the location of the file
    2. fab -H test.uk rsync:licenceFile
    """
    
    if (licenceFile == None):
        licenceFile = __getLocationOfFile__("What is the location of the licence file on the gold server?")
    
    #The folder that needs to be backed up
    folderToBackup = getMX()
    
    #Where to place the backups
    archiveFolder = getMX() + '/../archive'
    
    #Generate paths
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    backupFile = 'backup_' + timestamp + '.zip'
    backupPath = archiveFolder + '/' + backupFile
    
    #Create backup directory
    run('mkdir -p ' + archiveFolder)
    
    #Backup the directory
    murex_runCommand('echo "Backing up licence to ' + backupFile + '"; \
            zip -r ' + backupPath + ' ' + folderToBackup)

    #Copy licence from localhost to remote server
    rsync(licenceFile, getMX())

    #Explode the new licence
    murex_runCommand("echo 'Exploding licence';\
            jar xvf testfile.jar;\
            echo 'Removing jar';rm testfile.jar")

    #If required bounce the services
    if confirm("Do you want to bounce services on " + env.user + "@" + env.host + " ?"):
        murex_bounceServices()


def murex_runCommand(command):
    """
    Used for executing a command specifically for Murex
    1. The function writes the variable name MX
    2. The function then enters that directory and
    3. The function echoes which directory it is in
    4. The function executes the supplied command
    
    @type command: String
    @param command: The command to to run
    
    Example
    1. fab -H test.uk murex_runCommand:command="./launchmxj.app -s"
    2. fab dev_server murex_runCommand:command="./mxg2000_launchall start"
    
    """
    
    output.debug = False
    print("Executing on %s as %s" % (env.hosts, env.user))
    strCommand=''
    
    #If variable MX is not set in the environments definition or if the murex_runCommand is called
    #directly, pick up the $MX alias. Ensure alias is defined in .bash_profile
    if (getMX() == None):
        strCommand = 'echo "MX=$MX";cd $MX;echo "I am in `pwd`";' + command
    else:
        strCommand = 'echo "MX=' + getMX() + '";cd ' + getMX() + ';echo "I am in `pwd`";' + command
    
    run(strCommand)
    
def start():
    """
    Shortcut to murex_startServices

    Example
    1. fab -H test.uk start
    2. fab dev_server start
    """
    murex_startServices()
    
def murex_startServices():
    """
    Used for starting Murex services

    Example
    1. fab -H test.uk startServices
    2. fab dev_server startServices
    """
    murex_runCommand('./mxg2000_launchall start;./launchmxj.app -s')
    
def stop():
    """
    Shortcut to murex_stopServices

    Example
    1. fab -H test.uk stop
    2. fab dev_server stop
    """
    murex_stopServices()

def murex_stopServices():
    """
    Used for stopping Murex services

    Example
    1. fab -H test.uk stopServices
    2. fab dev_server stopServices
    """
    murex_runCommand('./mxg2000_launchall stop')
    murex_runCommand('./launchmxj.app -killall')

def murex_bounceServices():
    """
    Used for bouncing Murex services

    Example
    1. fab -H test.uk bounceServices
    2. fab dev_server bounceServices
    """
    murex_stopServices()
    run('echo "Sleeping 2 seconds"')
    time.sleep(2)
    murex_startServices()
    
def s():
    """
    Shortcut for murex_checkServices

    Example
    1. fab -H test.uk s
    2. fab dev_server s
    """
    murex_checkServices()

def murex_checkServices():
    """
    Used for checking Murex services

    Example
    1. fab -H test.uk checkServices
    2. fab dev_server checkServices
    """
    murex_runCommand('./launchmxj.app -s')

def __getLocationOfFile__(message):
    """
    Used for taking an input from a user for a path and checking if the file exists on the localhost.
    Returns the filepath supplied by the user. If the filepath does not exist, the function loops
    and asks the user again.
    
    @type message: String
    @param message: The command to be executed by the user  
    
    Internal function not called directly.
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
