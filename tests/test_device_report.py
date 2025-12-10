import pytest
import random
import time
import re

from datetime import datetime

from faker import Faker
import allure

from pages.device_report_page import DeviceReportPage
from utilities.custom_logger import LogGen
from utilities.login_helper import LoginHelper
from utilities.screenshot_utility import ScreenshotUtility


@pytest.mark.usefixtures("driver")
class TestDeviceReport:
    logger = LogGen.loggen()

    actual_page_heading = "Device Report"

    def setup_device_report_test(self, driver):
        """Common setup for Device Report tests: login, navigate to Device Report page, and initialize screenshot utility."""
        login_helper = LoginHelper()
        login_helper.login(driver)
        self.logger.info("Login successful")
        time.sleep(2)

        dr_page = DeviceReportPage(driver)
        dr_page.navigate_to_device_report()
        self.logger.info("Navigated to Device Report page")
        time.sleep(2)

        screenshot_util = ScreenshotUtility(driver)
        return dr_page, screenshot_util

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

    @pytest.mark.smoke
    def test_verify_vehicle(self, driver):
        dr_page, screenshot_util = self.setup_device_report_test(driver)

        # Verify the Page Heading
        page_heading = dr_page.get_device_report_heading()
        self.logger.info(f"Page Heading is: {page_heading}")

        try:
            assert page_heading == self.actual_page_heading, f"Expected Heading '{self.actual_page_heading}', but got '{page_heading}'"
            self.logger.info("Device Report page Heading verified successfully")
        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("test_valid_device_report_heading")
            self.logger.error(f"Test failed, screenshot saved at: {screenshot_path}")

        # Verify the Vehicle Table
        vehicle_table = dr_page.get_vehicle_page_list_table()
        self.logger.info(f"Table Heading is: {vehicle_table}")
        try:
            assert vehicle_table == self.actual_vehicle_table, f"Expected Table '{self.actual_vehicle_table}', but got '{vehicle_table}'"
            self.logger.info("Vehicle Table verified successfully")
        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("test_valid_vehicle_table")
            self.logger.error(f"Test failed, screenshot saved at: {screenshot_path}")

        # Verify the 'Add Vehicle' button
        addVehicle_btn = dr_page.get_add_vehicle_btn()
        self.logger.info(f"Text of 'Add Vehicle' button is: {addVehicle_btn}")
        try:
            assert addVehicle_btn == self.actual_add_vehicle_btn, f"Expected create button '{self.actual_add_vehicle_btn}', but got '{addVehicle_btn}'"
            self.logger.info("Add Vehicle button verified successfully")
            dr_page.click_logout()
            self.logger.info("Logout successfully")
        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("test_valid_add_vehicle_button")
            self.logger.error(f"Test failed, screenshot saved at: {screenshot_path}")

