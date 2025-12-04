from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, EmailField, PasswordField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange, Email

class signup_form(FlaskForm):
    username = StringField('اسم المستخدم', validators=[DataRequired(), Length(2,16,'الاسم يجب ان يتكون من حرفين الى 16 حرف')])
    age = IntegerField('السن', validators=[DataRequired(), NumberRange(10,90)])
    pos = SelectField('المنصب',choices=[('طالب','طالبة'),('معلم','معلمة')], validators=[DataRequired()])
    user_email = EmailField('البريد الالكتروني', validators=[DataRequired(), Email()])
    phone = IntegerField('رقم الهاتف', validators=[DataRequired()])
    password = PasswordField('كلمة السر', validators=[DataRequired()])
    conf_password = PasswordField('تأكيد كلمة السر', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('انشئ الحساب')

class login_form(FlaskForm):
    username = StringField('الاسم', validators=[DataRequired()])
    password = PasswordField('كلمة السر', validators=[DataRequired()])
    submit = SubmitField('تسجيل الدخول')

class post_form(FlaskForm):
    category = SelectField('التصنيف', choices=[('علمي'),('فني'),('ثقافي'),('رياضي'),('اجتماعي')], validators=[DataRequired()])
    title = StringField('العنوان', validators=[DataRequired(), Length(10,100)])
    content = TextAreaField('المحتوى',
        validators=[DataRequired()],
        render_kw={
            "class": "form-control",
            "rows": 10,
            "style": "background-color:#0A3D62; color:white; min-height:200px;"
        }
    )

class activity_form(FlaskForm):
    name = StringField('عنوان النشاط', validators=[Length(2,50),DataRequired('يجب وضع عنوان')])
    describtion = StringField('محتوى النشاط',
        validators=[Length(2,100),DataRequired('يجب وضع محتوى')],
        render_kw={
            "class": "form-control",
            "rows": 10,
            "style": "background-color:#0A3D62; color:white;"
        }
    )
    category = SelectField('تصنيف النشاط', choices=('علمي','ثقافي','فني','رياضي','اجتماعي','بيئي','تكنولوجي','اخلاقي','معسكر','ورشة عمل'),validators=[DataRequired('يجب اختيار تصنيف')])