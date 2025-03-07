from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect
from .. import db
from ..models import Question, Answer
from ..forms import AnswerForm
from .auth_views import login_required
from datetime import datetime

# 'main': 블루프린트의 별칭
# __name__: 모듈명 "question_views"
# url_prefix: 접두어 URL
bp = Blueprint('answer', __name__, url_prefix='/answer')

# /create/2 페이지를 요청받으면 question_id에는 2가 넘어옴
# POST 방식: form의 엘리먼트가 POST 방식이므로 같은 값
@bp.route('/create/<int:question_id>', methods=('POST',))
@login_required
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)

    if form.validate_on_submit():
        # POST 폼방식으로 전송된 데이터의 항목 중 name 속성이 content인 값
        content = request.form['content']
        answer = Answer(question = question, content=content, create_date=datetime.now(), user=g.user)
        db.session.add(answer)
        # question.answer_set.append(answer) - backref 사용 시
        db.session.commit()
        return redirect('{}#answer_{}'.format(url_for('question.detail', question_id=question_id), answer.id))
    return render_template('question/question_detail.html', question=question, form=form)

@bp.route('/modify/<int:answer_id>', methods=('GET', 'POST'))
@login_required
def modify(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if g.user != answer.user:
        flash('수정권한이 없습니다.')
        return redirect(url_for('question.detail', question_id=answer.question.id))
    if request.method == "POST":
        # 브라우저에서 전송한 폼 데이터를 AnswerForm 객체로 매핑 (request.form)
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer)
            answer.modify_date = datetime.now()
            db.session.commit()
            return redirect('{}#answer_{}'.format(url_for('question.detail', question_id=question_id), answer.id))
    else:
        form = AnswerForm(obj=answer)
    return render_template('answer/answer_form.html', form=form)

@bp.route('/delete/<int:answer_id>')
@login_required
def delete(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    question_id = answer.question.id
    if g.user != answer.user:
        flash('삭제권한이 없습니다.')
    else:
        db.session.delete(answer)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))

@bp.route('/vote/<int:answer_id>')
@login_required
def vote(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if g.user == answer.user:
        flash("본인이 작성한 댓글은 추천할 수 없습니다.")
    elif g.user in answer.voter:
        flash("이미 추천한 댓글을 다시 추천할 수 없습니다.")
    else:
        answer.voter.append(g.user)
        db.session.commit()
    return redirect('{}#answer_{}'.format(url_for('question.detail', question_id=question_id), answer.id))