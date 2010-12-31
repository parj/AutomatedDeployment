"""
Created on Dec 24, 2010

@author: Parjanya Mudunuri <parjanya@gmail.com>
"""
from fabric.api import env

"""
Global Variables
"""


MX='' #: Holds the MX apptree path

def server_dev_all():
    '''
    All dev servers. Useful for bulk operations
    '''
    
    global MX
    env.user = 'parj'
    env.hosts = ['localhost','192.168.1.100']
    MX='/Data/Documents/Programming/repo'
    
def server_dev():
    """
    Dev server - parj@localhost
    """
    global MX
    env.user = 'parj'
    env.hosts = ['127.0.0.1']
    MX='/opt/DEV/parj/thirdparty/murex'
 
def server_staging():
    """
    Staging server - parj@192.168.1.100
    """
    global MX
    env.user = 'parj'
    env.hosts = ['192.168.1.100']
    MX='/opt/UAT/parj/thirdparty/murex'

def server_gold():
    """
    Gold server - parj@localhost
    """
    global MX
    env.user = 'parj'
    env.hosts = ['localhost']
    MX='/Data/Documents/Programming/repo'
    
def getMX():
    """
    Returns the value of the global MX variable
    """
    return MX

def setMX(path):
    """
    Sets the value of the global MX variable
    
    @type path: String
    @param path: Path of the MX apptree  
    """
    global MX
    MX=path