import pytest
import random
import time
import re

from datetime import datetime

from faker import Faker
import allure

from pages.reseller_page import ResellerPage
from utilities.custom_logger import LogGen
from utilities.login_helper import LoginHelper
from utilities.screenshot_utility import ScreenshotUtility

@pytest.mark.usefixtures("driver")
class TestReseller:
    logger = LogGen.loggen()

    actual_page_heading = "Manage Reseller"
    actual_reseller_table = "List Of Reseller"
    actual_create_btn  = "Create"

    # Generate Faker data
    fake = Faker()
    reseller_name = fake.company()  # fake company name
    reseller_email = fake.email()  # fake email
    reseller_address = fake.address()  # fake address

    # Expected datas
    expected_reseller_success_msg = "Reseller added successfully"
    status = "Active"
    reseller_wallet = "0"
    created_by = "outdidsuperadmin@gmail.com"
    modified_by = "-"
    modified_date = "-"

    # Test Data for Already Existed Reseller
    already_exist_reseller_error_test_data = [
        {"resellerName": "Nagashree", "resellerPhone" : "8989898989", "resellerEmail" : "nagashreenaik040@gmail.com", "resellerAddress": "BTM", "expected_error": "Email ID and Reseller Name already exists"},
        {"resellerName": "Nagashree", "resellerPhone": "8989898989", "resellerEmail": "nagashreenaik0@gmail.com", "resellerAddress": "BTM","expected_error": "Reseller Name already exists"},
        {"resellerName": "Nagashree1", "resellerPhone": "8989898989", "resellerEmail": "nagashreenaik040@gmail.com", "resellerAddress": "BTM","expected_error": "Email ID already exists"},
    ]

    def setup_reseller_test(self, driver):
        """Common setup for Reseller tests: login, navigate to Reseller page, and initialize screenshot utility."""
        login_helper = LoginHelper()
        login_helper.login(driver)
        self.logger.info("Login successful")
        time.sleep(2)

        res_page = ResellerPage(driver)
        res_page.navigate_to_Reseller()
        self.logger.info("Navigated to Reseller page")
        time.sleep(2)

        screenshot_util = ScreenshotUtility(driver)
        return res_page, screenshot_util

    def check_time_difference(self, modified_time_str, current_time_str):
        """Check if the modified time and current time difference is greater or less than 5 seconds."""
        # Define the format of the date and time
        time_format = "%d/%m/%Y %I:%M:%S %p"

        # Convert both strings to datetime objects
        modified_time = datetime.strptime(modified_time_str, time_format)
        current_time = datetime.strptime(current_time_str, time_format)

        # Calculate the absolute time difference in seconds
        time_difference = abs((current_time - modified_time).total_seconds())

        # If the difference is greater than 5 seconds, return True; if less than 5 seconds, return False
        return time_difference > 5, time_difference  # Return a tuple (is_greater_than_5_seconds, time_difference)

    def get_fake_phone(self):
        return str(self.fake.random_number(digits=10, fix_len=True))



    @pytest.mark.smoke
    def test_create_reseller(self, driver):
        res_page, screenshot_util = self.setup_reseller_test(driver)

        # Verify the Page Heading
        page_heading = res_page.get_reseller_heading()
        self.logger.info(f"Page Heading is: {page_heading}")

        try:
            assert page_heading == self.actual_page_heading, f"Expected Heading '{self.actual_page_heading}', but got '{page_heading}'"
            self.logger.info("Reseller page Heading verified successfully")
        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("test_valid_reseller_heading")
            self.logger.error(f"Test failed, screenshot saved at: {screenshot_path}")

        # Verify the Reseller Table
        reseller_table = res_page.get_reseller_list_table()
        self.logger.info(f"Table Heading is: {reseller_table}")
        try:
            assert reseller_table == self.actual_reseller_table, f"Expected Table '{self.actual_reseller_table}', but got '{reseller_table}'"
            self.logger.info("Reseller Table verified successfully")
        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("test_valid_reseller_table")
            self.logger.error(f"Test failed, screenshot saved at: {screenshot_path}")

        # Verify the Create button
        create_btn = res_page.get_create_btn()
        self.logger.info(f"Text of Create button is: {create_btn}")
        try:
            assert create_btn == self.actual_create_btn, f"Expected create button '{self.actual_create_btn}', but got '{create_btn}'"
            self.logger.info("Create button verified successfully")
            res_page.click_logout()
            self.logger.info("Logout successfully")
        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("test_valid_Create_button")
            self.logger.error(f"Test failed, screenshot saved at: {screenshot_path}")



    @pytest.mark.regress
    def test_already_exist_reseller(self, driver):
        res_page, screenshot_util = self.setup_reseller_test(driver)

        try:
            # Click the 'Add OTC' button to open the form
            res_page.click_Create_btn()
            time.sleep(2)
            self.logger.info("Successfully clicked 'Create' button")

            for test in self.already_exist_reseller_error_test_data:  # Updated to use the renamed attribute
                input_reseller_name = test["resellerName"]
                input_reseller_phone = test["resellerPhone"]
                input_reseller_email = test["resellerEmail"]
                input_reseller_address = test["resellerAddress"]
                expected_error = test["expected_error"]
                self.logger.info(
                    f"Existed Reseller Name: '{input_reseller_name}', Reseller Phone: '{input_reseller_phone}', Reseller Email: '{input_reseller_email}', Reseller Address: '{input_reseller_address}', Expected error: '{expected_error}'"
                )

                try:
                    # Clear the input field before entering new text
                    res_page.clear_element(res_page.reseller_name)
                    self.logger.info("Cleared Reselller Name field")
                    res_page.enter_reseller_name(input_reseller_name)
                    self.logger.info(f"Entered Reseller Name: '{input_reseller_name}'")

                    res_page.clear_element(res_page.reseller_phone)
                    self.logger.info("Cleared Reselller Phone field")
                    res_page.enter_reseller_phone(input_reseller_phone)
                    self.logger.info(f"Entered Reseller Phone: '{input_reseller_phone}'")

                    res_page.clear_element(res_page.reseller_email)
                    self.logger.info("Cleared Reselller Email field")
                    res_page.enter_reseller_email(input_reseller_email)
                    self.logger.info(f"Entered Reseller Email: '{input_reseller_email}'")

                    res_page.clear_element(res_page.reseller_address)
                    self.logger.info("Cleared Reselller Address field")
                    res_page.enter_reseller_address(input_reseller_address)
                    self.logger.info(f"Entered Reseller Address: '{input_reseller_address}'")

                    res_page.click_add_btn()

                    try:
                        get_reseller_error_msg = res_page.get_reseller_error_msg()
                        self.logger.info(f"Reseller error message is: {get_reseller_error_msg}")
                        assert get_reseller_error_msg == expected_error, (
                        f"Expected Resellerr error message '{expected_error}', but got '{get_reseller_error_msg}'")
                        res_page.click_ok_btn()
                        self.logger.info("Clicked the 'OK' button successfully")
                    except Exception as e:
                        screenshot_path = screenshot_util.capture_screenshot("add_otc_failure")
                        self.logger.error(
                            f"Error message not found or incorrect: {str(e)}")
                        self.logger.error(f"Screenshot saved at: {screenshot_path}")
                        raise

                except Exception as e:
                    screenshot_path = screenshot_util.capture_screenshot("test_reseller_already_exist_error_msg")
                    self.logger.error(f"Test failed: {str(e)}")
                    self.logger.error(f"Screenshot saved at: {screenshot_path}")

            res_page.click_logout()
            self.logger.info("Logout successfully")

        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("test_reseller_already_exist_error_msg")
            self.logger.error(f"Test failed: {str(e)}")
            self.logger.error(f"Screenshot saved at: {screenshot_path}")
            with open(screenshot_path, "rb") as image_file:
                allure.attach(
                    image_file.read(),
                    name="Test Add Button Error Failure",
                    attachment_type=allure.attachment_type.PNG
                )
            raise

    """
    @pytest.mark.integration
    def test_create_reseller(self, driver):
        #
        res_page, screenshot_util = self.setup_reseller_test(driver)

        email = LoginHelper.email  # Access the email class attribute
        self.logger.info(f"Email value: {email}")  # Or use it as needed

        # Validate Create button clickable (Scenario 1)
        try:
            button = res_page.wait_for_element(res_page.create_btn)
            assert button.is_enabled(), "'Create' button is not enabled"
            res_page.click_Create_btn()
            self.logger.info("Successfully clicked 'Create' button")
        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("create_button_failure")
            self.logger.error(f"Failed to validate 'Create' button: {str(e)}")
            self.logger.error(f"Current URL: {driver.current_url}")
            #self.logger.error(f"Page source: {driver.page_source[:500]}...")
            self.logger.error(f"Screenshot saved at: {screenshot_path}")
            raise

        # Validate Add Manage Reseller page (Scenario 2)
        try:
            self.logger.info("'Add Output Type Config' popup displayed")
            assert res_page.wait_for_element(res_page.add_res_page).is_displayed(), "Page heading not displayed"
            assert res_page.wait_for_element(res_page.reseller_name).is_displayed(), "Reseller Name field not displayed"
            assert res_page.wait_for_element(res_page.reseller_phone).is_displayed(), "Reseller Phone field not displayed"
            assert res_page.wait_for_element(res_page.reseller_email).is_displayed(), "Reseller Email field not displayed"
            assert res_page.wait_for_element(res_page.reseller_address).is_displayed(), "Reseller Address field not displayed"
            assert res_page.wait_for_element(res_page.add_btn).is_displayed(), "Add button not displayed"
            self.logger.info("Page contains heading, Text fields and Add button")
        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("add_reseller_page_failure")
            self.logger.error(f"Failed to verify 'Add Manage Reseller' page or elements: {str(e)}")
            self.logger.error(f"Current URL: {driver.current_url}")
            #self.logger.error(f"Page source: {driver.page_source[:500]}...")
            self.logger.error(f"Screenshot saved at: {screenshot_path}")
            raise

        # Validate Add Reseller and verify the success message
        res_page.enter_reseller_name(self.reseller_name)
        self.logger.info(f"Entered Reseller Name : {self.reseller_name}")
        res_page.enter_reseller_phone(self.get_fake_phone())
        self.logger.info(f"Entered Reseller Phone : {self.get_fake_phone()}")
        res_page.enter_reseller_email(self.reseller_email)
        self.logger.info(f"Entered Reseller Email : {self.reseller_email}")
        res_page.enter_reseller_address(self.reseller_address)
        self.logger.info(f"Entered Reseller Address : {self.reseller_address}")
        time.sleep(3)
        res_page.click_add_btn()
        # Log after the update with the exact time
        current_time = datetime.now()
        current_time_after_add = current_time.strftime("%d/%m/%Y %I:%M:%S %p")
        self.logger.info(f"Current Time after add is: {current_time_after_add}")
        self.logger.info("Clicked the add button")

        try:
            get_reseller_success_msg = res_page.get_reseller_success_msg()
            self.logger.info(f"Reseller success message is: {get_reseller_success_msg}")
            assert get_reseller_success_msg == self.expected_reseller_success_msg, (
                f"Expected Reseller success message '{self.expected_reseller_success_msg}', but got '{get_reseller_success_msg}'")
            res_page.click_ok_btn()
            self.logger.info("Clicked the 'OK' button successfully")
        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("add_reseller_failure")
            self.logger.error(f"Success message '{self.expected_reseller_success_msg}' not found or incorrect: {str(e)}")
            self.logger.error(f"Screenshot saved at: {screenshot_path}")
            raise

        # Verify the created Reseller in List of Reseller Table
        try:
            table_data = res_page.get_table_data()
            found = False
            for row in table_data:
                if row['Reseller Name'] == self.reseller_name and row['Phone Number'] == self.reseller_phone and row['Email ID'] == self.reseller_email and row['Status'] == self.status:
                    found = True
                    self.logger.info(
                        f"Found created Reseller entry: Reseller Name '{self.reseller_name}', Phone Number  '{self.reseller_phone}', Email ID '{self.reseller_email}', Status : {row['Status']} ")

                    res_page.click_view_btn_in_row(self.reseller_email)


                    # Check if the difference between the current time and created date is greater than 5 seconds
                    is_greater, time_difference = self.check_time_difference(row['Created Date'],
                                                                             current_time_after_add)
                    if row['Created Date'] == current_time_after_add:
                        self.logger.info(
                            f"Created date {row['Created Date']} and current date {current_time_after_add} are the same")
                    elif is_greater:  # Fixed syntax: 'else if' should be 'elif' in Python
                        self.logger.error(
                            f"Created date {row['Created Date']} and current date {current_time_after_add} " f"differ by {time_difference} seconds, which is greater than 5 seconds.")
                        raise AssertionError(f"Created date and current date differ by more than 5 seconds.")
                    else:
                        self.logger.info(
                            f"Created date {row['Created Date']} and current date {current_time_after_add} "
                            f"differ by {time_difference} seconds, which is within the 5-second threshold.")
                    break
            assert found, f"OTC entry with Output Type '{self.outputType}' and Output Type Name '{self.outputTypeName}' not found in table"
            self.logger.info("OTC entry verified successfully in the table")
        except Exception as e:
            self.logger.error(f"Failed to verify OTC entry in table: {str(e)}")
            screenshot_path = screenshot_util.capture_screenshot("test_added_otc_in_table_failure")
            self.logger.error(f"Test failed, screenshot saved at: {screenshot_path}")
            raise

        res_page.click_logout()
        self.logger.info("Logout successfully")
    """

