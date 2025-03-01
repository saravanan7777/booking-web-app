from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from models.models import Booking, Hotel, db
from datetime import datetime

bookings = Blueprint('bookings', __name__)

@bookings.route('/my-bookings')
@login_required
def my_bookings():
    if current_user.role == "admin":
        return render_template('index.html')
    user_bookings = current_user.bookings  # This gets all bookings for the logged-in user
    return render_template('confirmation.html', bookings=user_bookings)


@bookings.route('/<int:hotel_id>/book', methods=['GET', 'POST'])
@login_required
def book_hotel(hotel_id):
    if current_user.role == "admin":
        return render_template('index.html')
    hotel = Hotel.query.get_or_404(hotel_id)

    if request.method == 'POST':
        checkin = datetime.strptime(request.form['checkin'], '%Y-%m-%d').date()
        checkout = datetime.strptime(request.form['checkout'], '%Y-%m-%d').date()

        new_booking = Booking(name=current_user.username, email=current_user.email,
                              checkin=checkin, checkout=checkout, hotel_id=hotel.id, user_id=current_user.id)
        db.session.add(new_booking)
        db.session.commit()
        return redirect(url_for('bookings.my_bookings', booking_id=new_booking.id))

    return render_template('booking_form.html', hotel=hotel)

@bookings.route('/confirmation/<int:booking_id>')
@login_required
def confirmation(booking_id):
    if current_user.role == "admin":
        return render_template('index.html')
    booking = Booking.query.get_or_404(booking_id)
    return render_template('confirmation.html', booking=booking)
