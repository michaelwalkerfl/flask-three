"""Application entry point."""
from webapp import create_app

app = create_app(config='development')

if __name__ == "__main__":
    app.run(ssl_context=('ssl/cert.pem', 'ssl/key.pem'), host="0.0.0.0", port=5000)
