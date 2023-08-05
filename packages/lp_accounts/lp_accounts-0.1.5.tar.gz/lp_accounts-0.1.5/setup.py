from setuptools import setup
setup(
  name='lp_accounts',
  packages=['lp_accounts'],
  package_data={'lp_accounts': ['fixtures/*', 'migrations/*', 'validators/*']},
  version='0.1.5',
  description='REST Framework for User Accounts',
  author='Jim Simon',
  author_email='hello@launchpeer.com',
  url='https://github.com/Launchpeer/django-rest-account',
  download_url='https://github.com/Launchpeer/django-rest-account/archive/master.tar.gz',
  keywords=[],
  classifiers=[],
)