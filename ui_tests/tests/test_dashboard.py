from playwright.sync_api import expect
from ui_tests.logger import get_logger
import pytest

logger = get_logger()


def test_line_chart_connecting_null_values(credentials,login_page, logged_in_page,page):

    username,password = credentials
    logger.info("Test - Verify connecting Null values on a Line Chart in a Dashboard")
    login_page.login(username, password)
    logger.info("logged in successsfully")

    logged_in_page.verify_current_page("/web/")
    logged_in_page.go_to_dashboards()
    logged_in_page.verify_current_page("/web/dashboards")
    logged_in_page.click_on_new_dashboard()

    #Create a new dashboard
    logged_in_page.enter_dashboard_details("Test_Dashboard", "Test desc")
    logged_in_page.click_save_button()
    logged_in_page.verify_success_message()

    #Adding a panel to the dashboard with line chart
    logged_in_page.add_panel("Test Panel")
    logged_in_page.select_stream_type()
    logged_in_page.select_stream_input()

    # Adding fields to the chart
    logged_in_page.add_elements_to_Y_axis()
    logged_in_page.add_chart_type('line')

    #Connecting Null values
    logged_in_page.go_to_config()
    logged_in_page.select_toggle('Connect null values')
    logged_in_page.click_apply()
    logged_in_page.save_panel()
    page.wait_for_timeout(30000)

    
