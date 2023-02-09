from db import inc_data
from flask import Blueprint
from db import db
import json
import chardet

api = Blueprint('api', __name__)

@api.route("/",methods = ["GET"]) 
def hello_world():
    return "Welcome!"

@api.route("/cb/getData",methods = ["GET"])
def get_data():
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