# Tran Nhat Anh Thuan - 2180604743
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import subprocess
import os

# Bat Flask server truoc khi test
flask_process = subprocess.Popen(["python", "app.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(3)  # Doi server khoi dong

# Cau hinh Selenium
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

def run_test_case(task_name, expected_in_list, test_name):
    """Chay mot test case kiem tra viec them cong viec vao danh sach."""
    try:
        driver.get("http://127.0.0.1:5000/")  # Truy cap trang
        
        # Nhap cong viec vao o input
        input_field = driver.find_element(By.NAME, "task")
        input_field.send_keys(task_name)
        input_field.send_keys(Keys.RETURN)
        
        time.sleep(2)  # Doi trang cap nhat
        
        # Chi lay noi dung cong viec (trong the <span>)
        tasks = driver.find_elements(By.TAG_NAME, "li")
        task_texts = [task.find_element(By.TAG_NAME, "span").text.strip() for task in tasks]
        
        # So sanh voi gia tri da loai bo khoang trang
        if expected_in_list and task_name.strip() in [t.strip() for t in task_texts]:
            print(f"✅ TEST PASSED: {test_name}")
        elif not expected_in_list and task_name.strip() not in [t.strip() for t in task_texts]:
            print(f"✅ TEST PASSED: {test_name}")
        else:
            print(f"❌ TEST FAILED: {test_name} - Expected in list: {expected_in_list}, got {task_texts}")
    except Exception as e:
        print(f"❌ TEST ERROR: {test_name} - {str(e)}")

# Cac test case kiem tra viec them cong viec
test_cases = [
    ("Hoc Selenium", True, "Them cong viec vao danh sach"),
    ("", False, "Khong them cong viec rong"),
    ("   ", False, "Khong them cong viec chi chua khoang trang"),
    ("L" * 300, False, "Khong them cong viec qua dai"),
]

try:
    # Chay cac test case them cong viec
    for task_name, expected_in_list, test_name in test_cases:
        run_test_case(task_name, expected_in_list, test_name)

    # Kiem tra xoa cong viec nhung van con trong danh sach
    driver.get("http://127.0.0.1:5000/")
    time.sleep(2)
    
    tasks_before = driver.find_elements(By.TAG_NAME, "li")
    # Tim nut xoa bang XPath (tim theo chuoi 'Xoa')
    delete_buttons = driver.find_elements(By.XPATH, '//a[contains(text(), "Xoa")]')
    
    if delete_buttons:
        delete_buttons[0].click()
        time.sleep(2)  # Doi cap nhat
        
        tasks_after = driver.find_elements(By.TAG_NAME, "li")
        if len(tasks_after) == len(tasks_before) - 1:
            print("✅ TEST PASSED: Xoa cong viec thanh cong")
        else:
            print("❌ TEST FAILED: Xoa cong viec nhung no van con trong danh sach")
    else:
        print("❌ TEST FAILED: Khong tim thay nut xoa")
    
    # Kiem tra UI cap nhat sau khi xoa cong viec
    delete_buttons = driver.find_elements(By.XPATH, '//a[contains(text(), "Xoa")]')
    if delete_buttons:
        delete_buttons[0].click()
        time.sleep(0.5)  # Doi rat ngan de xem UI cap nhat ngay khong
        tasks_after_ui = driver.find_elements(By.TAG_NAME, "li")
        if len(tasks_after_ui) == len(tasks_after) - 1:
            print("✅ TEST PASSED: UI cap nhat sau khi xoa cong viec")
        else:
            print("❌ TEST FAILED: UI khong cap nhat ngay lap tuc sau khi xoa")
    else:
        print("❌ TEST FAILED: Khong tim thay nut xoa de kiem tra UI")

finally:
    driver.quit()
    print("🔻 Da dong trinh duyet")
    
    # Tat Flask server sau khi test xong
    flask_process.terminate()
    print("🔻 Da tat Flask server")
