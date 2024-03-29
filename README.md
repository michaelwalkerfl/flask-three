# Flask-Three
A completely done for you secure Flask 3 Web Application Template that includes user and admin dashboards, email notifications and more.

![python3.11](https://img.shields.io/badge/python-3.11-brightgreen.svg?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)

### Setting up

```
git clone https://github.com/michaelwalkerfl/flask-three.git
cd flask-three
python3 -m venv venv
source venv/bin/activate (if Windows, use: venv\Scripts\activate.bat
```



### Configure Environment
Create a file named `config.env`. Do not commit this file to your repository, as it contains secrets. 

Add a secret key to this file e.g., `FLASK_SECRET_KEY=ThisIsOurTopSecretEncryptionKeyThatOurApplicationUses`

Other variables that can be added:

- `APP_NAME=Flask-Three`
- `FLASK_ENV=development`
- `DEVELOPMENT_DATABASE=sqlite:///development.db`
- `TEST_DATABASE=sqlite:///test.db`
- `PRODUCTION_DATABASE=sqlite:///production.db`


### Dependency Installation
```
pip install -r requirements.txt
```

### Redis needs to be installed (and turned on) 
```
brew install redis (If Ubuntu/Debian use: apt install redis-server)
brew services start (or restart)
```

### Run application from terminal
```
FLASK_APP=wsgi.py
flask run --cert=adhoc
```

### Commands
#### Create database, roles and admin user
These commands can be run from the command line interface to quickly set up a database, roles and an admin user for your Flask application.
```
flask create-database
flask create-roles
flask create-admin
```

### Tests
#### Functional and Unit tests can be found in the tests directory.
Run the following command from the root directory.
```
python -m pytest --cov=webapp
```

### TODO
#### Add:
- Docker
- CI/CD for automated tests and deployment
