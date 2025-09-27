from pages.login_page import LoginPage
from utilities.custom_logger import LogGen
from utilities.screenshot_utility import ScreenshotUtility
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class LoginHelper:
    url = "http://172.235.29.67:7777/superadmin/"
    logger = LogGen.loggen()
    email = "outdidsuperadmin@gmail.com"
    password = "1234"

    def login(self, driver, email=None, password=None):
        """Helper method to perform login"""
        login_page = LoginPage(driver)
        screenshot_util = ScreenshotUtility(driver)
        email = email or self.email
        password = password or self.password
        driver.get(self.url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        self.logger.info(f"Navigating to URL: {self.url}")
        #self.logger.info(f"Page source: {driver.page_source[:1000]}")
        #screenshot_path = screenshot_util.capture_screenshot("debug_login_initial")
        #self.logger.info(f"Initial screenshot saved at: {screenshot_path}")
        login_page.enter_email(email)
        login_page.enter_password(password)
        login_page.click_signIn()
        self.logger.info("Clicking Sign In")