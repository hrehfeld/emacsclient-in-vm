import sys
import subprocess

import ntpath
import posixpath

import os


import argparse

vboxpath = os.environ['VBOX_MSI_INSTALL_PATH']
if not vboxpath or not os.path.exists(vboxpath):
    vboxpath = os.environ['ProgramW6432'] + '\Oracle\VirtualBox'
vboxmanage = vboxpath + "\VBoxManage.exe"

def non83_path(p):
    cmd = ['powershell', '-Command' ,'(Get-Item -LiteralPath "' + p + '").FullName']
    r = str(subprocess.run(cmd, check=True, universal_newlines=True, stdout=subprocess.PIPE).stdout).strip()
    if r.startswith('Get-Item'):
        raise Exception(r)
    return r

def convert_path(p):
    p = ntpath.realpath(p)
    #TODO: not exactly save
    if '~' in p:
        p = non83_path(p)
    drive,path = ntpath.splitdrive(p)
    drive = drive[0].lower()
    drive = '/mnt/' + drive
    path = path.replace('\\', '/')
    return drive + path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Call emacsclient in a vm')
    parser.add_argument('vm', help='client vm name')
    parser.add_argument('user', help='client vm user name')
    parser.add_argument('pw', help='client vm password')
    parser.add_argument('args', nargs='+', help='arguments to pass to emacsclient')    

    args = parser.parse_args()

    emacsargs = [convert_path(p) for p in args.args]
    
    cmd = [vboxmanage, 'guestcontrol', args.vm, 'run', '--username', args.user, '--password', args.pw, '-q'
           , '/usr/bin/emacsclient', '--', '-n'] + emacsargs
    
    subprocess.run(cmd)
    
