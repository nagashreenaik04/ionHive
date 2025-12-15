from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class ResellerPage(BasePage):

    #Locators
    reseller_link = (By.LINK_TEXT, "Manage Reseller")
    reseller_page = (By.XPATH, '//h3[text()="Manage Reseller"]')
    reseller_list_table = (By.XPATH, '//h4[text()="List Of Reseller"]')
    create_btn = (By.XPATH, '//button[text()="Create"]')

    add_res_page = (By.XPATH, '//h3[text()="Add Manage Reseller"]')
    back_btn = (By.XPATH, '//button[text()="Back"]')
    add_btn = (By.XPATH, '//button[text()="Add"]')
    ok_btn = (By.XPATH, '//button[text()="OK"]')

    reseller_name = (By.XPATH, '//input[@placeholder="Reseller Name"]')
    reseller_phone = (By.XPATH, '//input[@placeholder="Phone Number"]')
    reseller_email = (By.XPATH, '//input[@placeholder="Email ID"]')
    reseller_address = (By.XPATH, '//input[@placeholder="Address"]')

    # List of Reseller table
    reseller_table = (By.XPATH, "//table[@class='table table-striped']")
    table_header = (By.TAG_NAME, "thead")
    table_header_cell = (By.TAG_NAME, "th")
    row_table = (By.XPATH, ".//tbody/tr")
    table_data_cell = (By.TAG_NAME, "td")
    status_span = (By.TAG_NAME, "span")
    active_label = (By.XPATH, ".//label[@class='active']")

    # logout locator
    logout_drpdwn = (By.XPATH, '//*[@id="root"]/div/nav/div[2]/ul/li[2]')
    logout_btn = (By.XPATH, "(//i[@class='ti-power-off text-primary'])[2]")

    # Messages
    reseller_success_msg = (By.XPATH, '//h2[text()="Reseller added successfully"]')
    reseller_error1_msg = (By.XPATH, '//h2[text()="Error"]')
        #(By.XPATH, '//div[text() ="Email ID and Reseller Name already exists"]')
    #'//div[text() ="Reseller Name already exists"]'
    #'//div[text() ="Email ID already exists"]'
    reseller_error2_msg = (By.XPATH, '(//h2[text()="Error"]/following::div)[1]')

    #View Reseller Details
    res_name_dtls = (By.XPATH, "//div[text()='Reseller Name: ']/span")
    res_phone_dtls = (By.XPATH, "//div[text()='Phone Number:  ']/span")
    res_email_dtls = (By.XPATH, "//div[text()='Email ID: ']/span")
    res_wallet_dtls = (By.XPATH, "//div[text()='Reseller Wallet: ']/span")
    res_address_dtls = (By.XPATH, "//div[text()='Address: ']/span")
    res_createdBy_dtls = (By.XPATH, "//div[text()='Created By: ']/span")
    res_createdDate_dtls = (By.XPATH, "//div[text()='Created Date: ']/span")
    res_modifiedBy_dtls = (By.XPATH, "//div[text()='Modified By: ']/span")
    res_modifiedDate_dtls = (By.XPATH, "//div[text()='Modified Date: ']/span")
    res_status_dtls = (By.XPATH, "//div[text()='Status: ']/span")

    #Edit button
    view_btn = (By.XPATH, "//button[contains(text(),'View')]")
    edit_btn = (By.XPATH, "//button[text()='Edit']")
    reseller_name_inp = (By.XPATH, "(//label[text()='Reseller Name']/following::input)[1]")
    email_inp = (By.XPATH, "(//label[text()='Email ID']/following::input)[1]")
    phone_inp = (By.XPATH, "(//label[text()='Phone Number']/following::input)[1]")
    wallet_inp =  (By.XPATH, "(//label[text()='Wallet']/following::input)[1]")
    address_inp = (By.XPATH, "(//label[text()='Address']/following::input)[1]")
    status_inp = (By.XPATH, "//label[text()='Status']/following::select")
    update_btn = (By.XPATH, "//button[text()='Update']")
    updt_suc_msg = (By.XPATH, "//h2[text()='Reseller updated successfully']")



    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_Reseller(self):
        self.click(self.reseller_link)

    def get_reseller_heading(self):
        return self.find_element(self.reseller_page).text

    def get_reseller_list_table(self):
        return self.find_element(self.reseller_list_table).text

    def get_create_btn(self):
        return self.find_element(self.create_btn).text

    def click_Create_btn(self):
        self.click(self.create_btn)

    def get_add_reseller_heading(self):
        return self.find_element(self.add_res_page).text

    def click_back_btn(self):
        self.click(self.back_btn)

    def click_add_btn(self):
        self.click(self.add_btn)

    def enter_reseller_name(self, resellerName):
        self.send_keys(self.reseller_name, resellerName)

    def enter_reseller_phone(self, resellerPhone):
        self.send_keys(self.reseller_phone, resellerPhone)

    def enter_reseller_email(self, resellerEmail):
        self.send_keys(self.reseller_email, resellerEmail)

    def enter_reseller_address(self, resellerAddress):
        self.send_keys(self.reseller_address, resellerAddress)

    def click_logout(self):
        self.click(self.logout_drpdwn)
        self.click(self.logout_btn)

    def get_reseller_success_msg(self):
        return self.get_text(self.reseller_success_msg)

    def get_reseller_error_msg(self):
        return self.get_text(self.reseller_error2_msg)

    def click_ok_btn(self):
        self.click(self.ok_btn)

    def get_table_data(self):
        """Retrieve all data from the Reseller table as a list of dictionaries."""
        # Wait for the table to be visible
        self.wait_for_element(self.reseller_table)

        # Locate the table
        table = self.find_element(self.reseller_table)

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

    def click_view_btn_in_row(self, reseller_email):
        """
        Find the row matching reseller_email and click its 'View' button.

        :param reseller_name: The reseller's name to match
        :return: True if clicked, raises ValueError otherwise
        """
        # Wait for table before searching
        self.wait_for_element(self.reseller_table)
        rows = self.find_element(self.reseller_table).find_elements(*self.row_table)

        for row in rows:
            if reseller_email in row.text:
                view_btn = row.find_element(By.XPATH, ".//button[contains(text(),'View')]")
                view_btn.click()
                return True

        raise ValueError(f"View button for reseller '{reseller_email}' not found")


    def get_reseller_name_details(self):
        return self.find_element(self.res_name_dtls).text

    def get_reseller_phone_details(self):
        return self.find_element(self.res_phone_dtls).text

    def get_reseller_email_details(self):
        return self.find_element(self.res_email_dtls).text

    def get_reseller_wallet_details(self):
        return self.find_element(self.res_wallet_dtls).text

    def get_reseller_address_details(self):
        return self.find_element(self.res_address_dtls).text

    def get_reseller_createdby_details(self):
        return self.find_element(self.res_createdBy_dtls).text

    def get_reseller_createdDate_details(self):
        return self.find_element(self.res_createdDate_dtls).text

    def get_reseller_modifiedBy_details(self):
        return self.find_element(self.res_modifiedBy_dtls).text

    def get_reseller_modifiedDate_details(self):
        return self.find_element(self.res_modifiedDate_dtls).text

    def get_reseller_status_details(self):
        return self.find_element(self.res_status_dtls).text

    def click_edit_btn(self):
        self.click(self.edit_btn)

    def edit_phone_field(self,phone):
        self.clear_element(self.phone_inp)
        self.send_keys(self.phone_inp,phone)

    def edit_password_field(self,password):
        self.clear_element(self.phone_inp)
        self.send_keys(self.phone_inp,password)

    def edit_reseller_address(self, address):
        self.clear_element(self.address_inp)
        self.send_keys(self.address_inp,address)

    def edit_wallet(self,wallet):
        self.clear_element(self.wallet_inp)
        self.send_keys(self.wallet_inp,wallet)

    def select_status(self, status):
        self.webelement_selectFromDropdown(self.status_inp, status)

    def click_update_btn(self):
        self.click(self.update_btn)

    def get_updat_suc_msg(self):
        return self.find_element(self.updt_suc_msg).text

    def get_table_row_data(self, row_number):
        """
        Returns the FULL text of the given row number from the reseller table.
        Example: row 4 → returns full text of that row.
        """
        # Wait for the table
        self.wait_for_element(self.reseller_table)

        # Build row XPath using relative locator inside the table
        row_xpath = f"(//table[@class='table table-striped']//tbody//tr)[{row_number}]"

        row = self.driver.find_element(By.XPATH, row_xpath)
        return row.text.strip()

    def click_view_btn_row_number(self, row_number):
        """
        Clicks the 'View' button of a specific row number in the reseller table.
        Example: row_number = 4 → clicks the View button in 4th row.
        """
        # Wait for table to be visible
        self.wait_for_element(self.reseller_table)

        # XPath for the View button within the given row
        view_xpath = f"(//table[@class='table table-striped']//tbody//tr[{row_number}]//button[contains(text(),'View')])[1]"

        try:
            view_btn = self.driver.find_element(By.XPATH, view_xpath)
            view_btn.click()
            return True
        except Exception:
            raise ValueError(f"View button not found for row number: {row_number}")





