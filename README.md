# NodeGo 挂机脚本

适用于VPS等固定IP地址的挂机脚本，本脚本使用Python编写，依赖于pm2进程监控。



## 安装及设置

1. 安装Python依赖

   ~~~shell
   git clone path/to/NodeGo
   
   sudo apt update
   sudo apt upgrade
   sudo apt install python3 python3-pip python3-venv
   
   cd path/to/NodeGo
   python3 -m venv myenv
   pip install requests
   ~~~

   安装pm2 

   ~~~shell
   npm install pm2 -g
   ~~~

2. 配置accessToken.txt

   进入https://app.nodego.ai/ 界面，F12打开控制台，将accessToken的值复制到accessToken.txt，注意不要带有引号

   ![image-20250227153253912](https://typora-mine.oss-cn-beijing.aliyuncs.com/typoraimage-20250227153253912.png)

## 运行

使用pm2进行管理

~~~shell
pm2 start NodeGo.py
~~~



查看运行日志

~~~shell
pm2 log NodeGo
~~~



