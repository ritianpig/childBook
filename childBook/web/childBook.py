from flask import request,jsonify
from . import web
from models import db, BookMessages, BookBadges, BookClass, user_favs, user_shares, Testa, Scroll, Users, user_badges
import json
import random
from urllib import request as req

@web.route('/gettoken',methods=["GET","POST"])
def gettoken():
    if request.method == "GET":
        results_dict = {}

        get_appid = request.args.get('appid')
        get_appsecret = request.args.get('secret')
        get_token = request.args.get('token')

        resp = req.urlopen("https://api.weixin.qq.com/sns/jscode2session?appid={}"
                           "&secret={}&js_code={}&grant_type=authorization_code".format
                           (get_appid, get_appsecret, get_token))
        resp1 = resp.read().decode()
        resp2 = json.loads(resp1)

        keys_list = []
        for k in resp2.keys():
            keys_list.append(k)

        if 'unionid' in keys_list:
            unionid = resp2['unionid']
            add_user = Users(user=unionid)
            db.session.add(add_user)
            db.session.commit()
            results_dict['unionid'] = unionid

            return jsonify(results_dict)

        else:
            return '或许参数输入有误，获取unionid失败'

    else:

        results_dict = {}

        get_appid = request.args.get('appid')
        get_appsecret = request.args.get('secret')
        get_token = request.args.get('token')

        resp = req.urlopen("https://api.weixin.qq.com/sns/jscode2session?appid={}"
                           "&secret={}&js_code={}&grant_type=authorization_code".format
                           (get_appid, get_appsecret, get_token))
        resp1 = resp.read().decode()
        resp2 = json.loads(resp1)

        keys_list = []
        for k in resp2.keys():
            keys_list.append(k)

        if 'unionid' in keys_list:
            unionid = resp2['unionid']
            add_user = Users(user=unionid)
            db.session.add(add_user)
            db.session.commit()
            results_dict['unionid'] = unionid

            return jsonify(results_dict)

        else:
            return '或许参数输入有误，获取unionid失败'


@web.route('/getmain',methods=["GET","POST"])
def getmain():
    # 构造字典，存储最终结果
    results_dict = {}
    # scroll　
    res_scroll = db.session.query(Scroll).first()
    scroll = json.loads(res_scroll.scroll)

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
                # 将结果由int转换为str
                dict_k['fav'] = str(dict_k['fav'])
                dict_k['time'] = str(dict_k['time'])
                books_list.append(dict_k)
            # 为分类构造字典赋值
            dict_res_BC['books'] = books_list
            dict_res_BC['name'] = i.name
            dict_res_BC['class_id'] = str(i.class_id)

            list_res_BC.append(dict_res_BC)
        results_dict['cl'] = list_res_BC
        return jsonify(results_dict)

    else:

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
                # 将结果由int转换为str
                dict_k['fav'] = str(dict_k['fav'])
                dict_k['time'] = str(dict_k['time'])
                books_list.append(dict_k)
            # 为分类构造字典赋值
            dict_res_BC['books'] = books_list
            dict_res_BC['name'] = i.name
            dict_res_BC['class_id'] = str(i.class_id)

            list_res_BC.append(dict_res_BC)
        results_dict['cl'] = list_res_BC
        return jsonify(results_dict)

# 累加收听次数
@web.route('/uploadbooktime',methods=["GET","POST"])
def getTime():
    if request.method == "GET":
        get_id = request.args.get('id')
        res_time = db.session.query(BookMessages).filter_by(book_id=get_id).first()
        #　判断接收的id是否存在数据库中，如果存在累加，返回ok，否则返回错误信息
        if res_time :
            res_time.time += 1
            db.session.commit()

            return 'ok'
        else:
            return '输入的id不存在'
    else:

        get_id = request.args.get('id')
        res_time = db.session.query(BookMessages).filter_by(book_id=get_id).first()
        # 　判断接收的id是否存在数据库中，如果存在累加，返回ok，否则返回错误信息
        if res_time:
            res_time.time += 1
            db.session.commit()

            return 'ok'
        else:
            return '输入的id不存在'

# 获取绘本信息，并且判断用户属性状态
@web.route('/getbook',methods=["GET","POST"])
def getbook():
    if request.method == "GET":

        results_dict = {}
        get_id = request.args.get('id')
        get_unionid = request.args.get('unionid')

        # 获取绘本所有book_id不等于get_id的数据
        res_bms = db.session.query(BookMessages).filter(BookMessages.book_id!=get_id).all()
        res_bms_list = []
        for res_bm in res_bms:
            # 取数据库特定数据组成字典，添加到列表中
            rec_dict = dict(book_id=res_bm.book_id,class_id=res_bm.class_id,image=res_bm.image)
            res_bms_list.append(rec_dict)

        # 随机从列表中取３个值组成新的列表
        recommends = random.sample(res_bms_list,3)

        res_BM = db.session.query(BookMessages).filter_by(book_id=get_id).first()
        res_uf = db.session.query(user_favs).filter_by(user=get_unionid,book_id=get_id).first()
        res_us = db.session.query(user_shares).filter_by(user=get_unionid,book_id=get_id).first()
        results_dict['recommends'] = recommends
        dict_BM = res_BM.to_json()
        del dict_BM['id']
        # 解析json
        dict_BM['pages'] = json.loads(dict_BM['pages'])
        results_dict.update(dict_BM)

        # 判断该绘本用户是否收藏
        if res_uf:
            results_dict['isFav'] = '1'
        else:
            results_dict['isFav'] = '0'

        # 判断该绘本用户是否分享
        if res_us:
            results_dict['isShare'] = '1'
        else:
            results_dict['isShare'] = '0'

        return jsonify(results_dict)

    else:

        results_dict = {}
        get_id = request.args.get('id')
        get_unionid = request.args.get('unionid')

        # 获取绘本所有book_id不等于get_id的数据
        res_bms = db.session.query(BookMessages).filter(BookMessages.book_id != get_id).all()
        res_bms_list = []
        for res_bm in res_bms:
            # 取数据库特定数据组成字典，添加到列表中
            rec_dict = dict(book_id=res_bm.book_id, class_id=res_bm.class_id, image=res_bm.image)
            res_bms_list.append(rec_dict)

        # 随机从列表中取３个值组成新的列表
        recommends = random.sample(res_bms_list, 3)

        res_BM = db.session.query(BookMessages).filter_by(book_id=get_id).first()
        res_uf = db.session.query(user_favs).filter_by(user=get_unionid, book_id=get_id).first()
        res_us = db.session.query(user_shares).filter_by(user=get_unionid, book_id=get_id).first()
        results_dict['recommends'] = recommends
        dict_BM = res_BM.to_json()
        del dict_BM['id']
        # 解析json
        dict_BM['pages'] = json.loads(dict_BM['pages'])
        results_dict.update(dict_BM)

        # 判断该绘本用户是否收藏
        if res_uf:
            results_dict['isFav'] = '1'
        else:
            results_dict['isFav'] = '0'

        # 判断该绘本用户是否分享
        if res_us:
            results_dict['isShare'] = '1'
        else:
            results_dict['isShare'] = '0'

        return jsonify(results_dict)

@web.route('/uploadfav',methods=["GET","POST"])
def uploadfav():
    if request.method == "GET":
        get_id = request.args.get('id')
        get_unionid = request.args.get('unionid')

        if get_unionid:
            res_fav = db.session.query(BookMessages).filter_by(book_id=get_id).first()
            res_uf = db.session.query(user_favs).filter_by(user=get_unionid,book_id=get_id).first()
            # 判断用户是否在用户数据库中
            res_get_us = db.session.query(Users).filter_by(user=get_unionid).first()
            if res_get_us:
                # 判断用户收藏表是否有该条记录
                if res_uf:
                    return 'ok2'
                else:
                    add_user_fav = user_favs(user=get_unionid,book_id=get_id)
                    res_fav.fav += 1
                    db.session.add(add_user_fav)
                    db.session.commit()
                    return 'ok'
            else:
                add_user = Users(user=get_unionid)
                add_user_fav = user_favs(user=get_unionid, book_id=get_id)
                res_fav.fav += 1
                db.session.add(add_user)
                db.session.add(add_user_fav)
                db.session.commit()
                return 'ok'

        else:
            return 'unionid不能为空'
    else:

        get_id = request.args.get('id')
        get_unionid = request.args.get('unionid')

        if get_unionid:
            res_fav = db.session.query(BookMessages).filter_by(book_id=get_id).first()
            res_uf = db.session.query(user_favs).filter_by(user=get_unionid, book_id=get_id).first()
            # 判断用户是否在用户数据库中
            res_get_us = db.session.query(Users).filter_by(user=get_unionid).first()
            if res_get_us:
                # 判断用户收藏表是否有该条记录
                if res_uf:
                    return 'ok2'
                else:
                    add_user_fav = user_favs(user=get_unionid, book_id=get_id)
                    res_fav.fav += 1
                    db.session.add(add_user_fav)
                    db.session.commit()
                    return 'ok'
            else:
                add_user = Users(user=get_unionid)
                add_user_fav = user_favs(user=get_unionid, book_id=get_id)
                res_fav.fav += 1
                db.session.add(add_user)
                db.session.add(add_user_fav)
                db.session.commit()
                return 'ok'

        else:
            return 'unionid不能为空'


@web.route('/getfav',methods=["GET","POST"])
def getfav():
    if request.method == "GET":
        results_dict = {}
        results_list = []
        get_unionid = request.args.get('unionid')
        # 获取用户收藏表，首先查询用户收藏的所有的绘本id，通过id查找相关信息
        favs_list = []
        res_ufavs = db.session.query(user_favs).filter_by(user=get_unionid).all()
        for res_ufav in res_ufavs:
            favs_list.append(res_ufav.book_id)

        for i in favs_list:
            res_bm = db.session.query(BookMessages).filter_by(book_id =i).first()
            dict_i = dict(book_id=res_bm.book_id,class_id=res_bm.class_id,
                          title=res_bm.title,image=res_bm.image)
            results_list.append(dict_i)

        results_dict['favs'] = results_list

        return jsonify(results_dict)

    else:

        results_dict = {}
        results_list = []
        get_unionid = request.args.get('unionid')
        # 获取用户收藏表，首先查询用户收藏的所有的绘本id，通过id查找相关信息
        favs_list = []
        res_ufavs = db.session.query(user_favs).filter_by(user=get_unionid).all()
        for res_ufav in res_ufavs:
            favs_list.append(res_ufav.book_id)

        for i in favs_list:
            res_bm = db.session.query(BookMessages).filter_by(book_id=i).first()
            dict_i = dict(book_id=res_bm.book_id, class_id=res_bm.class_id,
                          title=res_bm.title, image=res_bm.image)
            results_list.append(dict_i)

        results_dict['favs'] = results_list

        return jsonify(results_dict)

# 用户首次分享，将分享信息存入用户分享表
@web.route('/uploadsharebook',methods=["GET","POST"])
def sharebook():
    if request.method == "GET":
        get_id = request.args.get('id')
        get_unionid = request.args.get('unionid')

        if get_unionid:
            # 判断依据是，首次用户分享表中没有数据给该用户加100金币，再次分享时，存在数据，则不再增加金币
            res_users_coins = db.session.query(Users).filter_by(user=get_unionid).first()
            # 判断用户分享表是否已经存在该数据
            res_ushare = db.session.query(user_shares).filter_by(user=get_unionid,book_id=get_id).first()
            if res_ushare:
                res_ushare.share_times += 1
                db.session.commit()
                return 'ok2'
            else:
                res_users_coins.coins += 100
                add_ushare = user_shares(user=get_unionid,book_id=get_id,share_times=1)
                db.session.add(add_ushare)
                db.session.commit()
                return 'ok'

        else:
            return 'unionid不能为空'

    else:

        get_id = request.args.get('id')
        get_unionid = request.args.get('unionid')

        if get_unionid:
            # 判断依据是，首次用户分享表中没有数据给该用户加100金币，再次分享时，存在数据，则不再增加金币
            res_users_coins = db.session.query(Users).filter_by(user=get_unionid).first()
            # 判断用户分享表是否已经存在该数据
            res_ushare = db.session.query(user_shares).filter_by(user=get_unionid, book_id=get_id).first()
            if res_ushare:
                res_ushare.share_times += 1
                db.session.commit()
                return 'ok2'
            else:
                res_users_coins.coins += 100
                add_ushare = user_shares(user=get_unionid, book_id=get_id, share_times=1)
                db.session.add(add_ushare)
                db.session.commit()
                return 'ok'

        else:
            return 'unionid不能为空'

# 用户首次分享后获得此绘本图卡
@web.route('/uploadsharebadge',methods=["GET","POST"])
def getshare():
    if request.method == "GET":
        get_id = request.args.get('id')
        get_unionid = request.args.get('unionid')
        get_badgeid =request.args.get('badgeid')

        # 先判断用户是否有该图卡，如果有则返回用户已拥有此图卡
        res_haveBadge = db.session.query(user_badges).filter_by(user=get_unionid,book_id=get_id,
                                                                badge_id=get_badgeid).first()
        # 判断用户是否是第一次分享此绘本
        if res_haveBadge:
            return 'ok2'
        else:
            add_badges = user_badges(user=get_unionid,book_id=get_id,badge_id=get_badgeid)
            db.session.add(add_badges)
            db.session.commit()
            return 'ok'

    else:

        get_id = request.args.get('id')
        get_unionid = request.args.get('unionid')
        get_badgeid = request.args.get('badgeid')

        # 先判断用户是否有该图卡，如果有则返回用户已拥有此图卡
        res_haveBadge = db.session.query(user_badges).filter_by(user=get_unionid, book_id=get_id,
                                                                badge_id=get_badgeid).first()
        # 判断用户是否是第一次分享此绘本
        if res_haveBadge:
            return 'ok2'
        else:
            add_badges = user_badges(user=get_unionid, book_id=get_id, badge_id=get_badgeid)
            db.session.add(add_badges)
            db.session.commit()
            return 'ok'

# 获取该用户，查看的当前绘本的所有图卡信息，如果用户拥有此绘本下的某个图卡，则own=1
@web.route('/getbadge',methods=["GET","POST"])
def getbadge():
    if request.method == "GET":
        get_id = request.args.get('id')
        get_unionid = request.args.get('unionid')
        # 通过传入的unionid和id来确定返回该绘本的图卡信息
        res_user_badges = db.session.query(user_badges).filter_by(user=get_unionid,book_id=get_id).all()
        # 根据book_id查找图卡所有信息
        res_badges = db.session.query(BookBadges).filter_by(book_id=get_id).first()
        badges_list = json.loads(res_badges.badges)

        for x in badges_list:
            # 给own赋初始值
            x['own'] = '0'
            for res_user_badge in res_user_badges:
                # 当用户绘本中有该系图卡下面的图卡时，own=1
                if res_user_badge.badge_id in x.values():
                    x['own'] = '1'
        results_dict = dict(book_id=get_id,url=res_badges.url,badges=badges_list)
        return jsonify(results_dict)

    else:

        get_id = request.args.get('id')
        get_unionid = request.args.get('unionid')
        # 通过传入的unionid和id来确定返回该绘本的图卡信息
        res_user_badges = db.session.query(user_badges).filter_by(user=get_unionid, book_id=get_id).all()
        # 根据book_id查找图卡所有信息
        res_badges = db.session.query(BookBadges).filter_by(book_id=get_id).first()
        badges_list = json.loads(res_badges.badges)

        for x in badges_list:
            # 给own赋初始值
            x['own'] = '0'
            for res_user_badge in res_user_badges:
                # 当用户绘本中有该系图卡下面的图卡时，own=1
                if res_user_badge.badge_id in x.values():
                    x['own'] = '1'
        results_dict = dict(book_id=get_id, url=res_badges.url, badges=badges_list)
        return jsonify(results_dict)

# 获取用户金币数
@web.route('/getcoin',methods=["GET","POST"])
def getcoin():
    if request.method == "GET":
        get_unionid = request.args.get('unionid')

        res_users_coins = db.session.query(Users).filter_by(user=get_unionid).first()
        users_coin_dict = dict(unionid=get_unionid,coins=str(res_users_coins.coins))

        return jsonify(users_coin_dict)

    else:

        get_unionid = request.args.get('unionid')

        res_users_coins = db.session.query(Users).filter_by(user=get_unionid).first()
        users_coin_dict = dict(unionid=get_unionid, coins=str(res_users_coins.coins))

        return jsonify(users_coin_dict)

# 增加金币
@web.route('/uploadcoinadd',methods=["GET","POST"])
def addCoin():
    if request.method == "GET":
        get_num = request.args.get('num',type=int)
        get_unionid = request.args.get('unionid')

        res_users_coins = db.session.query(Users).filter_by(user=get_unionid).first()
        res_users_coins.coins += get_num
        db.session.commit()

        return 'ok'

    else:

        get_num = request.args.get('num', type=int)
        get_unionid = request.args.get('unionid')

        res_users_coins = db.session.query(Users).filter_by(user=get_unionid).first()
        res_users_coins.coins += get_num
        db.session.commit()

        return 'ok'

# 消费金币
@web.route('/uploadcoinmin', methods=["GET", "POST"])
def minCoin():
    if request.method == "GET":
        get_num = request.args.get('num',type=int)
        get_unionid = request.args.get('unionid')

        res_users_coins = db.session.query(Users).filter_by(user=get_unionid).first()
        res_users_coins.coins -= get_num
        db.session.commit()

        return 'ok'

    else:

        get_num = request.args.get('num', type=int)
        get_unionid = request.args.get('unionid')

        res_users_coins = db.session.query(Users).filter_by(user=get_unionid).first()
        res_users_coins.coins -= get_num
        db.session.commit()

        return 'ok'

# 从服务器获取绘本信息，储存到测试表
@web.route('/downBooks',methods=["GET","POST"])
def test():
    if request.method == "GET":
        get_books = request.args.get('books')
        resp = req.urlopen('https://httdatahb.51babyapp.com/books/{}/{}.json'.format(get_books,get_books))
        resp1 = resp.read().decode()
        test1 = Testa(test=resp1)
        db.session.add(test1)
        db.session.commit()
        resp2 = json.loads(resp1)
        return jsonify(resp2)

    else:

        get_books = request.args.get('books')
        resp = req.urlopen('https://httdatahb.51babyapp.com/books/{}/{}.json'.format(get_books, get_books))
        resp1 = resp.read().decode()
        test1 = Testa(test=resp1)
        db.session.add(test1)
        db.session.commit()
        resp2 = json.loads(resp1)
        return jsonify(resp2)

# 从测试表取出数据保存到bookMessages
@web.route('/saveBooks',methods=["GET","POST"])
def asd():
    if request.method == "GET":
        datas = db.session.query(Testa).all()
        for data in datas:
            J_data = json.loads(data.test)
            print(type(J_data['mp3']))
            add_data = BookMessages(book_id=J_data['id'], class_id=J_data['class_id'], title=J_data['title']
                                    , title_cn=J_data['title_cn'], url=J_data['url'], image=J_data['cover'],
                                    mp3=J_data['mp3'], pages=str(J_data['pages']))
            db.session.add(add_data)
            db.session.commit()

        return 'ok'

    else:

        datas = db.session.query(Testa).all()
        for data in datas:
            J_data = json.loads(data.test)
            print(type(J_data['mp3']))
            add_data = BookMessages(book_id=J_data['id'], class_id=J_data['class_id'], title=J_data['title']
                                    , title_cn=J_data['title_cn'], url=J_data['url'], image=J_data['cover'],
                                    mp3=J_data['mp3'], pages=str(J_data['pages']))
            db.session.add(add_data)
            db.session.commit()

        return 'ok'
