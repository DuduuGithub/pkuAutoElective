from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import random

def get_next_image_number(directory):
    """获取下一个可用的图片编号"""
    existing_files = os.listdir(directory)
    numbers = [int(f.split('.')[0]) for f in existing_files if f.endswith('.png')]
    return max(numbers, default=0) + 1 if numbers else 1

def main():
    # 数据保存目录
    save_dir = "captcha/data"
    os.makedirs(save_dir, exist_ok=True)

    edge_driver_service=Service('D:\code\project\pkuAutoElective\edgeDriver\edgedriver_win64\msedgedriver.exe')
    driver=webdriver.Edge(service=edge_driver_service)

    driver.get("https://elective.pku.edu.cn/")

    wait=WebDriverWait(driver,30)

    # 登录
    account_input=wait.until(EC.presence_of_element_located((By.ID, "user_name")))
    account_input.send_keys("2300016603")

    password_input=wait.until(EC.presence_of_element_located((By.ID, "password")))
    password_input.send_keys("wangchenshuo0506")

    login_button=wait.until(EC.presence_of_element_located((By.ID, "logon_button")))
    login_button.click()

    next_number=0
    
    # 循环点击补退选
    while next_number<1000:
        next_url_element=wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/table[1]/tbody/tr/td/ul/li[4]/a")))
        next_url_element.click()
        
        # 等待验证码元素出现
        captcha_element = wait.until(
            EC.presence_of_element_located((By.ID, "imgname"))
        )
        # 获取下一个可用的图片编号
        next_number = get_next_image_number(save_dir)
        
        # 保存验证码图片
        captcha_element.screenshot(f"{save_dir}/{next_number}.png")
        print(f"已保存验证码图片: {next_number}.png")

        # 随机等待一段时间后继续
        random_wait = random.uniform(0.5, 1)
        time.sleep(random_wait)
        


if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            print(f"发生错误: {str(e)}")
            print("程序将在3秒后重新启动...")
            time.sleep(3)
