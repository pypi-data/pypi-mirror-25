# django-rest-stripe
> A Python Package for Django + Django Rest Framework

## Usage
| **Project** | **Version**|
| :--------:  | ---------- |
| [Quadco](https://github.com/Launchpeer/quadco-backend) | [v0.1.5](https://github.com/Launchpeer/django-rest-stripe/releases/tag/v0.1.5)|
| [The Modern Testament](https://github.com/Launchpeer/the-modern-testament-backend) | [v0.1.4](https://github.com/Launchpeer/django-rest-stripe/releases/tag/v0.1.4)|



## Installation
```bash
pip install lp_stripe
```

## Setup
**REQUIRED** Run migrations
```bash
python manage.py migrate
```

**REQUIRED** Enable `lp_stripe` App by adding the following to the bottom of `settings.py`
```python
INSTALLED_APPS += [
    'lp_stripe',
]
```

**REQUIRED** Add the following to the bottom of `urls.py`
```python
urlpatterns += [url(r'^', include('lp_stripe.urls'))]
```

**REQUIRED** Setup Production/Testing API Keys in `settings.py`
```python
STRIPE_API_KEY = ''
STRIPE_TEST_API_KEY = ''
```

**OPTIONAL** Setup Stripe mode in `settings.py`
```python
from lp_strip.conf import Settings
STRIPE_MODE = os.environ.get('STRIPE_MODE', Settings.MODE_TEST)
```

| **Key** | **Value** | **Description** |
| :----:  | --------- | --------------- |
| `MODE_TEST` | 1 | Uses `STRIPE_TEST_API_KEY` |
| `MODE_LIVE` | 2 | Uses `STRIPE_API_KEY` |


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
  - Password: `97irwAQza4A/YfFwHNvOUWWataHrC9R8imxxnOz1fwQ=`

### Fixtures
```json
[
  {
    "model": "auth.user",
    "pk": 1,
    "fields": {
      "password": "pbkdf2_sha256$36000$C6t2f61ErYku$qU5c47ogDKJ9iGafalQC0+lggrOkco/MiZPogxO5CXc=",
      "last_login": null,
      "is_superuser": true,
      "username": "hello@launchpeer.com",
      "first_name": "",
      "last_name": "",
      "email": "hello@launchpeer.com",
      "is_staff": true,
      "is_active": true,
      "date_joined": "2017-09-03T19:55:15.963Z",
      "groups": [],
      "user_permissions": []
    }
  },
  {
    "model": "auth.user",
    "pk": 2,
    "fields": {
      "password": "pbkdf2_sha256$36000$jMjtByfsRh7O$G6DrJMwLbMXnhHRheweGgya+YanUFP9fHx81aB5/nOE=",
      "last_login": null,
      "is_superuser": false,
      "username": "derek.jeter",
      "first_name": "Derek",
      "last_name": "Jeter",
      "email": "derek.jeter@launchpeer.com",
      "is_staff": false,
      "is_active": true,
      "date_joined": "2017-09-03T22:26:26Z",
      "groups": [],
      "user_permissions": []
    }
  },
  {
    "model": "auth.user",
    "pk": 3,
    "fields": {
      "password": "pbkdf2_sha256$36000$LupZmypHvqBc$2qC8oqrO7qkiS4yA+VqQSRmR4B0VvB+RvV+fEjxLDTw=",
      "last_login": null,
      "is_superuser": false,
      "username": "ken.griffey",
      "first_name": "Ken",
      "last_name": "Griffey",
      "email": "ken.griffey@launchpeer.com",
      "is_staff": true,
      "is_active": true,
      "date_joined": "2017-09-05T18:25:34Z",
      "groups": [],
      "user_permissions": []
    }
  }
]
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
