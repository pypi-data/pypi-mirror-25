# django-rest-account
> A Python Package for Django + Django Rest Framework

## Usage
| **Project** | **Version**|
| :--------:  | ---------- |
| [Quadco](https://github.com/Launchpeer/quadco-backend) | [v0.1.6](https://github.com/Launchpeer/django-rest-account/releases/tag/v0.1.6) |
| [The Modern Testament](https://github.com/Launchpeer/the-modern-testament-backend) | [v0.1.5](https://github.com/Launchpeer/django-rest-account/releases/tag/v0.1.5) |
|[Gotcha](https://github.com/Launchpeer/gotcha-backend)|[v0.1.6](https://github.com/Launchpeer/django-rest-account/releases/tag/v0.1.6)|


## Installation
```bash
pip install lp_accounts
```

## Setup
**REQUIRED** Enable `lp_accounts` App by adding the following to the bottom of `settings.py`
```python
INSTALLED_APPS += [
    'lp_accounts',
]
```

**REQUIRED** Add the following to the bottom of `urls.py`
```python
urlpatterns += [url(r'^', include('lp_accounts.urls'))]
```

**REQUIRED** Configure Reset Password Email Configuration in `settings.py`
```python
RESET_PASSWORD_SENDER = ''
RESET_PASSWORD_SUBJECT = ''
RESET_PASSWORD_BODY = '%s'
```

**Requried** Configure Confirmation Email Configuration in `settings.py`
```python
CONFIRM_EMAIL_ENABLED = True
CONFIRM_EMAIL_SENDER = ''
CONFIRM_EMAIL_SUBJECT = ''
CONFIRM_EMAIL_BODY = ''
```

**Optional** Configure Google Sign-In in `settings.py`
```python
# Google Sign-In Integration
# https://developers.google.com/identity/sign-in/web/backend-auth
GOOGLE_APP_ID = ''
```

**Optional** Configure Facebook Login in `settings.py`
```python
# Facebook Login Integration
# https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow#checktoken
FACEBOOK_APP_ID = ''
FACEBOOK_CLIENT_SECRET = ''
```

## Development Documentation
### Setup Development Environment
```
# Setup a virtual environment
virtualenv -p $(which python3) env

# Activate virtual environment
source env/bin/activate

# Setup Django
pip install -r requirements.txt
ln -s ../lp_accounts testproject
python manage.py migrate

# Run Server
python manage.py runserver
```

### Admin Access
[Admin URL](http://127.0.0.1:8000/admin)
  - Username: `hello@launchpeer.com`
  - Password: `l6Jw7Dhrsb8WqGca8gBFmivWh7/kHSLNfARvjqWKnKw=`


### Testing
```
python manage.py test testproject
```

### Account Types
| **Key** 	| **Value** 	        | **Description** 	                                                |
|:--------:	|----------	        |-----------------	                                                |
|TYPE_DEFAULT|1|User that registers with username and password|
|TYPE_GOOGLE|2|User that registers with Google Sign-In|
|TYPE_FACEBOOK|3|User that registers with Facebook Login|

## Publishing to PyPi
### `.pypirc`
Install this file to `~/.pypirc`
```python
[distutils]
index-servers =
  pypi
  testpypi

[pypi]
repository: https://upload.pypi.org/legacy/
username: launchpeer
password: DoD5T5bNzC5+JQZczvwYO+pBNGqp+zg2idVzEtH2gUs=

[testpypi]
repository: https://test.pypi.org/legacy/
username: launchpeer
password: DoD5T5bNzC5+JQZczvwYO+pBNGqp+zg2idVzEtH2gUs=
```

### Deploy to PyPiTest
```
python setup.py sdist upload -r testpypi
```

### Deploy to PyPi
```
python setup.py sdist upload -r pypi
```
