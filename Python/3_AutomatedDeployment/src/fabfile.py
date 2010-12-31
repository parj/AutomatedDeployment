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
  
output.debug = False  #:Set to True for verbose logging

def host_info():
    """
    Gets uname and hostname
    """
    print 'Checking uname of host: ',  env.host
    run('uname -a;hostname;')

def uptime():
    """
    Gets uptime
    """
    run('uptime')

def vmstat():
    """
    Gets vmstat
    """
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
        
    rsync = __rsync__() + fromDirectory + ' ' + toUser + '@' + toServer + ':' + toDirectory
    local(rsync)

###Murex Specific Code###
def murex_buildAppTree():
    """
    Used for packaging the Murex AppTree
    The file created is murex.tar.gz
    The location should be defined in the variable MX under the server details in environments.py.
    If it is not defined, then the $MX variable environment variable is used
    
    @type appTree: String
    @param appTree: Location of apptree on the localhost
    
    Example:
    1. fab -H test.uk murex_buildAppTree 
    """
    
    murex_runCommand('rm ../murex.tar.gz;tar zvcf ../murex.tar.gz . -X exclude')
    
def murex_deployAppTree(appTree=None, backup=True, bounceServices=None):
    """
    Used for deploying a packaged [murex.tar.gz] AppTree
    1. It backups to $MX/../archive
    2. The location path is created if it does not exist
    3. Services are stopped
    4. The backup is named appTree_backup_2010_11_12_12_30_59.zip [Year_Month_Date_Hour_Min_Sec]
    5. Everything in the $MX folder is deleted
    6. The appTree zip file is rsync'ed from the localhost to the remote server
    7. The apptree is exploded and the packaged file removed
    8. You are given the option of starting the services
    
    @type appTree: String
    @param appTree: Location of apptree on the localhost
    @type startServices: Boolean
    @param startServices: If left blank, the user is questioned if services need to be bounced. For bulk operations, set to True or False for bouncing services automatically.  
    
    Example:
    1. fab -H test.uk murex_deployAppTree    NOTE: In this situation you will be asked for the location of the file
    2. fab -H test.uk murex_deployAppTree:appTree=/tmp/murex.tar.gz
    3. fab server_dev murex_deployAppTree:appTree=/tmp/murex.tar.gz, startServices=True
    """  
    if (appTree == None):
        appTree = __getLocationOfFile__("What is the location of the app tree file [murex.tar.gz] on the localhost?")
        
    #The folder that needs to be backed up
    murexAppTreePath = getMX()
    
    #Get the filename
    appTreeFileName = os.path.basename(appTree)
    
    #Create the apptree folder in case it does not exist
    run('mkdir -p ' + murexAppTreePath)
    
    try:
        #Stop the services, if there is an error ignore it
        murex_stopServices(ignoreError = True)
    except:
        ignoreError = False #Do Nothing 
    
    #Backup if required
    if (backup):
        __backup__(folderToBackup = murexAppTreePath, 
                   prefix='appTree', 
                   removeDirectory=True, 
                   archiveFolder=murexAppTreePath + '/../archive')        
    
    #Copy apptree from localhost to remote server
    rsync(appTree, murexAppTreePath)
    
    tarCommand = __tar__() + 'zxf ' + appTreeFileName
    
    #Explode the new apptree
    murex_runCommand("echo 'Exploding apptree';" + tarCommand + ";rm " + appTreeFileName)
    
    #TODO: Add init of files      
    
    #If required start the services
    murex_confirmBounceServices(bounceServices)    
        
def murex_deployLicence(licenceFile=None, backup=True, bounceServices=None):
    """
    Used for deploying the licence of Murex. 
    1. It backups to $MX/../archive - usually
    2. The backup is named licence_backup_2010_11_12_12_30_59.zip [Year_Month_Date_Hour_Min_Sec]
    3. The licence jar file is rsync'ed from the localhost to the remote server
    4. The licence is exploded and the orginal file removed
    5. You are given the option of bouncing the services
    
    @type licenceFile: String
    @param licenceFile: The path of the licence file on the localhost machine. If this is not supplied
    the user will be asked  
    @type bounceServices: Boolean
    @param bounceServices: If left blank, the user is questioned if services need to be bounced. For bulk operations, set to True or False for bouncing services automatically.  
    
    Specify the full path of the licence directory of the remote server in the variable folderToBackup 
    Example: 
    1. fab -H test.uk murex_deployLicence    In this situation you will be asked for the location of the file
    2. fab -H test.uk murex_deployLicence:licenceFile=/tmp/licence.jar
    3. fab server_dev murex_deployLicence:licenceFile=/tmp/licence.jar,bounceServices=True
    """
    
    if (licenceFile == None):
        licenceFile = __getLocationOfFile__("What is the location of the licence file on the localhost?")
    
    #The folder that needs to be backed up
    folderToBackup = getMX() + '/fs/licence'
    licenceFileName = os.path.basename(licenceFile)
    
    #Backup if required
    if (backup):
        __backup__(folderToBackup = folderToBackup, 
                   prefix='licence', 
                   removeDirectory=False,
                   archiveFolder=getMX() + '/../archive')

    #Copy licence from localhost to remote server
    rsync(licenceFile, folderToBackup)
    
    jarCommand = __jar__() + 'xf ' + licenceFileName

    #Explode the new licence
    murex_runCommand('echo "Exploding licence";\
            cd ' + folderToBackup + ';\
            echo "I am in `pwd`" ;\
            ' + jarCommand + ';\
            echo "Removing jar";rm ' + licenceFileName)

    murex_confirmBounceServices(bounceServices)

def murex_runCommand(command, ignoreError=False):
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
    if (output.debug):
        print("Executing on %s as %s" % (env.hosts, env.user))
    strCommand=''

    #If variable MX is not set in the environments definition or if the murex_runCommand is called
    #directly, pick up the $MX alias. Ensure alias is defined in .bash_profile
    if (getMX() == None):
        if (output.debug): #If debugging is on, be more verbose
            strCommand = 'echo "MX=$MX";cd $MX;echo "I am in `pwd`";' + command
        else:   #Quietly execute
            strCommand = 'cd $MX;' + command
    else:
        if (output.debug): #If debugging is on, be more verbose
            strCommand = 'echo "MX=' + getMX() + '";cd ' + getMX() + ';echo "I am in `pwd`";' + command
        else: #Quietly execute
            strCommand = 'cd ' + getMX() + ';' + command 
    
    if ignoreError:
        try:
            run(strCommand)
        except:
            if (output.debug): #If debugging is on, be more verbose
                print("Ignoring error while executing " + strCommand)            
    else:
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

def murex_stopServices(ignoreError=False):
    """
    Used for stopping Murex services

    Example
    1. fab -H test.uk stopServices
    2. fab dev_server stopServices
    """
    murex_runCommand('./mxg2000_launchall stop', ignoreError)
    murex_runCommand('./launchmxj.app -killall', ignoreError)
    #run('fuser -k ' + getMX())
    
def murex_confirmBounceServices(bounceServices):
    """
    If bounceServices variable is None, i.e User not has supplied a preference, the user will be
    questioned if the services are to be restarted.
    
    If a bulk deployment is taking place, set the bounceServices to True to automatically bounce
    each server
    
    @type bounceServices: Boolean
    @param bounceServices: If left blank, the user is questioned if services need to be bounced. For bulk operations, set to True or False for bouncing services automatically.  
    """
    
    #If user has not specified True or False for bouncing services, ask
    if (bounceServices == None):
        if confirm("Do you want to bounce services on " + env.user + "@" + env.host + " ?"):
            murex_bounceServices()
    else: #Use the True/False option for bouncing services
        if (bounceServices):
            murex_bounceServices()
    
def murex_bounceServices():
    """
    Used for bouncing Murex services

    Example
    1. fab -H test.uk bounceServices
    2. fab dev_server bounceServices
    """
    try:
        murex_stopServices(ignoreError=True)
    except:
        ignoreError=True   #Do Nothing
        
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


### Hidden functions ###
def __backup__(folderToBackup, prefix, removeDirectory=False, 
               archiveFolder=getMX() + '../archive'):
    """
    Used for backing up a directory
    1. It backups the path specified in the variable folderToBackup
    2. The backup is named backup_<prefix>_2010_11_12_12_30_59.zip [Year_Month_Date_Hour_Min_Sec]
    3. The backup zip is stored in the path specified in the variable archiveFolder

    @type folderToBackup: String
    @param folderToBackup: The folder to backup 
    
    Specify the full path of the licence directory of the remote server in the variable folderToBackup 
    Internal function not to be called directly
    
    Example: 
    __backup__(folderToBackup = folderToBackup, prefix='licence', removeDirectory=False)
    """
    
    #Generate paths
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    backupFile = prefix + '_backup_' + timestamp + '.zip'
    backupPath = archiveFolder + '/' + backupFile

    zipCommand = __zip__() + backupPath + ' ' + folderToBackup
    
    #Create backup directory
    run('mkdir -p ' + archiveFolder)

    #Backup the directory
    murex_runCommand('echo "Backing up licence to ' + backupFile + '";'+ zipCommand)
        
    if (removeDirectory):
        murex_runCommand('cd ' + folderToBackup + ';rm -rf *')
    
def __getLocationOfFile__(message):
    """
    Used for taking an input from a user for a path and checking if the file exists on the localhost.
    Returns the filepath supplied by the user. If the filepath does not exist, the function loops
    and asks the user again.
    
    @type message: String
    @param message: The command to be executed by the user  
    
    Internal function not to be called directly
    
    Example:
    licenceFile = __getLocationOfFile__("What is the location of the licence file on the localhost?")
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

def __tar__():
    """
    Used for returning tar command. If output.debug set to true, tar will be verbose
    """
    tarCommand = ''
    
    if (output.debug):
        tarCommand = 'tar v'
    else:
        tarCommand = 'tar '
        
    return tarCommand

def __jar__():
    """
    Used for returning jar command. If output.debug set to true, jar will be verbose
    """
    jarCommand = ''
    
    if (output.debug):
        jarCommand = 'jar v'
    else:
        jarCommand = 'jar '
        
    return jarCommand

def __rsync__():
    """
    Used for returning rsync command. If output.debug set to true, rsync will be verbose
    """
    rsyncCommand = ''
    
    if (output.debug):
        rsyncCommand = 'rsync -av '
    else:
        rsyncCommand = 'rsync -aq '
        
    return rsyncCommand

def __zip__():
    """
    Used for returning zip command. If output.debug set to true, zip will be verbose
    """
    zipCommand = ''
    
    if (output.debug): #If debugging is on, be more verbose
        zipCommand = 'zip -rv '
    else:
        zipCommand = 'zip -rq '
    
    return zipCommand