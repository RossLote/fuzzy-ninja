from fabric.api import local
import os

def prepare_deployment():
    local('python manage.py test --settings=website.test_settings')
    msg = raw_input('Your commit message:')
    local('git add . && git commit -m \'{}\''.format(msg)) # or local('hg add && hg commit')
    
def watch():
    dirs = []
    files = [f for f in os.listdir('.')]
    for f in files:
        if f != '.git':
            dirs.append(f)
    
    dirs = ' '.join(dirs)
    cmd = 'when-changed -r {} -c fab prepare_deployment'.format(dirs)
    
    local(cmd)
    