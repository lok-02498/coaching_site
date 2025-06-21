from flask_bcrypt import Bcrypt
from colorama import Cursor
from flask import Flask, request, redirect, flash, render_template, session, url_for, make_response, send_file
from flask_mail import Mail, Message
from psutil import users
from xhtml2pdf import pisa
from werkzeug.utils import secure_filename
import os
import io
import mysql.connector
import random


app = Flask(__name__)
app.secret_key = 'your_secret_key'
bcrypt = Bcrypt(app)  # Use a strong secret key

# ---------- Flask-Mail Configuration ----------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'support4ois@gmail.com'
app.config['MAIL_PASSWORD'] = 'scnt dczi vwxb nxrb'
app.config['MAIL_DEFAULT_SENDER'] = 'support4ois@gmail.com'

mail = Mail(app)

# ---------- MySQL Connection ----------
def get_db_connection():
    return mysql.connector.connect(
        host='p3plzcpnl509598.prod.phx3.secureserver.net',        # e.g., mysql123.secureserver.net
        user='flaskuser',        # e.g., ois_user
        password='KRIshna2005',# your db user password
        database='ois',    # e.g., ois
        port=3306
    )



# ---------- Routes ----------
@app.route('/')
def cover():
    return render_template('cover.html')

@app.route('/index')
@app.route('/home')
def index():
    return render_template('index.html')



@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/courses')
def show_courses():
    print("SESSION USERNAME:", session.get('username'))  # Debug

    if 'username' not in session:
        flash("Please log in to view courses", "error")
        return redirect(url_for('cover'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('courses.html', courses=courses)


@app.route('/enroll/<slug>')
def enroll_course(slug):
    return f"You are trying to enroll in: {slug.replace('-', ' ').title()}"
@app.route('/admission/<slug>')
def admission_slug(slug):
    return render_template('admission_form.html', course_slug=slug)

@app.route('/admission_form')
def admission_form_page():
    return render_template('admission_form.html')

@app.route('/submit', methods=['POST'])
def submit_admission():
    data = request.form.to_dict()
    data['qual'] = request.form.getlist('qual')

    photo = request.files.get('photo')
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

    html = render_template('admission_pdf_template.html', data=data)
    pdf = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.StringIO(html), dest=pdf)
    pdf.seek(0)

    if pisa_status.err:
        flash('Error generating PDF.', 'danger')
        return redirect(url_for('show_courses'))  # Make sure this function exists

    msg = Message(subject='New Admission Form Submitted', recipients=['support4ois@gmail.com'])
    msg.body = f"New admission form submitted by {data.get('student_name')}.\nPlease find the attached PDF."
    msg.attach("admission_form.pdf", "application/pdf", pdf.read())

    try:
        mail.send(msg)
        flash('Admission form submitted successfully. PDF emailed to admin.', 'success')
    except Exception as e:
        print(f"Email sending error: {e}")
        flash('Form submitted but email failed.', 'danger')

    return redirect(url_for('show_courses'))  # ✅ Redirect to courses page


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
            recipients=['support4ois@gmail.com']
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


from flask import flash, redirect, url_for, session, render_template

@app.route('/review')
def review_page():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT name, course, rating, review, created_at FROM feedbacks ORDER BY created_at DESC")
    feedbacks = cursor.fetchall()

    for fb in feedbacks:
        fb['raw_created_at'] = fb['created_at'].isoformat()  # For JS libraries like timeago
        fb['created_at'] = fb['created_at'].strftime('%d %b %Y %I:%M %p')  # Readable format

    cursor.close()
    conn.close()
    return render_template('review.html', feedbacks=feedbacks)



@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    name = request.form['name']
    course = request.form['course']
    rating = request.form['rating']
    review = request.form['review']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO feedbacks (name, course, rating, review) VALUES (%s, %s, %s, %s)",
        (name, course, rating, review)
    )
    conn.commit()
    cursor.close()
    conn.close()
    flash('Thank you for your feedback!', 'success')
    return redirect('/review')
@app.route('/dashboard')
def dashboard():
    if 'username' not in session or session.get('role') != 'admin':
        flash("Access denied. Admins only.", "error")
        return redirect(url_for('cover'))
    return render_template('admin_dashboard.html')

@app.route('/login/student', methods=['POST'])
def login_student():
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s AND role = 'student'", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and bcrypt.check_password_hash(user['password'], password):
        session['username'] = user['username']
        session['role'] = user['role']
        flash('Student login successful', 'success')
        return redirect(url_for('cover'))
    else:
        flash('Invalid student credentials', 'error')
        return redirect(url_for('cover'))

@app.route('/login/admin', methods=['POST'])
def login_admin():
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s AND role = 'admin'", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and bcrypt.check_password_hash(user['password'], password):
        session['username'] = user['username']
        session['role'] = user['role']
        flash('Admin login successful', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid admin credentials', 'error')
        return redirect(url_for('cover'))


@app.route('/signup/student', methods=['POST'])
def signup_student():
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        flash('Username already exists', 'error')
        cursor.close()
        conn.close()
        return redirect(url_for('cover'))

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, 'student')",
                   (username, hashed_password))
    conn.commit()
    cursor.close()
    conn.close()

    session['username'] = username
    session['role'] = 'student'
    flash('Signup successful as student', 'success')
    return redirect(url_for('cover'))





@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('cover'))

@app.route('/send-email-otp', methods=['POST'])
def send_email_otp():
    email = request.form['email']
    otp = str(random.randint(100000, 999999))
    session['email_otp'] = otp
    session['otp_email'] = email

    # Send OTP to email
    msg = Message(subject='Your OTP for Login', recipients=[email])
    msg.body = f'Your OTP is: {otp}'
    mail.send(msg)

    flash('OTP sent to your email!', 'success')
    return redirect(url_for('cover', show='emailLogin'))

@app.route('/verify-email-otp', methods=['POST'])
def verify_email_otp():
    entered_otp = request.form['otp']
    if entered_otp == session.get('email_otp'):
        session['username'] = session['otp_email']
        session['role'] = 'student'  
        flash('Logged in successfully via OTP!', 'success')
        return redirect(url_for('cover'))
    else:
        flash('Invalid OTP.', 'error')
        return redirect(url_for('cover', show='emailLogin'))  # Keep modal open

@app.route('/verify-email-otp')
def verify_email_otp_page():
    return redirect(url_for('cover'))






# ---------- Run ----------


if __name__ == '__main__':
    app.run(debug=True)
