# Tran Nhat Anh Thuan - 2180604743
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import subprocess
import os

class TestToDoList(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Bật Flask server trước khi test
        cls.flask_process = subprocess.Popen(["python", "app.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(3)  # Đợi server khởi động

        # Cấu hình Selenium
        service = Service(ChromeDriverManager().install())
        cls.driver = webdriver.Chrome(service=service)

    @classmethod
    def tearDownClass(cls):
        # Đóng trình duyệt và Flask server sau khi test xong
        cls.driver.quit()
        print("Đã đóng trình duyệt")
        cls.flask_process.terminate()
        print("Đã tắt Flask server")

    def setUp(self):
        # Truy cập trang trước mỗi test case
        self.driver.get("http://127.0.0.1:5000/")

    def test_add_task_to_list(self):
        """Kiểm tra việc thêm công việc vào danh sách."""
        test_cases = [
            ("Hoc Selenium", True, "Them cong viec vao danh sach"),
            ("", False, "Khong them cong viec rong"),
            ("   ", False, "Khong them cong viec chi chua khoang trang"),
            ("L" * 300, False, "Khong them cong viec qua dai"),
        ]

        for task_name, expected_in_list, test_name in test_cases:
            with self.subTest(test_name=test_name):
                # Nhập công việc vào ô input
                input_field = self.driver.find_element(By.NAME, "task")
                input_field.clear()  # Xóa ô input trước khi nhập
                input_field.send_keys(task_name)
                input_field.send_keys(Keys.RETURN)
                
                time.sleep(2)  # Đợi trang cập nhật
                
                # Chỉ lấy nội dung công việc (trong thẻ <span>)
                tasks = self.driver.find_elements(By.TAG_NAME, "li")
                task_texts = [task.find_element(By.TAG_NAME, "span").text.strip() for task in tasks]
                
                # So sánh với giá trị đã loại bỏ khoảng trắng
                if expected_in_list:
                    self.assertIn(task_name.strip(), [t.strip() for t in task_texts], 
                                f"TEST FAILED: {test_name} - Expected in list: {expected_in_list}, got {task_texts}")
                else:
                    self.assertNotIn(task_name.strip(), [t.strip() for t in task_texts], 
                                   f"TEST FAILED: {test_name} - Expected in list: {expected_in_list}, got {task_texts}")

    def test_progress_change(self):
        """Kiểm tra việc cập nhật tiến độ công việc."""
        progress_test_cases = [
            ("Test Progress", 10, 10, "Tang tien do cong viec len 10%"),
            ("Test Progress", -10, 0, "Giam tien do cong viec xuong 0%"),
        ]

        for task_name, change, expected_progress, test_name in progress_test_cases:
            with self.subTest(test_name=test_name):
                # Thêm công việc nếu chưa có
                tasks = self.driver.find_elements(By.TAG_NAME, "li")
                task_texts = [task.find_element(By.TAG_NAME, "span").text.strip() for task in tasks]
                if task_name not in task_texts:
                    input_field = self.driver.find_element(By.NAME, "task")
                    input_field.send_keys(task_name)
                    input_field.send_keys(Keys.RETURN)
                    time.sleep(2)

                # Lấy lại danh sách tasks sau khi thêm
                tasks = self.driver.find_elements(By.TAG_NAME, "li")
                for task in tasks:
                    if task.find_element(By.TAG_NAME, "span").text.strip() == task_name:
                        buttons = task.find_elements(By.TAG_NAME, "button")
                        button_text = "+10%" if change > 0 else "-10%"
                        for button in buttons:
                            if button.text == button_text:
                                button.click()
                                time.sleep(2)  # Đợi trang reload
                                # Lấy lại danh sách tasks sau khi click
                                tasks_updated = self.driver.find_elements(By.TAG_NAME, "li")
                                for updated_task in tasks_updated:
                                    if updated_task.find_element(By.TAG_NAME, "span").text.strip() == task_name:
                                        progress_text = updated_task.find_element(By.CLASS_NAME, "text-muted").text
                                        current_progress = int(progress_text.split()[0].replace("%", ""))
                                        self.assertEqual(current_progress, expected_progress,
                                                       f"TEST FAILED: {test_name} - Expected progress: {expected_progress}%, got {current_progress}%")
                                        return
                        self.fail(f"TEST FAILED: {test_name} - Không tìm thấy nút {button_text}")

    def test_completion_status(self):
        """Kiểm tra trạng thái hoàn thành công việc."""
        completion_test_cases = [
            ("Test Completion", "Danh dau cong viec hoan thanh"),
        ]

        for task_name, test_name in completion_test_cases:
            with self.subTest(test_name=test_name):
                # Thêm công việc nếu chưa có
                tasks = self.driver.find_elements(By.TAG_NAME, "li")
                task_texts = [task.find_element(By.TAG_NAME, "span").text.strip() for task in tasks]
                if task_name not in task_texts:
                    input_field = self.driver.find_element(By.NAME, "task")
                    input_field.send_keys(task_name)
                    input_field.send_keys(Keys.RETURN)
                    time.sleep(2)

                # Lấy lại danh sách tasks sau khi thêm
                tasks = self.driver.find_elements(By.TAG_NAME, "li")
                for task in tasks:
                    if task.find_element(By.TAG_NAME, "span").text.strip() == task_name:
                        checkbox = task.find_element(By.CLASS_NAME, "form-check-input")
                        checkbox.click()
                        time.sleep(2)  # Đợi trang cập nhật
                        # Lấy lại danh sách tasks sau khi click
                        tasks_updated = self.driver.find_elements(By.TAG_NAME, "li")
                        for updated_task in tasks_updated:
                            if updated_task.find_element(By.TAG_NAME, "span").text.strip() == task_name:
                                span = updated_task.find_element(By.TAG_NAME, "span")
                                self.assertIn("completed", span.get_attribute("class"),
                                            f"TEST FAILED: {test_name} - Công việc không được đánh dấu hoàn thành")
                                return
                self.fail(f"TEST FAILED: {test_name} - Không tìm thấy công việc")

if __name__ == "__main__":
    unittest.main()