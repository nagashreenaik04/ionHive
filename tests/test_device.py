import random
import time
from datetime import datetime

import pytest
import allure
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.support.select import Select

from pages.device_page import ChargerPage
from utilities.custom_logger import LogGen
from utilities.login_helper import LoginHelper
from utilities.screenshot_utility import ScreenshotUtility
from faker import Faker


@pytest.mark.usefixtures("driver")
class TestCharger:
    logger = LogGen.loggen()



    def setup_otc_test(self, driver):
        """Common setup for OTC tests: login, navigate to OTC page, and initialize screenshot utility."""
        login_helper = LoginHelper()
        login_helper.login(driver)
        self.logger.info("Login successful")
        time.sleep(2)

        charger_page = ChargerPage(driver)
        charger_page.navigate_to_OTC()
        self.logger.info("Navigated to OTC page")
        time.sleep(2)

        screenshot_util = ScreenshotUtility(driver)
        return charger_page, screenshot_util

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



