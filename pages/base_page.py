
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, locator, timeout=50):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def click(self, locator):
        element = self.wait_for_element(locator)
        element.click()

    def send_keys(self, locator, text):
        element = self.wait_for_element(locator)
        element.send_keys(text)

    def get_text(self, locator):
        element = self.wait_for_element(locator)
        return element.text

    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    def find_element(self, locator):
        return self.wait_for_element(locator)

    def webelement_selectFromDropdown(self, locator, text):
        drpSelect = Select(self.wait_for_element(locator))
        drpSelect.select_by_visible_text(text)

    def refresh(self):
        self.driver.refresh()  # Refresh the current page

    def clear_element(self,locator):
        element = self.wait_for_element(locator)
        element.clear()
        #WebDriverWait(self.driver,5).until(EC.visibility_of_element_located(locator)).clear()

    def scroll_up(self):
        #self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def switch_parent_window(self):
        self.driver.switch_to.default_content()

    def get_attribute(self, locator, attribute):
        element = self.wait_for_element(locator)
        return element.get_attribute(attribute) or ""








