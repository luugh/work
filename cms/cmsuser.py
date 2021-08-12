#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import pymysql
import sys
import json
import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


class cmsUserOp:
    def __init__(self, dbip):
        self.db = pymysql.connect(dbip, 'root', 'Star.123Mysql', 'cms', charset="utf8")
        self.cursor = self.db.cursor()
       
    def userList(self, request_dict):
        sql1 = 'SELECT system_user.EMPLOYEENUMBER,system_user.PASSWORD,system_user.usertype,role.name as premission ,' \
               'CAST(system_user.CREATEDATE AS CHAR) FROM system_user left join systemuser_role ' \
               'on system_user.id = systemuser_role.systemuserid left join role on systemuser_role.roleid = role.id'
        self.cursor.execute(sql1)
        result1 = self.cursor.fetchall()
        list1 = []
        for i in result1:
            dictuser = {}
            dictuser["userName"] = i[0]
            dictuser["password"] = i[1]
            dictuser["userPermission"] = i[3]
            dictuser["insertDate"] = i[4]
            if i[2] == 1:
               dictuser["userType"] = "General"
            elif i[2] == 0:
               dictuser["userType"] = "Administrator"
            else:
               dictuser["userType"] = "undefind"
            list1.append(dictuser)

        return list1

    def roleDetect(self, request_dict):
        userPermission = request_dict['userPermission']
        sql4 = 'SELECT name,id FROM role WHERE name="'+userPermission+'"'
        self.cursor.execute(sql4)
        result2 = self.cursor.fetchone()
        return result2

    def createUser(self, request_dict):
        newUserName = request_dict['UserName']
        password = request_dict['password']
        userType = request_dict['userType']
        insertDate = request_dict['insertDate']
        userPermission = request_dict['userPermission']
        sql2 = 'INSERT INTO system_user (EMPLOYEENUMBER,PASSWORD,usertype,' \
               'CREATEDATE,STATUS,PARENTID,SUBSIDIARYID,PARTNERID,CONTACTTYPE,' \
               'CONTACTID,INITPASSWORDFLAG,ERRORPASSWORDNUMBER,operator_id) ' \
               'VALUES ("'+newUserName+'","'+password+'",'+userType+',"'+insertDate+'",1,0,0,0,0,0,0,0,0)'
        result3 = self.roleDetect(userPermission)
        if result3 != None:
           userPermissionId = str(result3[1])
           self.cursor.execute(sql2)
           sql3 = 'INSERT INTO systemuser_role (roleid,systemuserid) values ('+userPermissionId+\
                  ',(SELECT ID FROM system_user WHERE EMPLOYEENUMBER ="'+newUserName+'"))'
           self.cursor.execute(sql3)
           self.db.commit()
           return "Sucess"
        else:
           return ("There is no %s role" %userPermission)

    def deleteUser(self, request_dict):
        OldUserName = request_dict['UserName']
        sql5 = 'DELETE FROM systemuser_role ' \
               'WHERE systemuserid=(SELECT ID FROM system_user WHERE EMPLOYEENUMBER ="'+OldUserName+'")'
        sql6 = 'DELETE FROM system_user WHERE EMPLOYEENUMBER ="'+OldUserName+'"'
        self.cursor.execute(sql5)
        self.cursor.execute(sql6)
        self.db.commit()
        return "Done"
         
    def passwordModify(self, request_dict):
        newPassword = request_dict['newPassword']
        userName = request_dict['userName']
        sql7 = 'UPDATE system_user SET PASSWORD="'+newPassword+'" WHERE EMPLOYEENUMBER="'+userName+'"'
        self.cursor.execute(sql7)
        self.db.commit()
        return "Done"
        
    def nameModify(self, request_dict):
        userName = request_dict['userName']
        newName = request_dict['newName']
        sql8 = 'UPDATE system_user SET EMPLOYEENUMBER="'+newName+'" WHERE EMPLOYEENUMBER="'+userName+'"'
        self.cursor.execute(sql8)
        self.db.commit()
        return "Done"

    def roleModify(self, request_dict):
        userPermission = request_dict['userPermission']
        userName = request_dict['userName']
        result4 = self.roleDetect(userPermission)
        if result4 != None:
           sql9 = 'UPDATE systemuser_role SET roleid='+str(result4[1])+\
                  ' WHERE systemuserid=(SELECT ID FROM system_user WHERE EMPLOYEENUMBER ="'+userName+'")'
           self.cursor.execute(sql9)
           self.db.commit()
           return "Done"
        else:
           return ("There is no %s role" %userPermission) 
        
    def __del__(self):
        self.db.close()
        
def Default(request):
    return 'no acton'

# @csrf_exempt
def CmsModifyApi(request):
        request = 'action:newUserName,UserName:test1,password:1234,newpassword: ,' \
                  'userType:1,insertDate:2018-11-29 00:00:00,' \
                  'userPermission:vod,serverIp:221.4.223.100'
        # AUTH_URL = ''
        request_dict = dict(request)
        cms1 = cmsUserOp(request_dict('serverIp'))
        Actions = {'userList': cms1.userList(), 'newUserName': cms1.createUser(), 'OldUserName': cms1.deleteUser(),
                   'newPassword': cms1.passwordModify(), 'nwqName': cms1.nameModify(), 'newRole': cms1.roleModify()}

        Data = Actions.get('action', Default)(request_dict)
        data = json.dumps(Data)
        return HttpResponse

# @csrf_exempt
# def CmsModify(request):
#     return render(request, "")

if __name__ == '__main__':
    CmsModifyApi()