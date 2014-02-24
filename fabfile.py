from fabric.api import local
import os

def prepare_deployment():
    local('python manage.py test --settings=website.test_settings')
    local('git add . --ignore-removal', capture=True) # or local('hg add && hg commit')
    #msg = raw_input('Your commit message:')
    local('git commit -m "test"', capture=True)
    
def watch():
    dirs = []
    files = [f for f in os.listdir('.')]
    for f in files:
        if f != '.git':
            dirs.append(f)
    
    dirs = ' '.join(dirs)
    cmd = 'when-changed -r {} -c fab prepare_deployment'.format(dirs)
    
    local(cmd, capture=True)
    