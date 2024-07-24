使用 8266+DC继电器+旧USB台灯+旧机顶盒连接巴法云，使用小爱同学控制灯泡开关
原本是使用8266直接串接TCP连接至巴法云，但是8266使用micropython 时处理能力有点弱鸡，刚好手上有废弃机顶盒可以刷armbian，就使用旧机顶盒与巴法云进行通信，再把收到的消息转发到内网的8266设备上。

1、旧机顶盒刷ARMBIAN 教程地址：https://www.ecoo.top   这个配合DDNS可以搭建自己的远程服务器及NAS文件共享
2、8266刷入micropython固件参考：https://zhuanlan.zhihu.com/p/101632278
3、登录https://cloud.bemfa.com/ 注册巴法云账号，使用邮箱注册，新建主题（米家同步设备的时候使用邮箱绑定同步）。
![image](https://github.com/user-attachments/assets/d981900f-dcd8-4deb-9f7d-26733429c4f8)  
4、新建完主题，打开米家APP，选择我的->添加其他平台设备->找到巴法云->绑定账号，绑定后就能看到设备了。如果没看到设备，先确认添加的主题是不是以002结尾，再同步设备。
5、将localservice.py 放入armbian内运行，可以使用crontab -e 设置设备重启后自动运行。======脚本内加入try捕获异常，除非机顶盒负载严重自动清理内存，一般不会掉线
8266连线图如下：
之前被卖家坑了，叫接的电源是3.3V的接口，一直调不通，用万用表测了才发现电源接的有问题
8266连线：
![image](https://github.com/user-attachments/assets/6404380c-9c5c-4e71-a52a-abfff3bd3bc3)

继电器连线：
![image](https://github.com/user-attachments/assets/28d19ca5-bf43-466a-9f4e-8fb1415f74c3)

我的连线：
直接使用板载5V作为灯泡的电源
![image](https://github.com/user-attachments/assets/64337c56-f538-40e9-b64f-a2f895dbc8d8)

这样就可以使用小爱同学控制灯泡的开关了：
![8467743fc2a01b986d0913faacb504c](https://github.com/user-attachments/assets/83d31246-b06c-4a7c-a3e8-a76042d175ee)






