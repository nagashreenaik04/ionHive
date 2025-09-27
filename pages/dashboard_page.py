from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class DashboardPage(BasePage):

    #Locators
    welcome_msg = (By.XPATH,'//h3[text()="Welcome to "]')

    def __init__(self, driver):
        super().__init__(driver)

    def capture_welcomeMsg(self):
        #return self.get_text(self.welcome_msg)
        welcomeMsg = self.get_text(self.welcome_msg)
        return welcomeMsg

