from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField
from wtforms.validators import InputRequired, Email, Length


class RegisterForm(FlaskForm):
    firstname = StringField('First Name', validators=[InputRequired('Please enter first name')])
    lastname = StringField('Last Name', validators=[InputRequired('Please enter second name')])
    username = StringField('Username', validators=[InputRequired('Please enter a username'),Length(min=4,message='Username - Minimum Characters: 4')])
    dob = StringField('DOB')
    country = StringField('Country')
    email = StringField('Email',validators=[InputRequired('Please enter an email ID'), Email('Please enter a valid email ID')])
    password = PasswordField('Password', validators=[InputRequired('Please enter a password'),Length(min=6, message='Password - Minimum Characters: 6')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired('Please enter email ID'), Email('Please enter a valid email ID')])
    password = PasswordField('Password', validators=[InputRequired('Please enter the password')])
    submit = SubmitField('Login')

class BookReco(FlaskForm):
	book = StringField(validators=[InputRequired('Please enter book name')])
