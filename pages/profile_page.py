
from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class ProfilePage(BasePage):

    #Locators
    profile_link = (By.LINK_TEXT,'Profile')
    password_field = (By.XPATH,'//input[@placeholder="Password"]')
    update_btn = (By.XPATH,'//button[text()="Update"]')
    ok_btn = (By.XPATH,'//button[text()="OK"]')

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_profile_page(self):
        self.click(self.profile_link)

    def update_password(self,password):
        self.clear_element(self.password_field)
        self.send_keys(self.password_field,password)

    def click_update(self):
        self.click(self.update_btn)

    def click_okBtn(self):
        self.click(self.ok_btn)
