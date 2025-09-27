import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome", help="Specify the browser: chrome, edge, or firefox"
    )

@pytest.fixture(scope="class")
def driver(request):
    browser_name = request.config.getoption("browser_name").lower()

    if browser_name == "firefox":
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service)
    elif browser_name == "edge":
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service)
    else:
        # Default to Chrome for 'chrome' or any invalid/unspecified browser
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

    driver.maximize_window()  # Maximize browser window
    yield driver  # Provide driver to tests
    driver.quit()  # Cleanup after tests