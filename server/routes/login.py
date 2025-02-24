
# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.', 'error')
            return redirect(url_for('login'))

        login_user(user)
        flash('Logged in successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('login.html', user=current_user)