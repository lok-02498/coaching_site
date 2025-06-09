from flask import Flask, json,render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/courses')
def courses():
    return render_template('courses.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # You can store data or send email here
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        print(f"Message from {name} ({email}): {message}")
        return redirect('/')
    return render_template('contact.html')
from flask import request, redirect

@app.route("/submit-contact", methods=["POST"])
def submit_contact():
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    message = request.form["message"]
    
    # You can save to database or send an email here
    print(f"New message from {name} ({email}, {phone}): {message}")
    
    return redirect("/")  # Or show a thank you page





if __name__ == '__main__':
    app.run(debug=True)
