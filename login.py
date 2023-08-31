import time
from selenium import webdriver 
from selenium.webdriver.support.ui import Select
from selenium import webdriver


def login(user_account, user_password, jxnu_url):
    options = webdriver.EdgeOptions()
    # options.add_argument('--headless')
    options.add_argument('--no-proxy-server')
    driver = webdriver.Edge(options=options)
    print("begin...")
    driver.get(jxnu_url)
    # time.sleep(20)
    domain = Select(driver.find_element("id", 'domain'))
    domain.select_by_value('@cmcc')
    account = driver.find_element('id', 'username')
    password = driver.find_element('id', 'password')
    submit = driver.find_element('id', 'login-account')

    account.send_keys(user_account)
    password.send_keys(user_password)
    
    submit.click()
    driver.close()

if __name__ == "__main__":
    account = "学号"
    password = "校园网密码"
    jxnu_url= "http://172.16.8.8/srun_portal_pc?ac_id=1&theme=pro"
    login(account, password, jxnu_url)