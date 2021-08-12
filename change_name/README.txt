0.2更新20201105：
1、添加新参数<ser_ip>，可单独指定服务器进行进行来源，名称的更新

>>>>>>>>>>>>>>>>>
说明：
1、本脚本执行python版本为：python3

2、Modify_information.xlsx表中第一列为需要修改的频道，第二列为需要修改的对应信息
目前有多个参数可以修改tv_name代表名称，origin代表备注，格式如下（需要修改的内容中不能包含英文单引号）

tv_name=XXX,origin=XXX,ser_ip=XXX

3、	
在login.txt内添加账户名称，密码（第一行名称，第二行密码）；
Modify_information.xlsx表格中添加需要修改的节目信息，按照2中的格式，表格中已有一个例子；
batch_modification.py为执行脚本。