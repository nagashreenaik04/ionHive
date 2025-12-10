
from pages.base_page import BasePage
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By

class DeviceReportPage(BasePage):
    #Locators
    manage_report_drpdwn = (By.XPATH, "//span[text()='Manage Report']")
    device_report_link = (By.LINK_TEXT, "Device Report")
    device_report_page = (By.XPATH, "//h3[text()='Device Report']")

    from_date_field = (By.XPATH, "(//label[text()='From Date']//following::input)[1]")
    to_date_field = (By.XPATH, "//label[text()='To Date']//following::input")
    select_device_drpdwn = (By.XPATH, "//select[@name='selectField']")
    search_btn = (By.XPATH, "//button[contains(text(),'Search')]")
    export_btn = (By.XPATH, "//button[contains(text(),'Export')]")
    print_btn = (By.XPATH, "//button[contains(text(),'Print')]")

    # List of Device Report table
    device_report_table = (By.XPATH, "//table[@class='table table-striped']")
    table_header = (By.TAG_NAME, "thead")
    table_header_cell = (By.TAG_NAME, "th")
    row_table = (By.XPATH, ".//tbody/tr")
    table_data_cell = (By.TAG_NAME, "td")

    # logout locator
    logout_drpdwn = (By.XPATH, '//*[@id="root"]/div/nav/div[2]/ul/li[2]')
    logout_btn = (By.XPATH, "(//i[@class='ti-power-off text-primary'])[2]")

    def __init__(self, driver):
        super().__init__(driver)

    def click_manage_report(self):
        self.click(self.manage_report_drpdwn)

    def navigate_to_device_report(self):
        self.click(self.device_report_link)

    def get_device_report_heading(self):
        return self.find_element(self.device_report_page).text

    def click_logout(self):
        self.click(self.logout_drpdwn)
        self.click(self.logout_btn)

