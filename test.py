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
        # Setup Appium driver options
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.platform_version = "15"
        options.automation_name = "uiautomator2"
        options.udid = "emulator-5554"
        options.device_name = "emulator-5554"
        options.app_wait_for_launch = False
        options.no_reset = True  # Keeps the app state between sessions
        options.full_reset = False  # Doesn't reset app state

        # Initialize Appium server URL and start the driver session
        cls.appium_server_url = "http://localhost:4723"
        cls.driver = webdriver.Remote(
            command_executor=cls.appium_server_url, options=options
        )
        # Switch to native app context
        cls.driver.switch_to.context("NATIVE_APP")

        # Find the bot before tests start
        cls.find_bot(cls)

        # File paths for test files on the local system and in the device
        file_path = "/Users/itayeshkar/Documents/GitHub/Appium-Bot-Teser/test files/test.pdf"
        device_file_path = "/sdcard/Download/testFile.pdf"
        image_path = "/Users/itayeshkar/Documents/GitHub/Appium-Bot-Teser/test files/testImage.jpeg"
        device_image_path = "/sdcard/Download/testImage.jpeg"

        # Read files and encode to base64
        file_data = None
        image_data = None

        with open(file_path, "rb") as f:
            file_data = f.read()

        with open(image_path, "rb") as f:
            image_data = f.read()

        base64_file_data = base64.b64encode(file_data).decode("utf-8")
        base64_image_data = base64.b64encode(image_data).decode("utf-8")

        # Push files to the emulator
        cls.driver.push_file(device_image_path, base64_image_data)
        cls.driver.push_file(device_file_path, base64_file_data)
        print("Starting Test")

    @classmethod
    def tearDownClass(cls):
        # Quit the Appium driver session after tests are completed
        cls.driver.quit()

    def setUp(self):
        # Open the text bar (Web tabs) where interactions with the bot will occur
        try:
            bar = WebDriverWait(self.driver,5, EC.visibility_of_element_located((AppiumBy.XPATH,'//android.widget.FrameLayout[@content-desc="Web tabs "]',)))
            bar.click()
        except:
            pass

    def text_test(self, test_str: str) -> bool:
        # Send a text message to the bot and check the bot's response
        text = self.driver.find_element(
            AppiumBy.XPATH, '//android.widget.EditText[@text="Message"]'
        )
        text.send_keys(test_str)

        # Send the message
        send = self.driver.find_element(
            AppiumBy.XPATH, '//android.view.View[@content-desc="Send"]'
        )
        send.click()

        # Check if the bot responds with the expected text
        resp = self.get_bot_response()
        return "ERROR: SENT TEXT! SEND JPG!" in resp

    def file_test(self, is_image: bool = True) -> bool:
        # Test file sending and check if the bot responds correctly
        resp = self.get_bot_response()
        if is_image:
            return 'da6f923ff82391eb7edd31e4fd026b22cec50cb57dd3872befb635a1e86e2243' in resp
        return "ERROR: WRONG FILE! SEND JPG!" in resp

    def open_file_manager(self):
        # Open the file manager through the 'Attach media' option in Telegram
        attach_file = self.driver.find_element(
            AppiumBy.XPATH, '//android.widget.ImageView[@content-desc="Attach media"]'
        )
        attach_file.click()

        # Wait until 'File' option is visible and then click it
        files = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(
                (
                    AppiumBy.XPATH,
                    '//android.widget.FrameLayout[@text="File"]/android.widget.ImageView',
                )
            )
        )
        files.click()

        # Wait for 'Internal Storage' option and click it
        storage = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(
                (AppiumBy.XPATH, '//android.widget.TextView[@text="Internal Storage"]')
            )
        )
        storage.click()

        #moving from the recent files to the downloads folder if not in it
        try:
            folder = self.driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="Recent"]')
        except:
            return
        
        menu = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(
                (
                    AppiumBy.XPATH,
                    '//android.widget.ImageButton[@content-desc="Show roots"]',
                )
            )
        )
        menu.click()

        downloads = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(
                (
                    AppiumBy.XPATH,
                    '//android.widget.TextView[@resource-id="android:id/title" and @text="Downloads"]',
                )
            )
        )
        downloads.click()

    def get_files_for_test(self, search_file: str):
        # Open file manager and search for a specific file
        self.open_file_manager()

        # Search for the file in the file manager
        search = WebDriverWait(self.driver, 3).until(
            EC.visibility_of_element_located(
                (AppiumBy.XPATH, '//android.widget.Button[@content-desc="Search"]')
            )
        )
        search.click()

        # Enter the file name in the search bar
        search = self.driver.find_element(
            AppiumBy.XPATH,
            '//android.widget.AutoCompleteTextView[@resource-id="com.google.android.documentsui:id/search_src_text"]',
        )
        search.send_keys(search_file)

        # Wait until the file is found and then click on it
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
        # Fetch the latest message from the bot
        msg = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.view.ViewGroup")

        # Wait until a new message is received
        try:
            new_msg = WebDriverWait(self.driver, 5).until(
                lambda driver: 'Received' in driver.find_elements(
                    AppiumBy.CLASS_NAME, "android.view.ViewGroup"
                )[-1].text
            )
        except:
            return "FAILD TO GET BOT RESPONCE"
        # If a new message exists, return the bot's response
        msg = self.driver.find_elements(
            AppiumBy.CLASS_NAME, "android.view.ViewGroup"
        )[-1].text
        return msg

    # Test case to send a text message and check the response
    def test_text_message(self):
        self.assertTrue(self.text_test("Hello"))

    # Test case to send a non-image file and check the response
    def test_send_file(self):
        self.get_files_for_test("testFile.pdf")
        self.assertTrue(self.file_test(False))

    # Test case to send an image file and check the response
    def test_send_image_file(self):
        self.get_files_for_test("testImage.jpeg")
        self.assertTrue(self.file_test())

    def find_bot(self) -> None:
        # Activate Telegram if it's not currently the active app
        if self.driver.current_package != "org.telegram.messenger":
            self.driver.activate_app("org.telegram.messenger")

        # Search for the bot in the contact list
        try:
            self.driver.find_element(
                AppiumBy.XPATH, '//android.widget.TextView[@text="NSOBot"]'
            )
            return
        except:
            pass

        # If the bot isn't found, search for it
        search = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(
                (
                    AppiumBy.XPATH,
                    '//android.widget.ImageButton[@content-desc="Search"]/android.widget.ImageView',
                )
            )
        )
        search.click()

        # Try to type bot name into search field
        try:
            search.send_keys("NnnSssOoobot")
        except:
            # Fallback in case of error
            search = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(
                    (AppiumBy.XPATH, '//android.widget.EditText[@text="Search"]')
                )
            )
            search.send_keys("NnnSssOoobot")

        # Select the bot from the search results
        chat = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.view.ViewGroup")[
            0
        ]
        chat.click()

        #checking if a 'start chat' with the bot exists and if so clicks it
        try:
            start = WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located(
                    (AppiumBy.XPATH, '//android.widget.FrameLayout[@content-desc="Web tabs "]')
                )
            )
        except:
            return
        start.click()


if __name__ == "__main__":
    # Run the test suite
    suite = unittest.TestSuite()

    suite.addTest((TelegramBotTest("test_send_file")))
    suite.addTest((TelegramBotTest("test_send_image_file")))
    suite.addTest((TelegramBotTest("test_text_message")))

    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)
