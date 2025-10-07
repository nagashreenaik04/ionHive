import random
import time
from datetime import datetime

import pytest
import allure
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.support.select import Select
import string
from faker.providers import BaseProvider

from pages.device_page import ChargerPage
from utilities.custom_logger import LogGen
from utilities.login_helper import LoginHelper
from utilities.screenshot_utility import ScreenshotUtility
from faker import Faker
from utilities.device_data_provider import DeviceDataProvider


@pytest.mark.usefixtures("driver")
class TestCharger:
    logger = LogGen.loggen()
    fake = Faker()

    actual_page_heading = "Manage Device-Unallocated"
    actual_unallocated_charger_table = "List Of Chargers"
    actual_add_device_heading = "Add Manage Device"

    expected_create_success_msg = "Charger added successfully"
    status = "Active"

    #inputs from the faker class
    fake.add_provider(DeviceDataProvider)

    chargerID = fake.charger_id()
    vendor = fake.vendor()
    chargerModel = fake.charger_model()
    chargerType = fake.charger_type()
    maxCurrent = fake.max_current()
    maxPower = fake.max_power()
    bluetoothModule = fake.bluetooth()
    wifiModule = fake.wifi_module()
    connectorType = fake.connector_type()
    type_name_options = ""
    typeName = ""



    def setup_otc_test(self, driver):
        """Common setup for OTC tests: login, navigate to OTC page, and initialize screenshot utility."""
        login_helper = LoginHelper()
        login_helper.login(driver)
        self.logger.info("Login successful")
        time.sleep(2)

        charger_page = ChargerPage(driver)
        charger_page.click_device_drpdwn()
        charger_page.navigate_unallocated_charger()
        self.logger.info("Navigated to Unallocated Charger page")
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

    def charger_id(self, length=14):
        """Generate a ChargerID with max 14 characters (letters + digits only)."""
        allowed_chars = string.ascii_uppercase + string.digits  # Only A-Z and 0-9
        return ''.join(random.choices(allowed_chars, k=length))

    @pytest.mark.smoke
    def test_add_charger(self, driver):
        charger_page, screenshot_util = self.setup_otc_test(driver)

        # Verify the Page Heading
        page_heading = charger_page.get_unallocated_heading()
        self.logger.info(f"Page Heading is: {page_heading}")
        try:
            assert page_heading == self.actual_page_heading, f"Expected Heading '{self.actual_page_heading}', but got '{page_heading}'"
            self.logger.info("Unallocated charger page Heading verified successfully")
        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("test_valid_OTC_heading")
            self.logger.error(f"Test failed, screenshot saved at: {screenshot_path}")

        # Verify the Unallocated charger Table
        unallocated_charger_table = charger_page.get_unallocated_charger_list_table()
        self.logger.info(f"Table Heading is: {unallocated_charger_table}")
        try:
            assert unallocated_charger_table == self.actual_unallocated_charger_table, f"Expected Table '{self.actual_unallocated_charger_table}', but got '{unallocated_charger_table}'"
            self.logger.info("Unallocated Charger Table verified successfully")
        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("test_valid_OTC_table")
            self.logger.error(f"Test failed, screenshot saved at: {screenshot_path}")


        #Add Manage Device
        charger_page.click_create_btn()
        time.sleep(2)
        #verify the page heading
        add_page_heading = charger_page.get_add_device_heading()
        self.logger.info(f"Page Heading is: {add_page_heading}")
        try:
            assert add_page_heading == self.actual_add_device_heading, f"Expected Heading '{self.actual_add_device_heading}', but got '{add_page_heading}'"
            self.logger.info("Add Device page Heading verified successfully")
        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("test_valid_OTC_heading")
            self.logger.error(f"Test failed, screenshot saved at: {screenshot_path}")
        #enter the datas
        charger_page.enter_chargerID(self.chargerID)
        self.logger.info("Enter Charger ID : " + self.chargerID)
        charger_page.enter_vendor(self.vendor)
        self.logger.info("Enter Vendor : " + self.vendor)
        charger_page.enter_chargerModel(self.chargerModel)
        self.logger.info("Enter Charger Model : " + self.chargerModel)
        charger_page.enter_chargerType(self.chargerType)
        self.logger.info("Enter Charger Type : " + self.chargerType)
        charger_page.enter_maxCurrent(self.maxCurrent)
        self.logger.info("Enter Charger Max Current : " + str(self.maxCurrent))
        charger_page.enter_maxPower(self.maxPower)
        self.logger.info("Enter Charger Max Power : " + str(self.maxPower))
        charger_page.enter_wifiModule(str(self.wifiModule))
        self.logger.info("Enter Charger WiFi Module : " + str(self.wifiModule))
        charger_page.enter_bluetoothModule(str(self.bluetoothModule))
        self.logger.info("Enter Charger Bluetooth Module : " + str(self.bluetoothModule))
        charger_page.enter_connectorType(self.connectorType)
        self.logger.info("Enter Charger Connector Type : " + self.connectorType)
        time.sleep(5)
        # Get all options from Type Name dropdown
        type_name_options = charger_page.get_all_options_in_type_name()
        # Remove default placeholder if needed (like "Select type name")
        type_name_options = [opt for opt in type_name_options if opt.strip() and opt != "Select type name"]
        self.logger.info("Type name options: " +  str(type_name_options))
        # Pick a random option
        typeName = random.choice(type_name_options)
        # Use it to select in the dropdown
        charger_page.enter_typeName(typeName)
        self.logger.info("Enter type Name : " + typeName)
        time.sleep(3)
        charger_page.click_add_btn()
        # Log after the create with the exact time
        current_time = datetime.now()
        current_time_after_add = current_time.strftime("%d/%m/%Y %I:%M:%S %p")
        self.logger.info(f"Current Time after add is: {current_time_after_add}")
        self.logger.info("Clicked the 'Add' button")

        try:
            get_create_success_msg = charger_page.get_create_suc_msg()
            self.logger.info(f"Charger Created success message is: {get_create_success_msg}")
            assert get_create_success_msg == self.expected_create_success_msg, (
                f"Expected success message '{self.expected_create_success_msg}', but got '{get_create_success_msg}'")
            charger_page.click_ok_btn()
            self.logger.info("Clicked the 'OK' button successfully")
            # Verify the created Reseller in List of Reseller Table
            try:
                table_data = charger_page.get_table_data()
                found = False
                for row in table_data:
                    if row['Charger ID'] == self.chargerID and row['Charger Model'] == self.chargerModel and \
                            row['Charger Type'] == self.chargerType and row['Max Current'] == str(self.maxCurrent) and \
                            row['Status'] == self.status:
                        found = True
                        self.logger.info(
                            f"Found created charger entry: Charger ID '{self.chargerID}', Charger Model  '{self.chargerModel}', Charger Type {self.chargerType}, Max Current  {row['Created Date']},  Status : {row['Status']} ")

                self.logger.info("Reseller entry verified successfully in the table")

            except Exception as e:
                self.logger.error(f"Failed to verify created charger entry in table: {str(e)}")
                screenshot_path = screenshot_util.capture_screenshot("test_create_charger_in_table_failure")
                self.logger.error(f"Test failed, screenshot saved at: {screenshot_path}")
                raise

        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("create_charger_failure")
            self.logger.error(f"Success message '{self.expected_create_success_msg}' not found or incorrect: {str(e)}")
            self.logger.error(f"Screenshot saved at: {screenshot_path}")
            raise

        charger_page.click_logout()
        self.logger.info("Logout successfully")
        """
        charger_page.refresh()
        self.logger.info("Refresh screenshot successfully")
        time.sleep(5)

        # Verify the added charger in List of chragers Table
        try:
            table_data = charger_page.get_table_data()
            found = False
            for row in table_data:
                if row['ID'] == self.chargerID and row['Charger Model'] == self.chargerModel and row['Charger Type'] == self.chargerType and row['Max Current'] == self.maxCurrent and row['Status'] == self.status:
                    found = True
                    self.logger.info(f"Found created charger entry: Charger ID '{self.chargerID}', Charger Model  '{self.chargerModel}', Charger Type {self.chargerType}, Max Current  {row['Created Date']},  Status : {row['Status']} ")
                    
                    # Check if the difference between the current time and created date is greater than 5 seconds
                    is_greater, time_difference = self.check_time_difference(row['Created Date'],current_time_after_add)
                    if row['Created Date'] == current_time_after_add:
                        self.logger.info(
                            f"Created date {row['Created Date']} and current date {current_time_after_add} are the same")
                    elif is_greater:  # Fixed syntax: 'else if' should be 'elif' in Python
                        self.logger.error(f"Created date {row['Created Date']} and current date {current_time_after_add} " f"differ by {time_difference} seconds, which is greater than 5 seconds.")
                        raise AssertionError(f"Created date and current date differ by more than 5 seconds.")
                    else:
                        self.logger.info(
                            f"Created date {row['Created Date']} and current date {current_time_after_add} "
                            f"differ by {time_difference} seconds, which is within the 5-second threshold.")
                    break
                    
            assert found, f"Charger entry with Charger ID '{self.chargerID}' and Charger Model '{self.chargerModel}' not found in table"
            self.logger.info("Charger entry verified successfully in the table")
        except Exception as e:
            self.logger.error(f"Failed to verify Charger entry in table: {str(e)}")
            screenshot_path = screenshot_util.capture_screenshot("test_create_charger_in_table_failure")
            self.logger.error(f"Test failed, screenshot saved at: {screenshot_path}")
            raise
        
        charger_page.click_logout()
        self.logger.info("Logout successfully")
        """










