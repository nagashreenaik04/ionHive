import os
import time

class ScreenshotUtility:
    def __init__(self, driver):
        self.driver = driver
        self.screenshot_dir = './screenshots'
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)

    def capture_screenshot(self, test_name):
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_path = os.path.join(self.screenshot_dir, f"{test_name}_{timestamp}.png")
        self.driver.save_screenshot(screenshot_path)
        return screenshot_path