# from app import app, socketio, db

# with app.app_context():
#     db.create_all()

# # This is the callable gunicorn needs
# def socketio_app(environ, start_response):
#     return socketio.wsgi_app(environ, start_response)


# wsgi.py
# import eventlet
# eventlet.monkey_patch()

# from app import app, socketio, db

# with app.app_context():
#     db.create_all()

# # ✅ This is the correct WSGI application callable for Gunicorn
# application = socketio.app


# wsgi.py
import eventlet
eventlet.monkey_patch()

from app import app, socketio, db
from flask_socketio import WSGIApp  # ✅ Add this import

with app.app_context():
    db.create_all()

# ✅ This is the correct WSGI app for Flask-SocketIO 6+
application = WSGIApp(socketio, app)


