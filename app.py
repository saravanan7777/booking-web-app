from flask import Flask, render_template
from extensions import db, bcrypt, login_manager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:saro%402003@localhost:5432/booking'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)

# Import models AFTER initializing db
from models.models import User, Hotel, Booking

# Register Blueprints
from routes.auth import auth
from routes.hotels import hotels
from routes.bookings import bookings

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(hotels, url_prefix='/hotels')
app.register_blueprint(bookings, url_prefix='/bookings')

with app.app_context():
    db.create_all()



if __name__ == "__main__":
    app.run(debug=True)
