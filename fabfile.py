from fabric.api import local
import os

def prepare_deployment():
    test()
    msg = raw_input("Enter your commit message:")
    git(msg)

def test():
    local('./manage.py test --settings=website.test_settings')
    
def git(msg):
    local('git add . --ignore-removal') # or local('hg add && hg commit')
    local('git commit -m "test"'.format(msg), capture=False)
    
def watch():
    files_list = []
    #dirs = [d for d in os.listdir('.')]
    for root, dirs, files in os.walk("."):
        path = root.split('/')
        if '.git' not in path:
            for file in files:
                f, ext = os.path.splitext(file)
                if ext == '.py':
                    file_str = '%s/%s' % (root,file)
                    files_list.append(file_str)
    
    files = ' '.join(files_list)
    cmd = 'when-changed {} -c fab prepare_deployment'.format(files)
    
    local(cmd)
    
def get_files(directory):
    pass
    
