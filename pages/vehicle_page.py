
from pages.base_page import BasePage
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By

class VehiclePage(BasePage):


    #Locators
    vehicle_link = (By.XPATH, "//span[text()='Vehicle Model']")
    vehicle_page = (By.XPATH, "//h3[text()='Manage Vehicle Models']")
    vehicle_list_table = (By.XPATH, "//h4[text()='List Of Vehicles']")
    addVehicle_btn = (By.XPATH, "(//button[text()='Add Vehicle'])[1]")

    #Add Vehicle
    add_vhcl_heading = (By.XPATH, "//h4[text()='Add Vehicle']")
    model_field = (By.XPATH, '//input[@placeholder="Enter Model"]')
    type_field = (By.XPATH, '//input[@placeholder="Enter Type"]')
    company_field = (By.XPATH, '//input[@placeholder="Enter Vehicle Company"]')
    battery_size_field = (By.XPATH, '//input[@placeholder="Battery Size"]')
    charger_type_field = (By.XPATH, '//input[@placeholder="Enter Charger Type"]')
    upload_image_field = (By.NAME, 'vehicle_image_file')
    add_vehl_btn = (By.XPATH, "(//button[text()='Add Vehicle'])[2]")

    #messages
    suc_msg = (By.XPATH, "//h2[text()='Vehicle model added successfully']")
    ok_btn = (By.XPATH, "//button[text()='OK']")

    # logout locator
    logout_drpdwn = (By.XPATH, '//*[@id="root"]/div/nav/div[2]/ul/li[2]')
    logout_btn = (By.XPATH, "(//i[@class='ti-power-off text-primary'])[2]")

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_vehicle_page(self):
        self.click(self.vehicle_link)

    def get_vehicle_page_heading(self):
        return self.find_element(self.vehicle_page).text

    def get_vehicle_page_list_table(self):
        return self.find_element(self.vehicle_list_table).text

    def click_add_vehicle_btn(self):
        self.click(self.addVehicle_btn)

    def get_add_vehicle_heading(self):
        return self.find_element(self.add_vhcl_heading).text

    def get_add_vehicle_btn(self):
        return self.find_element(self.addVehicle_btn).text

    def enter_model_field(self, modelField):
        self.send_keys(self.model_field,modelField)

    def enter_charger_type_field(self, chargerTypeField):
        self.send_keys(self.charger_type_field,chargerTypeField)

    def enter_upload_image_field(self, uploadImageField):
        self.send_keys(self.upload_image_field,uploadImageField)

    def enter_type_field(self,typeField):
        self.send_keys(self.type_field,typeField)

    def enter_battery_size_field(self,batterySizeField):
        self.send_keys(self.battery_size_field,batterySizeField)

    def enter_company_field(self,companyField):
        self.send_keys(self.company_field,companyField)

    def click_add_btn(self):
        self.click(self.add_vehl_btn)

    def get_suc_msg(self):
        return self.find_element(self.suc_msg).text

    def click_ok_btn(self):
        self.click(self.ok_btn)

    def click_logout(self):
        self.click(self.logout_drpdwn)
        self.click(self.logout_btn)


