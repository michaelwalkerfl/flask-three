"""Application entry point. The config is selected with the APP_ENV environment variable."""

from webapp import create_app

app = create_app()

if __name__ == '__main__':
    app.run(ssl_context='adhoc', host='0.0.0.0', port=5001)
