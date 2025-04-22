# ui_tests/conftest.py
import pytest
from playwright.sync_api import sync_playwright
from ui_tests.pages.logged_in_page import LoggedInPage
from ui_tests.pages.login_page import LoginPage
import os,json

@pytest.fixture(scope="session")
def credentials():
    """
    Loads login credentials from credentials.json.
    Shared across all tests in the session.
    """
    creds_path = os.path.join(os.path.dirname(__file__),'credentials.json')
    if not os.path.exists(creds_path):
        raise FileNotFoundError(f"Credentials file not found at {creds_path}")
    with open(creds_path) as f:
        data = json.load(f)
    return data["username"], data["password"]

def pytest_addoption(parser):
    parser.addoption(
        "--headless", action="store", default="true", help="Run browser in headless mode: true/false"
    )

@pytest.fixture(scope="session", autouse=True)
def browser(pytestconfig):
    headless_option = pytestconfig.getoption("headless").lower() == "true"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless_option)
        yield browser
        browser.close()
        
@pytest.fixture
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    page.set_viewport_size({"width": 1920, "height": 1080})
    page.goto("http://localhost:5080/web/login")  # Change to actual URL
    yield page
    

@pytest.fixture
def login_page(page):
    return LoginPage(page)

@pytest.fixture
def logged_in_page(page):
    return LoggedInPage(page)