import subprocess
import time
import requests

from urllib3 import PoolManager, Retry
from urllib3.exceptions import HTTPError
def connect_to_wifi(wifi_name):
    cmd = f"netsh wlan connect name={wifi_name}"
    ret = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2)   # 等待两秒，等待网络状态更新
    return True if ret.returncode==0 else False

def get_time():
    time_info = time.localtime(time.time())
    cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time_info)
    return cur_time

def net_is_connected(test_address="https://www.baidu.com/"):
    retries = Retry(connect=1, read=1, redirect=1)
    http = PoolManager(retries=retries)
    try:
        http.request("GET", test_address, retries=False)
        return True
    except HTTPError as err:
        print(f"[{get_time()}] 出现如下错误，即将再次尝试...{err}")
        return False

def net_is_connected2(test_address="https://www.baidu.com"):
    requests.DEFAULT_RETRIES = 1
    try:
        requests.request("GET", test_address, verify=False)
        return True
    except Exception as err:
        print(f"[{get_time()}] 出现如下错误，即将再次尝试...\n{err}")
        return False

if __name__ == "__main__":
    net_is_connected()
