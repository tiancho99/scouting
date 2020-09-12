class Config:
    SECRET_KEY = 'SUPER_SECRETO'
    TEMPLATE_FOLDER = 'templates'
    STATIC_FOLDER = './static'
    SQLALCHEMY_DATABASE_URI = 'mysql://sebastian:supertiancho99@localhost/scouting'
    UPLOAD_FOLDER = './static/uploads'
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLAlCHEMY_ECHO = True