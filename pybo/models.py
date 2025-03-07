from pybo import db

# 테이블 객체 - N:N 관계 - 사용자 id와 질문 id 쌍
question_voter = db.Table(
    'question_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), primary_key=True)
)

answer_voter = db.Table(
    'answer_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), primary_key=True)
)

class Question(db.Model):
    # 기본 키: 데이터베이스에서 중복값을 가질 수 없음.
    # 또한 값이 자동으로 증가됨 (1, 2, 3...)
    id = db.Column(db.Integer, primary_key=True)
    # nullable: 빈값을 허용할지?
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    modify_date = db.Column(db.DateTime(), nullable=True)

    # User 모델과 Question 모델을 연결하기 위한 속성
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    # Question 모델에서 User 모델을 참조하기 위한 속성
    user = db.relationship('User', backref=db.backref('question_set'))
    # secondary 값으로 question_voter 테이블 객체 지정
    # 실제 데이터는 question_voter 테이블에 저장, 저장된 정보는 voter 속성을 통해 참조 가능
    voter = db.relationship('User', secondary=question_voter, backref=db.backref('question_voter_set'))


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # 답변을 질문과 연결
    # 외부 키: 기존 모델과 연결된 속성 (question 테이블의 id 컬럼)
    # ondelete='CASCADE': 질문을 삭제하면 해당 질문에 달린 답변도 삭제
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))

    # 답변 모델에서 질문 모델을 참조하기 위함 (answer.question.subject와 같이)
    # (참조할 모델명, 역참조 설정)
    question = db.relationship('Question', backref=db.backref('answer_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    modify_date = db.Column(db.DateTime(), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('answer_set'))
    voter = db.relationship('User', secondary=answer_voter, backref=db.backref('answer_voter_set'))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # unique=True: 같은 값을 저장할 수 없다
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    # unique=True: 같은 값을 저장할 수 없다
    email = db.Column(db.String(120), unique=True, nullable=False)

