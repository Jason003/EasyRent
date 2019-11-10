from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateField, SelectField
from wtforms.validators import DataRequired
from flask_admin.form.widgets import DatePickerWidget


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')


class InquireForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')


class LeaseForm(FlaskForm):
    start_date = DateField('Start Date', validators=[DataRequired()], format='%Y/%m/%d', widget=DatePickerWidget())
    end_date = DateField('End Date', validators=[DataRequired()], format='%Y/%m/%d', widget=DatePickerWidget())
    submit = SubmitField('Sign')


class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Comment')


class StudentVerifyForm(FlaskForm):
    university = StringField('University', validators=[DataRequired()])
    student_id = StringField('Student ID', validators=[DataRequired()])
    submit = SubmitField('Verify')

class FilterForm(FlaskForm):
    key_word = StringField('Key Word & Location')
    price = StringField('Less than')
    bedrooms = StringField('Bedrooms')
    bathrooms = StringField('Bathrooms')
    submit = SubmitField('Search')

