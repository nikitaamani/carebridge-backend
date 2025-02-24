# Home page
@app.route('/')
def home():
    return render_template('index.html', user=current_user)