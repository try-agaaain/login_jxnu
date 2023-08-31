import subprocess
import time

def connect_to_wifi(wifi_name):
    cmd = f"netsh wlan connect name={wifi_name}"
    ret = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2)   # 等待两秒，等待网络状态更新
    return True if ret.returncode==0 else False

def get_time():
    time_info = time.localtime(time.time())
    cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time_info)
    return cur_time


def net_is_connected(test_domain='baidu.com'):
    cmd = f"ping {test_domain} -n 1"
    ret = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return True if ret.returncode==0 else False
