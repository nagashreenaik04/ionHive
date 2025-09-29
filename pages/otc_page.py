
from pages.base_page import BasePage
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By

class OTCPage(BasePage):

    #Locators
    otc_link = (By.LINK_TEXT, "Output Type Config")
    otc_page = (By.XPATH, '//h3[text()="Output Type Config"]')
    otc_list_table = (By.XPATH, '//h4[text()="List Of Output Type Config"]')
    addOTC_btn = (By.XPATH, '//button[text()="Add Output Type Config"]')


    #list of OTC table
    sino_clb = (By.XPATH, '//th[text()="Sl.No"]')
    outputType_clb = (By.XPATH, '//th[text()="Output Type"]')
    outputTypeName_clb = (By.XPATH, '//th[text()="Output Type Name"]')
    createdBy_clb = (By.XPATH, '//th[text()="Created By"]')
    createdDate_clb = (By.XPATH, '//th[text()="Created Date"]')
    modifiedBy_clb = (By.XPATH, '//th[text()="Modified By"]')
    modifiedDate_clb = (By.XPATH, '//th[text()="Modified Date"]')
    status_clb = (By.XPATH, '//th[text()="Status"]')
    activeOrDeActive_clb = (By.XPATH, '//th[text()="Active/DeActive"]')
    option_clb = (By.XPATH, '//th[text()="Option"]')
    activeOrDeactive_radio_btn = (By.XPATH, '//input[@type="radio"]')
    edit_btn = (By.XPATH, '//button[text()="Edit"]')

    #add OTC and edit
    add_otc_heading = (By.XPATH, "//h4[@class='card-title' and text()='Add Output Type Config']")
    type_drpdwn = (By.CSS_SELECTOR, "div.input-group select.form-control")
    add_output_type_name_field = (By.XPATH, '(//input[@placeholder="Output Type Name"])[1]')
    edit_output_type_name_field = (By.XPATH, '(//input[@placeholder="Output Type Name"])[2]')
    add_btn = (By.XPATH, '//button[text()="Add"]')
    update_btn = (By.XPATH, '//button[text()="Update"]')
    ok_btn = (By.XPATH, '//button[text()="OK"]')
    otc_success_msg = (By.XPATH,'//h2[text()="Add Output Type Config successfully"]')
    otc_error_msg = (By.XPATH,'//div[text() ="Output type already exists"]')
    close_icn = (By.XPATH,'//span[text()="×"]')
    close_icon_edit_popup = (By.XPATH,'(//span[text()="×"])[2]')
    edit_type_field = (By.XPATH, "//input[@placeholder='Output Type']")
    type_name_readable = (By.XPATH, "//input[@placeholder='Output Type Name']")

    #search OTC
    search_field = (By.XPATH, '//input[@placeholder="Search by Output Type/Name"]')

    # List of OTC table
    otc_table = (By.XPATH, "//table[@class='table table-striped']")
    table_header = (By.TAG_NAME, "thead")
    table_header_cell = (By.TAG_NAME, "th")
    row_table = (By.XPATH, ".//tbody/tr")
    table_data_cell = (By.TAG_NAME, "td")
    status_span = (By.TAG_NAME, "span")
    active_label = (By.XPATH, ".//label[@class='active']")

    #logout locator
    logout_drpdwn = (By.XPATH, '//*[@id="root"]/div/nav/div[2]/ul/li[2]')
    logout_btn = (By.XPATH, "(//i[@class='ti-power-off text-primary'])[2]")

    #edit table
    edit_otc_heading = (By.XPATH, '//h4[text()="Edit Output Type Config"]')
    edit_otc_success_msg = (By.XPATH, "//h2[text()='Update Output Type Config successfully']" )
    edit_otc_error_msg = (By.XPATH, "//div[text()='Output type with this name already exists']")

    #success messages
    deactive_success = (By.XPATH, "//h2[text()='Deactivated successfully']")
    active_success = (By.XPATH, "//h2[text()='Activated successfully']")

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_OTC(self):
        self.click(self.otc_link)

    def get_otc_heading(self):
        return self.find_element(self.otc_page).text

    def get_otc_list_table(self):
        return self.find_element(self.otc_list_table).text

    def get_addOTC_btn(self):
        return self.find_element(self.addOTC_btn).text

    def click_addOTC(self):
        self.click(self.addOTC_btn)

    def get_sino_clb(self):
        return self.get_text(self.sino_clb)

    def get_output_type_clb(self):
        return self.get_text(self.outputType_clb)

    def get_output_type_name_clb(self):
        return self.get_text(self.outputTypeName_clb)

    def get_created_by_clb(self):
        return self.get_text(self.createdBy_clb)

    def get_modified_by_clb(self):
        return self.get_text(self.modifiedBy_clb)

    def get_created_date_clb(self):
        return self.get_text(self.createdDate_clb)

    def get_modified_date_clb(self):
        return self.get_text(self.modifiedDate_clb)

    def get_status_clb(self):
        return self.get_text(self.status_clb)

    def get_activeOrDeactive_clb(self):
        return self.get_text(self.activeOrDeActive_clb)

    def get_option_clb(self):
        return self.get_text(self.option_clb)

    def click_logout(self):
        self.click(self.logout_drpdwn)
        self.click(self.logout_btn)

    def select_output_type(self,outputType):
        self.webelement_selectFromDropdown(self.type_drpdwn, outputType)

    def enter_output_type_name(self,outputTypeName):
        self.send_keys(self.add_output_type_name_field, outputTypeName)

    def click_add_btn(self):
        self.click(self.add_btn)

    def click_edit_btn(self):
        self.click(self.edit_btn)

    def enter_edit_output_type_name(self,editOutputTypeName):
        self.clear_element(self.edit_output_type_name_field)
        self.send_keys(self.edit_output_type_name_field, editOutputTypeName)

    def click_update_btn(self):
        self.click(self.update_btn)

    def click_deactive_or_activate_btn_in_row(self, row_index):
        """Click the 'Active/Deactive' button in the specified row (1-based index)."""
        try:
            self.wait_for_element(self.otc_table)
            rows = self.find_elements(self.row_table)
            if row_index < 1 or row_index > len(rows):
                raise ValueError(f"Row {row_index} does not exist. Table has {len(rows)} rows.")
            target_row = rows[row_index - 1]
            deactivateOrActiveRadio_button = target_row.find_element(By.XPATH, ".//input[@type='radio']")
            deactivateOrActiveRadio_button.click()
        except (NoSuchElementException, TimeoutException) as e:
            raise Exception(f"Failed to click 'Edit' button in row {row_index}: {str(e)}")
        except ValueError as e:
            raise

    def get_otc_success_msg(self):
        return  self.get_text(self.otc_success_msg)

    def get_otc_error_msg(self):
        return  self.get_text(self.otc_error_msg)

    def get_edit_otc_success_msg(self):
        return  self.find_element(self.edit_otc_success_msg).text

    def get_edit_otc_error_msg(self):
        return  self.get_text(self.edit_otc_error_msg)

    def click_ok_btn(self):
        self.click(self.ok_btn)

    def get_table_data(self):
        """Retrieve all data from the OTC table as a list of dictionaries."""
        # Wait for the table to be visible
        self.wait_for_element(self.otc_table)

        # Locate the table
        table = self.find_element(self.otc_table)

        # Get headers
        headers = [header.text.strip() for header in table.find_elements(*self.table_header_cell)]

        # Get data rows
        rows = table.find_elements(*self.row_table)
        table_data = []

        for row in rows:
            cells = row.find_elements(*self.table_data_cell)
            row_data = {}
            for index, cell in enumerate(cells):
                if index >= len(headers):
                    continue  # Skip if there are more cells than headers
                header = headers[index]
                text = cell.text.strip()

                # Handle special cases for Status and Active/DeActive columns
                if header == "Status":
                    try:
                        text = cell.find_element(*self.status_span).text.strip()
                    except:
                        pass  # Use cell text if no span is found
                elif header == "Active/DeActive":
                    try:
                        label = cell.find_element(*self.active_label).text.strip()
                        text = label if label else text
                    except:
                        pass  # Use cell text if no label is found

                row_data[header] = text
            table_data.append(row_data)

        return table_data


    def get_validation_message(self, field):
        return self.driver.execute_script("return arguments[0].validationMessage;", self.driver.find_element(*field))

    def click_close_icon(self):
        self.click(self.close_icn)

    def click_close_icon_edit_popup(self):
        self.click(self.close_icon_edit_popup)

    def get_row_data_by_cell_content(self, cell_text, column_index=3):
        """
        Retrieve data for the row where a cell in the specified column contains the given text.
        :param cell_text: Text to match in the specified column (e.g., 'Type5').
        :param column_index: Column index (1-based) containing the text (default: 3 for 'Output Type Name').
        :return: Dictionary of row data, or None if not found.
        """
        try:
            table_data = self.get_table_data()
            for row in table_data:
                if row.get("Output Type Name") == cell_text:
                    return row
            self.logger().info(f"No row found with '{cell_text}' in column {column_index}")
            return None
        except Exception as e:
            self.logger().error(f"Error retrieving row data for '{cell_text}' in column {column_index}: {str(e)}")
            return None

    def get_edit_type_field(self):
        return self.wait_for_element(self.edit_type_field)

    def get_update_btn_not_clickable(self):
        return self.wait_for_element(self.update_btn)

    def get_type_name_readable(self):
        return self.wait_for_element(self.type_name_readable)

    def click_edit_btn_in_row(self, row_index):
        """Click the 'Edit' button in the specified row (1-based index)."""
        try:
            self.wait_for_element(self.otc_table)
            rows = self.find_elements(self.row_table)
            if row_index < 1 or row_index > len(rows):
                raise ValueError(f"Row {row_index} does not exist. Table has {len(rows)} rows.")
            target_row = rows[row_index - 1]
            edit_button = target_row.find_element(By.XPATH, ".//button[text()='Edit']")
            edit_button.click()
        except (NoSuchElementException, TimeoutException) as e:
            raise Exception(f"Failed to click 'Edit' button in row {row_index}: {str(e)}")
        except ValueError as e:
            raise

    def get_otc_deactivate_success_msg(self):
        return  self.get_text(self.deactive_success)

    def get_otc_activate_success_msg(self):
        return  self.get_text(self.active_success)
