import asyncio
import socket
import select


UDP_IP = '192.168.1.50'               #8266设备
UDP_PORT = 1139                       #8266 UDP 端口
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
uuid = xxxxxxxxxxxxxxxxxxxxx   #巴法云获取UUID
topic = light002     #创建的主题 002结尾的为灯泡设备 


async def send_udp_data(message):
    try:
        udp_socket.sendto(message.encode('utf-8'), (UDP_IP, UDP_PORT))
        print(f"发送 UDP 数据: {message} 到 {UDP_IP}:{UDP_PORT}")
    except Exception as e:
        print(f"发送 UDP 数据失败: {e}")
async def connTCP():
    global tcp_client_socket
    # 创建socket
    tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_client_socket.setblocking(False)  # 设置为非阻塞模式

    # 巴法云 IP 和端口
    server_ip = 'bemfa.com'
    server_port = 8344

    while True:
        try:
            # 尝试连接服务器
            tcp_client_socket.connect((server_ip, server_port))
            # 发送订阅指令
            substr = f'cmd=1&uid={uuid}&topic={topic}'+'\r\n'
            tcp_client_socket.send(substr.encode("utf-8"))
            break  # 连接成功，跳出循环
        except BlockingIOError:
            await asyncio.sleep(2)  # 连接失败，等待重试
        except Exception as e:
            print(f"连接失败: {e}")
            await asyncio.sleep(2)  # 其他异常，等待重试

async def ping():
    while True:
        # 发送心跳
        try:
            keeplive = 'ping\\r\\n'
            tcp_client_socket.send(keeplive.encode("utf-8"))
        except Exception as e:
            print(f"发送心跳失败: {e}")
            await connTCP()  # 重新连接
        await asyncio.sleep(30)  # 每30秒发送一次心跳

async def receive_data():
    while True:
        try:
            # 使用 select 检查 socket 是否可读
            ready_to_read, _, _ = select.select([tcp_client_socket], [], [], 1)
            if ready_to_read:
                # 接收服务器发送过来的数据
                recvData = tcp_client_socket.recv(1024)
                if len(recvData) != 0:
                    value = recvData.decode('utf-8')
                    print('recv:', value)
                    if 'msg=off' in value:
                        await send_udp_data("msg=off")
                    elif 'msg=on' in value:
                        await send_udp_data("msg=on")
                        
                else:
                    print("连接错误，重新连接")
                    await connTCP()  # 重新连接
            else:
                print("没有数据可读，继续等待...")
        except Exception as e:
            print(f"接收数据失败: {e}")
            await connTCP()  # 重新连接
        await asyncio.sleep(1)  # 等待一段时间再尝试接收数据
async def main():
    await connTCP()  # 初始连接
    await asyncio.gather(ping(), receive_data())  # 同时运行心跳和接收数据

# 运行主程序
if __name__ == "__main__":
    asyncio.run(main())
