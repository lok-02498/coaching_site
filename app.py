from flask import Flask, request, redirect, flash, render_template, session, url_for,jsp
from flask_mail import Mail, Message
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
from flask import render_template, request, make_response
from xhtml2pdf import pisa
import io
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Use a strong secret key

# ---------- Flask-Mail Configuration ----------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'support4ois@gmail.com'  # Your email
app.config['MAIL_PASSWORD'] = 'scnt dczi vwxb nxrb'     # App Password (not your Gmail login)
app.config['MAIL_DEFAULT_SENDER'] = 'support4ois@gmail.com'

mail = Mail(app)

# ---------- MySQL Configuration ----------
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'loki2002'
app.config['MYSQL_DB'] = 'company'

mysql = MySQL(app)

# ---------- Routes ----------
@app.route('/')
def cover():
    return render_template('cover.html')

@app.route('/home')
def home():
    return render_template('index.html')  # or index.html or whatever your homepage is

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
            'description': 'Learn core JavaScript concepts and build dynamic web applications.',
            'image_url': '/static/images/javascript.jpg',
            'slug': 'javascript'
        },
    ]
    return render_template('courses.html', courses=courses)

@app.route('/enroll/<slug>')
def enroll(slug):
    return f"You are trying to enroll in: {slug.replace('-', ' ').title()}"

@app.route('/admission_form')
def admission_form():
    return render_template('admission_form.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    name = request.form['name']
    email = request.form['email']
    phone = request.form.get('phone', '')
    message = request.form['message']

    try:
        # Email to admin
        msg_to_admin = Message(
            subject=f'New Contact Form Submission from {name}',
            recipients=['support4ois@gmail.com']  # Change to your actual admin email
        )
        msg_to_admin.body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
        mail.send(msg_to_admin)

        # Auto-reply to user
        msg_to_user = Message(
            subject='Thank you for contacting OM Info Solutions',
            recipients=[email]
        )
        msg_to_user.body = f"Hi {name},\n\nThank you for reaching out to us. We’ve received your message:\n\n\"{message}\"\n\nWe’ll get back to you soon.\n\nBest regards,\nOM Info Solutions"
        mail.send(msg_to_user)

        flash('Your message has been sent successfully!', 'success')
    except Exception as e:
        print(f"Mail error: {e}")
        flash('There was an error sending your message. Please try again later.', 'danger')

    return redirect('/contact')

@app.route('/review')
def review():
    return render_template('review.html')

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'register':
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']

            cur = mysql.connection.cursor()
            try:
                cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
                mysql.connection.commit()
                flash('Registration successful! You can now log in.', 'success')
            except:
                mysql.connection.rollback()
                flash('Email already exists or error occurred.', 'danger')
            finally:
                cur.close()

        elif action == 'login':
            email = request.form['email']
            password = request.form['password']

            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
            user = cur.fetchone()
            cur.close()

            if user:
                session['user_id'] = user[0]
                session['username'] = user[1]
                flash(f"Welcome back, {user[1]}!", 'success')
            else:
                flash("Invalid login credentials.", 'danger')

    return render_template('auth.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", 'info')
    return redirect('/auth')



import os
import io
from flask import request, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename
from xhtml2pdf import pisa
from flask_mail import Message
from flask import send_file

@app.route('/submit', methods=['POST'])
def submit_admission():
    data = request.form.to_dict()
    data['qual'] = request.form.getlist('qual')  # multiple checkboxes

    photo = request.files.get('photo')
    photo_path = None

    if photo and photo.filename != '':
        filename = secure_filename(photo.filename)
        upload_folder = os.path.join('static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        save_path = os.path.join(upload_folder, filename)
        photo.save(save_path)
        abs_path = os.path.abspath(save_path).replace('\\', '/')
        data['photo_path'] = f'file:///{abs_path}'
    else:
        data['photo_path'] = None

    # Render HTML for PDF
    html = render_template('admission_pdf_template.html', data=data)

    # Generate PDF
    pdf = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.StringIO(html), dest=pdf)
    pdf.seek(0)

    if pisa_status.err:
        flash('Error generating PDF.', 'danger')
        return redirect(url_for('courses'))

    # Send email with PDF attachment
    admin_email = 'support4ois@gmail.com'
    msg = Message(subject='New Admission Form Submitted', recipients=[admin_email])
    msg.body = f"New admission form submitted by {data.get('student_name')}.\nPlease find the attached PDF."
    msg.attach("admission_form.pdf", "application/pdf", pdf.read())

    try:
        mail.send(msg)
        flash('Admission form submitted successfully. PDF emailed to admin.', 'success')
    except Exception as e:
        print(f"Email sending error: {e}")
        flash('Form submitted but email failed.', 'danger')

    return redirect(url_for('courses'))







# ---------- Run App ----------
if __name__ == '__main__':
    app.run(debug=True)
