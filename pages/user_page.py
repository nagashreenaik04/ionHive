from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class UserPage(BasePage):

    #Locators
    user_link = (By.LINK_TEXT, "Manage Users")
    user_page = (By.XPATH, '//h3[text()="Manage User\'s"]')
    user_list_table = (By.XPATH, '//h4[text()="List Of User\'s"]')