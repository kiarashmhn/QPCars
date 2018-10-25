from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError, NumberRange
from QPcars.models import User


class LoginForm(Form):
    username = StringField('', validators=[DataRequired()])
    password = PasswordField('', validators=[DataRequired()])
    remember = BooleanField('Keep me logged in')
    submit = SubmitField('Submit')


class UserSignupForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    surName = StringField('SurName', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    identificationId = IntegerField('IdentId', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired(), Length(1, 200)])
    gender = SelectField(u'Gender', choices=[('Female', 'زن'), ('Male', 'مرد')])
    username = StringField('Username',
                           validators=[
                               DataRequired(), Length(3, 80),
                               Regexp('^[A-Za-z0-9_]{3,}$',
                                      message='Usernames consist of numbers, letters,'
                                              'and underscores.')])
    password = PasswordField('Password',
                             validators=[
                                 DataRequired(),
                                 EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Length(1, 120), Email()])

    # submit = SubmitField('Submit')

    def validate_email(self, email_field):
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError('There already is a user with this email address.')

    def validate_username(self, username_field):
        if User.query.filter_by(username=username_field.data).first():
            raise ValidationError('This username is already taken.')