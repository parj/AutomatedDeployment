"""
Created on Dec 31, 2010

.. sectionauthor:: Parjanya Mudunuri <parjanya@gmail.com>

Hosts all the Murex specific code for starting/stopping/conifguring a murex environments
"""

import time, os.path
from fabric.api import run, env
from fabric.state import output
from fabric.contrib.console import confirm
from datetime import datetime
from utilities import _jarCommand_, _tarCommand_, _zipCommand_, _getLocationOfFile_, rsync
from environments import _getMX_

###Murex Specific Code###
def murex_buildAppTree(outputFile = 'murex.tar.gz'):
    """
    Used for packaging the Murex AppTree. The file created by default is murex.tar.gz
    
    .. note::
        * The location should be defined in the variable MX under the server details in environments.py.
        * If it is not defined, then the $MX variable environment variable is used
    
    :type appTree: String
    :param appTree: Location of apptree on the localhost
    
    
    >>> fab -H test.uk murex_buildAppTree 
    >>> fab server_del murex_buildAppTree:outputFile='murex_2010.tar.gz'
    """
    
    murex_runCommand('rm ../murex.tar.gz;tar zvcf ../outputFile . -X exclude')
    
def murex_deployAppTree(appTree=None, backup=True, bounceServices=None):
    """
    Used for deploying a packaged Murex AppTree 
    
    .. note::
        * It backups to $MX/../archive
        * The location path is created if it does not exist
        * Services are stopped
        * The backup is named appTree_backup_2010_11_12_12_30_59.zip [Year_Month_Date_Hour_Min_Sec]
        * Everything in the $MX folder is deleted
        * The appTree zip file is rsync'ed from the localhost to the remote server
        * The apptree is exploded and the packaged file removed
        * You are given the option of starting the services
    
    :type appTree: String
    :param appTree: Location of apptree on the localhost
    :type bounceServices: Boolean
    :param bounceServices: If left blank, the user is questioned if services need to be bounced. For bulk operations, set to True or False for bouncing services automatically.  
    
    
    >>> fab -H test.uk murex_deployAppTree
    >>> fab -H test.uk murex_deployAppTree:appTree=/tmp/murex.tar.gz
    >>> fab server_dev murex_deployAppTree:appTree=/tmp/murex.tar.gz,bounceServices=True
    """  
    if (appTree == None):
        appTree = _getLocationOfFile_("What is the location of the app tree file [murex.tar.gz] on the localhost?")
        
    #The folder that needs to be backed up
    murexAppTreePath = _getMX_()
    
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
        _backup_(folderToBackup = murexAppTreePath, 
                   prefix='appTree', 
                   removeDirectory=True, 
                   archiveFolder=murexAppTreePath + '/../archive')        
    
    #Copy apptree from localhost to remote server
    rsync(appTree, murexAppTreePath)
    
    tarCommand = _tarCommand_() + 'zxf ' + appTreeFileName
    
    #Explode the new apptree
    murex_runCommand("echo 'Exploding apptree';" + tarCommand + ";rm " + appTreeFileName)
    
    #TODO: Add init of files      
    
    #If required start the services
    _murex_confirmBounceServices_(bounceServices)    
        
def murex_deployLicence(licenceFile=None, backup=True, bounceServices=None):
    """
    Used for deploying the licence of Murex
     
    .. note::
        * It backups to $MX/../archive - usually
        * The backup is named licence_backup_2010_11_12_12_30_59.zip [Year_Month_Date_Hour_Min_Sec]
        * The licence jar file is rsync'ed from the localhost to the remote server
        * The licence is exploded and the orginal file removed
        * You are given the option of bouncing the services
    
    :type licenceFile: String
    :param licenceFile: The path of the licence file on the localhost machine. If this is not supplied the user will be asked  
    :type bounceServices: Boolean
    :param bounceServices: If left blank, the user is questioned if services need to be bounced. For bulk operations, set to True or False for bouncing services automatically.  
    
    Specify the full path of the licence directory of the remote server in the variable folderToBackup 
    
    
    >>> fab -H test.uk murex_deployLicence    In this situation you will be asked for the location of the file
    >>> fab -H test.uk murex_deployLicence:licenceFile=/tmp/licence.jar
    >>> fab server_dev murex_deployLicence:licenceFile=/tmp/licence.jar,bounceServices=True
    """
    
    if (licenceFile == None):
        licenceFile = _getLocationOfFile_("What is the location of the licence file on the localhost?")
    
    #The folder that needs to be backed up
    folderToBackup = _getMX_() + '/fs/licence'
    licenceFileName = os.path.basename(licenceFile)
    
    #Backup if required
    if (backup):
        _backup_(folderToBackup = folderToBackup, 
                   prefix='licence', 
                   removeDirectory=False,
                   archiveFolder=_getMX_() + '/../archive')

    #Copy licence from localhost to remote server
    rsync(licenceFile, folderToBackup)
    
    jarCommand = _jarCommand_() + 'xf ' + licenceFileName

    #Explode the new licence
    murex_runCommand('echo "Exploding licence";\
            cd ' + folderToBackup + ';\
            echo "I am in `pwd`" ;\
            ' + jarCommand + ';\
            echo "Removing jar";rm ' + licenceFileName)

    _murex_confirmBounceServices_(bounceServices)

def murex_runCommand(command, ignoreError=False):
    """
    Used for executing a command specifically for Murex
    
    .. note::
        * The function writes the variable name MX
        * Then enters that directory and
        * If output.debug is set to True, Echoes which directory it is in
        * Finally, executes the supplied command
    
    :type command: String
    :param command: The command to to run
    
    
    >>> fab -H test.uk murex_runCommand:command="./launchmxj.app -s"
    >>> fab dev_server murex_runCommand:command="./mxg2000_launchall start"
    
    """
    if (output.debug):
        print("Executing on %s as %s" % (env.hosts, env.user))
    strCommand=''

    #If variable MX is not set in the environments definition or if the murex_runCommand is called
    #directly, pick up the $MX alias. Ensure alias is defined in .bash_profile
    if (_getMX_() == None):
        if (output.debug): #If debugging is on, be more verbose
            strCommand = 'echo "MX=$MX";cd $MX;echo "I am in `pwd`";' + command
        else:   #Quietly execute
            strCommand = 'cd $MX;' + command
    else:
        if (output.debug): #If debugging is on, be more verbose
            strCommand = 'echo "MX=' + _getMX_() + '";cd ' + _getMX_() + ';echo "I am in `pwd`";' + command
        else: #Quietly execute
            strCommand = 'cd ' + _getMX_() + ';' + command 
    
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

    
    >>> fab -H test.uk start
    >>> fab dev_server start
    """
    murex_startServices()
    
def murex_startServices():
    """
    Used for starting Murex services

    
    >>> fab -H test.uk startServices
    >>> fab dev_server startServices
    """
    murex_runCommand('./mxg2000_launchall start;./launchmxj.app -s')
    
def stop():
    """
    Shortcut to murex_stopServices

    
    >>> fab -H test.uk stop
    >>> fab dev_server stop
    """
    murex_stopServices()

def murex_stopServices(ignoreError=False):
    """
    Used for stopping Murex services

    :type ignoreError: Boolean
    :param ignoreError: Ignores if there is any error while calling stop services
    
    >>> fab -H test.uk stopServices
    >>> fab dev_server stopServices
    """
    murex_runCommand('./mxg2000_launchall stop', ignoreError)
    murex_runCommand('./launchmxj.app -killall', ignoreError)
    #run('fuser -k ' + _getMX_())

def murex_bounceServices():
    """
    Used for bouncing Murex services

    .. _murex_bounceServices:
    
    >>> fab -H test.uk bounceServices
    >>> fab dev_server bounceServices
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

    
    >>> fab -H test.uk s
    >>> fab dev_server s
    """
    murex_checkServices()

def murex_checkServices():
    """
    Used for checking Murex services

    
    >>> fab -H test.uk checkServices
    >>> fab dev_server checkServices
    """
    murex_runCommand('./launchmxj.app -s')
    
    
### Hidden functions ###
def _murex_confirmBounceServices_(bounceServices):
    """
    If bounceServices variable is None, i.e User not has supplied a preference, the user will be
    questioned if the services are to be restarted.
    
    .. note::
        If a bulk deployment is taking place, set the bounceServices to True to automatically bounce
        each server
        
    .. warning::
        This function should not be called directly from Fabric, instead use :ref:`murex_bounceServices <murex_bounceServices>`
    
    :type bounceServices: Boolean
    :param bounceServices: If left blank, the user is questioned if services need to be bounced. For bulk operations, set to True or False for bouncing services automatically.  
    """
    
    #If user has not specified True or False for bouncing services, ask
    if (bounceServices == None):
        if confirm("Do you want to bounce services on " + env.user + "@" + env.host + " ?"):
            murex_bounceServices()
    else: #Use the True/False option for bouncing services
        if (bounceServices):
            murex_bounceServices()
            
def _backup_(folderToBackup, prefix, removeDirectory=False, 
               archiveFolder=_getMX_() + '../archive'):
    """
    Used for backing up a directory
    
    .. note::
        * It backups the path specified in the variable folderToBackup
        * The backup is named backup_<prefix>_2010_11_12_12_30_59.zip [Year_Month_Date_Hour_Min_Sec]
        * The backup zip is stored in the path specified in the variable archiveFolder
        * Specify the full path of the licence directory of the remote server in the variable folderToBackup 
    
    .. warning:
        Internal function not to be called directly from command line

    :type folderToBackup: String
    :param folderToBackup: The folder to backup 
     
    >>> backup(folderToBackup = folderToBackup, prefix='licence', removeDirectory=False)
    """
    
    #Generate paths
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    backupFile = prefix + '_backup_' + timestamp + '.zip'
    backupPath = archiveFolder + '/' + backupFile

    zipCommand = _zipCommand_() + backupPath + ' ' + folderToBackup
    
    #Create backup directory
    run('mkdir -p ' + archiveFolder)

    #Backup the directory
    murex_runCommand('echo "Backing up ' + prefix + ' to ' + backupFile + '";'+ zipCommand)
        
    if (removeDirectory):
        murex_runCommand('cd ' + folderToBackup + ';rm -rf *')