### 登录的方式——selenium 或 request ？

request的方式通过发送请求完成校园网的登录，需要分析校园网页面的源码以构造请求所需的参数，在github上有同学尝试过：[huxiaofan1223/jxnu_srun: 深澜认证协议 (github.com)](https://github.com/huxiaofan1223/jxnu_srun) ，[realZnS/jxnu-srun-go: 江西师范大学校园网登录脚本 (github.com)](https://github.com/realZnS/jxnu-srun-go) 等。

但现在校园网更新了，从网页中分析并构造参数变得困难。另一方面，selenium是一种更便捷的方式，通过模拟用户操作网页的过程对网页进行控制实现登录过程。省去了request复杂的参数分析过程，因而这个工具中选用selenium。

### 网络的连接

python中有piwifi库可用于wifi连接的处理，使用这个库连接网络的方式大致如下：

```python
profile = pywifi.Profile()
profile.ssid = 'testap'
profile.auth = const.AUTH_ALG_OPEN
profile.akm.append(const.AKM_TYPE_WPA2PSK)
profile.cipher = const.CIPHER_TYPE_CCMP
profile.key = '12345678'

iface.remove_all_network_profiles()
tmp_profile = iface.add_network_profile(profile)
```

首先需要创建一个Profile示例，进行配置。这个可以通过`iface = wifi.interfaces()[0]; iface.scan_results()`获取对应wifi信息进行配置。但随后的步骤`iface.remove_all_network_profiles()`会把所有WIFI的配置信息丢弃掉，于是WIFI的密码都丢失了，这是很不方便的操作。

之后了解到`netsh`命令可以完成网络的连接，所以在这个工具中采用`netsh`来完成网络连接过程，更加方便有效。

### 用ping检测网络

最开始是通过urllib3.request发送网络请求看是否出现异常来判断网络状况，但request会重复3次，测试的很慢，所以就弃用了，后面采用ping的方式进行网络检测。

但ping其实也存在一些问题。我的电脑是开了代理的，然后开启了 TUN 模式，在这个模式下，ping的检测失效了。具体来说，当我断开网络后，ping发送的icmp包会传输到TUN虚拟出来的网卡上，由于某种特殊的原因，即使断网了ping的返回值依然正常，使得检测失效。

> 当使用wireshark进行抓包时（通过 icmp and ip.dest_host过滤），会发现ping命令的包并不能被捕获，所以也无法进行分析。而在终端上 ping 的执行始终是正常的。

对于这个问题，有两种解决方式：一种是关闭clash的 TUN 模式，另一种是采用request的方式来检测网络，为了使网络检测更通用一些，这里采用第二种方式，后面调整了代码不至于特别慢。

关于clash tun mode，这里有一个相关视频：[【进阶•代理模式篇】看懂就能解决99%的代理问题，详解系统代理、TUN/TAP代理、真VPN代理，clash/v2ray/singbox 虚拟网卡怎么接管系统全局流量？什么是真正的VPN？看完就知道了 - YouTube](https://www.youtube.com/watch?v=qItL005LUik&t=302s)

在第二种方式中，先尝试访问测试地址，如果访问失败，则认为网络断开了。在测试的时候遇到过一个问题：`HTTPSConnectionPool(host='baidu.com', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLEOFError(8, 'EOF occurred in violation of protocol (_ssl.c:1129)`。因为HTTPS是http over SSL，所以需要经过SSL认证，这里的测试地址是https://www.baidu.com，在没有网络的情况下访问可能会出现这个错误，于是将测试地址改为了http://example.com，这是一个常用的测试网站，然后安装了certifi包。但不确定是否解决了这个问题，后面这个问题自己消失了（有时候复现一个问题也挺麻烦的），就没去管了。

### 运行结果的编码问题

通过`subprocess.run`运行netsh获取网络信息时，需要对返回的结果解码，按理说使用和系统编码一致的方式解码就好了，但却经常出现问题。使用`chcp`查看系统编码方式是`gbk`的，但用于解码返回结果时却出现如下错误：
```
result = subprocess.run("netsh wlan show network",
                            shell=True, stdout=subprocess.PIPE, 
                            text=True, encoding='gbk')
Traceback (most recent call last):
  File "c:\Users\Administrator\Desktop\login_jxnu\try.py", line 4, in <module>
    result = subprocess.run("netsh wlan show network",
  File "D:\development\anaconda\envs\deep-todo\lib\subprocess.py", line 507, in run
    stdout, stderr = process.communicate(input, timeout=timeout)
  File "D:\development\anaconda\envs\deep-todo\lib\subprocess.py", line 1121, in communicate
    stdout = self.stdout.read()
UnicodeDecodeError: 'gbk' codec can't decode byte 0xb5 in position 229: illegal multibyte sequence
```
即使换成`utf-8`有时也会出错，这个问题很不稳定，有时正常有时出错。

后面的一个做法是先不对结果进行解码，将返回结果存放在一个临时文件中，然后从文件中读取结果，但打开文件的过程中其实也需要进行对文件内容进行解码，比如open(file_name, encoding="utf-8")，省略encoding参数时会使用默认的方式解码。

不管怎么做，都要经过解码过程，而合适的解码方式又是不确定的，使得这个问题暂时没法解决。

不过可以对这个错误进行异常处理，出现的时候就说“编码错误，无法显示”，这样不至于中断程序的执行。
