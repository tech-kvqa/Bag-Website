from app import app, socketio, db

with app.app_context():
    db.create_all()

# This is the callable gunicorn needs
def socketio_app(environ, start_response):
    return socketio.wsgi_app(environ, start_response)
