import time

from utils import net_is_connected, connect_to_wifi, get_time
from login import login

def main(wifi_list, account, password, jxnu_url):
    success = net_is_connected()
    if not success:
        for wifi_name in wifi_list:
            try:
                print(f"[{get_time()}] 网络已断开，尝试连接{wifi_name}...")
                success = connect_to_wifi(wifi_name)
                if success:
                    print(f"[{get_time()}] 已连接到{wifi_name}，正在登录校园网...")
                else:
                    print(f"[{get_time()}] 无法连接到 {wifi_name}，即将再次尝试...")
                login(account, password, jxnu_url)
                if net_is_connected():
                    print(f"[{get_time()}] 已成功登录校园网...\n\n\n")
                    break
                else:
                    print(f"[{get_time()}] 未能成功连接网络，尝试连接{wifi_name}...")
            except Exception as err:
                print(err)
    else:
        time.sleep(60)

if __name__ == "__main__":
    wifi_list = ["jxnu_stu"]
    account = "学号"
    password = "校园网密码"
    jxnu_url= "http://172.16.8.8/srun_portal_pc?ac_id=1&theme=pro"
    print(f"[{get_time()}] 开始执行...")
    while True:
        main(wifi_list, account, password, jxnu_url)
