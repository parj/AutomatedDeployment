'''
Created on Dec 24, 2010

@author: Parjanya Mudunuri <parjanya@gmail.com>
'''
from fabric.api import env

'''
Global Variables
'''

MX=''

def dev_all():
    global MX
    env.user = 'parj'
    env.hosts = ['localhost','192.168.1.100']
    MX='/Data/Documents/Programming/repo'
    
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
    
def getMX():
    return MX

def setMX(path):
    global MX
    MX=path