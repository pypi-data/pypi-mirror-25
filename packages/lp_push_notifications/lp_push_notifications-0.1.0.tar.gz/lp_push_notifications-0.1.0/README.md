#django-rest-push-notifications
> A Python Package for Django + Django Rest Framework

## Usage
| **Project** | **Version**|
| :--------:  | ---------- |

## Installation
```bash
pip install lp_push_notifications
```

## Setup
**Required**  Enable `lp_push_notifications` App by adding the following to the bottom of `settings.py`
```python
INSTALLED_APPS += [
    'lp_push_notifications',
]
```

**REQUIRED** Configure Push Notification Configuration in `settings.py`
```python
# Push Notification Settings
PUSH_NOTIFICATIONS_SETTINGS = {
        "FCM_API_KEY": "[your api key]",
        "GCM_API_KEY": "[your api key]",
        "APNS_CERTIFICATE": os.path.join(BASE_DIR, 'certificate.pem'),
        "APNS_TOPIC": "com.quad.pushdemo",
        "APNS_USE_SANDBOX": True,
        "WNS_PACKAGE_SECURITY_ID": "[your package security id, e.g: 'ms-app://e-3-4-6234...']",
        "WNS_SECRET_KEY": "[your app secret key, e.g.: 'KDiejnLKDUWodsjmewuSZkk']",
}
```

**REQUIRED** Add the following to the bottom of `urls.py`
```python
urlpatterns += [url(r'^', include('lp_push_notifications.urls'))]
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

### Testing
```
python manage.py test testproject
```

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