import pytest
import random
import time
from selenium.webdriver.common.keys import Keys

from datetime import datetime

from faker import Faker
import allure
from faker.providers import address

from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from pages.super.reseller_page import ResellerPage
from pages.super.user_page import UserPage
from utilities.custom_logger import LogGen
from utilities.login_helper import LoginHelper
from utilities.screenshot_utility import ScreenshotUtility

@pytest.mark.usefixtures("driver")
class TestResellerAndUser:
    logger = LogGen.loggen()

    actual_page_heading = "Manage Reseller"
    actual_reseller_table = "List Of Reseller"
    actual_create_btn  = "Create"

    # Generate Faker data
    fake = Faker()
    reseller_name =  None # fake company name
    reseller_email = fake.email()  # fake email
    reseller_address = fake.address().replace("\n", " ") # fake address
    reseller_phone = None

    # Expected datas
    expected_reseller_success_msg = "Reseller added successfully"
    status = "Active"
    reseller_wallet = "0"
    created_by = "outdidsuperadmin@gmail.com"
    modified_by = "-"
    modified_date = "-"

    expected_role = "Reseller Admin"
    expected_assigned_client = "-"
    expected_assigned_association = "-"

    #Edit Reseller Data's (edit reseller details - 4th row)
    expected_edt_reseller_name = "qara5001"
    expected_edt_reseller_phone = "9876543211"
    expected_edt_reseller_email = "qara5000@gmail.com"
    expected_edt_reseller_status = "Active"
    expected_edt_reseller_wallet = "1"
    expected_edt_reseller_address = "BTM"
    expected_edt_created_by = "QA"
    expected_edt_created_date = "24/05/2025 11:28:49 AM"
    expected_edt_modified_by = "outdidsuperadmin@gmail.com"
    expected_edt_suc_msg = "Reseller updated successfully"


    #Add Super Admin User
    srole_name = "Super Admin"
    spassword = 1234
    expected_add_suser_suc_msg = "User added successfully"
    expected_assigned_reseller = "-"
    smodified_by = "-"
    smodified_date = "-"

    #Edit user row details (6th row)
    eu_role_name = "Super Admin"
    eu_user_name = "spadminuser"
    eu_email = "spadmin@gmail.com"
    eu_status = "Active"
    eu_phone = "8793749812"
    eu_password = "4444"
    eu_assigned_reseller = "-"
    eu_assigned_client = "-"
    eu_assigned_association = "-"
    eu_created_by = "outdidsuperadmin@gmail.com"
    eu_created_date = "19/05/2025 04:36:09 PM"
    eu_modified_by = "outdidsuperadmin@gmail.com"
    expected_edit_suser_suc_msg = "User updated successfully"


    # Test Data for Already Existed Reseller
    already_exist_reseller_error_test_data = [
        {"resellerName": "Nagashree", "resellerPhone" : "8989898989", "resellerEmail" : "nagashreenaik040@gmail.com", "resellerAddress": "BTM", "expected_error": "Email ID already exists"},
        {"resellerName": "Nagashree", "resellerPhone": "8989898989", "resellerEmail": "nagashreenaik0@gmail.com", "resellerAddress": "BTM","expected_error": "Email ID and Reseller Name already exists"},
        {"resellerName": "Nagashree", "resellerPhone": "8989898989", "resellerEmail": "nagashreenaik000@gmail.com", "resellerAddress": "BTM","expected_error": "Reseller Name already exists"},
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

    @staticmethod
    def get_fake_phone():
        """Generate a fake 10-digit phone number"""
        return str(random.randint(6000000000, 9999999999))

    @staticmethod
    def get_reseller_name():
        fake = Faker()
        name = fake.company()
        return ''.join(ch for ch in name if ch.isalpha() or ch.isspace()).strip()

    # Assign reseller_phone using the method
    reseller_phone = get_fake_phone.__func__()
    reseller_name = get_reseller_name.__func__()



    @pytest.mark.smoke
    def test_reseller_page(self, driver):
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



    @pytest.mark.regression
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

                time.sleep(5)

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


    @pytest.mark.sanity
    def test_edit_reseller(self,driver):
        res_page, screenshot_util = self.setup_reseller_test(driver)

        Ephone = "7777766666"
        Ewallet = "100"
        Eaddress = "Bengaluru"
        Estatus = "Deactive"

        # Capture 4th row data before logout
        fourth_row_data = res_page.get_table_row_data(4)
        self.logger.info(f"Captured 4th Row Data: {fourth_row_data}")
        time.sleep(2)

        # Split the row into individual column values
        row_cells = fourth_row_data.split()

        assert self.expected_edt_reseller_name in row_cells[1], \
            f"Reseller Name mismatch. Expected {self.expected_edt_reseller_name}, actual {row_cells[1]}"

        assert self.expected_edt_reseller_phone in row_cells[2], \
            f"Phone Number mismatch. Expected {self.expected_edt_reseller_phone}, actual {row_cells[2]}"

        assert self.expected_edt_reseller_email in row_cells[3], \
            f"Email mismatch. Expected {self.expected_edt_reseller_email}, actual {row_cells[3]}"

        assert self.expected_edt_reseller_status in row_cells[4], \
            f"Status mismatch. Expected {self.expected_edt_reseller_status}, actual {row_cells[4]}"

        self.logger.info("Validation successful. All user details match expected values.")

        res_page.click_view_btn_row_number(4)
        self.logger.info("Clicked View button for 4th row")
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(5)
        self.logger.info("Navigate to the 'Reseller Details' page")
        res_page.click_edit_btn()
        self.logger.info("Navigate to the 'Edit Manage Reseller' page")
        time.sleep(2)
        res_page.edit_phone_field(Ephone)
        res_page.edit_wallet(Ewallet)
        res_page.edit_reseller_address(Eaddress)
        res_page.select_status(Estatus)
        time.sleep(2)
        res_page.click_update_btn()
        # Log after the update with the exact time
        current_time = datetime.now()
        current_time_after_update = current_time.strftime("%d/%m/%Y %I:%M:%S %p")
        self.logger.info(f"Current Time after add is: {current_time_after_update}")
        self.logger.info("Clicked the add button")

        try:
            get_upd_success_msg = res_page.get_updat_suc_msg()
            self.logger.info(f"Reseller Updated success message is: {get_upd_success_msg}")
            assert get_upd_success_msg == self.expected_edt_suc_msg, (
                f"Expected Reseller Updated success message '{self.expected_edt_suc_msg}', but got '{get_upd_success_msg}'")
            res_page.click_ok_btn()
            self.logger.info("Clicked the 'OK' button successfully")
            res_page.refresh()
            time.sleep(3)
        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("edit_reseller_failure")
            self.logger.error(f"Success message '{self.expected_edt_suc_msg}' not found or incorrect: {str(e)}")
            self.logger.error(f"Screenshot saved at: {screenshot_path}")
            raise

        #Verify the updated changes
        fourth_row_data = res_page.get_table_row_data(4)
        self.logger.info(f"Captured 4th Row Data: {fourth_row_data}")
        time.sleep(2)

        Estatus = "DeActive"

        # Split the row into individual column values
        row_cells = fourth_row_data.split()

        assert self.expected_edt_reseller_name in row_cells[1], \
            f"Reseller Name mismatch. Expected {self.expected_edt_reseller_name}, actual {row_cells[1]}"

        assert Ephone in row_cells[2], \
            f"Phone Number mismatch. Expected {Ephone}, actual {row_cells[2]}"

        assert self.expected_edt_reseller_email in row_cells[3], \
            f"Email mismatch. Expected {self.expected_edt_reseller_email}, actual {row_cells[3]}"

        assert Estatus in row_cells[4], \
            f"Status mismatch. Expected {Estatus}, actual {row_cells[4]}"

        self.logger.info("Validation successful. All user details match expected values.")

        res_page.click_view_btn_row_number(4)
        self.logger.info("Clicked View button for 4th row")
        time.sleep(5)

        assert res_page.get_reseller_name_details() == self.expected_edt_reseller_name, "Reseller Name should not change"
        assert res_page.get_reseller_phone_details() == Ephone, "Reseller Phone should not change"
        assert res_page.get_reseller_email_details() == self.expected_edt_reseller_email, "Reseller Email should not change"
        assert res_page.get_reseller_wallet_details() == Ewallet, "Reseller Wallet should not change"
        assert res_page.get_reseller_address_details() == Eaddress, "Reseller Address should not change"
        assert res_page.get_reseller_createdby_details() == self.expected_edt_created_by, "Reseller Created By should not change"
        assert res_page.get_reseller_createdDate_details() == self.expected_edt_created_date, "Reseller Created Date should not change"
        assert res_page.get_reseller_modifiedBy_details() == self.expected_edt_modified_by, "Reseller Modified By should not change"
        assert res_page.get_reseller_status_details() == Estatus, "Status should not change"
        self.logger.info(
            f"Found created Reseller entry: Reseller Name '{res_page.get_reseller_name_details()}', Phone Number  '{res_page.get_reseller_phone_details()}', Email ID '{res_page.get_reseller_email_details()}',Wallet : {res_page.get_reseller_wallet_details()}, Address : {res_page.get_reseller_address_details()}, Created By : {res_page.get_reseller_createdby_details()}, \
                                         Created Date : {res_page.get_reseller_createdDate_details()}, Modified By : {res_page.get_reseller_modifiedBy_details()}, Modified Date : {res_page.get_reseller_modifiedDate_details()} , Status : {res_page.get_reseller_status_details()} ")

        # Check if the difference between the current time and updated date is greater than 5 seconds
        is_greater, time_difference = self.check_time_difference(res_page.get_reseller_modifiedDate_details(),
                                                                 current_time_after_update)
        if res_page.get_reseller_modifiedDate_details() == current_time_after_update:
            self.logger.info(
                f"Updated date {res_page.get_reseller_modifiedDate_details()} and current date {current_time_after_update} are the same")
        elif is_greater:  # Fixed syntax: 'else if' should be 'elif' in Python
            self.logger.error(
                f"Updated date {res_page.get_reseller_modifiedDate_details()} and current date {current_time_after_update} " f"differ by {time_difference} seconds, which is greater than 5 seconds.")
            raise AssertionError(f"Created date and current date differ by more than 5 seconds.")
        else:
            self.logger.info(
                f"Updated date {res_page.get_reseller_modifiedDate_details()} and current date {current_time_after_update} "
                f"differ by {time_difference} seconds, which is within the 5-second threshold.")

        #Again Edit with Old datas
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        res_page.click_edit_btn()
        time.sleep(2)
        res_page.edit_phone_field(self.expected_edt_reseller_phone)
        res_page.edit_wallet(self.expected_edt_reseller_wallet)
        res_page.edit_reseller_address(self.expected_edt_reseller_address)
        res_page.select_status(self.expected_edt_reseller_status)
        time.sleep(2)
        res_page.click_update_btn()
        # Log after the update with the exact time
        current_time = datetime.now()
        current_time_after_update = current_time.strftime("%d/%m/%Y %I:%M:%S %p")
        self.logger.info(f"Current Time after add is: {current_time_after_update}")
        self.logger.info("Clicked the add button")

        try:
            get_upd_success_msg = res_page.get_updat_suc_msg()
            self.logger.info(f"Reseller Updated success message is: {get_upd_success_msg}")
            assert get_upd_success_msg == self.expected_edt_suc_msg, (
                f"Expected Reseller Updated success message '{self.expected_edt_suc_msg}', but got '{get_upd_success_msg}'")
            res_page.click_ok_btn()
            self.logger.info("Clicked the 'OK' button successfully")
            res_page.refresh()
            time.sleep(3)
        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("edit_reseller_failure")
            self.logger.error(f"Success message '{self.expected_edt_suc_msg}' not found or incorrect: {str(e)}")
            self.logger.error(f"Screenshot saved at: {screenshot_path}")
            raise

        # Logout
        res_page.click_logout()
        self.logger.info("Logout successfully")

    @pytest.mark.endtesting
    def test_add_super_admin_user(self, driver):
        res_page, screenshot_util = self.setup_reseller_test(driver)

        user_page = UserPage(driver)
        user_page.navigate_to_user_page()
        time.sleep(3)
        user_page.click_add_user_btn()
        time.sleep(2)
        user_page.select_role_name(self.srole_name)
        user_page.enter_user_name(self.reseller_name)
        user_page.enter_email(self.reseller_email)
        user_page.enter_phone(self.reseller_phone)
        user_page.enter_password(self.spassword)
        time.sleep(2)
        user_page.click_add_btn()
        # Log after the update with the exact time
        current_time = datetime.now()
        current_time_after_add = current_time.strftime("%d/%m/%Y %I:%M:%S %p")
        self.logger.info(f"Current Time after add is: {current_time_after_add}")
        self.logger.info("Clicked the add button")

        try:
            get_add_suc_msg = user_page.get_add_suc_msg()
            self.logger.info(f"User added success message is: {get_add_suc_msg}")
            assert get_add_suc_msg == self.expected_add_suser_suc_msg, (
                f"Expected User added success message '{self.expected_add_suser_suc_msg}', but got '{get_add_suc_msg}'")
            res_page.click_ok_btn()
            self.logger.info("Clicked the 'OK' button successfully")
            res_page.refresh()
            time.sleep(3)
        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("add_user_failure")
            self.logger.error(f"Success message '{self.expected_add_suser_suc_msg}' not found or incorrect: {str(e)}")
            self.logger.error(f"Screenshot saved at: {screenshot_path}")
            raise

        #Verify the added user in list of user table
        user_page.serch(self.reseller_email)
        self.logger.info(f"Serched email id. {self.reseller_email}")
        time.sleep(2)

        # -------- Verify First Row in User Table --------
        self.logger.info("Validating first row data in Users table...")

        first_row_values = user_page.get_first_row_data()
        self.logger.info(f"Extracted Row Data: {first_row_values}")

        assert self.srole_name in first_row_values[1], f"Role mismatch. Expected {self.srole_name}, actual {first_row_values[1]}"
        assert self.reseller_name in first_row_values[2], f"Username mismatch. Expected {self.reseller_name}, actual {first_row_values[2]}"
        assert self.reseller_email in first_row_values[3], f"Email mismatch. Expected {self.reseller_email}, actual {first_row_values[3]}"
        assert self.status in first_row_values[4], f"Status mismatch. Expected {self.status}, actual {first_row_values[4]}"

        self.logger.info("Validation successful. All user details match expected values.")

        # -------- Click View Button --------
        user_page.click_view_btn_first_row()
        self.logger.info("Clicked 'View' button for the matched user.")
        time.sleep(2)

        # -------- Verify User Details Page --------
        self.logger.info("Validating user details page values...")

        # Fetch details from UI
        user_name_val = user_page.find_element(user_page.user_name_vlu).text.strip()
        email_val = user_page.find_element(user_page.email_vlu).text.strip()
        phone_val = user_page.find_element(user_page.phone_vlu).text.strip()
        password_val = user_page.find_element(user_page.password_vlu).text.strip()
        role_val = user_page.find_element(user_page.rolename_vlu).text.strip()
        assigned_res_val = user_page.find_element(user_page.assigned_reseller_vlu).text.strip()
        assigned_client_val = user_page.find_element(user_page.assigned_client_vlu).text.strip()
        assigned_ass_val = user_page.find_element(user_page.assigned_association_vlu).text.strip()
        created_by_val = user_page.find_element(user_page.created_by_vlu).text.strip()
        created_date_val = user_page.find_element(user_page.created_date_vlu).text.strip()
        modified_by_val = user_page.find_element(user_page.modified_by_vlu).text.strip()
        modified_date_val = user_page.find_element(user_page.modified_date_vlu).text.strip()
        status_val = user_page.find_element(user_page.status_dtls_vlu).text.strip()

        time.sleep(3)
        # Assertions
        assert user_name_val == self.reseller_name, \
            f"Username mismatch. Expected: {self.reseller_name}, Got: {user_name_val}"

        assert email_val == self.reseller_email, \
            f"Email mismatch. Expected: {self.reseller_email}, Got: {email_val}"

        assert phone_val == self.reseller_phone, \
            f"Phone mismatch. Expected: {self.reseller_phone}, Got: {phone_val}"

        assert role_val == self.srole_name, \
            f"Role mismatch. Expected: {self.srole_name}, Got: {role_val}"

        assert assigned_res_val == self.expected_assigned_reseller, \
            f"Username mismatch. Expected: {self.expected_assigned_reseller}, Got: {assigned_res_val}"

        assert assigned_client_val == self.expected_assigned_client, \
            f"Username mismatch. Expected: {self.expected_assigned_client}, Got: {assigned_client_val}"

        assert assigned_ass_val == self.expected_assigned_association, \
            f"Username mismatch. Expected: {self.expected_assigned_association}, Got: {assigned_ass_val}"

        assert created_by_val == self.created_by, \
            f"Username mismatch. Expected: {self.created_by}, Got: {created_by_val}"

        # assert created_date_val == self.expected_created_date, \
        #     f"Username mismatch. Expected: {self.expected_created_date}, Got: {created_date_val}"

        assert modified_by_val == self.smodified_by, \
            f"Username mismatch. Expected: {self.smodified_by}, Got: {modified_by_val}"

        assert modified_date_val == self.smodified_date, \
            f"Username mismatch. Expected: {self.smodified_date}, Got: {modified_date_val}"

        assert status_val == self.status, \
            f"Status mismatch. Expected: {self.status}, Got: {status_val}"

        self.logger.info(f"User Password: {password_val}")

        # Check if the difference between the current time and created date is greater than 5 seconds
        is_greater, time_difference = self.check_time_difference(created_date_val,
                                                                 current_time_after_add)
        if created_date_val == current_time_after_add:
            self.logger.info(
                f"Created date {created_date_val} and current date {current_time_after_add} are the same")
        elif is_greater:  # Fixed syntax: 'else if' should be 'elif' in Python
            self.logger.error(
                f"Created date {created_date_val} and current date {current_time_after_add} " f"differ by {time_difference} seconds, which is greater than 5 seconds.")
            raise AssertionError(f"Created date and current date differ by more than 5 seconds.")
        else:
            self.logger.info(
                f"Created date {created_date_val} and current date {current_time_after_add} "
                f"differ by {time_difference} seconds, which is within the 5-second threshold.")

        self.logger.info("All user details verified successfully on the User Details page.")

        res_page.click_logout()
        self.logger.info("Logout successfully")

        time.sleep(1)

        expected_dashboard_url = ""

        # Login with newly created credentials
        login_helper = LoginHelper()
        login_helper.login(
            driver,
            email=self.reseller_email,
            password=password_val  # fetched earlier from User Details page
        )

        try:
            dashboard_page = DashboardPage(driver)
            dashboard_page.wait_for_element(dashboard_page.welcome_msg, timeout=30)
            welcome_text = dashboard_page.capture_welcomeMsg().strip(",")
            expected_welcome = f"Welcome to {self.reseller_email}"
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



    @pytest.mark.positivetest
    def test_edit_user(self,driver):
        res_page, screenshot_util = self.setup_reseller_test(driver)

        user_page = UserPage(driver)
        user_page.navigate_to_user_page()
        time.sleep(3)


        Ephone = "7777766666"
        Estatus = "Deactive"
        EPassword = "1234"

        user_page.scroll_to_user_row(6)
        time.sleep(3)

        sixth_row_values = user_page.get_row_data(6)
        self.logger.info(f"Captured 6th Row Data: {sixth_row_values}")
        time.sleep(2)

        assert self.eu_role_name in sixth_row_values[1], f"Role mismatch. Expected {self.eu_role_name}, actual {sixth_row_values[1]}"
        assert self.eu_user_name in sixth_row_values[2], f"Username mismatch. Expected {self.eu_user_name}, actual {sixth_row_values[2]}"
        assert self.eu_email in sixth_row_values[3], f"Email mismatch. Expected {self.eu_email}, actual {sixth_row_values[3]}"
        assert self.eu_status in sixth_row_values[4], f"Status mismatch. Expected {self.eu_status}, actual {sixth_row_values[4]}"

        self.logger.info("Validation successful. All user details match expected values.")

        # -------- Click View Button --------
        res_page.click_view_btn_row_number(6)
        self.logger.info("Clicked View button for 6th row")
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(5)

        # -------- Verify User Details Page --------
        self.logger.info("Validating user details page values...")

        # Fetch details from UI
        user_name_val = user_page.find_element(user_page.user_name_vlu).text.strip()
        email_val = user_page.find_element(user_page.email_vlu).text.strip()
        phone_val = user_page.find_element(user_page.phone_vlu).text.strip()
        password_val = user_page.find_element(user_page.password_vlu).text.strip()
        role_val = user_page.find_element(user_page.rolename_vlu).text.strip()
        assigned_res_val = user_page.find_element(user_page.assigned_reseller_vlu).text.strip()
        assigned_client_val = user_page.find_element(user_page.assigned_client_vlu).text.strip()
        assigned_ass_val = user_page.find_element(user_page.assigned_association_vlu).text.strip()
        created_by_val = user_page.find_element(user_page.created_by_vlu).text.strip()
        created_date_val = user_page.find_element(user_page.created_date_vlu).text.strip()
        modified_by_val = user_page.find_element(user_page.modified_by_vlu).text.strip()
        modified_date_val = user_page.find_element(user_page.modified_date_vlu).text.strip()
        status_val = user_page.find_element(user_page.status_dtls_vlu).text.strip()

        time.sleep(3)
        # Assertions
        assert user_name_val == self.eu_user_name, \
            f"Username mismatch. Expected: {self.eu_user_name}, Got: {user_name_val}"

        assert email_val == self.eu_email, \
            f"Email mismatch. Expected: {self.eu_email}, Got: {email_val}"

        assert phone_val == self.eu_phone, \
            f"Phone mismatch. Expected: {self.eu_phone}, Got: {phone_val}"

        assert role_val == self.eu_role_name, \
            f"Role mismatch. Expected: {self.eu_role_name}, Got: {role_val}"

        assert assigned_res_val == self.eu_assigned_reseller, \
            f"Username mismatch. Expected: {self.eu_assigned_reseller}, Got: {assigned_res_val}"

        assert assigned_client_val == self.eu_assigned_client, \
            f"Username mismatch. Expected: {self.eu_assigned_client}, Got: {assigned_client_val}"

        assert assigned_ass_val == self.eu_assigned_association, \
            f"Username mismatch. Expected: {self.eu_assigned_association}, Got: {assigned_ass_val}"

        assert created_by_val == self.eu_created_by, \
            f"Username mismatch. Expected: {self.eu_created_by}, Got: {created_by_val}"

        assert created_date_val == self.eu_created_date, \
            f"Username mismatch. Expected: {self.eu_created_date}, Got: {created_date_val}"

        assert modified_by_val == self.eu_modified_by, \
            f"Username mismatch. Expected: {self.eu_modified_by}, Got: {modified_by_val}"

        # assert modified_date_val == self.smodified_date, \
        #     f"Username mismatch. Expected: {self.smodified_date}, Got: {modified_date_val}"

        assert status_val == self.eu_status, \
            f"Status mismatch. Expected: {self.eu_status}, Got: {status_val}"

        assert password_val == self.eu_password, \
            f"Password mismatch. Expected: {self.eu_password}, Got: {password_val}"

        self.logger.info("All user details verified successfully on the User Details page.")

        self.logger.info("Navigate to the 'Reseller Details' page")
        user_page.click_edit_btn()
        self.logger.info("Navigate to the 'Edit Manage Reseller' page")
        time.sleep(3)
        user_page.edit_phone_field(Ephone)
        user_page.select_status(Estatus)
        user_page.edit_password_field(EPassword)
        time.sleep(2)
        user_page.click_update_btn()
        # Log after the update with the exact time
        current_time = datetime.now()
        current_time_after_update = current_time.strftime("%d/%m/%Y %I:%M:%S %p")
        self.logger.info(f"Current Time after add is: {current_time_after_update}")
        self.logger.info("Clicked the add button")

        try:
            get_update_suc_msg = user_page.get_edit_suc_msg()
            self.logger.info(f"User updated success message is: {get_update_suc_msg}")
            assert get_update_suc_msg == self.expected_edit_suser_suc_msg, (
                f"Expected User updated success message '{self.expected_edit_suser_suc_msg}', but got '{get_update_suc_msg}'")
            res_page.click_ok_btn()
            self.logger.info("Clicked the 'OK' button successfully")
            res_page.refresh()
            time.sleep(3)
        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("update_user_failure")
            self.logger.error(f"Success message '{self.expected_edit_suser_suc_msg}' not found or incorrect: {str(e)}")
            self.logger.error(f"Screenshot saved at: {screenshot_path}")
            raise

        #Verify updated changes
        Estatus = "DeActive"
        user_page.refresh()
        time.sleep(3)
        user_page.scroll_to_user_row(6)
        time.sleep(3)

        sixth_row_values = user_page.get_row_data(6)
        self.logger.info(f"Captured 6th Row Data: {sixth_row_values}")
        time.sleep(2)

        assert self.eu_role_name in sixth_row_values[1], f"Role mismatch. Expected {self.eu_role_name}, actual {sixth_row_values[1]}"
        assert self.eu_user_name in sixth_row_values[2], f"Username mismatch. Expected {self.eu_user_name}, actual {sixth_row_values[2]}"
        assert self.eu_email in sixth_row_values[3], f"Email mismatch. Expected {self.eu_email}, actual {sixth_row_values[3]}"
        assert Estatus in sixth_row_values[4], f"Status mismatch. Expected {Estatus}, actual {sixth_row_values[4]}"

        self.logger.info("Validation successful. All user details match expected values.")

        # -------- Click View Button --------
        res_page.click_view_btn_row_number(6)
        self.logger.info("Clicked View button for 6th row")
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(5)

        user_name_val = user_page.find_element(user_page.user_name_vlu).text.strip()
        email_val = user_page.find_element(user_page.email_vlu).text.strip()
        phone_val = user_page.find_element(user_page.phone_vlu).text.strip()
        password_val = user_page.find_element(user_page.password_vlu).text.strip()
        role_val = user_page.find_element(user_page.rolename_vlu).text.strip()
        assigned_res_val = user_page.find_element(user_page.assigned_reseller_vlu).text.strip()
        assigned_client_val = user_page.find_element(user_page.assigned_client_vlu).text.strip()
        assigned_ass_val = user_page.find_element(user_page.assigned_association_vlu).text.strip()
        created_by_val = user_page.find_element(user_page.created_by_vlu).text.strip()
        created_date_val = user_page.find_element(user_page.created_date_vlu).text.strip()
        modified_by_val = user_page.find_element(user_page.modified_by_vlu).text.strip()
        modified_date_val = user_page.find_element(user_page.modified_date_vlu).text.strip()
        status_val = user_page.find_element(user_page.status_dtls_vlu).text.strip()

        # -------- Verify User Details Page --------
        self.logger.info("Validating user details page values...")

        time.sleep(3)
        # Assertions
        assert user_name_val == self.eu_user_name, \
            f"Username mismatch. Expected: {self.eu_user_name}, Got: {user_name_val}"

        assert email_val == self.eu_email, \
            f"Email mismatch. Expected: {self.eu_email}, Got: {email_val}"

        assert phone_val == Ephone, \
            f"Phone mismatch. Expected: {Ephone}, Got: {phone_val}"

        assert role_val == self.eu_role_name, \
            f"Role mismatch. Expected: {self.eu_role_name}, Got: {role_val}"

        assert assigned_res_val == self.eu_assigned_reseller, \
            f"Username mismatch. Expected: {self.eu_assigned_reseller}, Got: {assigned_res_val}"

        assert assigned_client_val == self.eu_assigned_client, \
            f"Username mismatch. Expected: {self.eu_assigned_client}, Got: {assigned_client_val}"

        assert assigned_ass_val == self.eu_assigned_association, \
            f"Username mismatch. Expected: {self.eu_assigned_association}, Got: {assigned_ass_val}"

        assert created_by_val == self.eu_created_by, \
            f"Username mismatch. Expected: {self.eu_created_by}, Got: {created_by_val}"

        assert created_date_val == self.eu_created_date, \
            f"Username mismatch. Expected: {self.eu_created_date}, Got: {created_date_val}"

        assert modified_by_val == self.eu_modified_by, \
            f"Username mismatch. Expected: {self.eu_modified_by}, Got: {modified_by_val}"

        # assert modified_date_val == self.smodified_date, \
        #     f"Username mismatch. Expected: {self.smodified_date}, Got: {modified_date_val}"

        assert status_val == Estatus, \
            f"Status mismatch. Expected: {Estatus}, Got: {status_val}"

        assert password_val == EPassword, \
            f"Password mismatch. Expected: {EPassword}, Got: {password_val}"

        # Check if the difference between the current time and updated date is greater than 5 seconds
        is_greater, time_difference = self.check_time_difference(modified_date_val,
                                                                 current_time_after_update)
        if modified_date_val == current_time_after_update:
            self.logger.info(
                f"Updated date {modified_date_val} and current date {current_time_after_update} are the same")
        elif is_greater:  # Fixed syntax: 'else if' should be 'elif' in Python
            self.logger.error(
                f"Updated date {modified_date_val} and current date {current_time_after_update} " f"differ by {time_difference} seconds, which is greater than 5 seconds.")
            raise AssertionError(f"Created date and current date differ by more than 5 seconds.")
        else:
            self.logger.info(
                f"Updated date {modified_date_val} and current date {current_time_after_update} "
                f"differ by {time_difference} seconds, which is within the 5-second threshold.")

        self.logger.info("All user details verified successfully on the User Details page.")

        self.logger.info("Navigate to the 'Reseller Details' page")
        user_page.click_edit_btn()
        self.logger.info("Navigate to the 'Edit Manage Reseller' page")
        time.sleep(2)
        user_page.edit_phone_field(self.eu_phone)
        user_page.select_status(self.eu_status)
        user_page.edit_password_field(self.eu_password)
        time.sleep(2)
        user_page.click_update_btn()
        time.sleep(2)
        res_page.click_ok_btn()

        res_page.click_logout()
        self.logger.info("Logout successfully")

    @pytest.mark.negativetest
    def test_already_existed_user(self, driver):
        #
        res_page, screenshot_util = self.setup_reseller_test(driver)

        already_existed_sname = "Super"
        already_existed_semail = "outdidsuperadmin@gmail.com"
        already_existed_sphone = "9876543210"
        already_existed_password = 1234
        expected_error_message = "This email is already registered under the same role"

        user_page = UserPage(driver)
        user_page.navigate_to_user_page()
        time.sleep(3)

        user_page.click_add_user_btn()
        user_page.select_role_name(self.srole_name)
        user_page.enter_user_name(already_existed_sname)
        user_page.enter_email(already_existed_semail)
        user_page.enter_phone(already_existed_sphone)
        user_page.enter_password(already_existed_password)
        user_page.click_add_btn()

        try:
            get_alr_ext_err_msg = user_page.get_alr_exst_err_msg()
            self.logger.info(f"Error message is: {get_alr_ext_err_msg}")
            assert get_alr_ext_err_msg == expected_error_message, (
                f"Expected error message '{expected_error_message}', but got '{get_alr_ext_err_msg}'")
            res_page.click_ok_btn()
            self.logger.info("Clicked the 'OK' button successfully")
        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("update_user_failure")
            self.logger.error(f"Error message '{expected_error_message}' not found or incorrect: {str(e)}")
            self.logger.error(f"Screenshot saved at: {screenshot_path}")
            raise

        res_page.click_logout()
        self.logger.info("Logout successfully")

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
            # self.logger.error(f"Page source: {driver.page_source[:500]}...")
            self.logger.error(f"Screenshot saved at: {screenshot_path}")
            raise

        # Validate Add Manage Reseller page (Scenario 2)
        try:
            self.logger.info("'Add Output Type Config' popup displayed")
            assert res_page.wait_for_element(res_page.add_res_page).is_displayed(), "Page heading not displayed"
            assert res_page.wait_for_element(res_page.reseller_name).is_displayed(), "Reseller Name field not displayed"
            assert res_page.wait_for_element(
                res_page.reseller_phone).is_displayed(), "Reseller Phone field not displayed"
            assert res_page.wait_for_element(
                res_page.reseller_email).is_displayed(), "Reseller Email field not displayed"
            assert res_page.wait_for_element(
                res_page.reseller_address).is_displayed(), "Reseller Address field not displayed"
            assert res_page.wait_for_element(res_page.add_btn).is_displayed(), "Add button not displayed"
            self.logger.info("Page contains heading, Text fields and Add button")
        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("add_reseller_page_failure")
            self.logger.error(f"Failed to verify 'Add Manage Reseller' page or elements: {str(e)}")
            self.logger.error(f"Current URL: {driver.current_url}")
            # self.logger.error(f"Page source: {driver.page_source[:500]}...")
            self.logger.error(f"Screenshot saved at: {screenshot_path}")
            raise

        # Validate Add Reseller and verify the success message
        res_page.enter_reseller_name(self.reseller_name)
        self.logger.info(f"Entered Reseller Name : {self.reseller_name}")
        res_page.enter_reseller_phone(self.reseller_phone)
        self.logger.info(f"Entered Reseller Phone : {self.reseller_phone}")
        res_page.enter_reseller_email(self.reseller_email)
        self.logger.info(f"Entered Reseller Email : {self.reseller_email}")
        res_page.enter_reseller_address(self.reseller_address)
        self.logger.info(f"Entered Reseller Address : {self.reseller_address}")
        time.sleep(2)
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
            res_page.refresh()
            time.sleep(3)
            # Verify the created Reseller in List of Reseller Table
            try:
                table_data = res_page.get_table_data()
                found = False
                for row in table_data:
                    if row['Reseller Name'] == self.reseller_name and row['Phone Number'] == self.reseller_phone and \
                            row['Email ID'] == self.reseller_email and row['Status'] == self.status:
                        found = True
                        self.logger.info(
                            f"Found created Reseller entry: Reseller Name '{self.reseller_name}', Phone Number  '{self.reseller_phone}', Email ID '{self.reseller_email}', Status : {row['Status']} ")
                        res_page.click_view_btn_in_row(self.reseller_email)
                        self.logger.info("Navigate to the 'Reseller Details' page")
                        time.sleep(5)
                        assert res_page.get_reseller_name_details() == self.reseller_name, "Reseller Name should not change"
                        assert res_page.get_reseller_phone_details() == self.reseller_phone, "Reseller Phone should not change"
                        assert res_page.get_reseller_email_details() == self.reseller_email, "Reseller Email should not change"
                        assert res_page.get_reseller_wallet_details() == self.reseller_wallet, "Reseller Wallet should not change"
                        assert res_page.get_reseller_address_details() == self.reseller_address, "Reseller Address should not change"
                        assert res_page.get_reseller_createdby_details() == self.created_by, "Reseller Created By should not change"
                        assert res_page.get_reseller_modifiedBy_details() == self.modified_by, "Reseller Modified By should not change"
                        assert res_page.get_reseller_modifiedDate_details() == self.modified_date, "Reseller Modified Date should not change"
                        assert res_page.get_reseller_status_details() == self.status, "Status should not change"
                        self.logger.info(
                            f"Found created Reseller entry: Reseller Name '{res_page.get_reseller_name_details()}', Phone Number  '{res_page.get_reseller_phone_details()}', Email ID '{res_page.get_reseller_email_details()}',Wallet : {res_page.get_reseller_wallet_details()}, Address : {res_page.get_reseller_address_details()}, Created By : {res_page.get_reseller_createdby_details()}, \
                                     Created Date : {res_page.get_reseller_createdDate_details()}, Modified By : {res_page.get_reseller_modifiedBy_details()}, Modified Date : {res_page.get_reseller_modifiedDate_details()} , Status : {res_page.get_reseller_status_details()} ")

                        # Check if the difference between the current time and created date is greater than 5 seconds
                        is_greater, time_difference = self.check_time_difference(
                            res_page.get_reseller_createdDate_details(),
                            current_time_after_add)
                        if res_page.get_reseller_createdDate_details() == current_time_after_add:
                            self.logger.info(
                                f"Created date {res_page.get_reseller_createdDate_details()} and current date {current_time_after_add} are the same")
                        elif is_greater:  # Fixed syntax: 'else if' should be 'elif' in Python
                            self.logger.error(
                                f"Created date {res_page.get_reseller_createdDate_details()} and current date {current_time_after_add} " f"differ by {time_difference} seconds, which is greater than 5 seconds.")
                            raise AssertionError(f"Created date and current date differ by more than 5 seconds.")
                        else:
                            self.logger.info(
                                f"Created date {res_page.get_reseller_createdDate_details()} and current date {current_time_after_add} "
                                f"differ by {time_difference} seconds, which is within the 5-second threshold.")
                        break
                self.logger.info("Reseller entry verified successfully in the table")

            except Exception as e:
                self.logger.error(f"Failed to verify added reseller entry in table: {str(e)}")
                screenshot_path = screenshot_util.capture_screenshot("test_added_otc_in_table_failure")
                self.logger.error(f"Test failed, screenshot saved at: {screenshot_path}")
                raise

        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("add_reseller_failure")
            self.logger.error(
                f"Success message '{self.expected_reseller_success_msg}' not found or incorrect: {str(e)}")
            self.logger.error(f"Screenshot saved at: {screenshot_path}")
            raise

        # Verify the created Reseller in List of User Table
        self.logger.info("Navigating to User Page to verify added details...")

        user_page = UserPage(driver)
        user_page.navigate_to_user_page()
        time.sleep(6)
        # screenshot_util.capture_screenshot("navigated_to_user_page")

        # Search the user by reseller email
        user_page.serch(self.reseller_email)
        self.logger.info(f"Serched email id. {self.reseller_email}")
        time.sleep(2)

        # -------- Verify First Row in User Table --------
        self.logger.info("Validating first row data in Users table...")

        first_row_values = user_page.get_first_row_data()
        self.logger.info(f"Extracted Row Data: {first_row_values}")

        assert self.expected_role in first_row_values[
            1], f"Role mismatch. Expected {self.expected_role}, actual {first_row_values[1]}"
        assert self.reseller_name in first_row_values[
            2], f"Username mismatch. Expected {self.reseller_name}, actual {first_row_values[2]}"
        assert self.reseller_email in first_row_values[
            3], f"Email mismatch. Expected {self.reseller_email}, actual {first_row_values[3]}"
        assert self.status in first_row_values[
            4], f"Status mismatch. Expected {self.status}, actual {first_row_values[4]}"

        self.logger.info("Validation successful. All user details match expected values.")

        # -------- Click View Button --------
        user_page.click_view_btn_first_row()
        self.logger.info("Clicked 'View' button for the matched user.")
        time.sleep(2)

        # -------- Verify User Details Page --------
        self.logger.info("Validating user details page values...")

        # Fetch details from UI
        user_name_val = user_page.find_element(user_page.user_name_vlu).text.strip()
        email_val = user_page.find_element(user_page.email_vlu).text.strip()
        phone_val = user_page.find_element(user_page.phone_vlu).text.strip()
        password_val = user_page.find_element(user_page.password_vlu).text.strip()
        role_val = user_page.find_element(user_page.rolename_vlu).text.strip()
        assigned_res_val = user_page.find_element(user_page.assigned_reseller_vlu).text.strip()
        assigned_client_val = user_page.find_element(user_page.assigned_client_vlu).text.strip()
        assigned_ass_val = user_page.find_element(user_page.assigned_association_vlu).text.strip()
        created_by_val = user_page.find_element(user_page.created_by_vlu).text.strip()
        created_date_val = user_page.find_element(user_page.created_date_vlu).text.strip()
        modified_by_val = user_page.find_element(user_page.modified_by_vlu).text.strip()
        modified_date_val = user_page.find_element(user_page.modified_date_vlu).text.strip()
        status_val = user_page.find_element(user_page.status_dtls_vlu).text.strip()

        time.sleep(3)
        # Assertions
        assert user_name_val == self.reseller_name, \
            f"Username mismatch. Expected: {self.reseller_name}, Got: {user_name_val}"

        assert email_val == self.reseller_email, \
            f"Email mismatch. Expected: {self.reseller_email}, Got: {email_val}"

        assert phone_val == self.reseller_phone, \
            f"Phone mismatch. Expected: {self.reseller_phone}, Got: {phone_val}"

        assert role_val == self.expected_role, \
            f"Role mismatch. Expected: {self.expected_role}, Got: {role_val}"

        assert assigned_res_val == self.reseller_name, \
            f"Username mismatch. Expected: {self.reseller_name}, Got: {assigned_res_val}"

        assert assigned_client_val == self.expected_assigned_client, \
            f"Username mismatch. Expected: {self.expected_assigned_client}, Got: {assigned_client_val}"

        assert assigned_ass_val == self.expected_assigned_association, \
            f"Username mismatch. Expected: {self.expected_assigned_association}, Got: {assigned_ass_val}"

        assert created_by_val == self.created_by, \
            f"Username mismatch. Expected: {self.created_by}, Got: {created_by_val}"

        # assert created_date_val == self.expected_created_date, \
        #     f"Username mismatch. Expected: {self.expected_created_date}, Got: {created_date_val}"

        assert modified_by_val == self.modified_by, \
            f"Username mismatch. Expected: {self.modified_by}, Got: {modified_by_val}"

        assert modified_date_val == self.modified_date, \
            f"Username mismatch. Expected: {self.modified_date}, Got: {modified_date_val}"

        assert status_val == self.status, \
            f"Status mismatch. Expected: {self.status}, Got: {status_val}"

        self.logger.info(f"User Password: {password_val}")

        # Check if the difference between the current time and created date is greater than 5 seconds
        is_greater, time_difference = self.check_time_difference(created_date_val,
                                                                 current_time_after_add)
        if created_date_val == current_time_after_add:
            self.logger.info(
                f"Created date {created_date_val} and current date {current_time_after_add} are the same")
        elif is_greater:  # Fixed syntax: 'else if' should be 'elif' in Python
            self.logger.error(
                f"Created date {created_date_val} and current date {current_time_after_add} " f"differ by {time_difference} seconds, which is greater than 5 seconds.")
            raise AssertionError(f"Created date and current date differ by more than 5 seconds.")
        else:
            self.logger.info(
                f"Created date {created_date_val} and current date {current_time_after_add} "
                f"differ by {time_difference} seconds, which is within the 5-second threshold.")

        self.logger.info("All user details verified successfully on the User Details page.")

        # Verify the created super admin with login
        # -------- Open New Tab --------
        self.logger.info("Opening a new browser tab for login verification...")

        driver.execute_script("window.open('about:blank', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])

        self.logger.info("Switched to new browser tab")

        # res_page.click_logout()
        # self.logger.info("Logout successfully")
        time.sleep(3)

        # -------- Open New Tab --------
        self.logger.info("Opening a new browser tab for login verification...")

        # driver.execute_script("window.open('about:blank', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])

        self.logger.info("Switched to new browser tab")

        # -------- Navigate to Reseller Admin Login --------
        reseller_admin_url = "http://172.235.29.67:7777/reselleradmin"
        driver.get(reseller_admin_url)
        self.logger.info(f"Navigated to Reseller Admin URL: {reseller_admin_url}")

        # -------- Login with created reseller credentials --------
        login_page = LoginPage(driver)

        login_page.enter_email(self.reseller_email)
        self.logger.info(f"Entered reseller email: {self.reseller_email}")

        login_page.enter_password(password_val)  # password captured from User Details
        self.logger.info("Entered reseller password")

        login_page.click_signIn()
        self.logger.info("Clicked Sign In button")

        time.sleep(5)

        # -------- Verify successful login --------
        try:
            dashboard_page = DashboardPage(driver)
            dashboard_page.wait_for_element(dashboard_page.welcome_msg, timeout=30)
            welcome_text = dashboard_page.capture_welcomeMsg().strip(",")
            expected_welcome = f"Welcome to {self.reseller_email}"
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

        self.logger.info("Reseller login verified successfully ")

        # driver.quit()













