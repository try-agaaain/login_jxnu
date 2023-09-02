import time

from auto_connect.utils import underline_text, connect_to_wifi, fprint_info, get_wifi_list
from auto_connect.utils import net_is_connected2 as net_is_connected
from auto_connect.login import login

def begin(test_address = "http://www.baidu.com"):
    test_address_u = underline_text(test_address)
    fprint_info("可连接的wifi列表如下：")
    WIFIs = get_wifi_list()
    if WIFIs != "err":
        for index, wifi in enumerate(WIFIs):
            print(f"{wifi:<15s}", end="  |  ")
            if (index+1) % 4 == 0:
                print(end="\n")
        print(end="\n")
    else:
        print("<编码错误，无法显示>")
    if net_is_connected():
        fprint_info(f"测试地址 {test_address_u} 可正常访问，每60秒重复一次检测...")
    else:
        fprint_info(f"测试地址 {test_address_u} 访问失败，当前网络未连接...")

def main(wifi_list, account, password, jxnu_url, domain,
                    test_address = "http://www.baidu.com"):
    test_address_u = underline_text(test_address)
    if not net_is_connected(test_address):
        for wifi_name in wifi_list:
            fprint_info(f"网络已断开，尝试连接{wifi_name}...")
            if connect_to_wifi(wifi_name):
                if "jxnu_stu" in wifi_name:
                    fprint_info(f"{wifi_name} 可用，正在登录校园网...")
                    if net_is_connected(test_address):
                        fprint_info(f"测试地址 {test_address_u} 可正常访问，已成功登录校园网...\n")
                        break
                    elif login(account, password, jxnu_url, domain) and net_is_connected(test_address):
                        fprint_info(f"测试地址 {test_address_u} 可正常访问，已成功登录校园网...\n")
                    else:
                    else:
                        fprint_info(f"测试地址 {test_address_u} 访问失败，5秒后重试...\n")
                else:
                else:
                        fprint_info(f"测试地址 {test_address_u} 访问失败，5秒后重试...\n")
                else:
                    fprint_info(f"{wifi_name} 可用，测试网络是否连接...")
                if net_is_connected(test_address):
                    fprint_info(f"测试地址 {test_address_u} 可正常访问，网络已连接...\n")
                    break
                else:
                    fprint_info(f"测试地址 {test_address_u} 访问失败，5秒后重试...\n")
            else:
                fprint_info(f"测试地址 {test_address_u} 访问失败，5秒后重试...\n")
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
