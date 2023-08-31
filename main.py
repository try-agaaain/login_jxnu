import time

from utils import net_is_connected, connect_to_wifi, get_time
from login import login

def main(wifi_list, account, password, jxnu_url, domain):
    if not net_is_connected():
        for wifi_name in wifi_list:
            try:
                print(f"[{get_time()}] 网络已断开，尝试连接{wifi_name}...")
                success = connect_to_wifi(wifi_name)
                if success:
                    if "jxnu_stu" in wifi_name:
                        print(f"[{get_time()}] {wifi_name} 可用，正在登录校园网...")
                        login(account, password, jxnu_url, domain)
                    else:
                        print(f"[{get_time()}] {wifi_name} 可用，测试网络是否连接...")
                    if net_is_connected():
                        print(f"[{get_time()}] 已成功连接网络...\n\n\n")
                        break
                    else:
                        print(f"[{get_time()}] 未能成功连接网络，即将再次尝试...")
                else:
                    print(f"[{get_time()}] {wifi_name} 不可用，即将再次尝试...")
            except Exception as err:
                print(err)
    else:
        time.sleep(60)

if __name__ == "__main__":
    wifi_list = ["4405-5G", "X4408-AI"]
    account = "学号"
    password = "校园网密码"
    domain = "运营商"
    jxnu_url= "http://172.16.8.8/srun_portal_pc?ac_id=1&theme=pro"
    print(f"[{get_time()}] 开始执行...")
    while True:
        main(wifi_list, account, password, jxnu_url, domain)
