#Before executing this Test, there are some Pre-conditions are there
#i.e.,
#1.In 'List Of Roles' table, until 5 rows Role Name, Created By and Created Date datas are same as 'test_role' datas.
## if it is not same then make the test_role and List of roles data same by updated test_role.
#2.All 5 rows status should be 'Active'
#3.Observe the test_edit_role data and confirm is that okay to execute.
##if not updated the test_edit_role datas.

import time
from datetime import datetime

import pytest

from pages.super.role_page import RolePage
from utilities.custom_logger import LogGen
from utilities.login_helper import LoginHelper
from utilities.screenshot_utility import ScreenshotUtility


@pytest.mark.usefixtures("driver")
class TestRole:
    logger = LogGen.loggen()

    # Validate the Role page
    actual_page_heading = "Manage User Role's"
    actual_role_table = "List Of Role's"

    #
    existed_role_name = "Reseller Admin"

    # Define test cases for role verification
    test_roles = [
        {"Sl.No": "1", "Role Name": "Super Admin", "Created By": "superadmin@gmail.com", "Created Date":"01/01/1970 05:30:00 AM"},
        {"Sl.No": "2", "Role Name": "Client Admin", "Created By": "superadmin@gmail.com", "Created Date":"05/07/2024 11:17:53 AM"},
        {"Sl.No": "3", "Role Name": "Reseller Admin", "Created By": "superadmin", "Created Date":"05/07/2024 10:20:27 AM"},
        {"Sl.No": "4", "Role Name": "App User", "Created By": "superadmin@gmail.com", "Created Date":"05/07/2024 11:53:04 AM"},
        {"Sl.No": "5", "Role Name": "Association Admin", "Created By": "superadmin@gmail.com", "Created Date":"05/07/2024 11:36:50 AM"}
    ]

    expected_role_success_msg ="Update user role successfully"
    expected_deactive_success_msg = "Deactivated successfully"
    expected_err_msg = "Role name already exists"

    test_edit_role = [
        {"Sl.No": "1", "Role Name": "Super Admin", "edit_role": "Super"},
        {"Sl.No": "2", "Role Name": "Client Admin", "edit_role": "Client"},
        {"Sl.No": "3", "Role Name": "Reseller Admin", "edit_role": "Reseller"},
        {"Sl.No": "4", "Role Name": "App User", "edit_role": "App"},
        {"Sl.No": "5", "Role Name": "Association Admin", "edit_role": "Association"}
    ]


    def setup_role_test(self, driver):
        """Common setup for OTC tests: login, navigate to OTC page, and initialize screenshot utility."""
        login_helper = LoginHelper()
        login_helper.login(driver)
        self.logger.info("Login successful")
        time.sleep(2)

        role_page = RolePage(driver)
        role_page.navigate_to_role()
        self.logger.info("Navigated to Manage User Role's page")
        time.sleep(2)

        screenshot_util = ScreenshotUtility(driver)
        return role_page, screenshot_util

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
    def test_role_page(self, driver):
        role_page, screenshot_util = self.setup_role_test(driver)

        # Verify the Page Heading
        page_heading = role_page.get_role_heading()
        self.logger.info(f"Page Heading is: {page_heading}")
        try:
            assert page_heading == self.actual_page_heading, f"Expected Heading '{self.actual_page_heading}', but got '{page_heading}'"
            self.logger.info("Role Heading verified successfully")
        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("test_valid_role_heading")
            self.logger.error(f"Test failed, screenshot saved at: {screenshot_path}")

        # Verify the OTC Table
        role_table = role_page.get_role_list_table()
        self.logger.info(f"Table Heading is: {role_table}")
        try:
            assert role_table == self.actual_role_table, f"Expected Table '{self.actual_role_table}', but got '{role_table}'"
            self.logger.info("Role Table verified successfully")
        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("test_valid_role_table")
            self.logger.error(f"Test failed, screenshot saved at: {screenshot_path}")

        role_page.click_logout()
        self.logger.info("Logout successfully")

    # @pytest.mark.sanity
    def test_verify_role(self, driver):
        role_page, screenshot_util = self.setup_role_test(driver)

        try:
            # Fetch all role rows from UI
            actual_roles = role_page.get_all_roles()
            self.logger.info(f"Full table data from UI: {actual_roles}")

            # Ensure table has at least 5 rows
            assert len(actual_roles) >= 5, (
                f"Table contains only {len(actual_roles)} rows, but 5 rows are required."
            )

            # Only check the first 5 rows
            actual_first_five = actual_roles[:5]

            # Compare each expected row with UI row
            for expected, actual in zip(self.test_roles, actual_first_five):

                # ------------------------------------------------------
                # ROLE NAME – JUST LOG MESSAGE, DO NOT FAIL THE TEST
                # ------------------------------------------------------
                if expected["Role Name"] != actual["Role Name"]:
                    self.logger.warning(
                        f"[ROLE NAME MISMATCH] Actual Role Name: '{actual['Role Name']}' | "
                        f"Expected Role Name: '{expected['Role Name']}'"
                    )
                else:
                    self.logger.info(f"Role Name matched: {actual['Role Name']}")

                # ------------------------------------------------------
                # CREATED BY – MUST MATCH → FAIL IF DIFFERENT
                # ------------------------------------------------------
                assert expected["Created By"] == actual["Created By"], (
                    f"Actual Created By: '{actual['Created By']}' | "
                    f"Expected Created By: '{expected['Created By']}'"
                )

                # ------------------------------------------------------
                # CREATED DATE – MUST MATCH → FAIL IF DIFFERENT
                # ------------------------------------------------------
                assert expected["Created Date"] == actual["Created Date"], (
                    f"Actual Created Date: '{actual['Created Date']}' | "
                    f"Expected Created Date: '{expected['Created Date']}'"
                )

            self.logger.info("Created By & Created Date validated successfully for first 5 rows.")
            self.logger.info("Role Name mismatches (if any) were logged without failing the test.")
            role_page.click_logout()
            self.logger.info("Logout successfully")

        except Exception as e:
            screenshot_path = screenshot_util.capture_screenshot("test_verify_role_failure")
            self.logger.error(f"Validation failed! Screenshot saved at: {screenshot_path}")
            pytest.fail(str(e))


    @pytest.mark.regression
    def test_edit_first_five_rows(self, driver):
        role_page, screenshot_util = self.setup_role_test(driver)

        for role_data in self.test_edit_role:  # Iterate over all 5 rows
            slno = role_data["Sl.No"]
            original_role_name = role_data["Role Name"]
            new_role_name = role_data["edit_role"]

            try:
                # STEP 1: Get the row by Sl.No fresh every iteration
                row = role_page.get_row_by_slno(slno)
                assert row is not None, f"Row with Sl.No {slno} not found."

                cells = row.find_elements(*role_page.table_data_cell)
                actual_role_name = cells[1].text.strip()
                assert actual_role_name == original_role_name, (
                    f"Role Name mismatch → Expected: '{original_role_name}', Actual: '{actual_role_name}'"
                )

                self.logger.info(f"Sl.No {slno} Found Successfully | Original Role Name: {actual_role_name}")

                # STEP 2: Click Edit button
                # edit_button = cells[-1].find_element(*role_page.edit_btn)
                # edit_button.click()
                last_cell = row.find_elements(*role_page.table_data_cell)[-1]  # Get last cell of the row
                edit_button = last_cell.find_element(*role_page.edit_btn)  # Use find_element properly
                edit_button.click()
                self.logger.info(f"Clicked Edit button for Sl.No {slno}")
                time.sleep(1)

                # STEP 3: Clear Role Name
                role_page.clear_role_name()
                time.sleep(0.5)

                # STEP 4: Enter new role name
                role_page.enter_role_name(new_role_name)
                time.sleep(0.5)

                # STEP 5: Click Update button
                role_page.click_update()
                time.sleep(2)

                # STEP 6: Verify success message
                get_role_success_msg = role_page.get_role_success_msg()
                assert get_role_success_msg == self.expected_role_success_msg
                role_page.click_ok_btn()
                # Log after the update with the exact time
                current_time = datetime.now()
                current_time_after_update = current_time.strftime("%d/%m/%Y %I:%M:%S %p")

                # STEP 7: Verify updated Role Name
                updated_row = role_page.get_row_by_slno(slno)  # Get fresh row
                updated_cells = updated_row.find_elements(*role_page.table_data_cell)
                updated_role_name = updated_cells[1].text.strip()
                assert updated_role_name == new_role_name
                self.logger.info(f"Updated Role Name for Sl.No {slno} verified: '{updated_role_name}'")

                row = role_page.get_row_by_slno(slno)
                cells = row.find_elements(*role_page.table_data_cell)
                actual_modified_date = cells[5].text.strip()
                # Check if the difference between the current time and updated date is greater than 5 seconds
                is_greater, time_difference = self.check_time_difference(actual_modified_date, current_time_after_update)
                if actual_modified_date == current_time_after_update:
                    self.logger.info(
                        f"Updated date {actual_modified_date} and current date {current_time_after_update} are the same")
                elif is_greater:  # Fixed syntax: 'else if' should be 'elif' in Python
                    self.logger.error(
                        f"Updated date {actual_modified_date} and current date {current_time_after_update} " f"differ by {time_difference} seconds, which is greater than 5 seconds.")
                    raise AssertionError(f"Updated date and current date differ by more than 5 seconds.")
                else:
                    self.logger.info(
                        f"Updated date {actual_modified_date} and current date {current_time_after_update} "
                        f"differ by {time_difference} seconds, which is within the 5-second threshold.")

                # STEP 8: Restore original Role Name
                updated_row = role_page.get_row_by_slno(slno)  # Fetch row again
                restored_cells = updated_row.find_elements(*role_page.table_data_cell)
                edit_button = restored_cells[-1].find_element(*role_page.edit_btn)
                edit_button.click()
                time.sleep(1)

                role_page.clear_role_name()
                role_page.enter_role_name(original_role_name)
                role_page.click_update()
                time.sleep(2)
                role_page.click_ok_btn()
                current_time = datetime.now()
                current_time_after_update = current_time.strftime("%d/%m/%Y %I:%M:%S %p")

                restored_row = role_page.get_row_by_slno(slno)
                restored_cells = restored_row.find_elements(*role_page.table_data_cell)
                restored_role_name = restored_cells[1].text.strip()
                assert restored_role_name == original_role_name
                self.logger.info(f"Original Role Name for Sl.No {slno} restored successfully: '{restored_role_name}'")
                time.sleep(2)

                row = role_page.get_row_by_slno(slno)
                cells = row.find_elements(*role_page.table_data_cell)
                actual_modified_date = cells[5].text.strip()
                # Check if the difference between the current time and updated date is greater than 5 seconds
                is_greater, time_difference = self.check_time_difference(actual_modified_date,
                                                                         current_time_after_update)
                if actual_modified_date == current_time_after_update:
                    self.logger.info(
                        f"Updated date {actual_modified_date} and current date {current_time_after_update} are the same")
                elif is_greater:  # Fixed syntax: 'else if' should be 'elif' in Python
                    self.logger.error(
                        f"Updated date {actual_modified_date} and current date {current_time_after_update} " f"differ by {time_difference} seconds, which is greater than 5 seconds.")
                    raise AssertionError(f"Updated date and current date differ by more than 5 seconds.")
                else:
                    self.logger.info(
                        f"Updated date {actual_modified_date} and current date {current_time_after_update} "
                        f"differ by {time_difference} seconds, which is within the 5-second threshold.")


            except Exception as e:
                screenshot_path = screenshot_util.capture_screenshot(f"edit_restore_failure_slno_{slno}")
                self.logger.error(f"Failed while editing/restoring row {slno}. Screenshot: {screenshot_path}")
                pytest.fail(str(e))

        role_page.click_logout()
        self.logger.info("Logout successfully")

    @pytest.mark.integration
    def test_deactive_and_active_first_five_rows(self, driver):
        role_page, screenshot_util = self.setup_role_test(driver)

        for role_data in self.test_edit_role:  # Iterate over all 5 rows
            slno = role_data["Sl.No"]
            role_name = role_data["Role Name"]
            original_status = "Active"

            try:
                # STEP 1: Get the row by Sl.No fresh every iteration
                row = role_page.get_row_by_slno(slno)
                assert row is not None, f"Row with Sl.No {slno} not found."

                cells = row.find_elements(*role_page.table_data_cell)

                # --- Verify Role Name ---
                actual_role_name = cells[1].text.strip()
                assert actual_role_name == role_name, (
                    f"Role Name mismatch → Expected: '{role_name}', Actual: '{actual_role_name}'"
                )

                # --- ADD THIS: Verify Status column contains 'Active' ---
                status_text = cells[6].text.strip()
                assert status_text.strip() == "Active", (
                    f"Status mismatch → Expected: 'Active', Actual: '{status_text}'"
                )

                self.logger.info(
                    f"Sl.No {slno} Found Successfully | Role Name: {actual_role_name} | Status: {status_text}"
                )

                # --- Click DeActive checkbox ---
                # last_cell = row.find_elements(*role_page.table_data_cell)[-2]  # Get last cell of the row
                # deactive_checkbox = last_cell.find_element(*role_page.deactive_lbl)
                row = role_page.get_row_by_slno(slno)  # fresh fetch
                # find the “DeActive” checkbox inside that row (relative xpath):
                checkbox = row.find_element(*role_page.deactive_lbl)
                checkbox.click()
                # deactive_checkbox.click()
                time.sleep(2)  # wait for the action to complete


                # # Verify success message
                get_deative_success_msg = role_page.get_deactive_success_msg()
                assert get_deative_success_msg == self.expected_deactive_success_msg
                role_page.click_ok_btn()
                current_time = datetime.now()
                current_time_after_update = current_time.strftime("%d/%m/%Y %I:%M:%S %p")
                role_page.refresh()
                time.sleep(3)

                # Verify updated Role Name
                updated_row = role_page.get_row_by_slno(slno)  # Get fresh row
                updated_cells = updated_row.find_elements(*role_page.table_data_cell)
                updated_status = updated_cells[6].text.strip()
                assert updated_status != original_status
                self.logger.info(f"Updated Status for Sl.No {slno} verified: '{updated_status}'")

                row = role_page.get_row_by_slno(slno)
                cells = row.find_elements(*role_page.table_data_cell)
                actual_modified_date = cells[5].text.strip()
                # Check if the difference between the current time and updated date is greater than 5 seconds
                is_greater, time_difference = self.check_time_difference(actual_modified_date,
                                                                         current_time_after_update)
                if actual_modified_date == current_time_after_update:
                    self.logger.info(
                        f"Updated date {actual_modified_date} and current date {current_time_after_update} are the same")
                elif is_greater:  # Fixed syntax: 'else if' should be 'elif' in Python
                    self.logger.error(
                        f"Updated date {actual_modified_date} and current date {current_time_after_update} " f"differ by {time_difference} seconds, which is greater than 5 seconds.")
                    raise AssertionError(f"Updated date and current date differ by more than 5 seconds.")
                else:
                    self.logger.info(
                        f"Updated date {actual_modified_date} and current date {current_time_after_update} "
                        f"differ by {time_difference} seconds, which is within the 5-second threshold.")

                # STEP 8: Restore original Role Name
                updated_row = role_page.get_row_by_slno(slno)  # Fetch row again
                restored_cells = updated_row.find_elements(*role_page.table_data_cell)
                active_checkbox = restored_cells[-2].find_element(*role_page.active_lbl)
                active_checkbox.click()
                time.sleep(2)
                role_page.click_ok_btn()
                current_time = datetime.now()
                current_time_after_update = current_time.strftime("%d/%m/%Y %I:%M:%S %p")
                role_page.refresh()
                time.sleep(3)

                restored_row = role_page.get_row_by_slno(slno)
                restored_cells = restored_row.find_elements(*role_page.table_data_cell)
                restored_status = restored_cells[6].text.strip()
                assert restored_status == original_status
                self.logger.info(f"Original Status for Sl.No {slno} restored successfully: '{restored_status}'")
                time.sleep(2)

                row = role_page.get_row_by_slno(slno)
                cells = row.find_elements(*role_page.table_data_cell)
                actual_modified_date = cells[5].text.strip()
                # Check if the difference between the current time and updated date is greater than 5 seconds
                is_greater, time_difference = self.check_time_difference(actual_modified_date,
                                                                         current_time_after_update)
                if actual_modified_date == current_time_after_update:
                    self.logger.info(
                        f"Updated date {actual_modified_date} and current date {current_time_after_update} are the same")
                elif is_greater:  # Fixed syntax: 'else if' should be 'elif' in Python
                    self.logger.error(
                        f"Updated date {actual_modified_date} and current date {current_time_after_update} " f"differ by {time_difference} seconds, which is greater than 5 seconds.")
                    raise AssertionError(f"Updated date and current date differ by more than 5 seconds.")
                else:
                    self.logger.info(
                        f"Updated date {actual_modified_date} and current date {current_time_after_update} "
                        f"differ by {time_difference} seconds, which is within the 5-second threshold.")



            except Exception as e:
                screenshot_path = screenshot_util.capture_screenshot(f"edit_restore_failure_slno_{slno}")
                self.logger.error(f"Failed while deactivating/restoring row {slno}. Screenshot: {screenshot_path}")
                pytest.fail(str(e))

        role_page.click_logout()
        self.logger.info("Logout successfully")

    @pytest.mark.endtesting
    def test_existing_rolename(self, driver):
        role_data = self.test_edit_role[0]  # first item only
        slno = role_data["Sl.No"]
        expected_role_name = role_data["Role Name"]
        role_page, screenshot_util = self.setup_role_test(driver)

        # STEP 1: locate the row by Sl.No
        row = role_page.get_row_by_slno(slno)
        assert row is not None, f"Row with Sl.No {slno} not found."

        cells = row.find_elements(*role_page.table_data_cell)
        actual_role_name = cells[1].text.strip()
        assert actual_role_name == expected_role_name, (
            f"Role Name mismatch → Expected: '{expected_role_name}', Actual: '{actual_role_name}'"
        )

        # STEP 2: Click Edit button for that row
        last_cell = row.find_elements(*role_page.table_data_cell)[-1]
        edit_button = last_cell.find_element(*role_page.edit_btn)
        edit_button.click()
        time.sleep(1)

        # STEP 3: Clear and enter the existing/duplicate role name
        role_page.clear_role_name()
        time.sleep(0.5)
        role_page.enter_role_name(self.existed_role_name)
        time.sleep(0.5)

        # STEP 4: Click Update
        role_page.click_update()
        time.sleep(2)

        #Verify the error message
        get_err_msg = role_page.get_err_msg()
        assert get_err_msg == self.expected_err_msg
        role_page.click_ok_btn()

        # At this point, add assertions/validations as per application behavior:
        # e.g., verify error message appears that name exists, or verify input rejected, etc.

        role_page.click_logout()

