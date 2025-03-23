# Flask-Three
A completely done for you secure Flask 3 Web Application Template that includes user and admin dashboards, email notifications and more.

![python3.11](https://img.shields.io/badge/python-3.11-brightgreen.svg?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)

## Features
- User Authentication & Authorization
- Admin Dashboard
- Email Notifications (via SendGrid)
- Redis Session Management
- Background Task Processing (via Redis Queue)
- PostgreSQL Database
- Docker Support
- Modern UI with Responsive Design

## Quick Start with Docker

1. Clone the repository:
```bash
git clone https://github.com/michaelwalkerfl/flask-three.git
cd flask-three
```

2. Create and configure `config.env`:
```bash
# Required Configuration
FLASK_SECRET_KEY=your_secret_key_here
DEVELOPMENT_DATABASE=postgresql://flaskthreeuser:flaskthreepassword@db/flaskthree
SESSION_REDIS=redis://redis:6379/0

# Database Configuration
DB_USER=flaskthreeuser
DB_PASS=flaskthreepassword
DB_NAME=flaskthree

# Mail Configuration (optional)
MAIL_SERVER=smtp.sendgrid.net
MAIL_USERNAME=your_username
MAIL_PASSWORD=your_password

# Admin User Configuration
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=your_admin_password
```

3. Start the application with Docker Compose:
```bash
docker-compose up --build
```

The application will be available at:
- Web Interface: http://127.0.0.1:5001
- PostgreSQL: localhost:5433
- Redis: localhost:6379

## Manual Setup (without Docker)

1. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate.bat
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install and start Redis:
```bash
# macOS
brew install redis
brew services start redis

# Ubuntu/Debian
sudo apt install redis-server
sudo systemctl start redis
```

4. Configure environment variables in `config.env` (see configuration section above)

5. Run the application:
```bash
export FLASK_APP=wsgi.py
flask run --cert=adhoc
```

## Development Commands

Initialize the database and create admin user:
```bash
flask create-database
flask create-roles
flask create-admin
```

## Testing

Run the test suite:
```bash
python -m pytest --cov=webapp
```

## Configuration Options

The application supports different configuration environments:
- development (default)
- test
- production
- ubuntu

Configuration variables can be set in `config.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| APP_NAME | Application name | flask-three |
| FLASK_ENV | Environment mode | development |
| FLASK_SECRET_KEY | Secret key for sessions | - |
| DEVELOPMENT_DATABASE | Database URL for development | sqlite:///development.db |
| TEST_DATABASE | Database URL for testing | sqlite:///test.db |
| PRODUCTION_DATABASE | Database URL for production | sqlite:///production.db |
| SESSION_REDIS | Redis URL for session storage | redis://redis:6379/0 |
| MAIL_SERVER | SMTP server for emails | smtp.sendgrid.net |
| MAIL_PORT | SMTP port | 587 |
| MAIL_USERNAME | SMTP username | - |
| MAIL_PASSWORD | SMTP password | - |

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


