'''
Created on Dec 23, 2010

@author: Parjanya Mudunuri <parjanya@gmail.com>
'''

from fabric.api import run, env
from fabric.operations import local,prompt
from fabric.state import output
from fabric.contrib.console import confirm
import time, os.path, sys
from datetime import datetime

'''
Global Variables
'''
MX=''
def dev_server():
    global MX
    env.user = 'parj'
    env.hosts = ['localhost']
    MX='/Data/Documents/Programming/repo'

def staging_server():
    global MX
    env.user = 'parj'
    env.hosts = ['192.168.1.100']
    MX='/Data/Documents/Programming/repo'

def gold_server():
    global MX
    env.user = 'parj'
    env.hosts = ['localhost']
    MX='/Data/Documents/Programming/repo'

def host_info():
    print 'Checking lsb_release of host: ',  env.host
    run('lsb_release -a')

def uptime():
    run('uptime')

def vmstat():
    run('vmstat')
 
def rsync(fromDirectory, toDirectory, toServer=env.host, toUser=env.user):
    if (toServer == None):
        toServer = env.host
        
    rsync = 'rsync -av ' + fromDirectory + ' ' + toUser + '@' + toServer + ':' + toDirectory
    local(rsync)

def deploy_licence(licenceFile=None):
    global MX
    
    if (licenceFile == None):
        licenceFile = __getLocationOfFile__("What is the location of the licence file on the gold server?")
    
    #The folder that needs to be backed up
    folderToBackup = MX
    
    #Where to place the backups
    archiveFolder = MX + '/../archive'
    
    #Generate paths
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    backupFile = 'backup_' + timestamp + '.zip'
    backupPath = archiveFolder + '/' + backupFile
    
    #Create backup directory
    run('mkdir -p ' + archiveFolder)
    
    #Backup the directory
    runMurexCommand('echo "Backing up licence to ' + backupFile + '"; \
            zip -qr ' + backupPath + ' ' + folderToBackup)

    #Copy licence from localhost to remote server
    rsync(licenceFile, MX)

    #Explode the new licence
    runMurexCommand("echo 'Exploding licence';\
            jar xvf testfile.jar;\
            echo 'Removing jar';rm testfile.jar")

    #If required bounce the services
    if confirm("Do you want to bounce services on " + env.user + "@" + env.host + " ?"):
        bounceServices()
    
def runMurexCommand(command):
    output.debug = False
    print("Executing on %s as %s" % (env.host, env.user))
    run('echo "MX=$MX";cd $MX;echo "I am in `pwd`";' + command)

def startServices():
    runMurexCommand('./mxg2000_launchall start;./launchmxj.app -s')

def stopServices():
    runMurexCommand('./mxg2000_launchall stop')
    runMurexCommand('./launchmxj.app -killall')

def bounceServices():
    stopServices()
    run('echo "Sleeping 2 seconds"')
    time.sleep(2)
    startServices()

def checkServices():
    runMurexCommand('./launchmxj.app -s')
    
def __getLocationOfFile__(message):
    fileExists = False
    iFile = None
    
    while (not(fileExists)):
        iFile = prompt(message)
        fileExists = os.path.isfile(iFile)
        
        if (not(fileExists)):
            print(iFile + " does not exist. Please provide absolute path on the localhost")
        else:
            local('echo "File found"; ls -lrt ' + iFile, capture=False)
        
    return iFile
