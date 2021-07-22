from flask import Flask, jsonify,request
import re
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False # jsonify返回的中文正常显示
from common.mysql_operate import db
# data = [
#     {"id": 1, "username": "小明", "password": "123456", "role": 0, "sex": 0, "telephone": "10086", "address": "北京市海淀区"},
#     {"id": 2, "username": "李华", "password": "abc", "role": 1, "sex": 0, "telephone": "10010", "address": "广州市天河区"},
#     {"id": 3, "username": "大白", "password": "666666", "role": 0, "sex": 1, "telephone": "10000", "address": "深圳市南山区"}
# ]


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/users", methods=["GET"])
def get_all_users():
    """获取所有用户信息"""
    sql = "SELECT * FROM user"
    data = db.select_db(sql)
    print("获取所有用户信息 == >> {}".format(data))
    return jsonify({"code":"0", "data":data, "msg":"操作成功"})

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(username):
    """获取某个用户信息"""
    sql = "select * from user where username = '{}'".format(username)
    data = db.select_db(sql)
    print("获取{}用户信息 == >> {}".format(username))
    if data:
        return jsonify({"code": "0", "data": data, "msg": "操作成功"})
    return jsonify({"code": "1004", "msg": "查不到相关用户的信息"})

@app.route("/register", methods=['POST'])
def user_register():
    username = request.json.get("username").strip() # 用户名
    password = request.json.get("password").strip() # 密码
    sex = request.json.get("sex", "0").strip() # 性别，默认为0(男性)
    telephone = request.json.get("telephone", "").strip() # 手机号，默认为空串
    address = request.json.get("address", "").strip() # 地址，默认为空串
    sql1 = "select username from user where username = '{}'".format(username)
    sql_name =  db.select_db(sql1)
    sql2 = "select telephone from user where username = '{}'".format(username)
    sql_phone = db.select_db(sql2)
    if username and password and telephone:
        if username == sql_name:
            return jsonify({"code": 2002, "msg": "用户名已存在！！！"})
        elif not (sex == "0" or sex == "1"):
            return jsonify({"code": 2003, "msg": "输入的性别只能是 0(男) 或 1(女)！！！"})
        elif not (len(telephone) == 11 and re.match("^1[3,5,7,8]\d{9}$", telephone)):
            return jsonify({"code": 2004, "msg": "手机号格式不正确！！！"})
        elif telephone == sql_phone:
            return jsonify({"code": 2005, "msg": "手机号已经被注册！！！"})
        else:
            sql3 = "INSERT INTO user(username, password, role, sex, telephone, address) " \
                  "VALUES('{}', '{}', '1', '{}', '{}', '{}')".format(username, password, sex, telephone, address)
            db.execute_db(sql3)
            return jsonify({"code": 0, "msg": "恭喜，注册成功！"})
    else:
        return jsonify({"code": 2001, "msg": "用户名/密码/手机号不能为空，请检查！！！"})
@app.route("/login", methods=['POST'])
def user_login():
    username = request.values.get("username")
    password = request.values.get("password")
    sql1 = "select username from user where username = '{}'".format(username)
    sql_name = db.select_db(sql1)
    sql2 = "select password from user where username = '{}'".format(username)
    sql_pwd = db.select_db(sql2)
    if username and password:
        if username == sql_name and password == sql_pwd:
            return jsonify({"code": 0, "msg": "恭喜，登录成功！"})
        return jsonify({"code": 1002, "msg": "用户名或密码错误！！！"})
    else:
        return jsonify({"code": 1001, "msg": "用户名或密码不能为空！！！"})



if __name__ == '__main__':
    app.run()