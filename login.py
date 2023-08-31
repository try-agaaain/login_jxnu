import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium import webdriver

def add_args_for_options(options, args):
    for arg in args:
        options.add_argument(arg)

def check_avaliable_browser(args):
    try:
        options = webdriver.ChromeOptions()
        add_args_for_options(options, args)
        driver = webdriver.Chrome(options=options)
        return driver
    except Exception as _:
        print(_)
        try:
            options = webdriver.EdgeOptions()
            add_args_for_options(options, args)
            driver = webdriver.Edge(options=options)
            return driver
        except Exception as _:
            print(_)
            try:
                options = webdriver.FirefoxOptions()
                add_args_for_options(options, args)
                driver = webdriver.Firefox()
                return driver
            except Exception as _:
                return None

def login(user_account, user_password, jxnu_url, domain='移动'):
    options = webdriver.EdgeOptions()
    args = ["--headless", "--no-proxy-server"]
    add_args_for_options(options, args)
    driver = webdriver.Edge(options=options)
    driver.get(jxnu_url)

    domain_select = {
        '移动': '@cmcc',
        '联通': '@cucc',
        '电信': '@ctcc',
        '校园带宽': '@jxnu'
    }
    domain_select = domain_select.get(domain)
    assert domain_select, "运行商选择错误，请重新选择！"
    domain = Select(driver.find_element("id", 'domain'))
    domain.select_by_value(domain_select)
    account = driver.find_element('id', 'username')
    password = driver.find_element('id', 'password')
    submit = driver.find_element('id', 'login-account')

    account.send_keys(user_account)
    password.send_keys(user_password)
    submit.click()
    time.sleep(1)
    driver.close()

if __name__ == "__main__":
    account = "学号"
    password = "校园网密码"
    domain = "运营商"
    jxnu_url= "http://172.16.8.8/srun_portal_pc?ac_id=1&theme=pro"
    login(account, password, jxnu_url, domain)
