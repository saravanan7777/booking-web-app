from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:saro%402003@localhost:5432/booking'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    checkin = db.Column(db.Date, nullable=False)
    checkout = db.Column(db.Date, nullable=False)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'), nullable=False)
    hotel = db.relationship('Hotel', backref=db.backref('bookings', lazy=True))

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# View Hotels
@app.route('/hotels')
def v_hotels():
    hotels = Hotel.query.all()
    return render_template('hotels.html', hotels=hotels)

# Hotel Details & Booking
@app.route('/hotels/<int:hotel_id>')
def hotel_detail(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    return render_template('hotel_detail.html', hotel=hotel)

@app.route('/hotels/<int:hotel_id>/book', methods=['GET', 'POST'])
def book_hotel(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)

    if request.method == 'POST':  # When form is submitted
        name = request.form['name']
        email = request.form['email']
        checkin = datetime.strptime(request.form['checkin'], '%Y-%m-%d').date()
        checkout = datetime.strptime(request.form['checkout'], '%Y-%m-%d').date()

        new_booking = Booking(name=name, email=email, checkin=checkin, checkout=checkout, hotel_id=hotel.id)
        db.session.add(new_booking)
        db.session.commit()

        # ✅ Fix: Redirect using booking_id
        return redirect(url_for('confirmation', booking_id=new_booking.id))

    return render_template('booking_form.html', hotel=hotel)

@app.route('/confirmation/<int:booking_id>')
def confirmation(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return render_template('confirmation.html', booking=booking)


# Add Hotel
@app.route('/hotels/add', methods=['GET', 'POST'])
def add_hotel():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        price = float(request.form['price'])

        new_hotel = Hotel(name=name, location=location, price=price)
        db.session.add(new_hotel)
        db.session.commit()

        return redirect(url_for('view_hotels'))

    return render_template('add_hotel.html')

# Edit Hotel
@app.route('/hotels/<int:hotel_id>/edit', methods=['GET', 'POST'])
def edit_hotel(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)

    if request.method == 'POST':
        hotel.name = request.form['name']
        hotel.location = request.form['location']
        hotel.price = float(request.form['price'])
        
        db.session.commit()
        return redirect(url_for('view_hotels'))

    return render_template('edit_hotel.html', hotel=hotel)

# Delete Hotel
@app.route('/hotels/<int:hotel_id>/delete', methods=['POST'])
def delete_hotel(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    db.session.delete(hotel)
    db.session.commit()
    return redirect(url_for('view_hotels'))

if __name__ == "__main__":
    app.run(debug=True)
