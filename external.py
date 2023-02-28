from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = 'krcusz26wrh'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'data'
SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
