from app import app, socketio, db

# Optional: Ensure database is initialized on deployment
with app.app_context():
    db.create_all()

# This is what Gunicorn will use
socketio_app = socketio
