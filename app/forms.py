from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, EmailField, PasswordField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange, Email

class signup_form(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(2,16,'username must be between 2 <-> 16')])
    age = IntegerField('age', validators=[DataRequired(), NumberRange(10,90)])
    pos = SelectField('position',choices=[('student','Student'),('teacher','Teacher')], validators=[DataRequired()])
    user_email = EmailField('email', validators=[DataRequired(), Email()])
    phone = IntegerField('phone number', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    conf_password = PasswordField('confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign-up')

class login_form(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Login')

class post_form(FlaskForm):
    category = SelectField('category', choices=[('علمي'),('فني'),('ثقافي'),('رياضي'),('اجتماعي')], validators=[DataRequired()])
    title = StringField('title', validators=[DataRequired(), Length(10,100)])
    content = TextAreaField('Content',
        validators=[DataRequired()],
        render_kw={
            "class": "form-control",
            "rows": 10,
            "style": "background-color:#0A3D62; color:white; min-height:200px;"
        }
    )