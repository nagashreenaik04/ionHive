import pytest
from utilities.custom_logger import LogGen

@pytest.mark.usefixtures("driver")
class TestUser:
    logger = LogGen.loggen()

    def test_user_created_or_not(self, driver):
        # Instantiate the TestReseller class
        reseller_test = TestReseller()

        # Only call the specific method
        reseller_test.test_create_reseller(driver)

        self.logger.info("Successfully called only test_create_reseller from TestReseller")