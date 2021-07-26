from flask import Flask, jsonify,request
import re
import time
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False # jsonify返回的中文正常显示
from common.mysql_operate import db
from common.redis_operate import redis_db
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
    '''注册'''
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
    '''登录'''
    username = request.values.get("username")
    password = request.values.get("password")
    print(username)
    sql1 = "select username from user where username = '{}'".format(username)
    sql_name = db.select_db(sql1)
    sql2 = "select * from user where username = '{}'".format(username)
    sql_info = db.select_db(sql2)
    if username and password:
        if not sql_name:
            return jsonify({"code": 1003, "msg": "用户名不存在！"})
        if sql_info:
            timeStamp = int(time.time())#获取当前时间戳
            token = "{}{}".format(username,timeStamp)
            redis_db.handle_redis_token(username,token)#把token放到Redis中储存
            login_info = {
                "id":sql_info[0],
                "username":username,
                "token":token,
                "login_time":time.strftime("%Y/%m/%d %H:%M:%S")
            }
            return jsonify({"code": 0,"login_info":login_info, "msg": "恭喜，登录成功！"})
        return jsonify({"code": 1002, "msg": "用户名或密码错误！！！"})
    else:
        return jsonify({"code": 1001, "msg": "用户名或密码不能为空！！！"})

@app.route("/delete/user/<int:id>", methods=['POST'])
def user_delete(id):
    username = request.json.get("username", "").strip()  # 当前登录的管理员用户
    token = request.json.get("token", "").strip()  # token口令
    if username and token:
        redis_token = redis_db.handle_redis_token(username)  # 从redis中取token
        if redis_token:
            if redis_token == token:  # 如果从redis中取到的token不为空，且等于请求body中的token
                sql1 = "SELECT role FROM user WHERE username = '{}'".format(username)
                res1 = db.select_db(sql1)
                print("根据用户名 【 {} 】 查询到用户类型 == >> {}".format(username, res1))
                user_role = res1[0]["role"]
                if user_role == 0:  # 如果当前登录用户是管理员用户
                    sql2 = "SELECT * FROM user WHERE id = '{}'".format(id)
                    res2 = db.select_db(sql2)
                    print("根据用户ID 【 {} 】 查询到用户信息 ==>> {}".format(id, res2))
                    if not res2:  # 如果要删除的用户不存在于数据库中，res2为空
                        return jsonify({"code": 3005, "msg": "删除的用户ID不存在，无法进行删除，请检查！！！"})
                    elif res2[0]["role"] == 0: # 如果要删除的用户是管理员用户，则不允许删除
                        return jsonify({"code": 3006, "msg": "用户ID：【 {} 】，该用户不允许删除！！！".format(id)})
                    else:
                        sql3 = "DELETE FROM user WHERE id = {}".format(id)
                        db.execute_db(sql3)
                        print("删除用户信息SQL ==>> {}".format(sql3))
                        return jsonify({"code": 0, "msg": "恭喜，删除用户信息成功！"})
                else:
                    return jsonify({"code": 3004, "msg": "当前用户不是管理员用户，无法进行操作，请检查！！！"})
            else:
                return jsonify({"code": 3003, "msg": "token口令不正确，请检查！！！"})
        else:
            return jsonify({"code": 3002, "msg": "当前用户未登录，请检查！！！"})
    else:
        return jsonify({"code": 3001, "msg": "管理员用户/token口令不能为空，请检查！！！"})



if __name__ == '__main__':
    app.run()