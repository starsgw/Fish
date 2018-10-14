from django.db import models

# Create your models here.


class ControlManager(models.Manager):
    def ids(self):
        idlist = []
        for con in self.all():
            idlist.append(con.conid)
        return idlist

    def login(self, id, password):
        idlist = self.ids()
        if id in idlist:
            con = Control.cons.get(conid=id)
            if password == con.conpwd:
                return ["index.html",0]
            else:
                return ["login.html",1]
        else:
            return ["login.html",1]

    def register(self, id, password, password2, name,command):
        idlist=self.ids()
        con2=Control.cons.get(conid=1001)
        if id in idlist:
            return ["register.html", 1]
        elif password!=password2:
            return ["register.html", 2]
        elif name=="":
            return ["register.html", 3]
        elif command!=con2.command:
            return ["register.html", 0]
        else:
            con=Control(conid=id,conpwd=password,conname=name)
            con.save()
            return ["login.html", 4]




class UserManager(models.Manager):
    def ids(self):
        idlist=[]
        for user in self.all():
            idlist.append(user.userid)
        return idlist

    def login(self,id,password):
        idlist=self.ids()
        if id in idlist:
            user=User.users.get(userid=id)
            if password==user.userpwd:
                return ["index.html",0]
            else:
                return ["login.html",1]
        else:
            return ["login.html",1]

    # def  referusername(self,userid):
    #     username=User.users.get(userid=userid)

    def register(self, id, password, password2, name):
        idlist=self.ids()
        if id in idlist:
            return ["register.html",1]
        elif password!=password2:
            return ["register.html",2]
        elif name=="":
            return ["register.html",3]
        else:
            user=User(userid=id,userpwd=password,username=name)
            user.save()
            return ["login.html",4]

class Control(models.Model):

    cons=ControlManager()
    conid=models.IntegerField(primary_key=True)
    conpwd=models.CharField(max_length=30)
    conname=models.CharField(max_length=20)
    command=models.CharField(max_length=20,null=True)



class User(models.Model):

    users=UserManager()
    userid=models.IntegerField(primary_key=True)
    userpwd=models.CharField(max_length=30)
    username=models.CharField(max_length=20)





class CommodityManager(models.Manager):#商品管理器
    def referall(self,userid):
        objs=Commodity.coms.filter(userid=userid)
        return objs

    def referone(self,comid):
        comobj=Commodity.coms.get(comid=comid)
        return comobj
    def deleteone(self,comid):
        comobj=Commodity.coms.filter(comid=comid)
        comobj.delete()
        return '商品删除成功'

    def comids(self):
        comidlist = []
        for god in self.all():
            comidlist.append(god.comid)
        return comidlist

    def inserttijiao(self,comid,comname,comdescribe,complace,userid,userqq,usertel,commoney,comtype):
        comidlist = self.comids()
        if comid in comidlist:
            return "该商品号已经存在"
        else:
            usercom=Commodity(comid=comid,comname=comname,comdescribe=comdescribe,complace=complace,userid=userid,userqq=userqq,usertel=usertel,commoney=commoney,comtype=comtype)
            usercom.save()
            return "upload.html"

    def select(self, titlelist):
        infoLists = []
        for title in titlelist:
            infoList = Commodity.coms.filter(comtype=title)
            infoLists.append(infoList)

            # for com in imgname:
            #     imgpath="img/goods/"+str(com.comid)+".jpg"
        return infoLists

    def searchcom(self,comname):
        comlist=Commodity.coms.filter(comname__contains=comname)
        return comlist

class Commodity(models.Model):#商品
    coms=CommodityManager()

    comid=models.IntegerField(primary_key=True)
    comname=models.CharField(max_length=50)
    comdescribe=models.CharField(max_length=300)
    complace=models.CharField(max_length=50)
    userid = models.IntegerField()
    userqq=models.CharField(max_length=20)
    usertel=models.CharField(max_length=20)
    dtime=models.DateField(auto_now_add=True)
    commoney=models.FloatField()
    comtype=models.CharField(max_length=50)


class UsercomManager(models.Manager):
    def referone(self,userid):
        list=[]
        usercomobj=Usercom.usercoms.filter(userid=userid)
        for uco in usercomobj:
            list.append(uco.comid)
        return list

    def insert(self, userid, comid):
        shop2=Usercom()
        shop2.userid=userid
        shop2.comid=comid
        shop2.save()

    def deleteone(self,comid):
        comobj=Usercom.usercoms.filter(comid=comid)
        comobj.delete()
        return '购物车删除成功'

class Usercom(models.Model):
    # id=models.AutoField()
    usercoms=UsercomManager()

    userid = models.IntegerField()
    comid=models.IntegerField()
