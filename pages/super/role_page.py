from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class RolePage(BasePage):

    #Locators
    role_link = (By.XPATH, "//span[text()='Manage User Roles']")
    role_page = (By.XPATH, '//h3[text()="Manage User Role\'s"]')
    role_list_table = (By.XPATH, '//h4[text()="List Of Role\'s"]')

    # List of Role table
    role_table = (By.XPATH, "//table[@class='table table-striped']")
    table_header = (By.TAG_NAME, "thead")
    table_header_cell = (By.TAG_NAME, "th")
    row_table = (By.XPATH, ".//tbody/tr")
    table_data_cell = (By.TAG_NAME, "td")
    status_span = (By.TAG_NAME, "span")
    active_label = (By.XPATH, ".//label[@class='active']")

    # Edit button
    edit_btn = (By.XPATH, ".//button[contains(text(),'Edit')]")
    role_name_field = (By.XPATH, '//input[@placeholder="Role Name"]')
    update_btn = (By.XPATH, '//button[text()="Update"]')

    # Active Deactive Checkbox
    deactive_lbl = (By.ID, 'optionsRadios2')
    deactive_suc = (By.XPATH, "//h2[text()='Deactivated successfully']")
    active_lbl =(By.XPATH, "//label[text()='Active']")
    active_suc = (By.XPATH, "//h2[text()='Activated successfully']")

    # Success
    suc_msg = (By.XPATH, "//h2[text()='Update user role successfully']")
    ok_btn = (By.XPATH, "//button[text()='OK']")

    #Error
    err_msg = (By.XPATH, "//div[text()='Role name already exists']")

    # logout locator
    logout_drpdwn = (By.XPATH, '//*[@id="root"]/div/nav/div[2]/ul/li[2]')
    logout_btn = (By.XPATH, "(//i[@class='ti-power-off text-primary'])[2]")

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_role(self):
        self.click(self.role_link)

    def get_role_heading(self):
        return self.find_element(self.role_page).text

    def get_role_list_table(self):
        return self.find_element(self.role_list_table).text

    def get_all_roles(self):
        table = self.find_element(self.role_table)
        rows = table.find_elements(*self.row_table)

        all_roles = []
        for row in rows:
            cells = row.find_elements(*self.table_data_cell)
            all_roles.append({
                "Sl.No": cells[0].text.strip(),
                "Role Name": cells[1].text.strip(),
                "Created By": cells[2].text.strip(),
                "Created Date": cells[3].text.strip(),
            })
        return all_roles

    def get_row_by_slno(self, slno):
        table = self.find_element(self.role_table)
        rows = table.find_elements(*self.row_table)

        for row in rows:
            cells = row.find_elements(*self.table_data_cell)
            if cells and cells[0].text.strip() == slno:
                return row
        return None

    def click_edit_button_on_row(self, row):
        row.find_element(*self.edit_btn).click()

    def clear_role_name(self):
        field = self.find_element(self.role_name_field)
        field.clear()

    def enter_role_name(self, role_name):
        field = self.find_element(self.role_name_field)
        field.send_keys(role_name)

    def click_update(self):
        self.click(self.update_btn)

    def get_role_success_msg(self):
        return  self.get_text(self.suc_msg)

    def click_ok_btn(self):
        self.click(self.ok_btn)

    def click_logout(self):
        self.click(self.logout_drpdwn)
        self.click(self.logout_btn)

    def click_deactive_checkbox(self):
        deactive_checkbox = self.find_element(self.deactive_lbl)
        deactive_checkbox.click()

    def click_active_checkbox(self):
        active_checkbox = self.find_element(self.active_lbl)
        active_checkbox.click()

    def get_deactive_success_msg(self):
        return  self.get_text(self.deactive_suc)

    def get_row_by_name(self, role_name):
        """Return the row element for a given role name."""
        rows = self.driver.find_elements(*self.row_table)
        for row in rows:
            cells = row.find_elements(*self.table_data_cell)
            if cells and cells[1].text.strip() == role_name:
                return row
        return None

    def get_checkbox_in_row(self, row, checkbox_type='deactive'):
        """
        Return the checkbox WebElement in the given row for deactivation or activation.
        checkbox_type: 'deactive' or 'active'
        """
        # Example: assume checkboxes are input elements with name or type attribute.
        # Adjust the XPath / attributes based on actual HTML.
        if checkbox_type == 'deactive':
            return row.find_element(By.XPATH, ".//input[@type='checkbox' or @name='deactive']")
        else:
            return row.find_element(By.XPATH, ".//input[@type='checkbox' or @name='active']")

    def get_err_msg(self):
        return  self.get_text(self.err_msg)



