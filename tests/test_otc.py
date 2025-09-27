import random
import time
from datetime import datetime

import pytest
import allure
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.support.select import Select

from pages.otc_page import OTCPage
from utilities.custom_logger import LogGen
from utilities.login_helper import LoginHelper
from utilities.screenshot_utility import ScreenshotUtility
from faker import Faker

@pytest.mark.usefixtures("driver")
class TestOTC:
    logger = LogGen.loggen()

    # Validate the OTC page
    actual_page_heading = "Output Type Config"
    actual_otc_table = "List Of Output Type Config"
    actual_add_otc_btn = "Add Output Type Config"

    # Generate Faker data
    fake = Faker()
    outputTypeName = fake.lexify(text='????????????', letters='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')[:random.randint(1, 12)]
    outputType = random.choice(["Gun", "Socket"])

    email = " "
    modifiedBy = "-"
    modifiedDate = "-"
    status = "Active"

    #validate OTC success message
    expected_otc_success_msg = "Add Output Type Config successfully"

    # edit validation
    expected_edit_otc_success_msg = "Update Output Type Config successfully"

    #already existed data
    existed_type = "Gun"
    existed_type_name = "Type5"
    expected_otc_error_msg = "Output type already exists"

    # Define test cases for type name field
    test_type_name = [
        {"input": "466575645757", "expected_value": "466575645757", "expected_valid": True},
        {"input": "4665756abcde", "expected_value": "4665756abcde", "expected_valid": True},
        {"input": "abcdefgh1234", "expected_value": "abcdefgh1234", "expected_valid": True},
        {"input": "#$%%1234", "expected_value": "1234", "expected_valid": False},
        {"input": "abcd&*()", "expected_value": "abcd", "expected_valid": False},
        {"input": "%d", "expected_value": "d", "expected_valid": False},
        {"input": "ac354kd45k9085", "expected_value": "ac354kd45k90", "expected_valid": False},
        {"input": "", "expected_value": "", "expected_valid": True}
    ]

    # Test data for Add button error validation
    add_btn_error_test_data = [
        {"type": "Gun", "type_name": "", "expected_error": "Please fill out this field."},
        {"type": "", "type_name": "abc", "expected_error": "Please select an item in the list."},
        {"type": "", "type_name": "", "expected_error": "Please fill out this field."}
    ]

    def setup_otc_test(self, driver):
        """Common setup for OTC tests: login, navigate to OTC page, and initialize screenshot utility."""
        login_helper = LoginHelper()
        login_helper.login(driver)
        self.logger.info("Login successful")
        time.sleep(2)

        otc_page = OTCPage(driver)
        otc_page.navigate_to_OTC()
        self.logger.info("Navigated to OTC page")
        time.sleep(2)

        screenshot_util = ScreenshotUtility(driver)
        return otc_page, screenshot_util

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
    def test_otc_page(self, driver):
        otc_page, screenshot_util = self.setup_otc_test(driver)

        # Verify the Page Heading
        page_heading = otc_page.get_otc_heading()
        self.logger.info(f"Page Heading is: {page_heading}")
        try:
            assert page_heading == self.actual_page_heading, f"Expected Heading '{self.actual_page_heading}', but got '{page_heading}'"
            self.logger.info("OTC Heading verified successfully")
        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("test_valid_OTC_heading")
            self.logger.error(f"Test failed, screenshot saved at: {screenshot_path}")

        # Verify the OTC Table
        otc_table = otc_page.get_otc_list_table()
        self.logger.info(f"Table Heading is: {otc_table}")
        try:
            assert otc_table == self.actual_otc_table, f"Expected Table '{self.actual_otc_table}', but got '{otc_table}'"
            self.logger.info("OTC Table verified successfully")
        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("test_valid_OTC_table")
            self.logger.error(f"Test failed, screenshot saved at: {screenshot_path}")

        # Verify the Add OTC button
        add_otc_btn = otc_page.get_addOTC_btn()
        self.logger.info(f"Text of Add OTC button is: {add_otc_btn}")
        try:
            assert add_otc_btn == self.actual_add_otc_btn, f"Expected add OTC button '{self.actual_add_otc_btn}', but got '{add_otc_btn}'"
            self.logger.info("Add OTC button verified successfully")
            otc_page.click_logout()
            self.logger.info("Logout successfully")
        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("test_valid_Add_OTC_button")
            self.logger.error(f"Test failed, screenshot saved at: {screenshot_path}")

    @pytest.mark.sanity
    def test_verify_table_columns(self, driver):
        """Test to verify all expected columns are present in the OTC table."""
        self.logger.info("Starting test_verify_table_columns")
        otc_page, screenshot_util = self.setup_otc_test(driver)

        # List of expected columns and their getter methods
        columns = [
            ("Sl.No", otc_page.get_sino_clb),
            ("Output Type", otc_page.get_output_type_clb),
            ("Output Type Name", otc_page.get_output_type_name_clb),
            ("Created By", otc_page.get_created_by_clb),
            ("Created Date", otc_page.get_created_date_clb),
            ("Modified By", otc_page.get_modified_by_clb),
            ("Modified Date", otc_page.get_modified_date_clb),
            ("Status", otc_page.get_status_clb),
            ("Active/DeActive", otc_page.get_activeOrDeactive_clb),
            ("Option", otc_page.get_option_clb),
        ]

        missing_columns = []
        for expected_column_name, get_method in columns:
            try:
                captured_column_name = get_method()
                self.logger.info(f"Checking column '{expected_column_name}': Expected '{expected_column_name}', Got '{captured_column_name}'")
                assert captured_column_name == expected_column_name, f"Expected column text '{expected_column_name}', but got '{captured_column_name}'"
            except Exception as e:
                self.logger.error(f"Column '{expected_column_name}' not found or incorrect: {str(e)}")
                missing_columns.append(expected_column_name)
                screenshot_path = screenshot_util.capture_screenshot(
                    f"missing_column_{expected_column_name.replace('.', '_').replace('/', '_')}")
                self.logger.error(f"Screenshot saved at: {screenshot_path}")
                with open(screenshot_path, "rb") as image_file:
                    allure.attach(image_file.read(), name=f"Missing Column {expected_column_name}",
                                  attachment_type=allure.attachment_type.PNG)

        assert not missing_columns, f"Missing or incorrect columns: {', '.join(missing_columns)}"
        self.logger.info("All expected columns are present in the OTC table")
        otc_page.click_logout()
        self.logger.info("Logout successfully")

    @pytest.mark.integration
    def test_add_otc(self, driver):
        #
        otc_page, screenshot_util = self.setup_otc_test(driver)

        email = LoginHelper.email  # Access the email class attribute
        self.logger.info(f"Email value: {email}")  # Or use it as needed

        # Validate Add OTC button clickable (Scenario 1)
        try:
            button = otc_page.wait_for_element(otc_page.addOTC_btn)
            assert button.is_enabled(), "'Add Output Type Config' button is not enabled"
            otc_page.click_addOTC()
            self.logger.info("Successfully clicked 'Add OTC' button")
        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("add_otc_button_failure")
            self.logger.error(f"Failed to validate 'Add Output Type Config' button: {str(e)}")
            self.logger.error(f"Current URL: {driver.current_url}")
            self.logger.error(f"Page source: {driver.page_source[:500]}...")
            self.logger.error(f"Screenshot saved at: {screenshot_path}")
            raise

        # Validate popup appearance and elements (Scenario 2)
        try:
            self.logger.info("'Add Output Type Config' popup displayed")
            assert otc_page.wait_for_element(otc_page.add_otc_heading).is_displayed(), "Popup heading not displayed"
            assert otc_page.wait_for_element(otc_page.type_drpdwn).is_displayed(), "Type dropdown not displayed"
            assert otc_page.wait_for_element(otc_page.add_output_type_name_field).is_displayed(), "Type Name field not displayed"
            assert otc_page.wait_for_element(otc_page.add_btn).is_displayed(), "Add button not displayed"
            self.logger.info("Popup contains heading, Type dropdown, Type Name field, and Add button")
        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("add_otc_popup_failure")
            self.logger.error(f"Failed to verify 'Add Output Type Config' popup or elements: {str(e)}")
            self.logger.error(f"Current URL: {driver.current_url}")
            self.logger.error(f"Page source: {driver.page_source[:500]}...")
            self.logger.error(f"Screenshot saved at: {screenshot_path}")
            raise

        #Validate Add OTC and verify the success message
        otc_page.select_output_type(self.outputType)
        self.logger.info(f"Selected output type: {self.outputType}")
        otc_page.enter_output_type_name(self.outputTypeName)
        self.logger.info(f"Entered output type name: {self.outputTypeName}")
        otc_page.click_add_btn()
        # Log after the update with the exact time
        current_time = datetime.now()
        current_time_after_add = current_time.strftime("%d/%m/%Y %I:%M:%S %p")
        self.logger.info(f"Current Time after add is: {current_time_after_add}")
        self.logger.info("Clicked the add OTC button")

        try:
            get_otc_success_msg = otc_page.get_otc_success_msg()
            self.logger.info(f"OTC success message is: {get_otc_success_msg}")
            assert get_otc_success_msg == self.expected_otc_success_msg, (f"Expected OTC success message '{self.expected_otc_success_msg}', but got '{get_otc_success_msg}'")
            otc_page.click_ok_btn()
            self.logger.info("Clicked the 'OK' button successfully")
        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("add_otc_failure")
            self.logger.error(f"Success message '{self.expected_otc_success_msg}' not found or incorrect: {str(e)}")
            self.logger.error(f"Screenshot saved at: {screenshot_path}")
            raise


        # Verify the added OTC in List of OTC Table
        try:
            table_data = otc_page.get_table_data()
            found = False
            for row in table_data:
                if row['Output Type'] == self.outputType and row['Output Type Name'] == self.outputTypeName and row['Created By'] == email and row['Modified By'] == self.modifiedBy and row['Modified Date'] == self.modifiedDate and row['Status'] == self.status:
                    found = True
                    self.logger.info(f"Found added OTC entry: Output Type '{self.outputType}', Output Type Name  '{self.outputTypeName}', Created By {row['Created By']}, Created Date  {row['Created Date']}, Modified By : {row['Modified By']}, Modified Date : {row['Modified Date']}, Status : {row['Status']} ")

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
            assert found, f"OTC entry with Output Type '{self.outputType}' and Output Type Name '{self.outputTypeName}' not found in table"
            self.logger.info("OTC entry verified successfully in the table")
        except Exception as e:
            self.logger.error(f"Failed to verify OTC entry in table: {str(e)}")
            screenshot_path = screenshot_util.capture_screenshot("test_added_otc_in_table_failure")
            self.logger.error(f"Test failed, screenshot saved at: {screenshot_path}")
            raise

        otc_page.click_logout()
        self.logger.info("Logout successfully")

    @pytest.mark.regressio
    def test_type_dropdown(self, driver):
        otc_page, screenshot_util = self.setup_otc_test(driver)

        # Test data for dropdown validation
        TEST_DATA = [

            {
                "output_type": "Gun",
                "expected_result": "success",
                "description": "Select valid option 'Gun' from Type dropdown"
            },
            {
                "output_type": "Select Type",
                "expected_result": "success",
                "description": "Select valid option 'Select Type' from Type dropdown"
            },
            {
                "output_type": "Socket",
                "expected_result": "success",
                "description": "Select valid option 'Socket' from Type dropdown"
            },
            {
                "output_type": "Connector",
                "expected_result": "failure",
                "description": "Attempt to select invalid option 'Connector' (not in dropdown)"
            }
        ]
        EXPECTED_DROPDOWN_OPTIONS = ["Select Type", "Gun", "Socket"]

        try:
            # Click the 'Add OTC' button to open the form
            otc_page.click_addOTC()
            self.logger.info("Successfully clicked 'Add OTC' button")

            # Verify dropdown options by visible text
            dropdown_element = otc_page.wait_for_element(otc_page.type_drpdwn)
            select = Select(dropdown_element)
            actual_options = [option.text.strip() for option in select.options]
            assert actual_options == EXPECTED_DROPDOWN_OPTIONS, (
                f"Dropdown options mismatch. Expected: {EXPECTED_DROPDOWN_OPTIONS}, Got: {actual_options}"
            )
            self.logger.info(f"Verified dropdown options: {actual_options}")

            # Test each output type in the test data
            for test_case in TEST_DATA:
                output_type = test_case["output_type"]
                expected_result = test_case["expected_result"]
                description = test_case["description"]
                self.logger.info(f"Running test case: {description}")

                try:
                    otc_page.select_output_type(output_type)
                    if expected_result == "success":
                        self.logger.info(f"Successfully selected '{output_type}' as expected")
                        time.sleep(2)
                        # Verify the selected option
                        selected_option = select.first_selected_option.text.strip()
                        assert selected_option == output_type, (
                            f"Expected '{output_type}' to be selected, but '{selected_option}' was selected"
                        )
                    else:
                        self.logger.error(f"Unexpectedly selected '{output_type}', which should not be in the dropdown")
                        screenshot_path = screenshot_util.capture_screenshot(
                            f"unexpected_selection_{output_type.replace(' ', '_')}")
                        self.logger.error(f"Screenshot saved at: {screenshot_path}")
                        raise AssertionError(f"Selected invalid option '{output_type}' unexpectedly")
                except (NoSuchElementException, TimeoutException) as e:
                    if expected_result == "failure":
                        self.logger.info(f"Correctly failed to select '{output_type}' as it is not in the dropdown")
                    else:
                        self.logger.error(f"Failed to select '{output_type}': {str(e)}")
                        screenshot_path = screenshot_util.capture_screenshot(
                            f"failed_selection_{output_type.replace(' ', '_')}")
                        self.logger.error(f"Screenshot saved at: {screenshot_path}")
                        raise

            self.logger.info("All test cases for Type dropdown completed successfully")
            otc_page.click_logout()
            self.logger.info("Logout successfully")

        except Exception as e:
            self.logger.error(f"Test failed: {str(e)}")
            screenshot_path = screenshot_util.capture_screenshot("test_type_dropdown_failure")
            self.logger.error(f"Screenshot saved at: {screenshot_path}")
            raise

    @pytest.mark.regression
    def test_type_name_field(self, driver):
        otc_page, screenshot_util = self.setup_otc_test(driver)

        try:
            # Click the 'Add OTC' button to open the form
            otc_page.click_addOTC()
            self.logger.info("Successfully clicked 'Add OTC' button")

            # Select a valid Type to ensure form submission is possible
            otc_page.select_output_type(self.outputType)
            self.logger.info(f"Selected output type: {self.outputType}")

            for test in self.test_type_name:
                input_text = test["input"]
                expected_value = test["expected_value"]
                expected_valid = test["expected_valid"]
                self.logger.info(
                    f"Testing input: '{input_text}', Expected value: '{expected_value}', Expected valid: {expected_valid}"
                )

                try:
                    # Clear the input field before entering new text
                    otc_page.clear_element(otc_page.add_output_type_name_field)
                    self.logger.info("Cleared Output Type Name field")

                    # Enter the input text
                    otc_page.enter_output_type_name(input_text)
                    self.logger.info(f"Entered input: '{input_text}'")

                    # Get the actual value in the field
                    actual_value = otc_page.get_attribute(otc_page.add_output_type_name_field, "value")
                    assert actual_value == expected_value, (
                        f"Expected field value '{expected_value}', but got '{actual_value}' for input '{input_text}'"
                    )
                    self.logger.info(f"Verified field value: '{actual_value}' matches expected '{expected_value}'")

                except Exception as e:
                    screenshot_path = screenshot_util.capture_screenshot(
                        f"type_name_test_failure_{input_text.replace(' ', '_').replace('&', '_').replace('*', '_').replace('(', '_').replace(')', '_')}"
                    )
                    self.logger.error(f"Test case failed for input '{input_text}': {str(e)}")
                    self.logger.error(f"Screenshot saved at: {screenshot_path}")
                    with open(screenshot_path, "rb") as image_file:
                        allure.attach(
                            image_file.read(),
                            name=f"Test Failure {input_text}",
                            attachment_type=allure.attachment_type.PNG
                        )
                    raise

            self.logger.info("All test cases for Output Type Name field completed successfully")
            otc_page.click_logout()
            self.logger.info("Logout successfully")

        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("test_type_name_field_failure")
            self.logger.error(f"Test failed: {str(e)}")
            self.logger.error(f"Screenshot saved at: {screenshot_path}")
            with open(screenshot_path, "rb") as image_file:
                allure.attach(
                    image_file.read(),
                    name="Test Type Name Field Failure",
                    attachment_type=allure.attachment_type.PNG
                )
            raise

    @pytest.mark.regressi
    def test_add_btn_error(self, driver):
        otc_page, screenshot_util = self.setup_otc_test(driver)

        try:
            otc_page.click_addOTC()
            time.sleep(2)
            self.logger.info("Successfully clicked 'Add OTC' button")

            for test in self.add_btn_error_test_data:  # Updated to use the renamed attribute
                input_type = test["type"]
                input_type_name = test["type_name"]
                expected_error = test["expected_error"]
                self.logger.info(
                    f"Testing Type: '{input_type}', Type Name: '{input_type_name}', Expected error: '{expected_error}'"
                )

                try:
                    otc_page.clear_element(otc_page.add_output_type_name_field)
                    self.logger.info("Cleared Output Type Name field")

                    if input_type:
                        otc_page.select_output_type(input_type)
                        self.logger.info(f"Selected Type: '{input_type}'")
                    else:
                        otc_page.select_output_type("Select Type")
                        self.logger.info("Selected placeholder 'Select Type'")

                    if input_type_name:
                        otc_page.enter_output_type_name(input_type_name)
                        self.logger.info(f"Entered Output Type Name: '{input_type_name}'")

                    otc_page.click_add_btn()
                    self.logger.info("Clicked 'Add' button")

                    error_message = None
                    if input_type_name == "":
                        element = otc_page.find_element(otc_page.add_output_type_name_field)
                        error_message = driver.execute_script("return arguments[0].validationMessage;", element)
                    else:
                        element = otc_page.find_element(otc_page.type_drpdwn)
                        error_message = driver.execute_script("return arguments[0].validationMessage;", element)

                    assert error_message == expected_error, (
                        f"Expected error message '{expected_error}', but got '{error_message}' for Type '{input_type}' and Type Name '{input_type_name}'"
                    )
                    self.logger.info(f"Verified error message: '{error_message}'")

                except Exception as e:
                    screenshot_path = screenshot_util.capture_screenshot(
                        f"test_add_btn_error_failure_type_{input_type.replace(' ', '_')}_name_{input_type_name.replace(' ', '_')}"
                    )
                    self.logger.error(
                        f"Test case failed for Type '{input_type}' and Type Name '{input_type_name}': {str(e)}")
                    self.logger.error(f"Screenshot saved at: {screenshot_path}")
                    with open(screenshot_path, "rb") as image_file:
                        allure.attach(
                            image_file.read(),
                            name=f"Test Failure Type_{input_type}_Name_{input_type_name}",
                            attachment_type=allure.attachment_type.PNG
                        )
                    raise

            self.logger.info("All test cases for Add button error validation completed successfully")
            otc_page.click_logout()
            self.logger.info("Logout successfully")

        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("test_add_btn_error_failure")
            self.logger.error(f"Test failed: {str(e)}")
            self.logger.error(f"Screenshot saved at: {screenshot_path}")
            with open(screenshot_path, "rb") as image_file:
                allure.attach(
                    image_file.read(),
                    name="Test Add Button Error Failure",
                    attachment_type=allure.attachment_type.PNG
                )
            raise

    @pytest.mark.regress
    def test_already_exist_otc(self, driver):
        otc_page, screenshot_util = self.setup_otc_test(driver)

        try:
            # Click the 'Add OTC' button to open the form
            otc_page.click_addOTC()
            self.logger.info("Successfully clicked 'Add OTC' button")

            #Enter already existed OTC
            otc_page.select_output_type(self.existed_type)
            otc_page.enter_output_type_name(self.existed_type_name)
            otc_page.click_add_btn()

            try:
                get_otc_error_msg = otc_page.get_otc_error_msg()
                self.logger.info(f"OTC error message is: {get_otc_error_msg}")
                assert get_otc_error_msg == self.expected_otc_error_msg, (
                    f"Expected OTC error message '{self.expected_otc_error_msg}', but got '{get_otc_error_msg}'")
                otc_page.click_ok_btn()
                self.logger.info("Clicked the 'OK' button successfully")
            except Exception as e:
                screenshot_path = screenshot_util.capture_screenshot("add_otc_failure")
                self.logger.error(f"Success message '{self.expected_otc_success_msg}' not found or incorrect: {str(e)}")
                self.logger.error(f"Screenshot saved at: {screenshot_path}")
                raise

            otc_page.click_logout()
            self.logger.info("Logout successfully")

        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("test_add_btn_error_failure")
            self.logger.error(f"Test failed: {str(e)}")
            self.logger.error(f"Screenshot saved at: {screenshot_path}")
            with open(screenshot_path, "rb") as image_file:
                allure.attach(
                    image_file.read(),
                name="Test Add Button Error Failure",
                attachment_type=allure.attachment_type.PNG
            )
            raise

    @pytest.mark.regres
    def test_close_icon_at_add_otc_popup(self, driver):
        otc_page, screenshot_util = self.setup_otc_test(driver)
        try:
            # Click the 'Add OTC' button to open the form
            otc_page.click_addOTC()
            self.logger.info("Successfully clicked 'Add OTC' button")
            time.sleep(2)
            #click the close icon in 'Add OTC' popup
            otc_page.click_close_icon()
            time.sleep(1)
            self.logger.info("Successfully clicked close icon")
            #Logout
            otc_page.click_logout()
            self.logger.info("Logout successfully")
        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("test_add_btn_error_failure")
            self.logger.error(f"Test failed: {str(e)}")
            self.logger.error(f"Screenshot saved at: {screenshot_path}")
            with open(screenshot_path, "rb") as image_file:
                allure.attach(
                    image_file.read(),
                    name="Test Add Button Error Failure",
                    attachment_type=allure.attachment_type.PNG
                )
            raise

    @pytest.mark.regre
    def test_close_icon_at_edit_otc_popup(self, driver):
        otc_page, screenshot_util = self.setup_otc_test(driver)
        try:
            # Click the 'Edit OTC' button to open the form
            otc_page.click_edit_btn()
            self.logger.info("Successfully clicked 'Edit OTC' button")
            time.sleep(2)
            # click the close icon in 'Edit OTC' popup
            otc_page.click_close_icon_edit_popup()
            time.sleep(1)
            self.logger.info("Successfully clicked close icon")
            # Logout
            otc_page.click_logout()
            self.logger.info("Logout successfully")
        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("test_add_btn_error_failure")
            self.logger.error(f"Test failed: {str(e)}")
            self.logger.error(f"Screenshot saved at: {screenshot_path}")
            with open(screenshot_path, "rb") as image_file:
                allure.attach(
                    image_file.read(),
                    name="Test Add Button Error Failure",
                    attachment_type=allure.attachment_type.PNG
                )
            raise

    @pytest.mark.regr
    def test_type_name_field_edit_popup(self, driver):
        otc_page, screenshot_util = self.setup_otc_test(driver)

        try:
            # Click the 'Edit OTC' button to open the form
            otc_page.click_edit_btn()
            self.logger.info("Successfully clicked 'Edit OTC' button")

            for test in self.test_type_name:
                input_text = test["input"]
                expected_value = test["expected_value"]
                expected_valid = test["expected_valid"]
                self.logger.info(
                    f"Testing input: '{input_text}', Expected value: '{expected_value}', Expected valid: {expected_valid}"
                )

                try:
                    # Clear the input field before entering new text
                    otc_page.clear_element(otc_page.edit_output_type_name_field)
                    self.logger.info("Cleared Output Type Name field")

                    # Enter the input text
                    otc_page.enter_edit_output_type_name(input_text)
                    self.logger.info(f"Entered input: '{input_text}'")

                    # Get the actual value in the field
                    actual_value = otc_page.get_attribute(otc_page.edit_output_type_name_field, "value")
                    assert actual_value == expected_value, (
                        f"Expected field value '{expected_value}', but got '{actual_value}' for input '{input_text}'"
                    )
                    self.logger.info(f"Verified field value: '{actual_value}' matches expected '{expected_value}'")

                except Exception as e:
                    screenshot_path = screenshot_util.capture_screenshot(
                        f"type_name_test_failure_{input_text.replace(' ', '_').replace('&', '_').replace('*', '_').replace('(', '_').replace(')', '_')}"
                    )
                    self.logger.error(f"Test case failed for input '{input_text}': {str(e)}")
                    self.logger.error(f"Screenshot saved at: {screenshot_path}")
                    with open(screenshot_path, "rb") as image_file:
                        allure.attach(
                            image_file.read(),
                            name=f"Test Failure {input_text}",
                            attachment_type=allure.attachment_type.PNG
                        )
                    raise

            self.logger.info("All test cases for Output Type Name field completed successfully")
            otc_page.click_logout()
            self.logger.info("Logout successfully")

        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("test_type_name_field_failure")
            self.logger.error(f"Test failed: {str(e)}")
            self.logger.error(f"Screenshot saved at: {screenshot_path}")
            with open(screenshot_path, "rb") as image_file:
                allure.attach(
                    image_file.read(),
                    name="Test Type Name Field Failure",
                    attachment_type=allure.attachment_type.PNG
                )
            raise

    @pytest.mark.re
    def test_updateDisable_typeFielReadable_typeNameFieldEditable(self, driver):
        otc_page, screenshot_util = self.setup_otc_test(driver)

        try:
            # Click the 'Edit OTC' button to open the form
            otc_page.click_edit_btn()
            self.logger.info("Successfully clicked 'Edit OTC' button")

            # Locate the 'Type' input field and verify it is read-only
            type_input = otc_page.get_edit_type_field()
            assert type_input.get_attribute("readonly") == "true", "Type field is not read-only"
            self.logger.info("Verified that 'Type' field is read-only")

            # Locate the 'Update' button and verify it is disabled
            update_button = otc_page.get_update_btn_not_clickable()
            assert update_button.get_attribute("disabled") == "true", "Update button is not disabled"
            self.logger.info("Verified that 'Update' button is disabled")

            # Optionally, attempt to edit the 'Type Name' field to ensure it can be edited
            type_name_input = otc_page.get_type_name_readable()
            assert type_name_input.get_attribute("readonly") is None, "Type Name field is unexpectedly read-only"
            self.logger.info("Verified that 'Type Name' field is editable")


        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("test_type_name_field_failure")
            self.logger.error(f"Test failed: {str(e)}")
            self.logger.error(f"Screenshot saved at: {screenshot_path}")
            with open(screenshot_path, "rb") as image_file:
                allure.attach(
                    image_file.read(),
                    name="Test Type Name Field Failure",
                    attachment_type=allure.attachment_type.PNG
                )
            raise

        otc_page.click_logout()
        self.logger.info("Logout successfully")


    @pytest.mark.retest
    def test_edit_otc(self, driver):
        otc_page, screenshot_util = self.setup_otc_test(driver)

        try:
            # Get table data
            table_data = otc_page.get_table_data()
            self.logger.info(f"Table has {len(table_data)} rows")

            # Check if the 7th row exists
            if len(table_data) < 7:
                raise ValueError(f"Table has only {len(table_data)} rows, cannot access 7th row")

            # Capture the 7th row's data (index 6)
            seventh_row = table_data[6]
            self.logger.info(f"7th row data: {seventh_row}")

            # Store important fields for comparison
            old_output_type = seventh_row['Output Type']
            old_output_type_name = seventh_row['Output Type Name']
            old_created_by = seventh_row['Created By']
            old_created_date = seventh_row['Created Date']
            old_modified_date = seventh_row['Modified Date']

            # Click the 'Edit' button in the 7th row
            otc_page.click_edit_btn_in_row(7)
            self.logger.info("Successfully clicked 'Edit' button in 7th row")
            time.sleep(2)

            """
            # Validate Edit OTC and verify the success message
            otc_page.enter_edit_output_type_name(self.outputTypeName)
            self.logger.info(f"Entered new output type name: {self.outputTypeName}")
            otc_page.click_update_btn()
            # Log after the update with the exact time
            current_time = datetime.now()
            current_time_after_add = current_time.strftime("%d/%m/%Y %I:%M:%S %p")
            self.logger.info(f"Current Time after add is: {current_time_after_add}")
            self.logger.info("Clicked the Update button")"""

            # --- Retry logic for duplicate entries ---
            max_attempts = 5
            success = False

            for attempt in range(max_attempts):
                if attempt > 0:
                    # generate a new unique name for retry
                    self.outputTypeName = f"OTC_{random.randint(1000, 9999)}"
                    self.logger.warning(f"Retrying with new Output Type Name: {self.outputTypeName}")

                otc_page.enter_edit_output_type_name(self.outputTypeName)
                self.logger.info(f"Entered Output Type Name: {self.outputTypeName}")

                otc_page.click_update_btn()
                # Log after the update with the exact time
                current_time = datetime.now()
                current_time_after_edit = current_time.strftime("%d/%m/%Y %I:%M:%S %p")
                self.logger.info(f"Current Time after add is: {current_time_after_edit}")
                self.logger.info("Clicked the Update button")
                time.sleep(2)

                update_btn_disabled = otc_page.get_update_btn_not_clickable().get_attribute("disabled") == "true"

                if otc_page.get_edit_otc_success_msg():
                    get_otc_success_msg = otc_page.get_edit_otc_success_msg()
                    self.logger.info(f"OTC error message is: {get_otc_success_msg}")
                    assert get_otc_success_msg == self.expected_edit_otc_success_msg, (
                        f"Expected OTC error message '{self.expected_otc_error_msg}', but got '{get_otc_success_msg}'")
                    otc_page.click_ok_btn()
                    self.logger.info("Clicked the 'OK' button successfully")
                    success = True
                    break  # exit loop on success

                elif otc_page.get_otc_error_msg():
                    get_otc_error_msg = otc_page.get_otc_error_msg()
                    self.logger.info(f"OTC error message is: {get_otc_error_msg}")
                    assert get_otc_error_msg == self.expected_otc_error_msg, (
                        f"Expected OTC error message '{self.expected_otc_error_msg}', but got '{get_otc_error_msg}'")
                    otc_page.click_ok_btn()
                    self.logger.info("Clicked the 'OK' button successfully")

                elif update_btn_disabled:
                    self.logger.warning("Update button is disabled, retrying...")

                else:
                    self.logger.warning("Unexpected state, retrying...")

            if not success:
                raise AssertionError("Failed to update OTC after maximum retries")

            """
            for attempt in range(max_attempts):
                if attempt > 0:
                    # Generate a new unique output type name if retrying
                    self.outputTypeName = self.outputTypeName + str(random.randint(100, 999))
                    self.logger.warning(f"Retrying with new Output Type Name: {self.outputTypeName}")

                otc_page.enter_edit_output_type_name(self.outputTypeName)
                self.logger.info(f"Entered new output type name: {self.outputTypeName}")
                otc_page.click_update_btn()
                # Log after the update with the exact time
                current_time = datetime.now()
                current_time_after_edit = current_time.strftime("%d/%m/%Y %I:%M:%S %p")
                self.logger.info(f"Current Time after add is: {current_time_after_edit}")
                self.logger.info("Clicked the Update button")
                time.sleep(2)

                if otc_page.get_edit_otc_success_msg() == self.expected_edit_otc_success_msg:
                    self.logger.info(f"OTC success message is: {otc_page.get_edit_otc_success_msg()}")
                    otc_page.click_ok_btn()
                    self.logger.info("Clicked the 'OK' button successfully")
                    time.sleep(2)
                    success = True
                    break  # stop loop after success
                elif otc_page.get_otc_error_msg() == self.expected_otc_error_msg:
                    self.logger.info(f"OTC error message is: {otc_page.get_otc_error_msg()}")
                    otc_page.click_ok_btn()
                    self.logger.info("Clicked the 'OK' button successfully")
                else:
                    # Locate the 'Update' button and verify it is disabled
                    update_button = otc_page.get_update_btn_not_clickable()
                    assert update_button.get_attribute("disabled") == "true", "Update button is not disabled"
                    self.logger.info("Verified that 'Update' button is disabled")
                """


        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("test_type_name_field_failure")
            self.logger.error(f"Test failed: {str(e)}")
            self.logger.error(f"Screenshot saved at: {screenshot_path}")
            with open(screenshot_path, "rb") as image_file:
                allure.attach(
                    image_file.read(),
                    name="Test Type Name Field Failure",
                    attachment_type=allure.attachment_type.PNG
                )
            raise

        # --- Verify AFTER edit ---
        try:
            table_data_after = otc_page.get_table_data()
            seventh_row_after = table_data_after[6]
            self.logger.info(f"After Edit - 7th row data: {seventh_row_after}")

            # Validations
            assert seventh_row_after['Output Type'] == old_output_type, "Output Type should not change"
            assert seventh_row_after['Created By'] == old_created_by, "Created By should not change"
            assert seventh_row_after['Created Date'] == old_created_date, "Created Date should not change"
            assert seventh_row_after['Output Type Name'] == self.outputTypeName, \
                f"Expected updated Output Type Name '{self.outputTypeName}', but got '{seventh_row_after['Output Type Name']}'"

            # Modified Date compare with current_time_after_updated
            # Check if the difference between the current time after edit and created date after edit is greater than 5 seconds
            is_greater, time_difference = self.check_time_difference(seventh_row_after['Modified Date'], current_time_after_edit)
            if seventh_row_after['Modified Date'] == current_time_after_edit:
                self.logger.info(
                    f"Edited date {seventh_row_after['Modified Date']} and current date after edit  {current_time_after_edit} are the same")
            elif is_greater:  # Fixed syntax: 'else if' should be 'elif' in Python
                self.logger.error(
                    f"Edited date {seventh_row_after['Modified Date']} and current date after edit {current_time_after_edit} " f"differ by {time_difference} seconds, which is greater than 5 seconds.")
                raise AssertionError(f"Edited date and current date after edit differ by more than 5 seconds.")
            else:
                self.logger.info(
                    f"Edited date {seventh_row_after['Modified Date']} and current date after edit {current_time_after_edit} "
                    f"differ by {time_difference} seconds, which is within the 5-second threshold.")

            """
            assert seventh_row_after['Modified Date'] == current_time_after_edit ,  \
                f"Modified Date after edited '{current_time_after_edit}', but displayed in table '{seventh_row_after['Modified Date']}'"
            self.logger.info("Modified Date after add " + current_time_after_edit)
            self.logger.info("Modified Date displayed in table is " + seventh_row_after['Modified Date'] )
            """


            # Modified Date must be updated
            assert seventh_row_after['Modified Date'] != old_modified_date, \
                "Modified Date should be updated after edit"
            self.logger.info(f"Modified Date updated successfully: {seventh_row_after['Modified Date']}")

            self.logger.info("OTC entry verified successfully after edit")

        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("verify_otc_edit_failure")
            self.logger.error(f"Verification failed: {str(e)}")
            self.logger.error(f"Screenshot saved at: {screenshot_path}")
            raise


        otc_page.click_logout()
        self.logger.info("Logout successfully")

    @pytest.mark.retes
    def test_deactivateAndActivate_otc(self, driver):
        otc_page, screenshot_util = self.setup_otc_test(driver)

        try:
            # Get table data
            table_data = otc_page.get_table_data()
            self.logger.info(f"Table has {len(table_data)} rows")

            # Check if the 7th row exists
            if len(table_data) < 7:
                raise ValueError(f"Table has only {len(table_data)} rows, cannot access 7th row")

            # Capture the 7th row's data (index 6)
            seventh_row = table_data[6]
            self.logger.info(f"7th row data: {seventh_row}")

            # Store important fields for comparison
            old_output_type = seventh_row['Output Type']
            old_output_type_name = seventh_row['Output Type Name']
            old_created_by = seventh_row['Created By']
            old_created_date = seventh_row['Created Date']
            old_modified_date = seventh_row['Modified Date']
            old_status = seventh_row['Status']
            old_active_or_deactive = seventh_row['Active/DeActive']

            self.logger.info(f"Old status of 7th row: {old_status}")

            # Decide expected new status
            if old_status == "Active":
                otc_page.click_deactive_or_activate_btn_in_row(7)
                # Log after the clicking the 'Deactive' radio button with the exact time
                current_time = datetime.now()
                current_time_after_edit = current_time.strftime("%d/%m/%Y %I:%M:%S %p")
                self.logger.info(f"Current Time after add is: {current_time_after_edit}")
                self.logger.info("Deactivate successfully")
                assert otc_page.get_otc_deactivate_success_msg() == "Deactivated successfully", \
                    f"Expected success message to mention 'Deactivated successfully', but got '{otc_page.get_otc_deactivate_success_msg()}'"
                otc_page.click_ok_btn()
                self.logger.info("Clicked the 'OK' button successfully")
                

            else:
                otc_page.click_deactive_or_activate_btn_in_row(7)
                # Log after the clicking the 'Active' radio button with the exact time
                current_time = datetime.now()
                current_time_after_edit = current_time.strftime("%d/%m/%Y %I:%M:%S %p")
                self.logger.info(f"Current Time after add is: {current_time_after_edit}")
                self.logger.info(("Activated successfully"))
                assert otc_page.get_otc_activate_success_msg() == "Activated successfully", \
                    f"Expected success message to mention 'Activated successfully', but got '{otc_page.get_otc_activate_success_msg()}'"
                otc_page.click_ok_btn()
                self.logger.info("Clicked the 'OK' button successfully")

        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("test_deactivateAndActivate_otc_error")
            self.logger.error(f"Test failed - Error in test_deactivateAndActivate_otc: {str(e)}")
            self.logger.error(f"Screenshot saved at: {screenshot_path}")
            with open(screenshot_path, "rb") as image_file:
                allure.attach(
                    image_file.read(),
                    name="Test Type Name Field Failure",
                    attachment_type=allure.attachment_type.PNG
                )
            raise

        # Refresh page
        time.sleep(5)

        time.sleep(8)


        # --- Verify AFTER updated the status ---
        try:
            table_data_after = otc_page.get_table_data()
            seventh_row_after = table_data_after[6]
            self.logger.info(f"After Edit - 7th row data: {seventh_row_after}")

            # Validations
            assert seventh_row_after['Output Type'] == old_output_type, "Output Type should not change"
            assert seventh_row_after['Created By'] == old_created_by, "Created By should not change"
            assert seventh_row_after['Created Date'] == old_created_date, "Created Date should not change"
            assert seventh_row_after['Output Type Name'] == old_output_type_name, "Output Type Name should not change"

            # Modified Date compare with current_time_after_deactive_or_active
            # Check if the difference between the current time after click the D OR A and created date after clicking is greater than 5 seconds
            is_greater, time_difference = self.check_time_difference(seventh_row_after['Modified Date'],
                                                                     current_time_after_edit)
            if seventh_row_after['Modified Date'] == current_time_after_edit:
                self.logger.info(
                    f"Updated date {seventh_row_after['Modified Date']} and current date after clicking the radio button  {current_time_after_edit} are the same")
            elif is_greater:  # Fixed syntax: 'else if' should be 'elif' in Python
                self.logger.error(
                    f"Updated date {seventh_row_after['Modified Date']} and current date after  clicking the radio button {current_time_after_edit} " f"differ by {time_difference} seconds, which is greater than 5 seconds.")
                raise AssertionError(f"Edited date and current date after edit differ by more than 5 seconds.")
            else:
                self.logger.info(
                    f"Updated date {seventh_row_after['Modified Date']} and current date after edit {current_time_after_edit} "
                    f"differ by {time_difference} seconds, which is within the 5-second threshold.")


            # Modified Date must be updated
            assert seventh_row_after['Modified Date'] != old_modified_date, \
                "Modified Date should be updated after edit"
            self.logger.info(f"Modified Date updated successfully: {seventh_row_after['Modified Date']}")


            # Status must be updated
            assert seventh_row_after['Status'] != old_status,  \
                "Status should be updated after updated "
            self.logger.info(f"Status updated successfully: {seventh_row_after['Status']}")

            # After: correct
            assert seventh_row_after['Active/DeActive'] != old_active_or_deactive, \
                "Radio button status should be updated after the status update"
            self.logger.info(f"Radio button status updated successfully: {seventh_row_after['Active/DeActive']}")

            self.logger.info("OTC entry verified successfully after updated the status")

        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("verify_otc_deactivateOrActive_failure")
            self.logger.error(f"Verification failed: {str(e)}")
            self.logger.error(f"Screenshot saved at: {screenshot_path}")
            raise

        otc_page.click_logout()
        self.logger.info("Logout successfully")


