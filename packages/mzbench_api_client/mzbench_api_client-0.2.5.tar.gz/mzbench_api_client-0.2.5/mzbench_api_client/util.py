
from __future__ import print_function

from contextlib import contextmanager
import sys
import os
import traceback
import shlex
import subprocess
import time
from multiprocessing import Process

def slurp(path):
    with open(path, 'r') as f:
        return f.read()

def spit(path, content):
    with open(path, 'w') as f:
        f.write(content)

def info(msg, logs=None, **kw):
    print("[ INFO ] {0}".format(msg))
    if logs is not None:
        new_log = {
            'text': msg,
            'timestamp': int(time.time()),
            'severity': 'info'}
        new_log.update(kw)
        logs.append(new_log)

def error(msg, logs=None, **kw):
    print("[ ERROR ] " + msg, file=sys.stderr)
    if "DEBUG" in os.environ:
        traceback.print_exc(file=sys.stderr)
    if logs is not None:
        new_log = {
            'text': msg,
            'timestamp': int(time.time()),
            'traceback': traceback.format_exc(),
            'severity': 'error'}
        new_log.update(kw)
        logs.append(new_log)

def check_output(*popenargs, **kwargs):
    r"""Run command with arguments and return its output as a byte string.
    Backported from Python 2.7 as it's implemented as pure python on stdlib.

    >>> check_output(['/usr/bin/python', '--version'])
    Python 2.6.2
    """
    process = subprocess.Popen(
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            *popenargs, **kwargs)

    output, err = process.communicate()
    retcode = process.poll()
    if retcode:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]
        error = subprocess.CalledProcessError(retcode, cmd)
        error.output = "Stdout+Stderr:\n{0}".format(output)
        print(error.output)
        raise error
    return output

def sudo_cmd(command):
    return cmd('sudo {0}'.format(command))

def draw_dots():
    dots = 0
    clean = 1

    while True:
        time.sleep(0.3)
        dots = dots + 1
        if dots % 7 == 0:
            if clean:
                print()
            sys.stdout.write(".")
            sys.stdout.flush()
            clean = 0


def cmd(command):
    args = shlex.split(command)

    if "flush" in dir(sys.stdout):
        sys.stdout.write('Executing ' + str(command))
        p = Process(target=draw_dots)
        try:
            p.start()
            output = check_output(args)
            print()
            return output
        finally:
            p.terminate()

    else:
        print('Executing', command)
        return check_output(args)

def remote_cmd(host, command, ssh_opts = ""):
    ssh_cmd = "ssh -A -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=false {0} {1} \"source /etc/profile; {2}\"".format(ssh_opts, host, command)
    return cmd(ssh_cmd)

def mangle_experiment_name(name):
    return name.replace(' ', '_').replace(',', '_')


@contextmanager
def chdir(dirname=None):
    curdir = os.getcwd()
    try:
        if dirname:
            os.chdir(dirname)
        yield
    finally:
        os.chdir(curdir)

@contextmanager
def silent_stdout():

    class Dummy(object):
        def write(self, _):
            pass

    saved_stdout = sys.stdout
    sys.stdout = Dummy()
    try:
        yield
    finally:
        sys.stdout = saved_stdout

def multiline_strip(s):
    '''Returns a copy of s with empty lines and
    leading and trailing spaces removed'''
    '\n'.join((x.strip() for x in s.split('\n') if x))
