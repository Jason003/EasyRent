from app import app
from flask import render_template, flash, redirect, url_for, g, session
from sqlalchemy import *
from app.forms import *
import uuid
import datetime

DATABASEURI = "postgresql://jl5501:root@34.74.165.156/proj1part2"
engine = create_engine(DATABASEURI)


@app.before_request
def before_request():
    """
    This function is run at the beginning of every web request
    (every time you enter an address in the web browser).
    We use it to setup a database connection that can be used throughout the request.

    The variable g is globally accessible.
    """
    try:
        g.conn = engine.connect()
        print('Connected to database')
    except:
        print("uh oh, problem connecting to database")
        import traceback;
        traceback.print_exc()
        g.conn = None


@app.teardown_request
def teardown_request(exception):
    """
    At the end of the web request, this makes sure to close the database connection.
    If you don't, the database could run out of memory!
    """
    try:
        g.conn.close()
    except Exception as e:
        pass


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = FilterForm()
    SQL = 'SELECT * FROM apartments where 1 = 1 '
    d = {}
    if form.submit():
        key_word = form.key_word.data
        if key_word:
            SQL += ' and (description like :key_word or address like :key_word) '
            d['key_word'] = '%' + key_word + '%'
        lessThan = form.price.data
        if lessThan:
            try:
                lessThan = int(lessThan)
                SQL += ' and price <= :lessThan'
                d['lessThan'] = lessThan
            except:
                flash('Less than should be a number')
        bedrooms = form.bedrooms.data
        if bedrooms:
            try:
                bedrooms = int(bedrooms)
                SQL += ' and bedrooms = :bedrooms'
                d['bedrooms'] = bedrooms
            except:
                flash('Bedrooms should be a number')
        bathrooms = form.bathrooms.data
        if bathrooms:
            try:
                bathrooms = int(bathrooms)
                SQL += ' and bathrooms = :bathrooms'
                d['bathrooms'] = bathrooms
            except:
                flash('Bathrooms should be a number')
    cursor = g.conn.execute(text(SQL), d)
    apartments = cursor.fetchall()
    cursor.close()
    return render_template('index.html', apartments=apartments, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        cursor = g.conn.execute(text('select * from users where username = :username and password = :password'),
                                {'username': form.username.data, 'password': form.password.data})
        user = cursor.fetchall()
        if len(user) == 0:
            flash('Incorrect Username or Password!')
            return render_template('login.html', title='Sign In', form=form)
        flash('Welcome back, {}!'.format(
            form.username.data))
        user = user[0]
        session['user_id'] = user[0]
        session['user_name'] = user[1]
        session['user_email'] = user[2]
        cursor = g.conn.execute(text('select * from students where user_id = :user_id'), {'user_id': user[0]})
        student = cursor.fetchall()
        if student and len(student):
            session['is_student'] = True
        else:
            session['is_student'] = False
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        g.conn.execute(text('''
INSERT INTO users VALUES (:id, :username, :email, :password)
'''), {'id': str(uuid.uuid1()), 'username': form.username.data, 'email': form.email.data,
       'password': form.password.data})
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('user_email', None)
    session.pop('is_student', None)
    return redirect(url_for('index'))


@app.route('/apartment/<apartment_id>')
def apartment(apartment_id):
    cursor = g.conn.execute(text(
        "SELECT * FROM apartments, brokers where apartment_id = :apartment_id and apartments.broker_id = brokers.broker_id"),
        {'apartment_id': apartment_id})
    apartment = cursor.fetchone()
    cursor = g.conn.execute(text(
        "SELECT * FROM comments c, users u where c.apartment_id = :apartment_id and c.user_id = u.user_id order by c.time desc"),
        {'apartment_id': apartment_id})
    comments = cursor.fetchall()
    cursor.close()
    return render_template('apartment.html', apt=apartment, comments=comments)


@app.route('/inquire/<apartment_id>', methods=['GET', 'POST'])
def inquire(apartment_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    form = InquireForm()
    cursor = g.conn.execute(text(
        "SELECT * FROM apartments, brokers where apartment_id = :apartment_id and apartments.broker_id = brokers.broker_id"),
        {'apartment_id': apartment_id})
    apartment = cursor.fetchone()
    if form.validate_on_submit():
        message = form.message.data
        cursor = g.conn.execute(
            text('insert into inquiries values (:inquiry_id, :user_id, :broker_id, :apartment_id, :content, :time)'),
            {'inquiry_id': str(uuid.uuid1()), 'user_id': session['user_id'], 'broker_id': apartment.broker_id,
             'apartment_id': apartment.apartment_id, 'content': message,
             'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
        flash('Message Sent!')
        cursor.close()
        return redirect(url_for('index'))
    cursor.close()
    print(apartment)
    return render_template('inquire.html', apt=apartment, form=form)


@app.route('/lease/<apartment_id>', methods=['GET', 'POST'])
def lease(apartment_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    form = LeaseForm()
    cursor = g.conn.execute(text(
        "SELECT * FROM apartments, brokers where apartment_id = :apartment_id and apartments.broker_id = brokers.broker_id"),
        {'apartment_id': apartment_id})
    apartment = cursor.fetchone()
    if form.validate_on_submit():
        cursor = g.conn.execute(
            text('insert into signedleases values (:lease_id, :user_id, :apartment_id, :start_date, :end_date)'),
            {'lease_id': str(uuid.uuid1()), 'user_id': session['user_id'],
             'apartment_id': apartment.apartment_id, 'start_date': form.start_date.data.strftime("%Y-%m-%d %H:%M"),
             'end_date': form.end_date.data.strftime("%Y-%m-%d %H:%M")})
        flash('Lease Signed!')
        cursor.close()
        return redirect(url_for('index'))
    cursor.close()
    print(apartment)
    return render_template('lease.html', apt=apartment, form=form)


@app.route('/comment/<apartment_id>', methods=['GET', 'POST'])
def comment(apartment_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    form = CommentForm()
    cursor = g.conn.execute(text(
        "SELECT * FROM apartments, brokers where apartment_id = :apartment_id and apartments.broker_id = brokers.broker_id"),
        {'apartment_id': apartment_id})
    apartment = cursor.fetchone()
    if form.validate_on_submit():
        comment = form.comment.data
        cursor = g.conn.execute(
            text('insert into comments values (:comment_id, :user_id, :apartment_id, :content, :time)'),
            {'comment_id': str(uuid.uuid1()), 'user_id': session['user_id'],
             'apartment_id': apartment.apartment_id, 'content': comment,
             'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        flash('Comment Posted!')
        cursor.close()
        return redirect(url_for('apartment', apartment_id=apartment_id))
    cursor.close()
    return render_template('comment.html', apt=apartment, form=form)


@app.route('/dashboard/<user_id>', methods=['GET', 'POST'])
def dashboard(user_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    cursor = g.conn.execute(text(
        "SELECT * FROM inquiries i, apartments a where i.apartment_id = a.apartment_id and i.user_id = :user_id"),
        {'user_id': session['user_id']})
    inquiries = cursor.fetchall()
    cursor = g.conn.execute(text(
        "SELECT * FROM signedleases s, apartments a where s.apartment_id = a.apartment_id and s.user_id = :user_id"),
        {'user_id': session['user_id']})
    leases = cursor.fetchall()
    cursor.close()
    return render_template('dashboard.html', inquiries=inquiries, leases=leases)


@app.route('/student_verify/<user_id>', methods=['GET', 'POST'])
def student_verify(user_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if session['is_student']:
        flash('You have been verified!')
        return redirect(url_for('dashboard', user_id=user_id))
    form = StudentVerifyForm()
    cursor = g.conn.execute(text(
        "SELECT * FROM users where user_id = :user_id"), {'user_id': user_id})
    user = cursor.fetchone()
    if form.validate_on_submit():
        cursor = g.conn.execute(
            text('select * from students where university = :university and student_id = :student_id'),
            {'university': form.university.data, 'student_id': form.student_id.data})
        currentStudent = cursor.fetchall()
        if currentStudent and len(currentStudent):
            flash('This Student Has been Verified!')
            return redirect(url_for('student_verify', user_id=user_id))
        cursor = g.conn.execute(
            text('insert into students values (:user_id, :university, :student_id)'),
            {'user_id': session['user_id'],
             'university': form.university.data, 'student_id': form.student_id.data})
        flash('Successfully Verified!')
        session['is_student'] = True
        cursor.close()
        return redirect(url_for('dashboard', user_id=user_id))
    cursor.close()
    return render_template('student_verify.html', form=form, user=user)
