from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_required, logout_user, current_user
from model import db, Donation  # Import your Donation model

app = Flask(__name__)

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('home'))

# View the logged-in user’s donations
@app.route('/mydonations')
@login_required
def mydonations():
    donations = Donation.query.filter_by(user_id=current_user.id).all()
    return render_template('mydonations.html', donations=donations, user=current_user)

# Add a new donation
@app.route('/adddonation', methods=['GET', 'POST'])
@login_required
def adddonation():
    if request.method == 'POST':
        amount = request.form.get('amount')
        charity_name = request.form.get('charity_name')
        
        # Debug: Print the current user's ID
        print(f"Current User ID: {current_user.id}")
        
        if not amount or not charity_name:
            flash('Donation amount and charity name are required.', 'error')
            return redirect(url_for('adddonation'))
        
        try:
            new_donation = Donation(amount=amount, charity_name=charity_name, user_id=current_user.id)
            db.session.add(new_donation)
            db.session.commit()
            flash('Donation added successfully!', 'success')
            return redirect(url_for('mydonations'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'error')
            return redirect(url_for('adddonation'))
    
    return render_template('adddonation.html', user=current_user)
