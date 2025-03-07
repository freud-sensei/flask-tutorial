from flask import Blueprint, url_for
from werkzeug.utils import redirect

# 'main': 블루프린트의 별칭
# __name__: 모듈명 "main_views"
# url_prefix: 접두어 URL
bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/hello')
def hello_pybo():
    return "Hello, Pybo!"

@bp.route('/')
def index():
    # redirect(URL): URL로 페이지를 redirect
    # url_for(라우팅 함수명): 라우팅 함수에 매핑된 URL을 리턴. 즉 '/list'
    return redirect(url_for('question._list'))