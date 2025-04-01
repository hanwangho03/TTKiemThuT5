# Tran Nhat Anh Thuan - 2180604743
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import subprocess
import os

# Bật Flask server trước khi test
flask_process = subprocess.Popen(["python", "app.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
time.sleep(3)  # Đợi server khởi động

# Cấu hình Selenium
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

def run_test_case(task_name, expected_in_list, test_name):
    """Chạy một test case kiểm tra việc thêm công việc vào danh sách."""
    try:
        driver.get("http://127.0.0.1:5000/")  # Truy cập trang
        
        # Nhập công việc vào ô input
        input_field = driver.find_element(By.NAME, "task")
        input_field.send_keys(task_name)
        input_field.send_keys(Keys.RETURN)
        
        time.sleep(2)  # Đợi trang cập nhật
        
        # Chỉ lấy nội dung công việc (trong thẻ <span>)
        tasks = driver.find_elements(By.TAG_NAME, "li")
        task_texts = [task.find_element(By.TAG_NAME, "span").text.strip() for task in tasks]
        
        # So sánh với giá trị đã loại bỏ khoảng trắng
        if expected_in_list and task_name.strip() in [t.strip() for t in task_texts]:
            print(f" TEST PASSED: {test_name}")
        elif not expected_in_list and task_name.strip() not in [t.strip() for t in task_texts]:
            print(f" TEST PASSED: {test_name}")
        else:
            print(f" TEST FAILED: {test_name} - Expected in list: {expected_in_list}, got {task_texts}")
    except Exception as e:
        print(f" TEST ERROR: {test_name} - {str(e)}")

def test_progress_change(task_name, change, expected_progress, test_name):
    """Chạy một test case kiểm tra việc cập nhật tiến độ công việc."""
    try:
        driver.get("http://127.0.0.1:5000/")
        time.sleep(2)

        # Thêm công việc nếu chưa có
        tasks = driver.find_elements(By.TAG_NAME, "li")
        task_texts = [task.find_element(By.TAG_NAME, "span").text.strip() for task in tasks]
        if task_name not in task_texts:
            input_field = driver.find_element(By.NAME, "task")
            input_field.send_keys(task_name)
            input_field.send_keys(Keys.RETURN)
            time.sleep(2)

        # Lấy lại danh sách tasks sau khi thêm
        tasks = driver.find_elements(By.TAG_NAME, "li")
        for task in tasks:
            if task.find_element(By.TAG_NAME, "span").text.strip() == task_name:
                buttons = task.find_elements(By.TAG_NAME, "button")
                button_text = "+10%" if change > 0 else "-10%"
                for button in buttons:
                    if button.text == button_text:
                        button.click()
                        time.sleep(2)  # Đợi trang reload
                        # Lấy lại danh sách tasks sau khi click
                        tasks_updated = driver.find_elements(By.TAG_NAME, "li")
                        for updated_task in tasks_updated:
                            if updated_task.find_element(By.TAG_NAME, "span").text.strip() == task_name:
                                progress_text = updated_task.find_element(By.CLASS_NAME, "text-muted").text
                                current_progress = int(progress_text.split()[0].replace("%", ""))
                                if current_progress == expected_progress:
                                    print(f" TEST PASSED: {test_name}")
                                else:
                                    print(f" TEST FAILED: {test_name} - Expected progress: {expected_progress}%, got {current_progress}%")
                                return
        print(f" TEST FAILED: {test_name} - Không tìm thấy nút {button_text}")
    except Exception as e:
        print(f" TEST ERROR: {test_name} - {str(e)}")

def test_completion_status(task_name, test_name):
    """Chạy một test case kiểm tra trạng thái hoàn thành công việc."""
    try:
        driver.get("http://127.0.0.1:5000/")
        time.sleep(2)

        # Thêm công việc nếu chưa có
        tasks = driver.find_elements(By.TAG_NAME, "li")
        task_texts = [task.find_element(By.TAG_NAME, "span").text.strip() for task in tasks]
        if task_name not in task_texts:
            input_field = driver.find_element(By.NAME, "task")
            input_field.send_keys(task_name)
            input_field.send_keys(Keys.RETURN)
            time.sleep(2)

        # Lấy lại danh sách tasks sau khi thêm
        tasks = driver.find_elements(By.TAG_NAME, "li")
        for task in tasks:
            if task.find_element(By.TAG_NAME, "span").text.strip() == task_name:
                checkbox = task.find_element(By.CLASS_NAME, "form-check-input")
                checkbox.click()
                time.sleep(2)  # Đợi trang cập nhật
                # Lấy lại danh sách tasks sau khi click
                tasks_updated = driver.find_elements(By.TAG_NAME, "li")
                for updated_task in tasks_updated:
                    if updated_task.find_element(By.TAG_NAME, "span").text.strip() == task_name:
                        span = updated_task.find_element(By.TAG_NAME, "span")
                        if "completed" in span.get_attribute("class"):
                            print(f" TEST PASSED: {test_name}")
                        else:
                            print(f" TEST FAILED: {test_name} - Công việc không được đánh dấu hoàn thành")
                        return
        print(f" TEST FAILED: {test_name} - Không tìm thấy công việc")
    except Exception as e:
        print(f" TEST ERROR: {test_name} - {str(e)}")

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_delete_task(task_name, test_name):
    """Chạy một test case kiểm tra việc xóa công việc khỏi danh sách."""
    try:
        driver.get("http://127.0.0.1:5000/")
        # Chờ cho ô input xuất hiện
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "task")))

        # Thêm công việc nếu chưa có
        tasks = driver.find_elements(By.TAG_NAME, "li")
        task_texts = [task.find_element(By.TAG_NAME, "span").text.strip() for task in tasks]
        if task_name not in task_texts:
            input_field = driver.find_element(By.NAME, "task")
            input_field.send_keys(task_name)
            input_field.send_keys(Keys.RETURN)
            # Chờ cho danh sách công việc cập nhật
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "li")))

        # Lấy lại danh sách tasks sau khi thêm
        tasks = driver.find_elements(By.TAG_NAME, "li")
        for task in tasks:
            if task.find_element(By.TAG_NAME, "span").text.strip() == task_name:
                # Tìm thẻ <a> có nội dung là "Xóa"
                delete_links = task.find_elements(By.TAG_NAME, "a")
                for link in delete_links:
                    if link.text.strip() == "Xóa":
                        # Chờ cho nút "Xóa" có thể nhấn được
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//li[contains(., '{task_name}')]//a[text()='Xóa']")))
                        # Cuộn đến phần tử trước khi nhấn
                        driver.execute_script("arguments[0].scrollIntoView(true);", link)
                        link.click()
                        # Chờ cho danh sách công việc cập nhật sau khi xóa
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "li")))
                        # Lấy lại danh sách tasks sau khi xóa
                        tasks_updated = driver.find_elements(By.TAG_NAME, "li")
                        task_texts_updated = [task.find_element(By.TAG_NAME, "span").text.strip() for task in tasks_updated]
                        if task_name not in task_texts_updated:
                            print(f" TEST PASSED: {test_name}")
                        else:
                            print(f" TEST FAILED: {test_name} - Công việc vẫn còn trong danh sách: {task_texts_updated}")
                        return
                print(f" TEST FAILED: {test_name} - Không tìm thấy nút Xóa")
                return
        print(f" TEST FAILED: {test_name} - Không tìm thấy công việc")
    except Exception as e:
        print(f" TEST ERROR: {test_name} - {str(e)}")
# Các test case kiểm tra việc thêm công việc
test_cases = [
    ("Hoc Selenium", True, "Them cong viec vao danh sach"),
    ("", False, "Khong them cong viec rong"),
    ("   ", False, "Khong them cong viec chi chua khoang trang"),
    ("L" * 300, False, "Khong them cong viec qua dai"),
]

# Các test case kiểm tra tiến độ và trạng thái
progress_test_cases = [
    ("Test Progress", 10, 10, "Tang tien do cong viec len 10%"),
    ("Test Progress", -10, 0, "Giam tien do cong viec xuong 0%"),
]

# Danh Dau cong viec Da hoan thanh
completion_test_cases = [
    ("Test Completion", "Danh dau cong viec hoan thanh"),
]

# Test case kiểm tra xóa công việc
delete_test_cases = [
    ("Test Delete", "Xoa cong viec khoi danh sach"),
]

try:
    # Chạy các test case thêm công việc
    for task_name, expected_in_list, test_name in test_cases:
        run_test_case(task_name, expected_in_list, test_name)

    # Chạy các test case liên quan đến tiến độ
    for task_name, change, expected_progress, test_name in progress_test_cases:
        test_progress_change(task_name, change, expected_progress, test_name)

    # # Chạy test case liên quan đến trạng thái hoàn thành
    # for task_name, test_name in completion_test_cases:
    #     test_completion_status(task_name, test_name)

    # Chạy test case liên quan đến xóa công việc
    for task_name, test_name in delete_test_cases:
        test_delete_task(task_name, test_name)

finally:
    driver.quit()
    print(" Da dong trinh duyet")
    
    # Tắt Flask server sau khi test xong
    flask_process.terminate()
    print(" Da tat Flask server")