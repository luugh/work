import datetime,requests,time,threading
import sys,pymysql,json,math
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from linkcache.redis import InRedis
#-----------import locallib-----
dir = sys.path[0]+"/dashboard"
sys.path.append(dir)

#------------------------------
def GetChannels(Iptvid,Ip,Order,Page,Num):
    Iptvid = Iptvid.replace(',','|').replace('，','|').replace('\n','|').replace(' ','|')
    if Ip != 'default':
        Exp = " AND hostIp = '"+Ip+"'"
    else:
        Exp = ''
    if Order == 'default' or Order == '':
        Order = "hostIp asc,channelMark asc"
    else:
        _Orders = []
        Orders = {"iptv-id":"channelMark","cdn":"hostIp","iptv-name":"channelName","status":"channelStatus"}
        _Order = Order.split(',')
        for Order in _Order:
            if Order.find('desc') >= 0:
                _Orders.append(Orders.get(Order.split(':')[0],'')+' desc')
            else:
                _Orders.append(Orders.get(Order,'')+' asc')
        Order = ','.join(_Orders)
    db=pymysql.connect("221.4.223.100","channelaction","d0177951d1493f49","cmdb",charset="utf8")
    cursor=db.cursor()
    cursor.execute("SELECT COUNT(*) FROM cdnChannel WHERE ((channelMark REGEXP '"+Iptvid+"') or (channelName REGEXP '"+Iptvid+"'))"+Exp)
    Count=cursor.fetchone()
    cursor.execute("SELECT * FROM cdnChannel WHERE ((channelMark REGEXP '"+Iptvid+"') or (channelName REGEXP '"+Iptvid+"'))"+Exp+" ORDER BY "+Order+" LIMIT "+str((int(Page)-1)*int(Num))+","+str(Num))
    Data=cursor.fetchall()
    cursor.execute("SELECT `language`,channelMark from tvLanguage")
    Languages=cursor.fetchall()
    db.close()
    Pages = math.ceil(int(Count[0])/int(Num))
    Lan = {i[1]:i[0] for i in Languages}
    return {'data':Data,'count':Count[0],'pages':Pages,'lan':Lan}

def GetHost(request):
    db=pymysql.connect("221.4.223.100","channelaction","d0177951d1493f49","cmdb",charset="utf8")
    cursor=db.cursor()
    cursor.execute("SELECT `ip`,`name` FROM `host` WHERE `name` REGEXP '直播|中继'")
    Hosts=cursor.fetchall()
    cursor.execute("SELECT hostIP,count(hostIp) as num FROM cdnChannel group by hostIP")
    Channels=cursor.fetchall()
    cursor.execute("SELECT distinct cdnChannel.hostIp as ip,translation.short as language FROM cdnChannel left join tvLanguage on cdnChannel.channelMark=tvLanguage.channelMark left join translation on tvLanguage.language=translation.english  WHERE tvLanguage.language in ('Chinese','Arabic','French','English','Hindi','Spanish','Kurdish','Vietnamese','Italian','Filipino','Albania') order by cdnChannel.hostip desc")
    Languages=cursor.fetchall()
    cursor.execute("SELECT distinct hostip as ip,series FROM cdnChannel group by hostIP")
    Series=cursor.fetchall()
    db.close()
    Data = []
    for ip in Hosts:
        tmp = {}
        tmp['hostip'] = ip[0]
        tmp['content'] = ip[1].replace(ip[0],'')
        tmp['num'] = ''
        tmp['lan'] = []
        tmp['other'] = ''
        for ch in Channels:
            if ch[0] == ip[0]:
                tmp['num'] = str(ch[1])
        for lan in Languages:
            if lan[0] == ip[0]:
                tmp['lan'].append(lan[1])
        for series in Series:
            if series[0] == ip[0]:
                tmp['other'] = series[1].replace(',',' / ')
        tmp['lan'] = ' / '.join(tmp['lan'])
        Data.append(tmp)
    return Data

def SearchChannel(request):
    Iptvid = request.POST.get('iptv_id','TV')
    Ip = request.POST.get('ip','default')
    Order = request.POST.get('order','')
    Page = request.POST.get('page',1)
    Num = request.POST.get('num',100)
    RawData = GetChannels(Iptvid,Ip,Order,Page,Num)
    Data = {}
    Data['pages'] = RawData['pages']
    Data['count'] = RawData['count']
    Data['data'] = []
    for channel in RawData['data']:
        tmp = {}
        if channel[6] == 1:
            status = "已下发"
        elif channel[6] == 0:
            status = "未下发"
        elif channel[6] == 2:
            status = "下发失败"
        else:
            status = channel[6]
        if channel[7] == 1:
            streamstatus = "正常"
        elif channel[7] == 0:
            streamstatus = "中断"
        else:
            streamstatus = channel[7]
        tmp['tvid'] = channel[9]
        tmp['iptvid'] = channel[2]
        tmp['name'] = channel[3]
        tmp['hostip'] = channel[1]
        tmp['speed'] = channel[8]
        tmp['steamstatus'] = streamstatus
        tmp['sourceurl'] = channel[4].split(',')[0]
        tmp['sourceurls'] = channel[4]
        tmp['currenturl'] = channel[5]
        try:
            tmp['language'] = RawData['lan'][channel[2]]
        except:
            tmp['language'] = ''
        tmp['status'] = status
        Data['data'].append(tmp)
    return Data

def ChannelControl(request):
    Action = request.POST.get('action','')
    User = {"userName":"admin","userPassword":"Q5t0wRLN"}
    LoginUrlFormat = "http://{0}:8180/cms/login.action"
    LogoutUrlFormat = "http://{0}:8180/cms/logout"
    if Action == 'start-ok':
        ActionUrlFormat = "http://{0}:8180/cms/servermonitor/jihuoChannelRecords.action"
    elif Action == 'stop-ok':
        ActionUrlFormat = "http://{0}:8180/cms/servermonitor/stopChannelRecords.action"
    Ids = request.POST.getlist('ids[]',[])
    IpNum,_IpNum = len(Ids),0
    Data,Threads,Tmp = [],{},[]
    for _Ids in Ids:
        Ip,Id = _Ids.split(':')
        LoginUrl = LoginUrlFormat.format(Ip)
        ActionUrl = ActionUrlFormat.format(Ip)
        LogoutUrl = LogoutUrlFormat.format(Ip)
        Threads[Ip] = threading.Thread(target=SendRequest, name=Ip, args=(User,LoginUrl,ActionUrl,LogoutUrl,Id,Data))
        Threads[Ip].start()
    while True:
        for Ip in Threads:
            if Threads[Ip].isAlive() != True and Ip not in Tmp:
                Tmp.append(Ip)
                _IpNum += 1
        if _IpNum == IpNum:
            break
        time.sleep(1)
    ChangeStatus(Action,Data)
    return Data

def SendRequest(User,LoginUrl,ActionUrl,LogoutUrl,Id,Data):
    thread = threading.current_thread()
    threadname = thread.getName()
    session = requests.Session()
    try:
        session.post(url=LoginUrl, data=User, timeout=10)
    except requests.exceptions.ConnectTimeout:
        Data.append(threadname+":登录超时")
    except requests.exceptions.ConnectionError:
        Data.append(threadname+":连接失败")
    except requests.exceptions.ReadTimeout:
        Data.append(threadname+":读取超时")
    else:
        try:
            response = session.post(url=ActionUrl, data={"ids":Id}, timeout=20)
            Data.append(threadname+':'+response.text)
        except requests.exceptions.ConnectTimeout:
            Data.append(threadname+":操作超时，请同步查看结果")
        try:
            session.get(url=LogoutUrl, timeout=5)
        except requests.exceptions.ConnectTimeout:
            pass

def ChangeStatus(Action,Data):
    if Action == 'start-ok':
        n = 1
    elif Action == 'stop-ok':
        n = 0
    SqlPre = "UPDATE cdnChannel SET channelStatus = {0} WHERE "
    SqlMain = []
    for Item in Data:
        Ip,Ids = Item.split(':')
        SqlMain.append("(hostIp='"+Ip+"' AND channelMark IN ('"+Ids.replace(",","','")+"'))")
    Sql = SqlPre.format(n) + " OR ".join(SqlMain)
    db=pymysql.connect("221.4.223.100","channelaction","d0177951d1493f49","cmdb",charset="utf8")
    cursor=db.cursor()
    cursor.execute(Sql)
    db.close()

def Default(request):
    return 'No this action!'

@csrf_exempt
def ChannelActionApi(request):
    if request.POST:
        AUTH_URL = 'http://119.146.223.77:8000/zabbix/user_info.php?sessionid=';
        cb = request.POST.get('cb', '')
        RawResponse = requests.get(AUTH_URL+cb).text
        JsonResult = json.loads(RawResponse.strip("()"))
        AuthResult = JsonResult['return']
        if AuthResult:
            Action = request.POST.get('action','')
            Actions = {'channel':SearchChannel,'host':GetHost,'start-ok':ChannelControl,'stop-ok':ChannelControl}
            Data = Actions.get(Action,Default)(request)
            data = json.dumps(Data)
            return HttpResponse(data, content_type="application/json")
        else:
            data = 'Auth failed!'
            return HttpResponse(data,content_type="text/html")
    else:
        data = 'Null'
        return HttpResponse(data,content_type="text/html")

@csrf_exempt
def ChannelAction(request):
    return render(request, "html/forms/channel.html")