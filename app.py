import datetime
from functools import wraps

import jwt
import pymysql
from flask import request, Flask, jsonify, Response
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from werkzeug.security import generate_password_hash, check_password_hash

import external
from external import db
from models import User, create_user_table
from my_request import pachong, pachong2

app = Flask(__name__)
app.config.from_object(external)
api = Api(app, default_mediatype="application/json")
app.config['SECRET_KEY'] = 'thisissecret'
app.secret_key = 'thisissecret'
ma = Marshmallow(app)
db.init_app(app)
CORS(app, resources=r'/*')
app.config['JSON_SORT_KEYS'] = False
JWT_SECRET_KEY = 'thisissecret'

conn = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='krcusz26wrh',
    db='data'
)
cursor = conn.cursor()


# token生成函数
def generate_token(username):
    token_data = {
        'user_name': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=6)
    }
    token = jwt.encode(token_data, app.config['SECRET_KEY'], algorithm='HS256')
    return token


# token验证函数1
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[0]
        if not token:
            return jsonify(code=401, message='Token is missing!')
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
            current_user = User.query.filter_by(username=data['user_name']).first()
            if current_user:
                pass
            else:
                return jsonify(code=401, message='Token is invalid!')
        except Exception as e:
            print(e)
            return jsonify(code=401, message='Token is invalid!')
        return f(*args, **kwargs)

    return decorated


# token验证函数2
def token_required2(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[0]
        if not token:
            return jsonify(code=401, message='Token is missing!')
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
            current_user = User.query.filter_by(username=data['user_name']).first()
            if current_user:
                pass
            else:
                return jsonify(code=401, message='Token is invalid!')
        except Exception as e:
            print("exception", e)
            return jsonify(code=401, message='Token is invalid!')

        return f(*(args[0], current_user.username), **kwargs)

    return decorated


# 登录
class login(Resource):
    def post(self):
        my_json = request.get_json()
        # 获取用户名与密码
        username = my_json.get("username")
        password = my_json.get("password")
        # 在数据库寻找是否有此用户名存在
        User_data = User.query.filter_by(username=username).first()
        if not User_data:
            return jsonify(code=404, message='User is invalid!')
        User_password = User_data.password
        User_token = generate_token(username)
        data = {
            "id": User_data.id,
            "username": username,
            "token": User_token
        }

        if check_password_hash(User_password, password):
            print("username", username)
            return jsonify(code=200, message="success", data=data)
        else:
            return jsonify(code=200, message='wrong password')


# 注册
class signin(Resource):
    def post(self):
        global new_user
        my_json = request.get_json()
        username = my_json.get("username")
        password = my_json.get("password")
        check_password = my_json.get('checkPassword')
        if password != check_password:
            return jsonify(code=404, message="you need to enter the same password")
        User_name_check = User.query.filter_by(username=username).first()
        if not User_name_check:
            hash_password = generate_password_hash(password, method='sha256')
            try:
                new_user = User(username=username, password=hash_password)
                db.session.add(new_user)
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
                return jsonify(code=404, message="wrong")
            try:
                user_table = create_user_table("h" + username)
            except Exception as e:
                print(e)
                return jsonify(code=404, message="无法创建表格")
        else:
            return jsonify(code=200, message="repeat username")
        return jsonify(code=200, message="success", data={
            "id": new_user.id,
            "username": new_user.username
        })


# 搜索
class get_in(Resource):
    @token_required2
    def get(self, current_user):
        tex = request.args.get('text')
        data = pachong(tex)

        sql = "insert into {} (name,artist,album,duration,rid) values(%s,%s,%s,%s,%s)".format("h" + current_user)
        for data_page in data:
            name = data_page['name']
            artist = data_page['artist']
            album = data_page['album']
            duration = data_page['duration']
            rid = data_page['rid']
            value = (name, artist, album, duration, rid)
            try:
                sql2 = "select * from {} where name = '{}'".format("h" + current_user, name)
                cursor.execute(sql2)
                data2 = cursor.fetchall()
                if data2:
                    pass
                else:
                    cursor.execute(sql, value)
                    conn.commit()
            except Exception as e:
                print(e)
        return jsonify(code=200, message="success", data={
            'list': data
        })


def change(current_user, rid):
    sql = "update {} set download_id =1, fav = 0 where rid = {}".format("h" + current_user, rid)
    cursor.execute(sql)
    conn.commit()
    print("right")


# 下载
class download(Resource):
    @token_required2
    def get(self, current_user, rid):
        data = pachong2(rid)
        try:
            change(current_user, rid)
            return Response(data, mimetype='audio/mpeg')
        except Exception as e:
            print(e)
            return jsonify(code=404, message="wrong")


# 搜索用户历史
class history(Resource):
    @token_required2
    def get(self, current_user):
        global list_data
        page = request.args.get('page')
        int_page = int(page)
        page_history = int_page * 10
        sql = "select * from {} where download_id = 1".format("h" + current_user)
        try:
            cursor.execute(sql)
            data = cursor.fetchall()
            list_data = []
            for data_get in data:
                list_data_number = {"name": data_get[1], "artist": data_get[2], "album": data_get[4],
                                    "duration": data_get[3],
                                    "fav": int(data_get[5]), "rid": data_get[6], "id": data_get[0]}
                list_data.append(list_data_number)
            return jsonify(code=200, message="success", data={
                'list': list_data
            })
        except Exception as e:
            print(e)
        return jsonify(code=404, message="wrong")


class put_history(Resource):
    @token_required2
    def delete(self, current_user):
        my_json = request.get_json()
        type_get = my_json.get("type")
        id_get = my_json.get("id")
        list_get = my_json.get('list')
        if type_get == 0:
            sql = "delete from {} where id = {} ".format("h" + current_user, id_get)
        elif type_get == 1:
            sql = "delete from {} where id in {} ".format("h" + current_user, tuple(list_get))
        try:
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            print(e)
        return jsonify(code=200, message="success")


class change_history(Resource):
    @token_required2
    def put(self, current_user):
        my_json = request.get_json()
        fav_get = my_json.get("fav")
        id_get = my_json.get("id")
        sql1 = "update {} set fav ={}  where id = {}".format("h" + current_user, fav_get, id_get)
        try:
            sql2 = "select * from {} where id = {}".format("h" + current_user, id_get)
            cursor.execute(sql1)
            conn.commit()
            cursor.execute(sql2)
            data_get = cursor.fetchall()[0]

            print(data_get)
            data = {"name": data_get[1], "artist": data_get[2], "album": data_get[4],
                    "duration": data_get[3], "rid": data_get[6]}
            return jsonify(code=200, message="success", data=data)
        except Exception as e:
            print(e)
            return jsonify(code=404, message="wrong")


api.add_resource(change_history, '/user/history/lc')
api.add_resource(put_history, '/user/history')
api.add_resource(history, '/user/history')
api.add_resource(download, '/search/download/<rid>')
api.add_resource(signin, '/user')
api.add_resource(login, '/user/login')
api.add_resource(get_in, '/search')
if __name__ == '__main__':
    app.run(port=8000, debug=True)
