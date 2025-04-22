from playwright.sync_api import Page, expect
from ui_tests.logger import get_logger

logger = get_logger()

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def select_from_custom_dropdown(self, input_locator: str, option_text: str,frame=None):
        logger.info(f"Selecting '{option_text}' from dropdown [{input_locator}]")
        if frame is not None:
            input_locator.click()
            option_text.click()
        else:
            self.page.locator(input_locator).click()
            self.page.locator(input_locator).fill(option_text)
            self.page.locator(f"div[role='option'] >> text={option_text}").click()

    def wait_for_url(self, expected_url: str, timeout: int = 5000):
        logger.info(f"Waiting for URL to be: {expected_url}")
        self.page.wait_for_url(expected_url, timeout=timeout)
        assert self.page.url == expected_url, f"Expected URL {expected_url}, but got {self.page.url}"

    def wait_for_success_message(self, message_text: str):
        logger.info(f"Waiting for success message: {message_text}")
        success_msg = self.page.locator(f".q-notification__message:has-text('{message_text}')")
        success_msg.wait_for(state="visible", timeout=5000)
        assert success_msg.is_visible(), f"Success message '{message_text}' not visible."
