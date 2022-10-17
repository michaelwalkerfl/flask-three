# Flask-Two
A Flask 2 Web Application Template.

![python3.9](https://img.shields.io/badge/python-3.9-brightgreen.svg?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)

### Setting up

```
git clone https://github.com/michaelwalkerfl/flask-two.git
cd flask-two
python3 -m venv env
source env/bin/activate (if Windows, use: env\Scripts\activate.bat
```



### Configure Environment
Create a file named `config.env`. Do not commit this file to your repository, as it contains secrets. 

Add a secret key to this file e.g., `FLASK_SECRET_KEY=ThisIsOurTopSecretEncryptionKeyThatOurApplicationUses`

Other variables that can be added:

- `APP_NAME=Flask-Two`
- `FLASK_ENV=development`
- `DEVELOPMENT_DATABASE=sqlite:///development.db`
- `TEST_DATABASE=sqlite:///test.db`
- `PRODUCTION_DATABASE=sqlite:///production.db`


### Dependency Installation
```
pip install -r requirements.txt
```

### Redis needs to be installed 
```
brew install redis (If Ubuntu/Debia use: apt install redis-server)
```

### Run application from terminal
```
FLASK_APP=wsgy=i.py
flask run 
```


#### TODO
Add:
- Role Permissions
- Admin Dashboard
- Mail (for notifications)
- Celery
- Docker
- CI/CD for automated tests and deployment
