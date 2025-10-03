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
    wifiModel_drpdwn = (By.XPATH, '(//label[text()="WiFi Module"]/following::select)[1]')
    bluetooth_drpdwn = (By.XPATH, '(//label[text()="Bluetooth Module"]/following::select)[1]')
    connectorType_drpdwn = (By.XPATH, '(//label[text()="Connector Type"]/following::select)[1]')
    typeName_drpdwn = (By.XPATH, '(//label[text()="Type Name"]/following::select)[1]')
    delete_icon = (By.XPATH, '//i[@class="mdi mdi-delete"]')
    add_icon = (By.XPATH, '//i[@class="mdi mdi-plus"]')
    add_btn = (By.XPATH, '//button[text() = "Add"]')
    selectClone_btn = (By.XPATH, '//button[text() = "Select Clone"]')
    back_btn = (By.XPATH, '//button[text() = "Back"]')


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






