import time

from auto_connect.utils import net_is_connected3, connect_to_wifi, get_time
from auto_connect.login import login

def main(wifi_list, account, password, jxnu_url, domain):
    if not net_is_connected3():
        for wifi_name in wifi_list:
            print(f"[{get_time()}] 网络已断开，尝试连接{wifi_name}...")
            if connect_to_wifi(wifi_name):
                if "jxnu_stu" in wifi_name:
                    print(f"[{get_time()}] {wifi_name} 可用，正在登录校园网...")
                    if net_is_connected3():
                        print(f"[{get_time()}] 已成功连接网络...\n")
                        break
                    elif login(account, password, jxnu_url, domain):
                        print(f"[{get_time()}] 已成功登录校园网...\n")
                    else:
                        print(f"[{get_time()}] 未能成功连接网络，即将再次重试...\n")
                else:
                    print(f"[{get_time()}] {wifi_name} 可用，测试网络是否连接...")
                if net_is_connected3():
                    print(f"[{get_time()}] 已成功连接网络...\n")
                    break
                else:
                    print(f"[{get_time()}] 未能成功连接网络，即将再次尝试...")
            else:
                print(f"[{get_time()}] {wifi_name} 不可用，即将再次尝试...")
                
    else:
        time.sleep(60)

if __name__ == "__main__":
    wifi_list = ["jxnu_stu", "4405", "X4408-AI"]    # 本机可连接的WIFI列表
    account = "学号"
    password = "校园网密码"
    domain = "运营商"   # 移动|联通|电信|校园带宽
    jxnu_url= "http://172.16.8.8/srun_portal_pc?ac_id=1&theme=pro"  # 校园网登录地址
    print(f"[{get_time()}] 开始执行...")
    while True:
        main(wifi_list, account, password, jxnu_url, domain)
