# ui_tests/pages/login_page.py
from playwright.sync_api import Page
from ui_tests.logger import get_logger

logger = get_logger()


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.email_input = page.get_by_label("User Email *")
        self.password_input = page.get_by_label("Password *")
        self.login_button = page.get_by_role("button", name="Login")

    def login(self, email: str, password: str):
        
        self.email_input.fill(email)
        logger.info(f"Entered user email: {email} ")
        self.password_input.fill(password)
        logger.info(f"Entered password: {password} ")
        self.login_button.click()
        logger.info("Clicked on Login button")
        self.page.wait_for_load_state("load")
