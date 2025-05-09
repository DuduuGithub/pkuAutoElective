from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
from emailSend import send_email
import random
from sound import play_music

def available_course(enrollment):
    total,current = map(int, enrollment.split('/'))
    return total-current


def main():
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

    # 进入补退选页面
    next_url_element=wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/table[1]/tbody/tr/td/ul/li[4]/a")))
    next_url_element.click()

    # 开始循环翻页监测
    select_element = wait.until(
        EC.presence_of_element_located((By.XPATH, "/html/body/table[2]/tbody/tr[7]/td/table/tbody/tr[23]/td[2]/form/select"))
    )

    select = Select(select_element)

    while True:
        for page in range(0,4):
            select.select_by_index(page)
            if page!=0:
                wait.until(EC.staleness_of(select_element))

            # 处理当前页面的数据
            base_xpath = "/html/body/table[2]/tbody/tr[7]/td/table/tbody/tr"

            target_courses=['壁球','击剑','排球','网球','羽毛球','棒、垒球','地板球','学术英语写作']

            course_condition = " or ".join(f"contains(text(), '{course}')" for course in target_courses)

            courses = wait.until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, f"{base_xpath}[position()>1][.//span[{course_condition}]]")
                )
            )

            for course in courses:
                course_name = course.find_element(By.XPATH, ".//td[1]//span").text
                class_num = course.find_element(By.XPATH, ".//td[6]").text
                enrollment = course.find_element(By.XPATH, ".//td[10]").text
                if available_course(enrollment):
                    print(f"页面{page+1},课程: {course_name}, 班号: {class_num}, 选课人数: {enrollment}","可选")
                    send_email(f"页面{page+1},课程: {course_name}, 班号: {class_num}, 选课人数: {enrollment}","可选")
                    play_music()
                      
                print(f"页面{page+1},课程: {course_name}, 班号: {class_num}, 选课人数: {enrollment}")
                
            # 如果不是最后一页，更新select元素
            if page < 3:
                select_element = wait.until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/table[2]/tbody/tr[7]/td/table/tbody/tr[23]/td[2]/form/select"))
                )
                select = Select(select_element)
            
            random_wait = random.uniform(0.5, 0.8)
            time.sleep(random_wait)

        # 完成四页循环后，重新进入补退选页面
        random_wait = random.uniform(0.8, 1)
        time.sleep(random_wait)
        
        # 重新点击补退选链接
        next_url_element = wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/table[1]/tbody/tr/td/ul/li[4]/a"))
        )
        next_url_element.click()
        
        # 等待新页面加载，并重新获取select元素
        select_element = wait.until(
            EC.presence_of_element_located((By.XPATH, "/html/body/table[2]/tbody/tr[7]/td/table/tbody/tr[23]/td[2]/form/select"))
        )
        select = Select(select_element)

    driver.quit()

while True:
    try:
        main()
    except Exception as e:
        print(f"发生错误: {str(e)}")
        print("程序将在3秒后重新启动...")
        time.sleep(3)
