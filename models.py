from external import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))


class BaseTable(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)


class UserTable(BaseTable):
    __tablename__ = "default_table"
    name = db.Column(db.String(50))
    data = db.Column(db.JSON)


def create_user_table(username):
    class UserHistoryTable(BaseTable):
        __tablename__ = username
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        name = db.Column(db.String(50))
        artist = db.Column(db.String(50))
        duration = db.Column(db.String(50))
        album = db.Column(db.String(50))
        fav = db.Column(db.String(50))
        rid = db.Column(db.String(50))
        download_id = db.Column(db.String(50))

    db.create_all()
    return UserHistoryTable
