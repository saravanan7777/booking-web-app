from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from models.models import Hotel, db
from flask import current_app
from werkzeug.utils import secure_filename
import os
from flask import abort
hotels = Blueprint('hotels', __name__)

# View hotels (Everyone can see)
@hotels.route('/')
def view_hotels():
    if current_user.role == "admin":
        return render_template('index.html')
    hotels = Hotel.query.all()
    return render_template('hotels.html', hotels=hotels)

# Admin-only page for managing hotels
@hotels.route('/manage')
@login_required
def manage_hotels():
    if current_user.role != "admin":
        abort(404) # Return error if not admin

    hotels = Hotel.query.all()
    return render_template('manage_hotels.html', hotels=hotels)

@hotels.route('/hotel_details')
def vhotels():
    if current_user.role == "admin":
        return render_template('index.html') 
    hotels=Hotel.query.all()
    return render_template('hotel_detail.html',hotels=hotels)
# Add Hotel (Admin only)
@hotels.route('/add', methods=['GET', 'POST'])
@login_required
def add_hotel():
    if current_user.role != "admin":
        abort(404)

    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        price = float(request.form['price'])
        
        # ✅ Handle image upload
        image_file = request.files['image']
        if image_file:
            filename = secure_filename(image_file.filename)  # Sanitize filename
            image_path = os.path.join(current_app.root_path, 'static/images', filename)
            image_file.save(image_path)  # Save the image file

        # ✅ Store the image filename (not full path) in the database
        new_hotel = Hotel(name=name, location=location, price=price, image=filename)
        db.session.add(new_hotel)
        db.session.commit()
        return redirect(url_for('hotels.manage_hotels'))

    return render_template('add_hotel.html')

@hotels.route('/<int:hotel_id>')
def hotel_detail(hotel_id):
    if current_user.role == "admin":
        return render_template('index.html')
    hotel=Hotel.query.get(hotel_id)
    return render_template('hotel_detail.html', hotel=hotel)

# Edit Hotel (Admin only)
@hotels.route('/<int:hotel_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_hotel(hotel_id):
    if current_user.role != "admin":
        return "Unauthorized Access", 403  

    hotel = Hotel.query.get_or_404(hotel_id)

    if request.method == 'POST':
        hotel.name = request.form['name']
        hotel.location = request.form['location']
        hotel.price = float(request.form['price'])

        db.session.commit()
        return redirect(url_for('hotels.manage_hotels'))

    return render_template('edit_hotel.html', hotel=hotel)
