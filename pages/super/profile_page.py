
from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class ProfilePage(BasePage):

    #Locators
    profile_link = (By.LINK_TEXT,'Profile')
    profile_heading = (By.XPATH, "//h3[text()='Profile']")
    username_lbl = (By.XPATH, "//label[text()='User Name']")
    email_lbl = (By.XPATH, "//label[text()='Email']")
    phone_lbl = (By.XPATH, "//label[text()='Phone']")
    password_lbl = (By.XPATH, "//label[text()='Password']")
    username_field = (By.XPATH, '//input[@placeholder="Username"]')
    email_field = (By.XPATH, '//input[@placeholder="Email"]')
    phone_field = (By.XPATH, '//input[@placeholder="Phone number"]')
    password_field = (By.XPATH,'//input[@placeholder="Password"]')
    update_btn = (By.XPATH,'//button[text()="Update"]')
    ok_btn = (By.XPATH,'//button[text()="OK"]')

    #succss message
    suc_msg =(By.XPATH, '//h2[text()="Profile updated successfully"]')

    # logout locator
    logout_drpdwn = (By.XPATH, '//*[@id="root"]/div/nav/div[2]/ul/li[2]')
    logout_btn = (By.XPATH, "(//i[@class='ti-power-off text-primary'])[2]")

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_profile_page(self):
        self.click(self.profile_link)

    def get_profile_heading(self):
        return self.find_element(self.profile_heading)

    def get_username_lbl(self):
        return self.find_element(self.username_lbl)

    def get_email_lbl(self):
        return self.find_element(self.email_lbl)

    def get_phone_lbl(self):
        return self.find_element(self.phone_lbl)

    def get_password_lbl(self):
        return self.find_element(self.password_lbl)

    def update_password(self,password):
        self.clear_element(self.password_field)
        self.send_keys(self.password_field,password)

    def click_update(self):
        self.click(self.update_btn)

    def click_okBtn(self):
        self.click(self.ok_btn)

    def verify_all_profile_elements_present(self):
        return {
            "profile_heading": self.is_element_present(self.profile_heading),
            "username_label": self.is_element_present(self.username_lbl),
            "email_label": self.is_element_present(self.email_lbl),
            "phone_label": self.is_element_present(self.phone_lbl),
            "password_label": self.is_element_present(self.password_lbl),
            "username_field": self.is_element_present(self.username_field),
            "email_field": self.is_element_present(self.email_field),
            "phone_field": self.is_element_present(self.phone_field),
            "password_field": self.is_element_present(self.password_field),
            "update_button": self.is_element_present(self.update_btn),
        }

    def click_logout(self):
        self.click(self.logout_drpdwn)
        self.click(self.logout_btn)

    def is_field_readonly(self, locator):
        element = self.find_element(locator)
        readonly = element.get_attribute("readonly")
        return readonly is not None

    def get_suc_msg(self):
        success_msg = self.find_element(self.suc_msg).text.strip()
        return success_msg

    def click_ok_btn(self):
        self.click(self.ok_btn)
