from datetime import datetime
from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect

from .. import db
from ..models import Question, Answer, User
from ..forms import QuestionForm, AnswerForm
from .auth_views import login_required

# 'main': 블루프린트의 별칭
# __name__: 모듈명 "question_views"
# url_prefix: 접두어 URL
bp = Blueprint('question', __name__, url_prefix='/question')

@bp.route('/list')
def _list():
    # GET 방식으로 요청한 URL에서 page, kw를 가져올 때 (/question/list/?page=5)
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    # 질문 목록 데이터를 작성일시 기준 역순으로 정렬
    question_list = Question.query.order_by(Question.create_date.desc())

    # 검색 구현
    if kw:
        search = f"%%{kw}%%"
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username)\
            .join(User, Answer.user_id == User.id).subquery()
        question_list = question_list \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.question_id == Question.id) \
            .filter(Question.subject.ilike(search) | # 질문 제목
                    Question.content.ilike(search) | # 질문 내용
                    User.username.ilike(search) | # 질문 작성자
                    sub_query.c.content.ilike(search) | # 답변 내용
                    sub_query.c.username.ilike(search) # 답변 작성자
                    ) \
            .distinct()
        question_list = question_list.paginate(page=page, per_page=10)
        return render_template('question/question_list.html',
                               question_list=question_list, page=page, kw=kw)


    # page: 현재 조회할 페이지 번호, per_page: 페이지마다 10건
    question_list = question_list.paginate(page=page, per_page=10)
    # 템플릿 파일(파이썬 문법을 사용할 수 있는 HTML 파일)을 화면으로 렌더링
    return render_template('question/question_list.html', question_list=question_list, page=page)

# detail/2 페이지를 요청하면, detail 함수가 실행되며, question_id에는 2가 전달됨
@bp.route('/detail/<int:question_id>')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question, form=form)

@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
    form = QuestionForm()
    # create 함수로 요청된 전송방식 / 전송된 폼 데이터 점검(required 등)
    if request.method == "POST" and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now(), user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    # 이땐 GET 방식
    return render_template('/question/question_form.html', form=form)

@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        # 강제로 오류 발생
        flash("수정권한이 없습니다")
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method == 'POST': # POST 방식: 데이터 수정 뒤 저장 후
        form = QuestionForm()
        if form.validate_on_submit(): # QuestionForm을 검증하고 데이터 저장
            form.populate_obj(question) # form 변수의 데이터를 question 객체에 업데이트
            question.modify_date = datetime.now()
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else: # GET 방식: 질문수정 버튼을 눌렀을 때
        form = QuestionForm(obj=question)
        # 조회한 데이터를 obj 매개변수에 저장
    return render_template('question/question_form.html', form=form)

@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash("삭제권한이 없습니다")
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))

@bp.route('/vote/<int:question_id>')
@login_required
def vote(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user == question.user:
        flash('본인이 작성한 글은 추천할 수 없습니다')
    elif g.user in question.voter:
        flash('이미 추천한 글을 다시 추천할 수 없습니다')
    else:
        # 동일한 사용자가 중복되지 않도록 내부 처리됨
        question.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))