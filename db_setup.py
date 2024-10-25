from app import app, db
from models import User

# Create the database tables
with app.app_context():
    db.create_all()
