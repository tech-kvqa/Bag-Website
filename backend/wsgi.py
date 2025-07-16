# from app import app, socketio, db

# with app.app_context():
#     db.create_all()

# # This is the callable gunicorn needs
# def socketio_app(environ, start_response):
#     return socketio.wsgi_app(environ, start_response)


# wsgi.py
import eventlet
eventlet.monkey_patch()  # ✅ MUST be at the very top before any imports

from app import app, socketio, db

with app.app_context():
    db.create_all()

# ✅ Gunicorn expects a callable — socketio IS a WSGI app
application = socketio
