#!/usr/bin/env python

import os
import re
import time
import subprocess
import tempfile
import base64
import json
import urllib2
import urlparse
import shutil
import hashlib
import traceback
import signal
import threading

def autoapply(exit, config):
    sleep = int(config['sleep'])
    while not exit.is_set():
        print(time.ctime(time.time()))
        try:
            with tempfile.NamedTemporaryFile() as f:
                fetch(config['url'], f)
                print_hash(f.name)
                kubectl(f.name)
        except Exception:
            traceback.print_exc()
        print('Sleeping for %i seconds ...' % sleep)
        exit.wait(60)
    print('Shutting down...')

def fetch(url, out):
    print('Fetching %s ...' % url)
    if url.startswith('git'):
        # special handling for Git URLs
        check_ssh_key()
        if url.startswith('git://'):
            url = url[6:]
        parts = url.split(':', 3)
        remote = parts[0] + ':' + parts[1]
        path = parts[2]
        branch = 'master'
        if '#' in path:
            p = path.split('#', 2)
            path = p[0]
            branch = p[1]
        with tempfile.NamedTemporaryFile() as tar_out:
            subprocess.call(['git', 'archive', '--remote', remote, branch, path], stdout=tar_out)
            subprocess.call(['tar', '-xOf', tar_out.name], stdout=out)
    else:
        out.write(urllib2.urlopen(url).read())
        out.flush()

def check_ssh_key():
    # when mounting secrets from Kubernetes, all files have the mode 644,
    # but SSH expects the key to have more restrictive permissions
    id_rsa = os.path.expanduser('~/.ssh/id_rsa')
    if os.path.exists(id_rsa):
        mode = os.stat(id_rsa).st_mode & 0777
        if mode != 0600:
            print('wrong mode %o, changing to 0600: %s' % (mode, id_rsa))
            os.chmod(id_rsa, 0600)

def print_hash(filename):
    print('Calculating hash ...')
    sha1 = hashlib.sha1()
    with open(filename, 'r') as f:
        sha1.update(f.read())
    print(sha1.hexdigest())

def kubectl(filename):
    print('Running kubectl apply ...')
    subprocess.call(['kubectl', 'apply', '-f', filename])

if __name__ == '__main__2':
    config = {
        'url': None,
        'sleep': '60'
    }
    for (key, value) in config.items():
        k = key.upper()
        if k in os.environ:
            value = os.environ[k]
            config[key] = value
        if not value:
            raise Exception('Missing configuration: %s' % k)
    exit = threading.Event()
    def quit(signal, _frame):
        print('Interrupted by %d, shutting down' % signal)
        exit.set()
    signal.signal(getattr(signal, 'SIGTERM'), quit)
    signal.signal(getattr(signal, 'SIGINT'), quit)
    autoapply(exit, config)


DEFAULT_BRANCH = 'master'
GIT_URL_PATTERN = re.compile('^(git://)?(?P<remote>[^:#]+:[^:#]+)(?::(?P<path>[^#:]+))?(?:#(?P<branch>.+))?$')
GITHUB_PATH = re.compile('^/([^/]+/[^/]+)/(.*)$')


if __name__ == '__main__':
    #url = urlparse.urlparse('git://github.com/pascalgn/hostinfo/examples/')
    run('git@wsxp-gitlab.westeurope.cloudapp.azure.com:UniperDigital/uniperdigital-deployment.git:uniperdigital-dev.yaml')
    run('ssh://git@wsxp-gitlab.westeurope.cloudapp.azure.com:80/UniperDigital/uniperdigital-deployment.git:uniperdigital-dev.yaml')
    #run('https://github.com/pascalgn/autoapply/')
