
from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class LoginPage(BasePage):

    #Locators
    email_field = (By.XPATH,'//input[@placeholder="Enter your email"]')
    password_field = (By.XPATH,'//input[@placeholder="Enter your password"]')
    signIn_btn = (By.XPATH,'//button[text()="SIGN IN"]')
    error_msg = (By.TAG_NAME,"p")
    logout_drpdwn = (By.XPATH, '//*[@id="root"]/div/nav/div[2]/ul/li[2]')
    logout_btn = (By.XPATH, "(//i[@class='ti-power-off text-primary'])[2]")

    def __init__(self, driver):
        super().__init__(driver)

    def enter_email(self,email):
        self.send_keys(self.email_field,email)

    def enter_password(self,password):
        self.send_keys(self.password_field,password)

    def click_signIn(self):
        self.click(self.signIn_btn)

    def get_error_message(self):
        errorMsg = self.get_text(self.error_msg)
        return errorMsg

    def get_validation_message(self, field):
        return self.driver.execute_script("return arguments[0].validationMessage;", self.driver.find_element(*field))

    def click_logout(self):
        self.click(self.logout_drpdwn)
        self.click(self.logout_btn)

    def get_email_value(self, attribute="value"):
        return self.get_attribute(self.email_field, attribute)

    def clear_email_field(self):
        self.clear_element(self.email_field)

    def get_password_value(self, attribute="value"):
        return self.get_attribute(self.password_field, attribute)

    def clear_password_field(self):
        self.clear_element(self.password_field)


