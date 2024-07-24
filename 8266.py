import network
import socket
import time
import machine

led1=Pin(2,machine.Pin.OUT)  #控制板载LED与灯泡同步
# Wi-Fi 配置
SSID = 'your_ssid'  # 替换为你的 Wi-Fi 名称
PASSWORD = 'your_password'  # 替换为你的 Wi-Fi 密码

# 固定 IP 配置
STATIC_IP = '192.168.1.50'  # 固定IP地址   与服务器在同一网段
SUBNET_MASK = '255.255.255.0'  # 24 位子网掩码
GATEWAY = '192.168.1.1'    # 网关

# 连接 Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
	wlan.active(False)
	time.sleep(1)
    wlan.active(True)
    wlan.ifconfig((STATIC_IP, SUBNET_MASK, GATEWAY, GATEWAY))  # 设置静态 IP
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        print("正在连接 Wi-Fi...")
        time.sleep(1)
    print("Wi-Fi 连接成功:", wlan.ifconfig())
    return wlan

# 创建 UDP socket 监听指定端口
def create_udp_socket(port=1139):  #指定监听端口为1139
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('', port))
    print(f"UDP socket 监听在端口 {port}")
    return udp_socket

# 检查 Wi-Fi 状态
def check_wifi_status(timer):
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        connect_wifi()

# 主程序
def main():
    connect_wifi()  # 连接 Wi-Fi
    udp_socket = create_udp_socket()  # 创建 UDP socket
    # 设置定时器，每20秒检查一次 Wi-Fi 状态
    machine.Timer(0).init(period=20000, mode=machine.Timer.PERIODIC, callback=check_wifi_status)
    while True:
        # 接收 UDP 数据
        try:
            data, addr = udp_socket.recvfrom(1024)  # 接收数据
			if data:
				res = data.decode('utf-8')
				print(f"接收到来自 {addr} 的数据: {res}")
				if 'msg=on' in res:
					led1.value(0)     #与字面意思相反，0才是高电平,开灯
				if ‘msg=off’in res:
					led1.value(1)     #关灯
					
        except Exception as e:
            print(f"接收数据时发生错误: {e}")

# 运行主程序
if __name__ == "__main__":
    main()
