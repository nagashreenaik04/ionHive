import pytest
import allure
import time
import re
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.profile_page import ProfilePage
from utilities.custom_logger import LogGen
from utilities.screenshot_utility import ScreenshotUtility
from pytest_html import extras

@pytest.mark.usefixtures("driver")
class TestLogin:

    url = "http://172.235.29.67:7777/superadmin/"

    logger = LogGen.loggen()
    email = "outdidsuperadmin@gmail.com"
    password = "1234"
    trim_email = "outdidsuperadmin@gmail.com         "

    #invalid login
    test_data = [
        ("aoutdidsuperadmins@gmail.com", "1234", "Error: Invalid email address or user is deactivated"),
        ("outdidsuperadmin@gmail.com", "1235", "Error: Invalid password"),
        ("outdidassociation@gmail.com", "1234", "Error: Unauthorized role"),
        ("aoutdidsuperadmins@gmail.com", "1235", "Error: Invalid email address or user is deactivated"),
    ]

    #signin Button Validation
    test_info = [
        ("", ""),
        ("outdidassociation@gmail.com", ""),
        ("", "1234")
    ]

    # Define test cases for email field
    test_email = [
        {"input": "test.user@example.com", "expected_value": "test.user@example.com", "expected_valid": True},
        {"input": "testuser123@example.com", "expected_value": "testuser123@example.com", "expected_valid": True},
        {"input": "test#user@example.com", "expected_value": "testuser@example.com", "expected_valid": False},
        {"input": "test$user@example.com", "expected_value": "testuser@example.com", "expected_valid": False},
        {"input": "test&user@example.com", "expected_value": "testuser@example.com", "expected_valid": False},
        {"input": "test*user@example.com", "expected_value": "testuser@example.com", "expected_valid": False}
    ]

    # Define test cases for password field
    test_password = [
        {"input": "1234", "expected_value": "1234", "expected_valid": True},
        {"input": "abcdefg", "expected_value": "", "expected_valid": False},
        {"input": "12av", "expected_value": "12", "expected_valid": False},
        {"input": "1234567", "expected_value": "1234", "expected_valid": False},
        {"input": "abc1", "expected_value": "1", "expected_valid": False},
        {"input": "!@$$", "expected_value": "", "expected_valid": False},
        {"input": "63&*", "expected_value": "63", "expected_valid": False},
        {"input": ")(~8", "expected_value": "8", "expected_valid": False},
        {"input": "", "expected_value": "", "expected_valid": True}
    ]

    # Define test cases with expected error messages for password field
    test_password_error = [
        ("1", "Password number must be a 4-digit number."),
        ("12", "Password number must be a 4-digit number."),
        ("123", "Password number must be a 4-digit number."),
        ("1235", "Error: Invalid password")
    ]

    # Define test cases with expected error messages for email field
    test_email_error = [
        ("as.", "Please include an '@' in the email address. 'as.' is missing an '@'."),
        ("as@", "Please enter a part following '@'. 'as@' is incomplete."),
        ("as@.", "'.' is used at a wrong position in '.'.")
    ]

    def _sanitize_filename(self, input_text):
        """Sanitize input text for use in filenames by replacing invalid characters."""
        # Replace invalid characters with underscore
        return re.sub(r'[<>:"/\\|?*]', '_', input_text)

    def login(self, driver, email=None, password=None):
        """Helper method to perform login"""
        login_page = LoginPage(driver)
        screenshot_util = ScreenshotUtility(driver)
        email = email or self.email
        password = password or self.password
        driver.get(self.url)
        self.logger.info(f"Logging in with email: {email}, password: {password}")
        #self.logger.info("Page source: %s", driver.page_source[:1000])
        #self.logger.info("Browser console logs: %s", driver.get_log("browser"))
        #screenshot_path = screenshot_util.capture_screenshot("debug_login")
        #self.logger.info(f"Debug screenshot saved at: {screenshot_path}")
        login_page.enter_email(email)
        login_page.enter_password(password)
        login_page.click_signIn()
        self.logger.info("Clicking Sign In")

    #@pytest.mark.sanity
    #@pytest.mark.retesting
    @pytest.mark.regression
    @pytest.mark.order(0)
    def test_valid_login(self, driver):
        screenshot_util = ScreenshotUtility(driver)
        try:
            self.login(driver)
            dashboard_page = DashboardPage(driver)
            dashboard_page.wait_for_element(dashboard_page.welcome_msg, timeout=30)
            welcome_text = dashboard_page.capture_welcomeMsg().strip(",")
            expected_welcome = f"Welcome to {self.email}"
            assert welcome_text == expected_welcome, f"Expected welcome message '{expected_welcome}', but got '{welcome_text}'"
            self.logger.info("Login verified successfully")
            login_page = LoginPage(driver)
            login_page.click_logout()
            self.logger.info("Successfully logged out")
        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("test_valid_login_failure")
            self.logger.error(f"Test failed, screenshot saved at: {screenshot_path}")
            with open(screenshot_path, "rb") as image_file:
                allure.attach(image_file.read(), name="Valid Login Failure", attachment_type=allure.attachment_type.PNG)
            raise AssertionError(f"Failed to verify login: {str(e)}")

    #@pytest.mark.smoke
    #@pytest.mark.retesting
    @pytest.mark.order(1)
    @pytest.mark.regression
    @pytest.mark.parametrize("email, password, expected_error", test_data)
    def test_invalid_login(self, driver, email, password, expected_error):
        screenshot_util = ScreenshotUtility(driver)
        try:
            self.login(driver, email, password)
            login_page = LoginPage(driver)
            actual_error = login_page.get_error_message()
            assert actual_error == expected_error, f"Expected error message '{expected_error}', but got '{actual_error}'"
            self.logger.info("Invalid login verified successfully")
        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot(f"test_invalid_login_failure_{email.replace('@', '_')}")
            self.logger.error(f"Test failed for email: {email}, screenshot saved at: {screenshot_path}")
            with open(screenshot_path, "rb") as image_file:
                allure.attach(image_file.read(), name="Invalid Login Failure", attachment_type=allure.attachment_type.PNG)
            raise AssertionError(f"Failed to verify error message: {str(e)}")

    #@pytest.mark.smoke
    #@pytest.mark.retesting
    @pytest.mark.regression
    @pytest.mark.order(5)
    @pytest.mark.parametrize("email, password", test_info)
    def test_signIn_btn(self, driver, email, password):
        screenshot_util = ScreenshotUtility(driver)
        login_page = LoginPage(driver)
        try:
            driver.get(self.url)
            self.logger.info(f"Testing Sign In with email: {email}, password: {password}")
            #self.logger.info("Page source: %s", driver.page_source[:1000])
            #self.logger.info("Browser console logs: %s", driver.get_log("browser"))
            screenshot_path = screenshot_util.capture_screenshot(f"debug_signIn_btn_{email.replace('@', '_')}")
            self.logger.info(f"Debug screenshot saved at: {screenshot_path}")
            if email:
                login_page.enter_email(email)
            if password:
                login_page.enter_password(password)
            login_page.click_signIn()
            expected_msg = "Please fill out this field."
            email_msg = login_page.get_validation_message(login_page.email_field)
            password_msg = login_page.get_validation_message(login_page.password_field)
            if not email:
                assert email_msg == expected_msg, f"Expected email validation '{expected_msg}', but got '{email_msg}'"
            else:
                assert email_msg == "", f"Email should not have validation message, but got '{email_msg}'"
            if not password:
                assert password_msg == expected_msg, f"Expected password validation '{expected_msg}', but got '{password_msg}'"
            else:
                assert password_msg == "", f"Password should not have validation message, but got '{password_msg}'"
            #self.logger.info("Validation messages verified successfully")
            self.logger.info(
                f"Validation messages verified successfully -> Email: '{email_msg}', Password: '{password_msg}'")
            #self.logger.info(f"===== Test Completed Successfully =====\n")
        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot(f"test_signIn_btn_failure_{email.replace('@', '_')}")
            self.logger.error(f"Sign-in failed, screenshot saved at: {screenshot_path}")
            with open(screenshot_path, "rb") as image_file:
                allure.attach(image_file.read(), name="SignIn Button Failure", attachment_type=allure.attachment_type.PNG)
            raise AssertionError(f"Failed to verify validation messages: {str(e)}")

    @pytest.mark.smoke
    @pytest.mark.retesting
    @pytest.mark.regression
    @pytest.mark.integration
    @pytest.mark.order(2)
    def test_update_password_login(self, driver):
        screenshot_util = ScreenshotUtility(driver)
        try:
            self.login(driver)
            profile_page = ProfilePage(driver)
            self.logger.info("Navigating to Profile Page")
            profile_page.navigate_to_profile_page()
            time.sleep(2)
            profile_page.update_password("4321")
            self.logger.info("Updated the password")
            profile_page.click_update()
            self.logger.info("Clicked the Update button")
            profile_page.click_okBtn()
            self.logger.info("Clicked the OK button")
            #screenshot_path = screenshot_util.capture_screenshot("debug_update_password_success")
            #self.logger.info(f"Password update screenshot saved at: {screenshot_path}")
            login_page = LoginPage(driver)
            login_page.click_logout()
            self.logger.info("Successfully logged out")
            self.login(driver, self.email, "4321")
            dashboard_page = DashboardPage(driver)
            dashboard_page.wait_for_element(dashboard_page.welcome_msg, timeout=30)
            welcome_text = dashboard_page.capture_welcomeMsg().strip(",")
            expected_welcome = f"Welcome to {self.email}"
            assert welcome_text == expected_welcome, f"Expected welcome message '{expected_welcome}', but got '{welcome_text}'"
            self.logger.info("Re-login with new password verified successfully")
            # Reset password to original
            profile_page.navigate_to_profile_page()
            time.sleep(2)
            profile_page.update_password("1234")
            profile_page.click_update()
            profile_page.click_okBtn()
            self.logger.info("Password reset to original")
            login_page.click_logout()
            self.logger.info("Successfully logged out")
        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("test_update_password_failure")
            self.logger.error(f"Password update failed, screenshot saved at: {screenshot_path}")
            with open(screenshot_path, "rb") as image_file:
                allure.attach(image_file.read(), name="Password Update Failure", attachment_type=allure.attachment_type.PNG)
            raise AssertionError(f"Failed to update password: {str(e)}")

    #@pytest.mark.sanity
    #@pytest.mark.retesting
    @pytest.mark.regression
    @pytest.mark.order(3)
    def test_email_field(self, driver):
        driver.get(self.url)  # Refresh page
        self.logger.info(f"Browser logs: {driver.get_log('browser')}")
        """Test that email field handles inputs as expected."""
        login_page = LoginPage(driver)
        screenshot_util = ScreenshotUtility(driver)

        for test in self.test_email:
            input_text = test["input"]
            self.logger.info(f"/input text: '{input_text}'")
            expected_value = test["expected_value"]
            self.logger.info(f"/expected value: '{expected_value}'")
            expected_valid = test["expected_valid"]
            self.logger.info(f"/expected valid: '{expected_valid}'")

            try:
                login_page.clear_email_field()  # Clear field
                login_page.enter_email(input_text)
                time.sleep(2)
                actual_value = login_page.get_email_value()
                self.logger.info(f"/actual_value: '{actual_value}'")
                result_valid = (actual_value and expected_value  == input_text)
                self.logger.info(f"/result valid: '{result_valid}'" )
                self.logger.info(f"Input: '{input_text}', Actual value: '{actual_value}', Expected value: '{expected_value}', Result valid: '{result_valid}', Expected valid: '{expected_valid}'")

                if result_valid == expected_valid:
                    self.logger.info(f"PASS: Input '{input_text}' - Value '{actual_value}', Validity '{result_valid}'")
                else:
                    screenshot_path = screenshot_util.capture_screenshot(
                        f"email_test_failure_{input_text.replace('@', '_')}")
                    self.logger.error(f"FAIL: Input '{input_text}' - Expected value '{expected_value}', got '{actual_value}', Result valid '{result_valid}', Expected valid '{expected_valid}'")
                    with open(screenshot_path, "rb") as image_file:
                        allure.attach(image_file.read(), name=f"Email Test Failure - {input_text}",
                                      attachment_type=allure.attachment_type.PNG)
                    assert False, f"Expected value '{expected_value}', got '{actual_value}', Result valid '{result_valid}', Expected valid '{expected_valid}'"

            except Exception as e:
                screenshot_path = screenshot_util.capture_screenshot(
                    f"email_test_error_{input_text.replace('@', '_')}")
                self.logger.error(f"Test failed for input '{input_text}': {str(e)}")
                with open(screenshot_path, "rb") as image_file:
                    allure.attach(image_file.read(), name=f"Email Test Error - {input_text}",
                                  attachment_type=allure.attachment_type.PNG)
                raise AssertionError(f"Failed to test email input '{input_text}': {str(e)}")

    #@pytest.mark.sanity
    #@pytest.mark.retesting
    @pytest.mark.regression
    @pytest.mark.order(3)
    def test_password_field(self, driver):
        driver.get(self.url)  # Refresh page
        self.logger.info(f"Browser logs: {driver.get_log('browser')}")
        """Test that email field handles inputs as expected."""
        login_page = LoginPage(driver)
        screenshot_util = ScreenshotUtility(driver)

        for test in self.test_password:
            input_text = test["input"]
            self.logger.info(f"/input text: '{input_text}'")
            expected_value = test["expected_value"]
            self.logger.info(f"/expected value: '{expected_value}'")
            expected_valid = test["expected_valid"]
            self.logger.info(f"/expected valid: '{expected_valid}'")

            try:
                login_page.clear_password_field()  # Clear field
                login_page.enter_password(input_text)
                time.sleep(2)
                actual_value = login_page.get_password_value()
                self.logger.info(f"/actual_value: '{actual_value}'")
                result_valid = (actual_value == input_text)
                self.logger.info(f"/result valid: '{result_valid}'")
                self.logger.info(
                    f"Input: '{input_text}', Actual value: '{actual_value}', Expected value: '{expected_value}', Result valid: '{result_valid}', Expected valid: '{expected_valid}'")

                if result_valid == expected_valid:
                    self.logger.info(f"PASS: Input '{input_text}' - Value '{actual_value}', Validity '{result_valid}'")
                else:
                    screenshot_path = screenshot_util.capture_screenshot(
                        f"email_test_failure_{input_text.replace('@', '_')}")
                    self.logger.error(
                        f"FAIL: Input '{input_text}' - Expected value '{expected_value}', got '{actual_value}', Result valid '{result_valid}', Expected valid '{expected_valid}'")
                    with open(screenshot_path, "rb") as image_file:
                        allure.attach(image_file.read(), name=f"Email Test Failure - {input_text}",
                                      attachment_type=allure.attachment_type.PNG)
                    assert False, f"Expected value '{expected_value}', got '{actual_value}', Result valid '{result_valid}', Expected valid '{expected_valid}'"

            except Exception as e:
                screenshot_path = screenshot_util.capture_screenshot(
                    f"email_test_error_{input_text.replace('@', '_')}")
                self.logger.error(f"Test failed for input '{input_text}': {str(e)}")
                with open(screenshot_path, "rb") as image_file:
                    allure.attach(image_file.read(), name=f"Email Test Error - {input_text}",
                                  attachment_type=allure.attachment_type.PNG)
                raise AssertionError(f"Failed to test email input '{input_text}': {str(e)}")

    #@pytest.mark.sanity
    #@pytest.mark.retesting
    @pytest.mark.regression
    @pytest.mark.order(4)
    def test_trim_email_field(self, driver):
        """Test login with trimmed email and verify dashboard page."""
        screenshot_util = ScreenshotUtility(driver)
        try:
            self.login(driver, email=self.trim_email)
            dashboard_page = DashboardPage(driver)
            dashboard_page.wait_for_element(dashboard_page.welcome_msg, timeout=30)
            welcome_text = dashboard_page.capture_welcomeMsg().strip(",")
            expected_welcome = f"Welcome to {self.email}"  # Expect trimmed email
            assert welcome_text == expected_welcome, f"Expected welcome message '{expected_welcome}', but got '{welcome_text}'"
            self.logger.info("Login with trimmed email verified successfully")
            login_page = LoginPage(driver)
            login_page.click_logout()
            self.logger.info("Successfully logged out")
        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("test_trim_email_failure")
            self.logger.error(f"Test failed, screenshot saved at: {screenshot_path}")
            with open(screenshot_path, "rb") as image_file:
                allure.attach(image_file.read(), name="Trim Email Login Failure",
                              attachment_type=allure.attachment_type.PNG)
            raise AssertionError(f"Failed to verify login with trimmed email: {str(e)}")

    #@pytest.mark.sanity
    #@pytest.mark.retesting
    @pytest.mark.regression
    @pytest.mark.order(2)
    @pytest.mark.parametrize("password, expected_error", test_password_error)
    def test_password_field_error(self, driver, password, expected_error):
        """Test error messages for invalid password inputs."""
        screenshot_util = ScreenshotUtility(driver)
        login_page = LoginPage(driver)
        try:
            self.login(driver, password=password)
            validation_msg = login_page.get_validation_message(login_page.password_field)
            actual_error = login_page.get_error_message() if not validation_msg else validation_msg
            self.logger.info(f"Validation message: '{validation_msg}', Actual error: '{actual_error}'")
            assert actual_error == expected_error, f"Expected error message '{expected_error}', but got '{actual_error}'"
            self.logger.info("Error message displayed successfully")
        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot(
                f"test_password_error_{self._sanitize_filename(password)}")
            self.logger.error(f"Test failed for password: {password}, screenshot saved at: {screenshot_path}")
            with open(screenshot_path, "rb") as image_file:
                allure.attach(image_file.read(), name=f"Password Error Test Failure - {password}",
                              attachment_type=allure.attachment_type.PNG)
            raise AssertionError(f"Failed to verify error message for password '{password}': {str(e)}")

    @pytest.mark.sanity
    #@pytest.mark.retesting
    @pytest.mark.regression
    @pytest.mark.order(2)
    @pytest.mark.parametrize("email, expected_error", test_email_error)
    def test_email_field_error(self, driver, email, expected_error):
        driver.get(self.url)  # Refresh page
        self.logger.info(f"Browser logs: {driver.get_log('browser')}")
        """Test error messages for invalid email inputs."""
        screenshot_util = ScreenshotUtility(driver)
        login_page = LoginPage(driver)
        try:
            login_page.enter_email(email)
            login_page.click_signIn()
            validation_msg = login_page.get_validation_message(login_page.email_field)
            actual_error = validation_msg or login_page.get_error_message()
            self.logger.info(
                f"Validation message: '{validation_msg}', Actual error: '{actual_error}'")  # Use self.logger
            assert actual_error == expected_error, f"Expected error message '{expected_error}', but got '{actual_error}'"
            self.logger.info("Error message displayed successfully")
        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot(f"test_email_error_{email.replace('@', '_at_')}")
            self.logger.error(
                f"Test failed for email: {email}, screenshot saved at: {screenshot_path}")  # Use self.logger
            with open(screenshot_path, "rb") as image_file:
                allure.attach(image_file.read(), name=f"Email Error Test Failure - {email}",
                              attachment_type=allure.attachment_type.PNG)
            raise AssertionError(f"Failed to verify error message for email '{email}': {str(e)}")



