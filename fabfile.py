from fabric.api import local

def prepare_deployment():
    local('python manage.py test --settings=website.test_settings')
    msg = raw_input('Your commit message:')
    local('git add . && git commit -m "{}"'.format(msg)) # or local('hg add && hg commit')