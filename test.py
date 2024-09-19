import unittest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import base64


class TelegramBotTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.platform_version = "15"
        options.automation_name = "uiautomator2"
        options.udid = "emulator-5554"
        options.device_name = "emulator-5554"
        options.app_wait_for_launch = False
        options.no_reset = True
        options.full_reset = False

        cls.appium_server_url = "http://localhost:4723"
        cls.driver = webdriver.Remote(
            command_executor=cls.appium_server_url, options=options
        )
        cls.driver.switch_to.context("NATIVE_APP")
        cls.find_bot(cls)

        file_path = (
            "/Users/itayeshkar/Documents/GitHub/Telegram-Bot-Tester/test files/test.pdf"
        )
        device_file_path = "/sdcard/Download/testFile.pdf"
        image_path = "/Users/itayeshkar/Documents/GitHub/Telegram-Bot-Tester/test files/testImage.jpeg"
        device_image_path = "/sdcard/Download/testImage.jpeg"

        file_data = None
        image_data = None

        with open(file_path, "rb") as f:
            file_data = f.read()

        with open(image_path, "rb") as f:
            image_data = f.read()

        base64_file_data = base64.b64encode(file_data).decode("utf-8")
        base64_image_data = base64.b64encode(image_data).decode("utf-8")

        cls.driver.push_file(device_image_path, base64_image_data)
        cls.driver.push_file(device_file_path, base64_file_data)
        print("Starting Test")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        # Opening the text bar where all actions will be done through
        try:
            bar = self.driver.find_element(
                AppiumBy.XPATH,
                '//android.widget.FrameLayout[@content-desc="Web tabs "]',
            )
            bar.click()
        except:
            pass

    def text_test(self, test_str: str) -> bool:
        # Finding the text bar, entering and sending a message
        text = self.driver.find_element(
            AppiumBy.XPATH, '//android.widget.EditText[@text="Message"]'
        )
        text.send_keys(test_str)
        send = self.driver.find_element(
            AppiumBy.XPATH, '//android.view.View[@content-desc="Send"]'
        )
        send.click()

        # Checking bot response
        resp = self.get_bot_response()
        return "ERROR: SENT TEXT! SEND JPG!" in resp

    def file_test(self, is_image: bool = True) -> bool:
        # Checking bot response
        resp = self.get_bot_response()
        if is_image:
            return "ERROR: WRONG FILE! SEND JPG!" not in resp
        return "ERROR: WRONG FILE! SEND JPG!" in resp

    def open_file_manager(self):
        attach_file = self.driver.find_element(
            AppiumBy.XPATH, '//android.widget.ImageView[@content-desc="Attach media"]'
        )
        attach_file.click()
        files = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(
                (
                    AppiumBy.XPATH,
                    '//android.widget.FrameLayout[@text="File"]/android.widget.ImageView',
                )
            )
        )
        files.click()
        storage = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(
                (AppiumBy.XPATH, '//android.widget.TextView[@text="Internal Storage"]')
            )
        )
        storage.click()

    def get_files_for_test(self, search_file: str):
        self.open_file_manager()
        search = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located(
                (AppiumBy.XPATH, '//android.widget.Button[@content-desc="Search"]')
            )
        )
        search.click()
        search = self.driver.find_element(
            AppiumBy.XPATH,
            '//android.widget.AutoCompleteTextView[@resource-id="com.google.android.documentsui:id/search_src_text"]',
        )
        search.send_keys(search_file)
        # time.sleep(1)'//android.widget.ImageView[@resource-id="com.google.android.documentsui:id/icon_thumb"]'
        file = WebDriverWait(self.driver, 5).until(
            lambda driver: len(
                driver.find_elements(
                    AppiumBy.XPATH,
                    '//android.widget.ImageView[@resource-id="com.google.android.documentsui:id/icon_thumb"]',
                )
            )
            == 1
        )
        file = self.driver.find_elements(
            AppiumBy.ID, "com.google.android.documentsui:id/item_root"
        )[0]
        file.click()

    def get_bot_response(self) -> str:
        msg = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.view.ViewGroup")
        new_msg = WebDriverWait(self.driver, 3).until(
            lambda driver: driver.find_elements(
                AppiumBy.CLASS_NAME, "android.view.ViewGroup"
            )[-1].text
            != msg
        )
        if new_msg:
            msg = self.driver.find_elements(
                AppiumBy.CLASS_NAME, "android.view.ViewGroup"
            )[-1].text
            return msg
        return "FAILED TO GET BOT RESPONSE"

    def test_text_message(self):
        self.assertTrue(self.text_test("Hello"))

    def test_send_file(self):
        self.get_files_for_test("testFile.pdf")
        self.assertTrue(self.file_test(False))

    def test_send_image_file(self):
        self.get_files_for_test("testImage.jpeg")
        self.assertTrue(self.file_test())

    def find_bot(self) -> None:
        if self.driver.current_package != "org.telegram.messenger":
            self.driver.activate_app("org.telegram.messenger")
        try:
            self.driver.find_element(
                AppiumBy.XPATH, '//android.widget.TextView[@text="NSOBot"]'
            )
            return
        except:
            pass
        search = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(
                (
                    AppiumBy.XPATH,
                    '//android.widget.ImageButton[@content-desc="Search"]/android.widget.ImageView',
                )
            )
        )
        search.click()
        try:
            search.send_keys("NnnSssOoobot")
        except:
            search = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(
                    (AppiumBy.XPATH, '//android.widget.EditText[@text="Search"]')
                )
            )
            search.send_keys("NnnSssOoobot")
        chat = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.view.ViewGroup")[
            0
        ]
        chat.click()


if __name__ == "__main__":
    unittest.main()
