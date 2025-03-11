# Trần Nhật Anh Thuận - 2180604743
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import subprocess
import os

# 🔥 Bật Flask server trước khi test
flask_process = subprocess.Popen(["python", "app.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(3)  # Đợi server khởi động

# Cấu hình Selenium
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

def run_test_case(task_name, expected_in_list, test_name):
    try:
        driver.get("http://127.0.0.1:5000/")  # Truy cập trang
        
        # Nhập công việc vào ô input
        input_field = driver.find_element(By.NAME, "task")
        input_field.send_keys(task_name)
        input_field.send_keys(Keys.RETURN)
        
        time.sleep(2)  # Đợi trang cập nhật
        
        # 🔥 Chỉ lấy nội dung công việc (trong thẻ <span>)
        tasks = driver.find_elements(By.TAG_NAME, "li")
        task_texts = [task.find_element(By.TAG_NAME, "span").text for task in tasks]  
        
        if expected_in_list and task_name in task_texts:
            print(f"✅ TEST PASSED: {test_name}")
        elif not expected_in_list and task_name not in task_texts:
            print(f"✅ TEST PASSED: {test_name}")
        else:
            print(f"❌ TEST FAILED: {test_name} - Expected in list: {expected_in_list}, got {task_texts}")
    except Exception as e:
        print(f"❌ TEST ERROR: {test_name} - {str(e)}")
test_cases = [
    ("Học Selenium", True, "Them cong viec vao danh sach"),
    ("", False, "Khong them cong viec rong"),
]

try:
    for task_name, expected_in_list, test_name in test_cases:
        run_test_case(task_name, expected_in_list, test_name)
    
    # 🛠 Test xóa công việc
    delete_buttons = driver.find_elements(By.LINK_TEXT, "Xóa")
    if delete_buttons:
        delete_buttons[0].click()
        time.sleep(2)
        print("✅ TEST PASSED: Xoa cong viec đau tien")
    else:
        print("❌ TEST FAILED: Không tìm thấy nút xóa")
    
finally:
    driver.quit()
    print("🔻 Đã đóng trình duyệt")

    # 🔥 Tắt Flask server sau khi test xong
    flask_process.terminate()
    print("🔻 Đã tắt Flask server")
