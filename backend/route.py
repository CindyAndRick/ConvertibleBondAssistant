from db import inc_data, follow
from flask import Blueprint
from db import db
import json
import chardet

api = Blueprint('api', __name__)

@api.route("/",methods = ["GET"]) 
def hello_world():
    return "Welcome!"

@api.route("/cb/getAllData",methods = ["GET"])
def get_all_data():
    list = db.session.query(inc_data).all()
    res = []
    for item in list:
        tmp = {}
        tmp['code'] = item.code
        tmp['name'] = item.name
        tmp['inc_d'] = item.inc_d
        tmp['inc_w'] = item.inc_w
        tmp['inc_m'] = item.inc_m
        tmp['expire'] = item.expire
        res.append(tmp)
    return json.dumps(res)

@api.route("/cb/getFollowData", methods = ["GET"])
def get_follow_data():
    follow_list = db.session.query(follow).all()
    follow_list = [item.code for item in follow_list]
    # print('follow_list', follow_list)
    list = db.session.query(inc_data).filter(inc_data.code.in_(follow_list)).all()
    print('list', list)
    res = []
    for item in list:
        tmp = {}
        tmp['code'] = item.code
        tmp['name'] = item.name
        tmp['inc_d'] = item.inc_d
        tmp['inc_w'] = item.inc_w
        tmp['inc_m'] = item.inc_m
        tmp['expire'] = item.expire
        res.append(tmp)
    return json.dumps(res)
