#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

const char *ssid = "wdxxl";     // 网络名称
const char *password = "88888888"; // 网络密码

IPAddress local_IP(192,168,3,50);
IPAddress gateway(192,168,3,1);
IPAddress subnet(255,255,255,0);


WiFiUDP Udp;
unsigned int localUdpPort = 1139; // 本地端口号
char incomingPacket[537];         // 接收缓冲区

unsigned long previousMillis = 0; // 上次检查WiFi状态的时间
const long interval = 10000;      // 检查间隔时间（毫秒）

void setup()
{
  pinMode(2, OUTPUT);
  Serial.begin(115200);
  Serial.println();
  Serial.printf("Connecting to %s ", ssid);
  WiFi.mode(WIFI_STA);
  WiFi.setAutoConnect(false);
  WiFi.begin(ssid, password);
  WiFi.config(local_IP, gateway, subnet);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(2000);
    Serial.print(".");
  }
  Serial.println(" connected");

  Udp.begin(localUdpPort);
  Serial.printf("Now listening at IP %s, UDP port %d\n", WiFi.localIP().toString().c_str(), localUdpPort);
}

void loop()
{
  unsigned long currentMillis = millis(); // 获取当前时间

  // 检查WiFi状态
  if (currentMillis - previousMillis >= interval)
  {
    previousMillis = currentMillis; // 更新上次检查时间
    if (WiFi.status() != WL_CONNECTED)
    {
      Serial.println("WiFi connection lost. Reconnecting...");
      setup();
    }
  }

  int packetSize = Udp.parsePacket(); // 获取当前队首数据包长度
  if (packetSize)                     // 有数据可用
  {
    Serial.printf("Received %d bytes from %s, port %d\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());
    int len = Udp.read(incomingPacket, 536); // 读取数据到incomingPacket
    if (len > 0)                             // 如果正确读取
    {
      incomingPacket[len] = 0; // 末尾补0结束字符串
      Serial.printf("UDP packet contents: %s\n", incomingPacket);

      if (strstr(incomingPacket, "light=on") != NULL) // 如果收到Turn off
      {
        digitalWrite(2, LOW); // 熄灭LED
        Serial.printf("light-on\n");
        // Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
        // Udp.write("LED has been turn off"); // 回复LED has been turn off
        // Udp.endPacket();
      }
      else if (strcmp(incomingPacket, "light=off") == 0) // 如果收到Turn on
      {
        digitalWrite(2, HIGH); // 点亮LED
        Serial.printf("light-off\n");
        // Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
        // Udp.write("LED has been turn on"); // 回复LED has been turn on
        // Udp.endPacket();
      }
      else // 如果非指定消息
      {
        Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
        Udp.write("Data Error!"); // 回复Data Error!
        Udp.endPacket();
      }
    }
  }
}
