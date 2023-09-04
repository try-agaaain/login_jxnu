import re
import subprocess
import time
import requests
import os
import sys
import subprocess

from urllib3 import PoolManager, Retry
from urllib3.exceptions import HTTPError

from auto_connect import DEBUG_ENABLE

# 处理命令运行过程中的编码问题：https://stackoverflow.com/a/67778646/22487325
def run_command_deprecated(cmd):
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    command = f"Set PYTHONUTF8=1 & {cmd}"
    result = subprocess.run(
        command, stdout=subprocess.PIPE, shell=True, encoding="utf-8")
    return result

def run_command(cmd):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    save_path = f"{current_directory}/temp.txt"
    ret = subprocess.run(f'{cmd} > {save_path}', shell=True)
    try:
        with open(save_path, 'rb') as file:
            output = file.read().decode('utf-8', errors='ignore')
        return ret.returncode, output
    except UnicodeDecodeError as _:
        return ret.returncode, None

def get_wifi_list():
    _, output = run_command("netsh wlan show networks")
    # 当出现编码错误时，output 为 None
    if output is None:
        return None
    pattern = r'SSID[^:]+: ([^\\ \r]+)'
    # 当没有匹配内容时，wifi_list 为 []
    wifi_list = re.findall(pattern, output)
    return wifi_list


def get_avaliable_networks():
    _, avaliable_wifi = run_command("netsh wlan show profile")
    return avaliable_wifi


def connect_to_wifi(wifi_name):
    wifi_list = get_wifi_list()
    if wifi_list is not None and wifi_name not in wifi_list:
            return False
    cmd = f"netsh wlan connect name={wifi_name}"
    returncode, _ = run_command(cmd)
    time.sleep(5)   # 等待两秒，等待网络状态更新
    return True if returncode == 0 else False


def fprint_info(info, end="\n"):
    time_info = time.localtime(time.time())
    cur_time = time.strftime("%Y-%m-%d %H:%M:%S", time_info)
    print(f"[{bold_text(cur_time)}] {info}", end=end)


def underline_text(text):
    os.system("")
    return f"\033[4m{text}\033[0m"

def bold_text(text):
    # 处理escape sequence失效的问题：https://stackoverflow.com/a/77027374/22487325
    os.system("")
    return f"\033[1m{text}\033[0m"

def ellipsis(text):
    if len(text) > 16:
        text = text[:13] + "..."
    return text

def net_is_connected(test_address="http://example.com/"):
    retries = Retry(connect=5, read=2, redirect=5)
    http = PoolManager(retries=retries)
    try:
        http.request("GET", test_address, retries=False)
        return True
    except HTTPError as err:
        debug(err)
        return False


def net_is_connected2(test_address1="http://www.baidu.com/"):
    requests.DEFAULT_RETRIES = 1
    try:
        res = requests.request("GET", test_address1,
                               verify=False, allow_redirects=False)
        if res.status_code == 200:
            return True
        return False
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
        fprint_info(f"debug: 出现如下错误\n{info}")


if __name__ == "__main__":
    net_is_connected2()
    # connect_to_wifi("jxnu_stu")
