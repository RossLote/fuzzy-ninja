from fabric.api import local

def prepare_deployment():
    local('python manage.py test --settings=website.test_settings')
    local('git add -p && git commit') # or local('hg add && hg commit')