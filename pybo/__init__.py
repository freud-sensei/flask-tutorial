from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData


naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()


# create_app 함수는 애플리케이션 팩토리 역할
def create_app():
    # 플라스크 애플리케이션 생성, __name__에는 모듈명 (여기선 "pybo")
    app = Flask(__name__)
    # 환경 변수 APP_CONFIG_FILE에 정의된 파일을 환경파일로 사용
    app.config.from_envvar('APP_CONFIG_FILE')

    # ORM: app에 db, migrate 객체 등록
    # 전역 변수로 db, migrate를 미리 만들어 두는 이유:
    # 다른 모듈에서도 사용할 수 있게끔
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
    from . import models

    # main_views.py 파일에 생성한 블루프린트 객체 bp
    from .views import main_views, question_views, answer_views, auth_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)

    # 필터
    from .filter import format_datetime, render_markdown
    app.jinja_env.filters['datetime'] = format_datetime
    app.jinja_env.filters['render_markdown'] = render_markdown

    return app