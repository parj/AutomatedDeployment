'''
Created on Dec 23, 2010

@author: Parjanya Mudunuri <parjanya@gmail.com>

To ensure this runs, Fabric should be deployed on the gold server
The gold server's public key should be in all server's ~/.ssh/authorized_keys
'''

from murex import *
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
