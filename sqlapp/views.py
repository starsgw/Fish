from django.shortcuts import render,render_to_response
from django.http import HttpResponse
# Create your views here.
from sqlapp.models import *
import os
from django.conf import settings
from alipay import AliPay
from django.http import JsonResponse


titlelist = ["开学好物", "数码产品", "生活用品", "学习资料", "乐器产品"]
infoLists = Commodity.coms.select(titlelist)
infoList1 = infoLists[0]  # 开学好物
infoList2 = infoLists[1]  # 数码产品
infoList3 = infoLists[2]  # 生活用品
infoList4 = infoLists[3]  # 学习资料
infoList5 = infoLists[4]  # 乐器产品


def login(request):
    request.session.clear()
    # print(33333333333333333333)
    return render(request,"login.html")

def login2(request):
    # print(4444444444444444444444444)
    id=int(request.POST.get("id"))
    password=request.POST.get("password")
    limit=request.POST.get("limit")

    username = User.users.get(userid=id).username
    num = len(Usercom.usercoms.referone(id))

    if limit=="用户":

        mess=User.users.login(id,password)
        # return render(request,mess[0],{"mess1":mess[1]})

    elif limit=="管理员":
        mess=Control.cons.login(id,password)

    res = render_to_response(mess[0],{"mess1": mess[1],"username":username,"num":num,"href":"/sqlapp/login/","loginmess":"切换用户", "titlelist": titlelist,
                                       "infoList1": infoList1, "infoList2": infoList2, "infoList3": infoList3,
                                       "infoList4": infoList4, "infoList5": infoList5})

    res.set_cookie("userid",id,max_age=600000)
    # res.set_cookie("password",password, max_age=1800)

    ses=request.session["userid"]=id
    request.session.set_expiry(300)

    return res

def register(request):
    limit = request.POST.get("limit")
    return render(request,"register.html",{"limit":limit})

def finish(request):
    limit="用户"
    id = int(request.POST.get("id"))
    password = request.POST.get("password")
    password2 = request.POST.get("password2")
    name=request.POST.get("name")
    mess=User.users.register(id,password,password2,name)
    return render(request, mess[0], {"mess1": mess[1],"limit":limit})

def finish2(request):
    cookie = request.COOKIES
    userid = cookie.get("userid")  # 从cooike中获取userid

    num = len(Usercom.usercoms.referone(userid))

    limit = "管理员"
    id = int(request.POST.get("id"))
    password = request.POST.get("password")
    password2 = request.POST.get("password2")
    name=request.POST.get("name")
    command= request.POST.get("command")
    mess=Control.cons.register(id,password,password2,name,command)
    return render(request, mess[0],{"mess1":mess[1],"limit":limit,"num":num})

def fish(request):
    cookie = request.COOKIES
    # userid = cookie.get("userid")  # 从cooike中获取userid
    username="游客用户！"
    try:
        userid =request.session["userid"]
    except:
        num = 0
        loginmess="登录"
    else:
        num = len(Usercom.usercoms.referone(userid))
        loginmess="切换用户"
        username=User.users.get(userid=userid).username

    return  render(request,"index.html",{"num":num,"loginmess":loginmess,"username":username,
                                         "titlelist": titlelist,
                                         "infoList1": infoList1, "infoList2": infoList2, "infoList3": infoList3,
                                         "infoList4": infoList4, "infoList5": infoList5
                                         })

def buy(request,comid):
    cookie = request.COOKIES
    userid = cookie.get("userid")  # 从cooike中获取userid
    # comid=request.GET.get("comid")
    print(comid)
    # print(1213122212400504565434264564)
    # comid=request.POST.get("comid")
    # username = User.users.get(userid=userid).username

    num = len(Usercom.usercoms.referone(userid))

    comidlist=Usercom.usercoms.referone(userid)


    try:
        request.session["userid"]
    except:
        return render(request,"login.html")
    else:
        if comid in comidlist:
            pass
        else:
            Usercom.usercoms.insert(userid, comid)
        username = User.users.get(userid=userid).username
        return render(request,"index.html",{"num":num,"loginmess":"切换用户","username":username,
                                            "titlelist": titlelist,
                                            "infoList1": infoList1, "infoList2": infoList2, "infoList3": infoList3,
                                            "infoList4": infoList4, "infoList5": infoList5
                                            })

def shoppingcar(request):
    cookie=request.COOKIES
    userid=cookie.get("userid")#从cooike中获取userid
    num = len(Usercom.usercoms.referone(userid))

    comidlist=Usercom.usercoms.referone(userid)

    comnamelist=[]
    comonames = Usercom.usercoms.referone(userid)

    for comid in comonames:
        comname = Commodity.coms.get(comid = comid)
        comnamelist.append(comname)
    try:
        request.session["userid"]
    except:
        return render(request,"login.html")
    else:
        username = User.users.get(userid=userid).username
        return render(request, "shoppingcar.html", {"comnamelist":comnamelist,"num":num,"loginmess":"切换用户","username":username})

def buycom(request):
    comid=request.GET['comid']
    comimg="img/goods/"+request.GET['comimg']

    cookie = request.COOKIES
    userid = cookie.get("userid")  # 从cooike中获取userid

    num = len(Usercom.usercoms.referone(userid))

    comname=Commodity.coms.referone(comid).comname
    comdescribe=Commodity.coms.referone(comid).comdescribe
    commoney = Commodity.coms.referone(comid).commoney
    complace = Commodity.coms.referone(comid).complace
    usertel = Commodity.coms.referone(comid).usertel
    userqq= Commodity.coms.referone(comid).userqq

    return render(request,"buycom.html",
                  {"num":num,"comimg":comimg,"comid":comid,"comname":comname,"comdescribe":comdescribe,
                   "commoney":commoney,"complace":complace,"usertel":usertel,"userqq":userqq})

def shoppingdel(request):
    comid = request.GET['comid']
    mess=Usercom.usercoms.deleteone(comid)
    cookie = request.COOKIES
    userid = cookie.get("userid")  # 从cooike中获取userid
    num = len(Usercom.usercoms.referone(userid))

    comidlist = Usercom.usercoms.referone(userid)

    compathlist = []
    for comid in comidlist:
        compath = "img/goods/" + str(comid) + ".jpg"
        compathlist.append(compath)

    comnamelist = []
    comonames = Usercom.usercoms.referone(userid)

    for comid in comonames:
        comname = Commodity.coms.get(comid=comid)
        comnamelist.append(comname)
    try:
        request.session["userid"]
    except:
        return render(request, "login.html")
    else:
        username = User.users.get(userid=userid).username
        return render(request, "shoppingcar.html", {"comnamelist": comnamelist, "compathlist": compathlist, "num": num,"loginmess":"切换用户","username":username})



# def pay1(request):
#     comid=request.GET['comid']
#     cookie = request.COOKIES
#     userid = cookie.get("userid")  # 从cooike中获取userid
#     num = len(Usercom.usercoms.referone(userid))
#     username = User.users.get(userid=userid).username
#     return render(request, "index2.html", {"comid":comid, "num":num, "loginmess": "退出登录", "username":username})

def index2(request):
    comid = request.GET['comid']
    commoney=Commodity.coms.get(comid=comid).commoney
    print(commoney)

    cookie = request.COOKIES
    userid = cookie.get("userid")  # 从cooike中获取userid
    num = len(Usercom.usercoms.referone(userid))
    username = User.users.get(userid=userid).username
    return render(request, "index2.html",locals(),{"comid":comid,"commoney":commoney, "num":num, "loginmess": "退出登录", "username":username})

def pay(request):
    commoney=request.POST.get("commoney")
    # print(commoney)
    # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    order_id = request.POST.get("order_id")
    # print(order_id)

    # 创建用于进行支付宝支付的工具对象
    alipay = AliPay(
        appid=settings.ALIPAY_APPID,
        app_notify_url=None,  # 默认回调url
        app_private_key_path=os.path.join(settings.BASE_DIR, "sqlapp/utils/alipay/ying_yong_si_yao.txt"),
        alipay_public_key_path=os.path.join(settings.BASE_DIR, "sqlapp/utils/alipay/zhifubao_gong_yao.txt"),
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False  配合沙箱模式使用
    )

    # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_id,
        total_amount=str(commoney),  # 将Decimal类型转换为字符串交给支付宝
        subject="测试订单",
        return_url="https://example.com",
        notify_url="https://example.com/notify"  # 可选, 不填则使用默认notify url
    )

    # 让用户进行支付的支付宝页面网址
    url = settings.ALIPAY_URL + "?" + order_string

    return JsonResponse({"code": 0, "message": "请求支付成功", "url": url})


def check_pay(request):
    # 创建用于进行支付宝支付的工具对象
    order_id = request.GET.get("order_id")
    alipay = AliPay(
        appid=settings.ALIPAY_APPID,
        app_notify_url=None,  # 默认回调url
        app_private_key_path=os.path.join(settings.BASE_DIR, "sqlapp/utils/alipay/ying_yong_si_yao.txt"),
        alipay_public_key_path=os.path.join(settings.BASE_DIR, "sqlapp/utils/alipay/zhifubao_gong_yao.txt"),
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        sign_type="RSA2",  # RSA2,官方推荐，配置公钥的时候能看到
        debug=True  # 默认False  配合沙箱模式使用
    )

    while True:
        # 调用alipay工具查询支付结果
        response = alipay.api_alipay_trade_query(order_id)  # response是一个字典
        # 判断支付结果
        code = response.get("code")  # 支付宝接口调用成功或者错误的标志
        trade_status = response.get("trade_status")  # 用户支付的情况

        if code == "10000" and trade_status == "TRADE_SUCCESS":
            # 表示用户支付成功
            # 返回前端json，通知支付成功
            return JsonResponse({"code": 0, "message": "支付成功"})

        elif code == "40004" or (code == "10000" and trade_status == "WAIT_BUYER_PAY"):
            # 表示支付宝接口调用暂时失败，（支付宝的支付订单还未生成） 后者 等待用户支付
            # 继续查询
            # print(code)
            # print(trade_status)
            continue
        else:
            # 支付失败
            # 返回支付失败的通知
            return JsonResponse({"code": 1, "message": "支付失败"})


def paysuccess(request):
    comid = request.GET['comid']
    cookie = request.COOKIES
    userid = cookie.get("userid")  # 从cooike中获取userid
    num = len(Usercom.usercoms.referone(userid))
    username = User.users.get(userid=userid).username

    comid = request.GET['comid']

    a=Usercom.usercoms.deleteone(comid)
    b=Commodity.coms.deleteone(comid)
    return render(request,"paysuccess.html",{"comid":comid,"num":num,"loginmess":"切换用户","username":username})

def insert(request):
    cookie = request.COOKIES
    userid = cookie.get("userid")  # 从cooike中获取userid
    num = len(Usercom.usercoms.referone(userid))


    try:
        request.session["userid"]
    except:
        return render(request,"login.html")
    else:
        username = User.users.get(userid=userid).username
        return render(request, 'insert.html',{"num":num,"loginmess":"切换用户","username":username})

def inserttijiao(request):
    comid=request.POST.get("comid")
    comname=request.POST.get("comname")
    comdescribe=request.POST.get("comdescribe")
    complace=request.POST.get("complace")
    # userid = int(request.POST.get("userid"))
    cookie = request.COOKIES
    userid = int(cookie.get("userid"))  # 从cooike中获取userid
    userqq = request.POST.get("userqq")
    usertel = request.POST.get("usertel")
    commoney = float(request.POST.get("commoney"))
    comtype = request.POST.get("comtype")

    # cookie = request.COOKIES
    # userid = cookie.get("userid")  # 从cooike中获取userid
    num = len(Usercom.usercoms.referone(userid))
    username = User.users.get(userid=userid).username

    uploadhtml=Commodity.coms.inserttijiao(comid,comname,comdescribe,complace,userid,userqq,usertel,commoney,comtype)
    return render(request,uploadhtml,{"num":num,"loginmess":"切换用户","username":username})

def upload(request):
    return render(request, "upload.html")

def uploadtijiao(request):

    f = request.FILES["f"]
    uploadpath = os.path.join(settings.BASE_DIR, "static/img/goods")
    f2 = open(os.path.join(uploadpath, str(f)), "wb")
    while True:
        bytes = f.read(1024)
        if bytes == b"":
            break
        else:
            f2.write(bytes)
    return render(request, "success.html", {"f2":f2})

def mycoms(request):
    cookie = request.COOKIES
    userid = cookie.get("userid")  # 从cooike中获取userid
    num = len(Usercom.usercoms.referone(userid))
    comobjs = Commodity.coms.referall(userid)

    try:
        request.session["userid"]
    except:
        return render(request,"login.html")
    else:
        username = User.users.get(userid=userid).username
        return render(request,"mycoms.html",{"comobjs":comobjs,"num":num,"loginmess":"切换用户","username":username})

def searchcom(request):
    comname=request.POST.get("comname")
    comlist=Commodity.coms.searchcom(comname)
    return render(request,"searchcom.html",{"comlist":comlist,"comname":comname})

# def delsession(request):
#     print(111111111)
#     request.session.clear()
#     print(000000)
#     data={"key":"登录"}
#     return JsonResponse(data)




