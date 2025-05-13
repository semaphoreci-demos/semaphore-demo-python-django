

# Django CI/CD with Semaphore and PythonAnywhere

![Python Version](https://img.shields.io/badge/python-3.8-blue.svg)
![Django Version](https://img.shields.io/badge/django-3.2-green.svg)
![License](https://img.shields.io/github/license/guderian120/semaphore-demo-python-django)
![Last Commit](https://img.shields.io/github/last-commit/guderian120/semaphore-demo-python-django)
![Code Style](https://img.shields.io/badge/code%20style-pylint-yellow.svg)
![Deployed](https://img.shields.io/badge/deployed-PythonAnywhere-lightgrey)


# Django CI/CD with Semaphore and PythonAnywhere Live Project 
[Live Project here ](https://guderian.pythonanywhere.com)

This project demonstrates a complete CI/CD pipeline using **Django**, **Semaphore**, and **PythonAnywhere**. It covers development setup, continuous integration, and automated deployment using SSH.

# Django CI/CD with Semaphore and PythonAnywhere

This project demonstrates a complete CI/CD pipeline using **Django**, **Semaphore**, and **PythonAnywhere**. It covers development setup, continuous integration, and automated deployment using SSH.

---

## 🧰 Project Setup

### 📦 Handling Dependencies

To avoid deprecated packages and resolve dependency issues with `mysqlclient`, make sure the following system packages are installed:

```bash
sudo apt-get update
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config libssl-dev
```

Then install Python dependencies:

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 🔧 Swapping Test Runners

If you're migrating from `django-nose` (which is no longer maintained), uninstall it:

```bash
pip uninstall django-nose nose
```

Switch to `pytest`:

```bash
pip install pytest pytest-django psycopg2-binary
```

Update your `settings.py` to use Django’s default test runner:

```python
# Remove or comment out these lines:
# TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
# NOSE_ARGS = [...]

# Add this:
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
```

---

## 🧪 CI with Semaphore

This project uses Semaphore to automate testing and deployment. Below is the complete `semaphore.yml` configuration:

```yaml
version: v1.0
name: Django CI/CD Pipeline
agent:
  machine:
    type: e1-standard-2
    os_image: ubuntu2004

global_job_config:
  prologue:
    commands:
      - sem-version python 3.8

blocks:
  - name: Install Dependencies
    task:
      prologue:
        commands:
          - sudo apt-get update && sudo apt-get install -y python3-dev default-libmysqlclient-dev build-essential pkg-config libssl-dev
          - pip install --upgrade pip setuptools wheel
      jobs:
        - name: pip
          commands:
            - checkout
            - cache restore
            - pip download --cache-dir .pip_cache -r requirements.txt
            - cache store
      env_vars:
        - name: DJANGO_TEST_ENV
          value: 'true'

  - name: Run Code Analysis
    task:
      jobs:
        - name: Pylint
          commands:
            - checkout
            - cache restore
            - pip install -r requirements.txt --cache-dir .pip_cache
            - git ls-files | grep -v 'migrations' | grep -v 'settings.py' | grep -v 'manage.py' | grep -E '.py$' | xargs pylint -E --load-plugins=pylint_django

  - name: Run Unit Tests
    task:
      prologue:
        commands:
          - sem-service start mysql
      jobs:
        - name: Model Tests
          commands:
            - checkout
            - cache restore
            - pip install -r requirements.txt --cache-dir .pip_cache
            - python manage.py test tasks.tests.test_models
        - name: View Tests
          commands:
            - python manage.py test tasks.tests.test_views
      env_vars:
        - name: DJANGO_TEST_ENV
          value: 'true'

  - name: Run Browser Tests
    task:
      env_vars:
        - name: DB_NAME
          value: pydjango
      prologue:
        commands:
          - sem-service start mysql
          - sudo apt-get update && sudo apt-get install -y -qq mysql-client
          - mysql --host=0.0.0.0 -uroot -e "create database $DB_NAME"
          - checkout
          - cache restore
          - pip install -r requirements.txt --cache-dir .pip_cache
          - nohup python manage.py runserver 127.0.0.1:8732 &
      jobs:
        - name: Browser Tests
          commands:
            - echo "Browser test command goes here"

  - name: Run Security Checks
    task:
      jobs:
        - name: Deployment Checklist
          commands:
            - checkout
            - cache restore
            - pip install -r requirements.txt --cache-dir .pip_cache
            - python manage.py check --deploy --fail-level ERROR
```

---

## 🛠 Conditional Database for Testing

To ensure smooth CI testing even without internet access to the production database, the settings file uses SQLite for test runs:

```python
if os.environ.get('DJANGO_TEST_ENV') == 'true':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.mysql'),
            'NAME': os.getenv('DB_NAME', 'None'),
            'USER': os.getenv('DB_USER', 'None'),
            'PASSWORD': os.getenv('DB_PASSWORD', 'None'),
            'HOST': os.getenv('DB_HOST', '127.0.0.1'),
            'PORT': os.getenv('DB_PORT', '3306')
        }
    }
```

---

## 🚀 Deployment to PythonAnywhere (CD)

### 🐍 Setting up WSGI

On PythonAnywhere, go to the **Web** tab and create a **manual configuration** web app. Then edit your `wsgi.py`:

```python
import os
import sys
from dotenv import load_dotenv

path = '/home/YOUR_USERNAME/semaphore-demo-python-django'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'pydjango_ci_integration.settings'

env_file = os.path.expanduser('~/.env-production')
load_dotenv(env_file)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

> Replace `YOUR_USERNAME` and project path accordingly.

### 🔑 SSH Access (Requires Paid PythonAnywhere Account)

To enable automated deployment:

```bash
ssh-copy-id YOUR_USERNAME@ssh.pythonanywhere.com
```

---

## 🔄 CD with Semaphore

### 🔐 Create Secrets

1. In Semaphore, go to your project > **Settings > Secrets**
2. Add:
   - `SSH_KEY`: Your private SSH key
   - `ENV_PRODUCTION`: Your `.env-production` file

### 📜 `deploy.sh`

Create a `deploy.sh` file:

```bash
cd $APP_URL
git fetch --all
git reset --hard origin/$SEMAPHORE_GIT_BRANCH

source $ENV_FILE
source ~/.virtualenvs/$APP_URL/bin/activate
python manage.py migrate

touch /var/www/"$(echo $APP_URL | sed 's/\./_/g')"_wsgi.py
```

### 🧱 Deployment Block (Semaphore UI)

1. Add a new block: **Deploy to PythonAnywhere**
2. Set environment variables:
   - `SSH_USER = your_pythonanywhere_username`
   - `APP_URL = your_username.pythonanywhere.com`
   - `ENV_FILE = ~/.env-production`
3. Add the two secrets: `SSH_KEY`, `ENV_PRODUCTION`
4. Under Jobs:
   - Name: `Push code`
   - Commands:
     ```bash
     checkout
     envsubst < deploy.sh > ~/deploy-production.sh
     chmod 0600 ~/.ssh/id_rsa_pa
     ssh-keyscan -H ssh.pythonanywhere.com >> ~/.ssh/known_hosts
     ssh-add ~/.ssh/id_rsa_pa
     scp -oBatchMode=yes ~/.env-production ~/deploy-production.sh $SSH_USER@ssh.pythonanywhere.com
     ssh -oBatchMode=yes $SSH_USER@ssh.pythonanywhere.com bash deploy-production.sh
     ```

---

## ✅ Final Thoughts

With this setup:
- Every push runs linting, unit tests, and security checks
- Deployment is triggered via a CD pipeline using SSH
- Environment-specific settings ensure test safety

Feel free to fork, clone, and contribute to improve this CI/CD flow for Django deployments.
