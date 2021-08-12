#!/usr/bin/env python
# -*- coding:utf-8 -*-
import threading
import socketserver
import json
import os, time, subprocess
import pymysql

def getNow():
    return time.strftime('%Y%m%d%H%M',time.localtime(time.time()))

class Insertdb():
    def __init__(self):
        self.user = "netest"
        self.passwd = "eh#DnGhy7"
        self.host = "119.146.223.77"
        self.db = "netest"
    def statusup(self,Srcip,Dstip,Count,Min,Max,Avg,Mdev,Packetloss,Status,Hostdate,Localdate):
        conn = pymysql.connect(user=self.user,passwd=self.passwd,host=self.host,db=self.db)
        cur = conn.cursor()
        sql1 = "INSERT INTO net_status (srcip,dstip,count,min,max,avg,mdev,packetloss,status,hostdate,localdate) values('"
        sql2 = Srcip+"','"+Dstip+"','"+Count+"','"+Min+"','"+Max+"','"+Avg+"','"+Mdev+"','"+Packetloss+"','"+Status+"','"+Hostdate+"','"+Localdate+"')"   
        sql = sql1+sql2
        indb = cur.execute(sql)
        if indb == 1:
            print("INFO:sucessfull indb")
        else:
            print("ERROR:fail indb")
        conn.commit()
        cur.close()
        conn.close()
    def statusdown(self,Srcip,Dstip,Status,Hostdate,Localdate):
        conn = pymysql.connect(user=self.user,passwd=self.passwd,host=self.host,db=self.db)
        cur = conn.cursor()
        sql1 = "INSERT INTO net_status (srcip,dstip,status,hostdate,localdate) values('"
        sql2 = Srcip+"','"+Dstip+"','"+Status+"','"+Hostdate+"','"+Localdate+"')"
        sql = sql1+sql2
        indb = cur.execute(sql)
        if indb == 1:
            print("INFO:sucessfull indb")
        else:
            print("INFO:fail indb")
        conn.commit()
        cur.close()
        conn.close()

class TestPing:
    def testping(self,count,ip,mutex,srcip,hostdate,localdate):
        mutex.acquire()#取得锁
        Indb = Insertdb()
        cmd = "ping -c "+ count + " " + ip
        result = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
        out, err = result.communicate()
        out = out.decode('utf8')
        if out.find("min/avg/max/mdev") != -1: 
            lossstr = out.split(" ")[-9]
            speedstr = out.split(" ")[-2]
            context = {
                'Srcip':srcip,
                'Dstip':ip,
                'Count':count,
                'Min':speedstr.split("/")[0],
                'Max':speedstr.split("/")[2],
                'Avg':speedstr.split("/")[1],
                'Mdev':speedstr.split("/")[3],
                'Packetloss':lossstr,
                'Status':"0",
                'Hostdate':hostdate,
                'Localdate':localdate
            }
            print("INFO:",context)
            Indb.statusup(**context)	
            mutex.release()#释放锁
        else:
            context = {
                'Srcip':srcip,
                'Dstip':ip,
                'Status':"1",
                'Hostdate':hostdate,
                'Localdate':localdate
            }
            print("INFO:",context)
            Indb.statusdown(**context)
            mutex.release()#释放锁

class Netest():
    def netest(self,srcip,IPList,sdate,Count):
        threads = []
        tp = TestPing()
        hostdate = getNow()
        localdate = sdate
        if len(IPList) == 0:
            print("ERROR:no ip")
        else:
            mutex = threading.Lock()#创建锁
            for x,y in zip(IPList,Count):
                count = y
                print("INFO:Start ping" ,x)
                Pross = threading.Thread(target=tp.testping,args=(count,x,mutex,srcip,hostdate,localdate))
                Pross.start()
                threads.append(Pross)
            for t in threads:
                t.join()
            print("INFO:over",getNow())

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        if data:
            r = 'start ping....'
            self.request.sendall(r.encode())
            data = data.decode()
            jdata = json.loads(data)
            print("INFO:Receive data  '%r'"%(data))
            cur_thread = threading.current_thread().name
            Ping = Netest()
            srcList = []
            dstList = []
            sdate = []
            Count = []
            response = []
            for i in range(len(jdata)):
                srcList.append(jdata[i]['src'])
                dstList.append(jdata[i]['dst'])
                sdate.append(jdata[i]['date'])
                Count.append(jdata[i]['count'])
            srcip = srcList[0]
            sdate = sdate[0]
            Ping.netest(srcip,dstList,sdate,Count)
            print(srcip + ":Ping finished as " + cur_thread)
        else:
            r = 'Recv data error....'
            self.request.sendall(r.encode())
  
           # self.request.sendall(res.encode())
    #        jresp = json.dumps(response).encode()
    #        self.request.sendall(jresp)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass



if __name__ == "__main__":
    try:
        HOST, PORT = "0.0.0.0", 9017
        socketserver.TCPServer.allow_reuse_address = True
        server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
        ip, port = server.server_address
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        print("Server running in :", server_thread.name)
        print(" .... waiting for connection ....")
        server.serve_forever()
    except KeyboardInterrupt:
        print ("Crtl+C Pressed. Shutting down....")
        exit()
