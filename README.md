## 江西师大校园网自动重连工具

### 🤔为什么搞这个小工具

校园网不稳定，时常自动断网，如果有远程控制的需求，那么断网是一件很麻烦的事情；虽然windows中有自动连接网络的选项，但有时候不起作用。

### 💡功能

+ 提供便捷的selenium模拟登录方式，不易因校园网升级后请求参数的变化而失效；
+ 自动化的进行网络状态的检测，并在网络中断后自动完成重新连接过程；
+ 除尝试自动连接校园网外，也可以尝试连接wifi列表中的其他可用网络；

### 🔧使用方式

step1: 环境安装：
```python
pip install -r requirements.txt
```
step2: 安装edgedirver
由于这个工具是使用selenium模拟浏览器进行登录的，所以需要有一个浏览器辅助工具：从设置中找到Edge的版本号(edge://settings/help)，再从[Microsoft Edge WebDriver - Microsoft Edge Developer](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)找到对应版本的EdgeDriver，并将其路径添加到环境变量中。

step3: 在main.py中设置校园网信息并运行

```python
python main.py
```



### 
