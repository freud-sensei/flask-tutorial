from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class QuestionForm(FlaskForm):
    # 필수 항목인지 체크 가능 (validators)
    subject = StringField('제목', validators=[DataRequired('제목을 입력해주세요.')])
    content = TextAreaField('내용', validators=[DataRequired('내용을 입력해주세요.')])

class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용을 입력해주세요.')])

class UserCreateForm(FlaskForm):
    username = StringField('사용자 이름', validators=[DataRequired('이름을 입력해주세요.'), Length(min=3, max=25, message='사용자 이름의 길이는 3자-25자 사이여야 합니다.')])
    password1 = PasswordField('비밀번호', validators=[DataRequired("이메일을 입력해주세요."), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호 확인', validators=[DataRequired("이메일을 입력해주세요.")])
    email = EmailField('이메일', validators=[DataRequired("이메일을 입력해주세요."), Email()])

class UserLoginForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired("이름을 입력해주세요."), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired("비밀번호를 입력해주세요.")])


