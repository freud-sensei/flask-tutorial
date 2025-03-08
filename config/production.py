from config.default import *

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b'\x9e\x92\x12\xa7\xcf1q\xf8i{\x1e\xc35\xa2\x95\xb9'
