# A Semaphore demo CI/CD pipeline using Python Django

Example Python Django application and CI/CD pipeline for integrating it with Semaphore 2.0.
This application demonstrates CRUD operations using class based views in Django. It also includes UI for all CRUD views.

# Local project setup

1. Run following command to install python pre-requisite for mysqlclient python 
   ```
   sudo apt-get install python3-dev default-libmysqlclient-dev ### Ubutnu
   
   sudo yum install python3-devel mysql-devel ### Redhat / CentOS
   
   brew install mysql-connector-c ### mac os
   ```
   for more information on pre-requisite for mysqlclient, visit this page: (https://pypi.org/project/mysqlclient/)

2. Use anaconda / virtualenv for setting up this project

3. Install pip requirements
   ```
   pip install -r requirements.txt
   ```
4. Create new mysql database

5. Setup your database credentials and SITE_URL in settings.py file available inside ### pydjango_ci_integration folder

6. Once you have setup your database, Open command prompt pointing to the Root of the project directory and run following command to create application default database
   ```
   (virtualenv / conda environment) > python manage.py migrate
   
   (virtualenv / conda environment) > python manage.py createsuperuser
   ```
7. Once all of the above command run sucessfully, We are ready to go. Start server by executing command
   ```
   (virtualenv / conda environment) > python manage.py runserver 127.0.0.1:8732
   ```
  and visit the web browser with 'http://127.0.0.1:8732'
  
## Environment variables

The following environment variables can be set to override defaults:

- `SECRET_KEY`: Django [secret key](https://docs.djangoproject.com/en/2.2/ref/settings/#secret-key).
- `DB_ENGINE`: Django database [backend](https://docs.djangoproject.com/en/2.2/ref/databases/).
- `DB_NAME`: database name.
- `DB_HOST`: database hostname.
- `DB_PORT`: database port.
- `DB_USER`: database user.
- `DB_PASSWORD`: database password.

# CI/CD on Semaphore

Fork this repository and use it to [create a project](https://docs.semaphoreci.com/article/63-your-first-project)
   ```
   curl https://storage.googleapis.com/sem-cli-releases/get.sh | bash
   sem connect <semaphore-organization-link> <semaphore-id> // found in Semaphore Dashboard
   cd <project directory>
   sem init
   ```
The CI pipeline will look like this:

![pipeline](https://github.com/semaphoreci-demos/semaphore-demo-python-django/blob/master/pydjango_ci_integration/pipepline.png)

The example pipeline contains 5 blocks:

* Install Dependencies
   * Installs pip requirements
* Run Code Analysis
   * Run code analysis / code linting with Pylint
* Run Unit Tests
   * Runs Unit Tests with unittest module for views and models file
* Run Browser Tests
   * Runs browser tests with python selenium webdriver
* Run Security Tests
   * Runs security checklist with Django default deployment checklist
   
