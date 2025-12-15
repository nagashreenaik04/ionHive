from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class UserPage(BasePage):

    #Locators
    user_link = (By.LINK_TEXT, "Manage Users")
    user_page = (By.XPATH, '//h3[text()="Manage User\'s"]')
    user_list_table = (By.XPATH, '//h4[text()="List Of User\'s"]')

    #Add User
    add_user_heading = (By.XPATH, '//h4[text()="Add User\'s"]')
    add_user_btn = (By.XPATH, '//button[text()="Add User\'s"]')
    role_name = (By.XPATH,'//span[text()="Role Name"]/following::select')
    user_name = (By.XPATH, '(//span[text()="User Name"]/following::input)[1]')
    email = (By.XPATH, '(//span[text()="Email ID"]/following::input)[1]')
    phone = (By.XPATH, '(//span[text()="Phone"]/following::input)[1]')
    password = (By.XPATH, '(//span[text()="Password"]/following::input)[1]')
    add_btn = (By.XPATH, "//button[text()='Add']")
    close_icon = (By.XPATH, "//span[text()='×']")


    #search
    search_field = (By.XPATH, '//input[@placeholder="Search now"]')

    view_btn = (By.XPATH, ".//button[contains(text(),'View')]")


    # List of User table
    user_table = (By.XPATH, "//table[@class='table table-striped']")
    table_header = (By.TAG_NAME, "thead")
    table_header_cell = (By.TAG_NAME, "th")
    row_table = (By.XPATH, ".//tbody/tr")
    table_data_cell = (By.TAG_NAME, "td")
    status_span = (By.TAG_NAME, "span")
    active_label = (By.XPATH, ".//label[@class='active']")

    #User Details locator
    user_dtls_heading = (By.XPATH, "//h4[text()='User Details']")
    user_name_dtls = (By.XPATH, "//div[contains(text(),'User Name:')]")
    email_dtls = (By.XPATH, "//strong[contains(text(),'Email Id:')]")
    phone_dtls = (By.XPATH, "//div[contains(text(),'Phone Number:')]")
    password_dtls = (By.XPATH, "//div[contains(text(),'Password:')]")
    rolename_dlts = (By.XPATH, "//div[contains(text(),'Role Name:')]")
    assigned_reseller_dtls = (By.XPATH, "//div[contains(text(),'Assigned Reseller Name:')]")
    assigned_client_dtls = (By.XPATH, "//div[contains(text(),'Assigned Client Name:')]")
    assigned_association_dtls = (By.XPATH, "//div[contains(text(),'Assigned Association Name:')]")
    created_by = (By.XPATH, "//div[contains(text(),'Created By:')]")
    created_date = (By.XPATH, "//div[contains(text(),'Created Date:')]")
    modified_by = (By.XPATH, "//div[contains(text(),'Modified By:')]")
    modified_date = (By.XPATH, "//div[contains(text(),'Modified Date:')]")
    status_dtls = (By.XPATH, "//div[contains(text(),'Status:')]")
    user_name_vlu = (By.XPATH,"(//div[contains(text(),'User Name:')]//following::span)[1]")
    email_vlu = (By.XPATH, "(//strong[contains(text(),'Email Id:')]//following::span)[1]")
    phone_vlu = (By.XPATH, "(//div[contains(text(),'Phone Number:')]//following::span)[1]")
    password_vlu = (By.XPATH, "(//div[contains(text(),'Password:')]//following::span)[1]")
    rolename_vlu = (By.XPATH, "(//div[contains(text(),'Role Name:')]//following::span)[1]")
    assigned_reseller_vlu = (By.XPATH, "(//div[contains(text(),'Assigned Reseller Name:')]//following::span)[1]")
    assigned_client_vlu = (By.XPATH, "(//div[contains(text(),'Assigned Client Name:')]//following::span)[1]")
    assigned_association_vlu = (By.XPATH, "(//div[contains(text(),'Assigned Association Name:')]//following::span)[1]")
    created_by_vlu = (By.XPATH, "(//div[contains(text(),'Created By:')]//following::span)[1]")
    created_date_vlu = (By.XPATH, "(//div[contains(text(),'Created Date:')]//following::span)[1]")
    modified_by_vlu = (By.XPATH, "(//div[contains(text(),'Modified By:')]//following::span)[1]")
    modified_date_vlu = (By.XPATH, "(//div[contains(text(),'Modified Date:')]//following::span)[1]")
    status_dtls_vlu = (By.XPATH, "(//div[contains(text(),'Status:')]//following::span)[1]")

    #Edit
    edit_btn = (By.XPATH, "//button[text()='Edit']")
    edit_user_heading = (By.XPATH, "//h3[text()='Edit User List']")
    username_lbl= (By.XPATH, "//label[text()='User Name']")
    phone_lbl = (By.XPATH, "//label[text()='Phone Number']")
    status_lbl = (By.XPATH, "//label[text()='Status']")
    email_lbl = (By.XPATH, "//label[text()='Email ID']")
    password_lbl = (By.XPATH, "//label[text()='Password']")
    username_inp = (By.XPATH, "(//label[text()='User Name']//following::input)[1]")
    phone_inp = (By.XPATH, "(//label[text()='Phone Number']//following::input)[1]")
    email_inp = (By.XPATH, "(//label[text()='Email ID']//following::input)[1]")
    password_inp = (By.XPATH, "(//label[text()='Password']//following::input)[1]")
    status_inp = (By.XPATH, "//label[text()='Status']//following::select")
    update_btn = (By.XPATH, "//button[text()='Update']")

    #add message
    add_suc_msg = (By.XPATH, "//h2[text()='User added successfully']")
    already_existed_err_msg = (By.XPATH, "//div[text()='This email is already registered under the same role']")

    #edit success
    edit_suc_msg = (By.XPATH, "//h2[text()='User updated successfully']")
    ok_btn = (By.XPATH, "//button[text()='OK']")

    # logout locator
    logout_drpdwn = (By.XPATH, '//*[@id="root"]/div/nav/div[2]/ul/li[2]')
    logout_btn = (By.XPATH, "(//i[@class='ti-power-off text-primary'])[2]")

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_user_page(self):
        self.click(self.user_link)

    def click_okBtn(self):
        self.click(self.ok_btn)

    def click_logout(self):
        self.click(self.logout_drpdwn)
        self.click(self.logout_btn)

    def serch(self,search_data):
        self.send_keys(self.search_field,search_data)

    def get_first_row_data(self):
        """Return list of values for first user row."""
        first_row = self.find_elements(self.row_table)[0]
        cells = first_row.find_elements(By.TAG_NAME, "td")
        return [cell.text.strip() for cell in cells]

    def get_row_data(self, row_number):
        """Return list of values for any user row (1-based row_number)."""
        row = self.find_elements(self.row_table)[row_number - 1]  # subtract 1 for 0-based index
        cells = row.find_elements(By.TAG_NAME, "td")
        return [cell.text.strip() for cell in cells]

    def click_view_btn_first_row(self):
        """Click View button of first row"""
        first_row = self.find_elements(self.row_table)[0]
        btn = first_row.find_element(By.XPATH, ".//button[contains(text(),'View')]")
        btn.click()

    def click_edit_btn(self):
        self.click(self.edit_btn)

    def click_update_btn(self):
        self.click(self.update_btn)

    def edit_phone_field(self,phone):
        self.clear_element(self.phone_inp)
        self.send_keys(self.phone_inp,phone)

    def edit_password_field(self,password):
        self.clear_element(self.password_inp)
        self.send_keys(self.password_inp,password)

    def select_status(self,status):
        self.webelement_selectFromDropdown(self.status_inp,status)

    def get_add_suc_msg(self):
        return self.find_element(self.add_suc_msg).text

    def get_edit_suc_msg(self):
        return self.find_element(self.edit_suc_msg).text

    def click_add_user_btn(self):
        self.click(self.add_user_btn)

    def select_role_name(self,roleName):
        self.webelement_selectFromDropdown(self.role_name,roleName)

    def enter_user_name(self,userName):
        self.send_keys(self.user_name,userName)

    def enter_email(self,email):
        self.send_keys(self.email,email)

    def enter_phone(self,phone):
        self.send_keys(self.phone,phone)

    def enter_password(self,password):
        self.send_keys(self.password,password)

    def click_add_btn(self):
        self.click(self.add_btn)

    def click_close_btn(self):
        self.click(self.close_icon)

    def get_add_user_heading(self):
        return self.find_element(self.add_user_heading).text

    def get_table_row_data(self, row_number):
        """
        Returns the FULL text of the given row number from the reseller table.
        Example: row 4 → returns full text of that row.
        """
        # Wait for the table
        self.wait_for_element(self.user_table)

        # Build row XPath using relative locator inside the table
        row_xpath = f"(//table[@class='table table-striped']//tbody//tr)[{row_number}]"

        row = self.driver.find_element(By.XPATH, row_xpath)
        return row.text.strip()

    def scroll_to_user_row(self, row_number):
        row = self.driver.find_element(
            By.XPATH, f"(//table//tbody/tr)[{row_number}]"
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", row
        )

    def get_alr_exst_err_msg(self):
        return self.find_element(self.already_existed_err_msg).text







