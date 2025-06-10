from flask import Flask, json,render_template, request, redirect, jsonify,url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/courses')
def courses():
    courses = [
        {
            'title': 'WEB DESIGNING',
            'duration': '3 Months',
            'level': 'Beginner',
            'fee': 4500,
            'description': 'Master HTML, CSS, and JavaScript to create beautiful responsive websites.',
            'image_url': '/static/images/web_design.jpg',
            'slug': 'web-designing'
        },
        {
            'title': 'TALLY',
            'duration': '2 Months',
            'level': 'Intermediate',
            'fee': 4000,
            'description': 'Learn accounting fundamentals and Tally ERP software for business use.',
            'image_url': '/static/images/tally.jpg',
            'slug': 'tally'
        },
        {
            'title': 'HARDWARE COURSE',
            'duration': '4 Months',
            'level': 'Beginner',
            'fee': 5500,
            'description': 'Understand computer hardware components, maintenance, and troubleshooting.',
            'image_url': '/static/images/hardware.jpg',
            'slug': 'hardware-course'
        },
        {
            'title': 'DTP',
            'duration': '2.5 Months',
            'level': 'Beginner',
            'fee': 3500,
            'description': 'Design brochures, flyers, and publications using CorelDRAW and Photoshop.',
            'image_url': '/static/images/dtp.jpeg',
            'slug': 'dtp'
        },
        {
            'title': 'PHP',
            'duration': '3 Months',
            'level': 'Intermediate',
            'fee': 5000,
            'description': 'Develop dynamic websites and backend logic using PHP and MySQL.',
            'image_url': '/static/images/php.jpg',
            'slug': 'php'
        },
        {
            'title': 'Dot Net',
            'duration': '3.5 Months',
            'level': 'Advanced',
            'fee': 6000,
            'description': 'Build secure enterprise applications using the .NET framework and C#.',
            'image_url': '/static/images/dotnet.jpeg',
            'slug': 'dotnet'
        },
        {
            'title': 'PYTHON PROGRAMMING',
            'duration': '2.5 Months',
            'level': 'Beginner to Intermediate',
            'fee': 4800,
            'description': 'Learn Python programming for web development, automation, and data analysis.',
            'image_url': '/static/images/python.jpg',
            'slug': 'python-programming'
        },
        {
            'title': 'JAVA PROGRAMMING',
            'duration': '3 Months',
            'level': 'Intermediate',
            'fee': 5000,
            'description': 'Understand object-oriented programming and build cross-platform applications using Java.',
            'image_url': '/static/images/java.png',
            'slug': 'java-programming'
        },
        {
            'title': 'C PROGRAMMING',
            'duration': '1.5 Months',
            'level': 'Beginner',
            'fee': 3000,
            'description': 'Master the fundamentals of procedural programming with hands-on C language projects.',
            'image_url': '/static/images/c.jpeg',
            'slug': 'c-programming'
        },
        {
            'title': 'C++ PROGRAMMING',
            'duration': '2 Months',
            'level': 'Beginner to Intermediate',
            'fee': 3500,
            'description': 'Enhance your programming logic and object-oriented skills using C++ language.',
            'image_url': '/static/images/cpp.jpg',
            'slug': 'cpp-programming'
        },
        {
            'title': 'JAVASCRIPT',
            'duration': '4 months',
            'level': 'Beginner to Intermediate',
            'fee': 5000,
            'description': 'Enhance your programming logic and object-oriented skills using C++ language.',
            'image_url': '/static/images/javascript.jpg',
            'slug': 'cpp-programming'
        },
    ]
    return render_template('courses.html', courses=courses)

# Optional: Enrollment route (placeholder)
@app.route('/enroll/<slug>')
def enroll(slug):
    return f"You are trying to enroll in: {slug.replace('-', ' ').title()}"


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
@app.route('/review')
def review():
    return render_template('review.html')














if __name__ == '__main__':
    app.run(debug=True)
