from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class ChargerPage(BasePage):

    #Locators
    device_drpdwn = (By.XPATH, "//span[text()='Manage Device']")
    unallocated_charger_link = (By.LINK_TEXT, "Unallocated Chargers")
    unallocated_page = (By.XPATH, '//h3[text()="Manage Device-Unallocated"]')
    unalloacted_charger_list_table = (By.XPATH, '//h4[text()="List Of Chargers"]')
    create_btn = (By.XPATH, '//button[text()="Create"]')
    assign_to_rslr = (By.XPATH, '//button[text()="Assign to Reseller"]')
    uploadDeviceCreate_btn = (By.XPATH, '//button[text()="Upload Device Create"]')
    assing_btn = (By.XPATH, '//button[text()="Assign"]')
    view_btn = (By.XPATH, '//button[text()="View"]')


    #allocated Chrager
    allocated_charger_link = (By.LINK_TEXT, "Allocated Chargers")
    allocated_page = (By.XPATH, '//h3[text()="Manage Devices - Allocated"]')
    reassign_btn = (By.XPATH, '//button[text()="Re-Assign"]')
    allocated_device_list_table = (By.XPATH, '//h4[text()="List Of Devices"]')

    #Create Charger
    add_device_heading = (By.XPATH, '//h3[text()="Add Manage Device"]')
    chargerID_field = (By.XPATH, '//input[@placeholder="Charger ID"]')
    vendor_field = (By.XPATH, '//input[@placeholder="Vendor"]')
    maxCurrent_field = (By.XPATH, '//input[@placeholder="Max Current"]')
    maxPower_field = (By.XPATH, '//input[@placeholder="Max Power"]')
    chargerModel_drpdwn = (By.XPATH, '(//label[text()="Charger Model"]/following::select)[1]')
    chargerType_drpdwn = (By.XPATH, '(//label[text()="Charger Type"]/following::select)[1]')
    wifiModule_drpdwn = (By.XPATH, '(//label[text()="WiFi Module"]/following::select)[1]')
    bluetooth_drpdwn = (By.XPATH, '(//label[text()="Bluetooth Module"]/following::select)[1]')
    connectorType_drpdwn = (By.XPATH, '(//label[text()="Connector Type"]/following::select)[1]')
    typeName_drpdwn = (By.XPATH, '(//label[text()="Type Name"]/following::select)[1]')
    delete_icon = (By.XPATH, '//i[@class="mdi mdi-delete"]')
    add_icon = (By.XPATH, '//i[@class="mdi mdi-plus"]')
    add_btn = (By.XPATH, '//button[text() = "Add"]')
    selectClone_btn = (By.XPATH, '//button[text() = "Select Clone"]')
    back_btn = (By.XPATH, '//button[text() = "Back"]')

    #messages
    create_suc_msg = (By.XPATH, "//h2[text()= 'Charger added successfully']")
    ok_btn = (By.XPATH, "//button[text()= 'OK']")

    #logout locator
    logout_drpdwn = (By.XPATH, '//*[@id="root"]/div/nav/div[2]/ul/li[2]')
    logout_btn = (By.XPATH, "(//i[@class='ti-power-off text-primary'])[2]")

    # List of chargers table
    charger_table = (By.XPATH, "//table[@class='table table-striped']")
    table_header = (By.TAG_NAME, "thead")
    table_header_cell = (By.TAG_NAME, "th")
    row_table = (By.XPATH, ".//tbody/tr")
    table_data_cell = (By.TAG_NAME, "td")
    status_span = (By.TAG_NAME, "span")
    active_label = (By.XPATH, ".//label[@class='active']")


    def click_device_drpdwn(self):
        self.click(self.device_drpdwn)

    def navigate_allocated_charger(self):
        self.click(self.allocated_charger_link)

    def navigate_unallocated_charger(self):
        self.click(self.unallocated_charger_link)

    def get_unallocated_heading(self):
        return self.find_element(self.unallocated_page).text

    def get_unallocated_charger_list_table(self):
        return self.find_element(self.unalloacted_charger_list_table).text

    def click_create_btn(self):
        self.click(self.create_btn)

    def click_assign_to_rslr_btn(self):
        self.click(self.assign_to_rslr)

    def click_uploadDeviceCreate_btn(self):
        self.click(self.uploadDeviceCreate_btn)

    def get_allocated_heading(self):
        return self.find_element(self.allocated_page).text

    def get_allocated_charger_list_table(self):
        return self.find_element(self.allocated_device_list_table).text

    def get_add_device_heading(self):
        return self.find_element(self.add_device_heading).text

    def enter_chargerID(self,chargerID):
        self.send_keys(self.chargerID_field, chargerID)

    def enter_vendor(self, vendor):
        self.send_keys(self.vendor_field, vendor)

    def enter_maxCurrent(self, maxCurrent):
        self.send_keys(self.maxCurrent_field, maxCurrent)

    def enter_maxPower(self, maxPower):
        self.send_keys(self.maxPower_field, maxPower)

    def enter_chargerModel(self, chargerModel):
        self.webelement_selectFromDropdown(self.chargerModel_drpdwn, chargerModel)

    def enter_chargerType(self, chargerType):
        self.webelement_selectFromDropdown(self.chargerType_drpdwn, chargerType)

    def enter_wifiModule(self, wifiModule):
        self.webelement_selectFromDropdown(self.wifiModule_drpdwn, wifiModule)

    def enter_bluetoothModule(self, bluetoothModule):
        self.webelement_selectFromDropdown(self.bluetooth_drpdwn, bluetoothModule)

    def enter_connectorType(self, connectorType):
        self.webelement_selectFromDropdown(self.connectorType_drpdwn, connectorType)

    def enter_typeName(self, typeName):
        self.webelement_selectFromDropdown(self.typeName_drpdwn, typeName)

    def click_add_btn(self):
        self.click(self.add_btn)

    def get_all_options_in_type_name(self):
         return self.get_all_options_from_dropdown(self.typeName_drpdwn)

    def get_create_suc_msg(self):
        return self.find_element(self.create_suc_msg).text

    def click_ok_btn(self):
        self.click(self.ok_btn)

    def click_logout(self):
        self.click(self.logout_drpdwn)
        self.click(self.logout_btn)

    def get_table_data(self):
        """Retrieve all data from the Charger table as a list of dictionaries."""
        # Wait for the table to be visible
        self.wait_for_element(self.charger_table)

        # Locate the table
        table = self.find_element(self.charger_table)

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
        self.wait_for_element(self.charger_table)
        rows = self.find_element(self.charger_table).find_elements(*self.row_table)

        for row in rows:
            if reseller_email in row.text:
                view_btn = row.find_element(By.XPATH, ".//button[contains(text(),'View')]")
                view_btn.click()
                return True

        raise ValueError(f"View button for reseller '{reseller_email}' not found")








