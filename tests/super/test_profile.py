import time
from datetime import datetime

import pytest

from pages.super.profile_page import ProfilePage
from pages.super.user_page import UserPage
from utilities.custom_logger import LogGen
from utilities.login_helper import LoginHelper
from utilities.screenshot_utility import ScreenshotUtility


@pytest.mark.usefixtures("driver")
class TestProfile:
    logger = LogGen.loggen()

    expected_suc_msg = "Profile updated successfully"
    expected_edit_suc_msg = "User updated successfully"
    search_email = "outdidsuperadmin@gmail.com"

    expected_role = "Super Admin"
    expected_username = "assoU001"
    expected_email = "outdidsuperadmin@gmail.com"
    expected_assigned_reseller = "-"
    expected_assigned_client = "-"
    expected_assigned_association = "-"
    expected_created_by = "vivek"
    expected_created_date = "01/01/1970 05:30:00 AM"
    expected_modified_by = expected_email
    expected_status = "Active"


    def setup_profile_test(self, driver):
        """Common setup for OTC tests: login, navigate to OTC page, and initialize screenshot utility."""
        login_helper = LoginHelper()
        login_helper.login(driver)
        self.logger.info("Login successful")
        time.sleep(2)

        prfl_page = ProfilePage(driver)
        prfl_page.navigate_to_profile_page()
        self.logger.info("Navigated to Profile page")
        time.sleep(2)

        screenshot_util = ScreenshotUtility(driver)
        return prfl_page, screenshot_util

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
    def test_profile_page(self, driver):
        prfl_page, screenshot_util = self.setup_profile_test(driver)

        results = prfl_page.verify_all_profile_elements_present()

        # Assert every element is present
        for element_name, is_present in results.items():
            assert is_present, f" {element_name} is NOT present on Profile Page"

        self.logger.info("All profile page elements are present")

        prfl_page.click_logout()
        self.logger.info("Logout successfully")

    @pytest.mark.sanity
    def test_username_and_email_field_readonly(self, driver):
        prfl_page, screenshot_util = self.setup_profile_test(driver)

        assert prfl_page.is_field_readonly(prfl_page.username_field), \
            "Username field is NOT readonly."

        assert prfl_page.is_field_readonly(prfl_page.email_field), \
            "Email field is NOT readonly."

        self.logger.info("Username and Email fields are readonly")

        prfl_page.click_logout()
        self.logger.info("Logout successfully")

    @pytest.mark.regression
    def test_update_btn_disabled(self, driver):
        prfl_page, screenshot_util = self.setup_profile_test(driver)

        # Step 1: Check if Update button is initially disabled
        update_btn_state_initial = prfl_page.find_element(prfl_page.update_btn).get_attribute("disabled")

        assert update_btn_state_initial is not None, \
            "Update button should be disabled before entering password."

        self.logger.info("Verified: Update button is disabled initially.")

        # Screenshot before typing
        #screenshot_util.capture_screenshot("update_disabled_initial")

        # Step 2: Enter a new password
        new_password = "4321"
        prfl_page.update_password(new_password)

        time.sleep(2)  # Give UI time to update state

        # Step 3: Check if Update button is now enabled
        update_btn_state_after = prfl_page.find_element(prfl_page.update_btn).get_attribute("disabled")

        assert update_btn_state_after is None, \
            "Update button should be enabled after entering password."

        self.logger.info("Verified: Update button is enabled after typing password.")

        # Screenshot after typing password
        #screenshot_util.capture_screenshot("update_enabled_after_input")

        prfl_page.click_logout()
        self.logger.info("Logout successfully")

    @pytest.mark.integration
    def test_update_button_remains_disabled_for_original_data(self, driver):
        prfl_page, screenshot_util = self.setup_profile_test(driver)

        # Step 1: Capture existing values
        old_phone = prfl_page.find_element(prfl_page.phone_field).get_attribute("value")
        old_password = prfl_page.find_element(prfl_page.password_field).get_attribute("value")

        self.logger.info(f"Captured Existing Data -> Phone: {old_phone}, Password: {old_password}")

        # Screenshot initial fields
        #screenshot_util.capture_screenshot("initial_profile_values")

        # Step 2: Clear fields
        prfl_page.clear_element(prfl_page.phone_field)
        prfl_page.clear_element(prfl_page.password_field)
        time.sleep(2)

        # Step 3: Enter temporary random data
        temp_phone = "7896541230"
        temp_pass = 4321

        prfl_page.send_keys(prfl_page.phone_field, temp_phone)
        prfl_page.send_keys(prfl_page.password_field, temp_pass)
        time.sleep(2)

        self.logger.info("Entered temporary phone & password")

        #screenshot_util.capture_screenshot("temporary_values_entered")

        time.sleep(1)

        # Step 4: Clear again and re-enter the original captured values
        prfl_page.clear_element(prfl_page.phone_field)
        prfl_page.clear_element(prfl_page.password_field)

        prfl_page.send_keys(prfl_page.phone_field, old_phone)
        prfl_page.send_keys(prfl_page.password_field, old_password)

        self.logger.info("Re-entered original phone & password")

        time.sleep(2)
        #screenshot_util.capture_screenshot("reentered_original_values")

        # Step 5: Verify Update button remains disabled
        update_button_state = prfl_page.find_element(prfl_page.update_btn).get_attribute("disabled")

        assert update_button_state is not None, \
            "Update button should remain disabled when old data is re-entered, but it became enabled."

        self.logger.info("Verified: Update button remained disabled after entering original values")

        # Step 6: Logout
        prfl_page.click_logout()
        self.logger.info("Logout successfully")


    @pytest.mark.integration
    def test_update_profile_and_verify_in_user_page(self, driver):
        prfl_page, screenshot_util = self.setup_profile_test(driver)

        prfl_page.click_logout()
        self.logger.info("Logout successfully")

    @pytest.mark.endtesting
    def test_update_in_user_page_and_verify_in_profile_page(self, driver):
        """Test updating phone & password in Profile Page and verify the success message."""

        prfl_page, screenshot_util = self.setup_profile_test(driver)

        # ------- Step 1: Capture Existing Field Values -------
        old_phone = prfl_page.find_element(prfl_page.phone_field).get_attribute("value")
        old_password = prfl_page.find_element(prfl_page.password_field).get_attribute("value")

        self.logger.info(f"Existing Profile Data -> Phone: {old_phone}, Password: {old_password}")
        #screenshot_util.capture_screenshot("old_profile_data")

        # ------- Step 2: Enter New Updated Values -------
        new_phone = "7896541230"
        new_password = "4321"

        prfl_page.clear_element(prfl_page.phone_field)
        prfl_page.send_keys(prfl_page.phone_field, new_phone)

        prfl_page.update_password(new_password)

        self.logger.info(f"Entered New Data -> Phone: {new_phone}, Password: {new_password}")
        #screenshot_util.capture_screenshot("new_values_entered")

        time.sleep(2)  # Optional, can be replaced by explicit wait

        # ------- Step 3: Click Update -------
        prfl_page.click_update()
        current_time = datetime.now()
        current_time_after_update = current_time.strftime("%d/%m/%Y %I:%M:%S %p")
        self.logger.info("Clicked Update button")
        time.sleep(2)

        # ------- Step 4: Validate Success Message -------
        try:
            success_msg = prfl_page.get_suc_msg()
            self.logger.info(f"Success message displayed: {success_msg}")

            assert success_msg == self.expected_suc_msg, \
                f"Expected success message '{self.expected_suc_msg}', but got '{success_msg}'"

            prfl_page.click_okBtn()
            self.logger.info("Clicked OK button on success popup")

        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("profile_update_failure")
            self.logger.error(f"Validation Failed: {str(e)}")
            self.logger.error(f"Screenshot captured: {screenshot_path}")
            raise
        self.logger.info("Profile update completed successfully")

        # --------------- NEWLY ADDED VERIFICATION LOGIC ----------------

        self.logger.info("Navigating to User Page to verify updated details...")

        user_page = UserPage(driver)
        user_page.navigate_to_user_page()
        time.sleep(6)
        #screenshot_util.capture_screenshot("navigated_to_user_page")

        # Search for the user using phone number
        user_page.serch(self.search_email)
        time.sleep(2)

        # -------- Verify First Row in User Table --------
        self.logger.info("Validating first row data in Users table...")

        first_row_values = user_page.get_first_row_data()
        self.logger.info(f"Extracted Row Data: {first_row_values}")

        assert self.expected_role in first_row_values[1], f"Role mismatch. Expected {self.expected_role}, actual {first_row_values[0]}"
        assert self.expected_username in first_row_values[2], f"Username mismatch. Expected {self.expected_username}"
        assert self.expected_email in first_row_values[3], f"Email mismatch. Expected {self.expected_email}"
        assert self.expected_status in first_row_values[4], f"Status mismatch. Expected {self.expected_status}"

        self.logger.info("Validation successful. All user details match expected values.")

        # -------- Click View Button --------
        user_page.click_view_btn_first_row()
        self.logger.info("Clicked 'View' button for the matched user.")
        #screenshot_util.capture_screenshot("user_view_page_opened")
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

        # Assertions
        assert user_name_val == self.expected_username, \
            f"Username mismatch. Expected: {self.expected_username}, Got: {user_name_val}"

        assert email_val == self.expected_email, \
            f"Email mismatch. Expected: {self.expected_email}, Got: {email_val}"

        assert phone_val == new_phone, \
            f"Phone mismatch. Expected: {new_phone}, Got: {phone_val}"

        assert password_val == new_password, \
            f"Password mismatch. Expected: {new_password}, Got: {password_val}"

        assert role_val == self.expected_role, \
            f"Role mismatch. Expected: {self.expected_role}, Got: {role_val}"

        assert assigned_res_val == self.expected_assigned_reseller, \
            f"Username mismatch. Expected: {self.expected_assigned_reseller}, Got: {assigned_res_val}"

        assert assigned_client_val == self.expected_assigned_client, \
            f"Username mismatch. Expected: {self.expected_assigned_client}, Got: {assigned_client_val}"

        assert assigned_ass_val == self.expected_assigned_association, \
            f"Username mismatch. Expected: {self.expected_assigned_association}, Got: {assigned_ass_val}"

        assert created_by_val == self.expected_created_by, \
            f"Username mismatch. Expected: {self.expected_created_by}, Got: {created_by_val}"

        assert created_date_val == self.expected_created_date, \
            f"Username mismatch. Expected: {self.expected_created_date}, Got: {created_date_val}"

        assert modified_by_val == self.expected_modified_by, \
            f"Username mismatch. Expected: {self.expected_modified_by}, Got: {modified_by_val}"

        # assert modified_date_val == self.expected_assigned_association, \
        #     f"Username mismatch. Expected: {self.expected_assigned_association}, Got: {modified_date_val}"

        assert status_val == self.expected_status, \
            f"Status mismatch. Expected: {self.expected_status}, Got: {status_val}"

        # Check if the difference between the current time and created date is greater than 5 seconds
        is_greater, time_difference = self.check_time_difference(modified_date_val, current_time_after_update)
        if modified_date_val == current_time_after_update:
            self.logger.info(
                f"Updated date {modified_date_val} and current date {current_time_after_update} are the same")
        elif is_greater:  # Fixed syntax: 'else if' should be 'elif' in Python
            self.logger.error(
                f"Updated date {modified_date_val} and current date {current_time_after_update} " f"differ by {time_difference} seconds, which is greater than 5 seconds.")
            raise AssertionError(f"Update date and current date differ by more than 5 seconds.")
        else:
            self.logger.info(
                f"Updated date {modified_date_val} and current date {current_time_after_update} "
                f"differ by {time_difference} seconds, which is within the 5-second threshold.")

        self.logger.info("All user details verified successfully on the User Details page.")

        #screenshot_util.capture_screenshot("user_details_validated")

        #Edit the old data in Edit User Page
        user_page.click_edit_btn()
        time.sleep(1)
        user_page.edit_phone_field(old_phone)
        user_page.edit_password_field(old_password)
        time.sleep(1)
        user_page.click_update_btn()
        time.sleep(1)
        try:
            edit_suc_msg = user_page.get_edit_suc_msg()
            self.logger.info(f"Success message displayed: {edit_suc_msg}")
            assert edit_suc_msg == self.expected_edit_suc_msg, \
                f"Expected success message '{self.expected_edit_suc_msg}', but got '{edit_suc_msg}'"
            prfl_page.click_okBtn()
            self.logger.info("Clicked OK button on success popup")
        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("profile_update_failure")
            self.logger.error(f"Validation Failed: {str(e)}")
            self.logger.error(f"Screenshot captured: {screenshot_path}")
            raise

        #Verify the Profile page
        prfl_page.navigate_to_profile_page()
        time.sleep(5)
        phone_val = prfl_page.find_element(prfl_page.phone_field).get_attribute("value").strip()
        password_val = prfl_page.find_element(prfl_page.password_field).get_attribute("value").strip()

        assert phone_val == old_phone, \
            f"Phone mismatch. Expected: {old_phone}, Got: {phone_val}"

        assert password_val == old_password, \
            f"Password mismatch. Expected: {old_password}, Got: {password_val}"

        # ------- Step 5: Logout -------
        prfl_page.click_logout()
        self.logger.info("Logout successful")



