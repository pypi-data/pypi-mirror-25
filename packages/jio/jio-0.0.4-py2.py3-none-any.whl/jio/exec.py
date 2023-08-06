import sys
import shlex
import subprocess


def syscall(command):
    '''Makes a syscall based on the specified command, returns stdout result of the command call'''
    if sys.platform == 'win32':
        p = subprocess.Popen(
            shlex.split(command),
            stdout=subprocess.PIPE,
            shell=True
        )
    else:
        p = subprocess.Popen(
            ['set -o pipefail && ' + command],
            stdout=subprocess.PIPE,
            shell=True,
            executable='/bin/bash'
        )
    standard_out = ''
    with p.stdout as stdo:
        standard_out = stdo.read().decode('utf-8')
    p.wait()
    if p.returncode == 124:
        return 'ERRTIMEOUT'
    if p.returncode == 1:
        return 'UNKNOWNFAIL: {}'.format(standard_out)
    return standard_out
