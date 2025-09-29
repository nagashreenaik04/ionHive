from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class ResellerPage(BasePage):

    #Locators
    reseller_link = (By.LINK_TEXT, "Manage Reseller")
    reseller_page = (By.XPATH, '//h3[text()="Manage Reseller"]')
    reseller_list_table = (By.XPATH, '//h4[text()="List Of Reseller"]')
    addCreate_btn = (By.XPATH, '//button[text()="Create"]')

    add_res_page = (By.XPATH, '//h3[text()="Add Manage Reseller"]')
    back_btn = (By.XPATH, '//button[text()="Back"]')
    add_btn = (By.XPATH, '//button[text()="Add"]')

    reseller_name = (By.XPATH, '//input[@placeholder="Reseller Name"]')
    reseller_phone = (By.XPATH, '//input[@placeholder="Phone Number"]')
    reseller_email = (By.XPATH, '//input[@placeholder="email"]')
    reseller_address = (By.XPATH, '//input[@placeholder="Address"]')

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_Reseller(self):
        self.click(self.reseller_link)

    def get_reseller_heading(self):
        return self.find_element(self.reseller_page).text

    def get_reseller_list_table(self):
        return self.find_element(self.reseller_list_table).text

    def get_addOTC_btn(self):
        return self.find_element(self.addOTC_btn).text

    def click_Create_btn(self):
        self.click(self.addCreate_btn)

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

