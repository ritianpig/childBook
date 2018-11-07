from flask import request,jsonify
from . import web
from models import db,BookMessages,BookBadges,BookClass
import json

@web.route('/getmain',methods=["GET","POST"])
def getmain():
    # 构造字典，存储最终结果
    results_dict = {}
    # scroll　暂时取固定值
    scroll = [{
                "id": "2001",
                "image": "https://app.51babyapp.com/wx/zy9/scroll/s2001.png"

            }, {
                "id": "2002",
                "image": "https://app.51babyapp.com/wx/zy9/scroll/s2002.png"

            }, {
                "id": "2010",
                "image": "https://app.51babyapp.com/wx/zy9/scroll/s2010.png"
            }]

    if request.method == "GET":
        # 构建列表，存储cl数据
        list_res_BC = []
        # 构建字典存储books列表
        results_dict['scroll'] = scroll
        # 查询分类列表中所有的分类信息
        res_BC = db.session.query(BookClass).all()
        for i in res_BC:
            # 构造绘本列表，储存分类下面的绘本信息
            books_list = []
            # 构造分类信息字典，存储分类信息
            dict_res_BC = {}
            res_BM = db.session.query(BookMessages).filter_by(class_id=i.class_id).all()
            for k in res_BM:
                # 将取出的结果转化为字典，并删除不需要返回的字典信息，而非数据库信息
                dict_k = k.to_json()
                del dict_k['id']
                del dict_k['class_id']
                del dict_k['url']
                del dict_k['mp3']
                del dict_k['pages']
                books_list.append(dict_k)
            # 为分类构造字典赋值
            dict_res_BC['books'] = books_list
            dict_res_BC['name'] = i.name
            dict_res_BC['class_id'] = i.class_id

            list_res_BC.append(dict_res_BC)
        results_dict['cl'] = list_res_BC
        return jsonify(results_dict)




    else:
        return '暂不支持的请求方式'


