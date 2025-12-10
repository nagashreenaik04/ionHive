
from pages.base_page import BasePage
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By

class DeviceReportPage(BasePage):
    #Locators
    manage_report_drpdwn = (By.XPATH, "//span[text()='Manage Report']")
    revenue_report_link = (By.LINK_TEXT, "Revenue Report")
    revenue_overview_heading = (By.XPATH, "//h4[text()='Revenue Overview']")
    charging_session_heading = (By.XPATH, "//h4[text()='Charging Session']")

    #revenue overview
    revenue_overview_tbl = (By.XPATH, "(//table[@class='table table-striped'])[1]")
    ro_table_header = (By.XPATH, "(//thead)[1]")
    table_header_cell = (By.TAG_NAME, "th")
    row_table = (By.XPATH, ".//tbody/tr")
    table_data_cell = (By.TAG_NAME, "td")

    #charging session
    charging_session_tbl = (By.XPATH, "(//table[@class='table table-striped'])[2]")
    cs_table_header = (By.XPATH, "(//thead)[2]")

    # logout locator
    logout_drpdwn = (By.XPATH, '//*[@id="root"]/div/nav/div[2]/ul/li[2]')
    logout_btn = (By.XPATH, "(//i[@class='ti-power-off text-primary'])[2]")

    def __init__(self, driver):
        super().__init__(driver)

    def click_manage_report(self):
        self.click(self.manage_report_drpdwn)

    def navigate_to_revenue_report(self):
        self.click(self.revenue_report_link)

    def get_revenue_overview_heading(self):
        return self.find_element(self.revenue_overview_heading).text

    def get_charging_session_heading(self):
        return self.find_element(self.charging_session_heading).text

    def click_logout(self):
        self.click(self.logout_drpdwn)
        self.click(self.logout_btn)

