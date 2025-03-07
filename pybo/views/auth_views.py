from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from .. import db
from ..forms import UserCreateForm, UserLoginForm
from ..models import User
import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    # 폼을 제출하는 경우
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if not user:
            # generate_password_hash 함수로 암호화한 데이터는 복호화할 수 없음
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            # 필드 자체 오류가 아닌, 프로그램 논리 오류를 발생시키는 함수
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    # post 요청 - 로그인을 수행한다
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()

        if not user:
            error = "존재하지 않는 사용자입니다."
        # 비밀번호는 반드시 암호화한 후 비교해야 한다
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.id
            _next = request.args.get('next', '')
            if _next:
                # 로그인 후 해당 페이지로 이동
                return redirect(_next)
            else:
                # 메인 페이지로 이동
                return redirect(url_for('main.index'))
            return redirect(url_for('main.index'))
        flash(error)
    # get 요청 - 로그인 화면을 보여준다
    return render_template("auth/login.html", form=form)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

# 라우팅 함수보다 항상 먼저 실행
# g: 플라스크의 컨텍스트 변수. (요청 -> 응답) 과정에서 유효.
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

# 데코레이터 함수는 기존 함수를 감싸서 만들 수 있음
def login_required(view):
    @functools.wraps(view) # 원래 함수의 정보를 유지할 수 있음
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            # 요청방식이 GET인 경우 로그인 후 원래 페이지로 다시 갈 수 있게 _next
            _next = request.url if request.method == "GET" else ""
            return redirect(url_for('auth.login', next=_next))
        return view(*args, **kwargs)
    return wrapped_view