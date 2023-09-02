import time

from auto_connect.utils import connect_to_wifi, get_time, get_wifi_list
from auto_connect.utils import net_is_connected2 as net_is_connected
from auto_connect.login import login

def begin():
    print(f"\n[{get_time()}] 可用的wifi列表：", end="\n")
    for wifi in get_wifi_list():
        print(f"{wifi:14s}", end="    ")
    print(end="\n")
    if net_is_connected:
        print(f"[{get_time()}] 当前网络连接正常...", end="\n")
    else:
        print(f"[{get_time()}] 当前网络未连接...", end="\n")

def main(wifi_list, account, password, jxnu_url, domain):
    if not net_is_connected():
        for wifi_name in wifi_list:
            print(f"[{get_time()}] 网络已断开，尝试连接{wifi_name}...")
            if connect_to_wifi(wifi_name):
                if "jxnu_stu" in wifi_name:
                    print(f"[{get_time()}] {wifi_name} 可用，正在登录校园网...")
                    if net_is_connected():
                        print(f"[{get_time()}] 已成功连接网络...\n")
                        break
                    elif login(account, password, jxnu_url, domain):
                        print(f"[{get_time()}] 已成功登录校园网...\n")
                    else:
                        print(f"[{get_time()}] 未能成功连接网络，5秒后重试...\n")
                else:
                    print(f"[{get_time()}] {wifi_name} 可用，测试网络是否连接...")
                if net_is_connected():
                    print(f"[{get_time()}] 已成功连接网络...\n")
                    break
                else:
                    print(f"[{get_time()}] 未能成功连接网络，5秒后重试...")
            else:
                print(f"[{get_time()}] {wifi_name} 不可用，5秒后重试...")
            time.sleep(5)
    else:
        time.sleep(60)

if __name__ == "__main__":
    # 之前连接过的可用WIFI，例如：["jxnu_stu_123", "4405", "X4408-AI"]，靠前的优先级更高
    wifi_list = ["wifi_name1", "wifi_name2", "wifi_name3"] 
    account = "学号"
    password = "校园网密码"
    domain = "运营商"   # 移动|联通|电信|校园带宽
    jxnu_url= "http://172.16.8.8/srun_portal_pc?ac_id=1&theme=pro"  # 校园网登录地址
    begin()
    while True:
        main(wifi_list, account, password, jxnu_url, domain)
