import re
import subprocess
import time
import requests


from urllib3 import PoolManager, Retry
from urllib3.exceptions import HTTPError

from auto_connect import DEBUG_ENABLE

def connect_to_wifi(wifi_name):
    result = subprocess.run("netsh wlan show network",
                            shell=True, stdout=subprocess.PIPE, text=True)
    pattern = r'SSID[^:]+: (.+?)\n'
    wifi_list = re.findall(pattern, result.stdout)
    if wifi_name not in wifi_list:
        return False
    cmd = f"netsh wlan connect name={wifi_name}"
    ret = subprocess.run(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(5)   # 等待两秒，等待网络状态更新
    return True if ret.returncode == 0 else False


def get_time():
    time_info = time.localtime(time.time())
    cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time_info)
    return cur_time


def net_is_connected(test_address="http://example.com/"):
    retries = Retry(connect=1, read=1, redirect=1)
    http = PoolManager(retries=retries)
    try:
        http.request("GET", test_address, retries=False)
        return True
    except HTTPError as err:
        debug(err)
        return False


def net_is_connected2(test_address="http://example.com/"):
    requests.DEFAULT_RETRIES = 1
    try:
        requests.request("GET", test_address, verify=False)
        return True
    except Exception as err:
        debug(err)
        return False


def net_is_connected3(test_domain='baidu.com'):
    cmd = f"ping {test_domain} -n 1"
    ret = subprocess.run(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return True if ret.returncode == 0 else False

def debug(info):
    if DEBUG_ENABLE:
        print(f"[{get_time()}] debug: 出现如下错误\n{info}")

if __name__ == "__main__":
    net_is_connected()
    # connect_to_wifi("jxnu_stu")
