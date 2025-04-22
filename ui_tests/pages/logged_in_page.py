import re
from playwright.sync_api import Page
from ui_tests.logger import get_logger
from ui_tests.pages.basepage import BasePage


logger = get_logger()

class LoggedInPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        
        self.dashboards_link = page.locator('a[data-test="menu-link-/dashboards-item"]')
        self.dashboard_heading = page.locator('div.q-table__title')
        self.new_dashboard_button = page.locator('button[data-test="dashboard-add"]')  # New Dashboard button
        self.dashboard_name_input = page.locator('input[data-test="add-dashboard-name"]')  # Name input field
        self.dashboard_description_input = page.locator('input[data-test="add-dashboard-description"]')  # Description input field
        self.save_button = page.locator('button[data-test="dashboard-add-submit"]')  # Save button
        self.success_message_locator = page.locator('div.q-notification__message')  # Success message locator
        self.add_dashboard_panel_locator_elem = "//span[text()='Add Panel']/../.."       
        self.stream_type_dropdown_elem = 'input[aria-label="Stream Type"]'
        self.stream_input_dropdown_elem = 'input[data-test="index-dropdown-stream"]'
        self.stream_type_logs = '//div[@class="q-item__label"]/span[text()="logs"]'
        self.stream_input_default = '//div[@class="q-item__label"]/span[text()="default"]'
        self.panel_name = 'input[data-test="dashboard-panel-name"]'
        #Fields
        self.kubernetes_annotations_prometheus_io_path ='//*[contains(@data-test, "field-list-item") and contains(., "kubernetes_annotations_prometheus_io_path")]//button[@data-test="dashboard-add-y-data"]'
        self.code = '//*[contains(@data-test, "field-list-item") and contains(., "code")]//button[@data-test="dashboard-add-y-data"]'
        self.apply_button = 'button[data-test="dashboard-apply"]'
        self.save_buton = 'button[data-test="dashboard-panel-save"]'
        self.line_chart_locator_elem = "//div[@data-test='selected-chart-line-item']"
        self.config_button_locator_elem = "//div[@class='collapsed-title' and text()='Config']"
        self.connect_all_null_toggle_elem = "//div[@data-test='dashboard-config-connect-null-values']"


    def go_to_dashboards(self):        
        self.dashboards_link.click()
        logger.info("Clicked on Dashboards link")
        self.page.wait_for_load_state("load")

    def verify_current_page(self,url="/web/dashboards"):
        self.page.wait_for_timeout(3000)
        self.page.wait_for_load_state("load")
        logger.info("Verifying if we are on the Dashboards page")
        # self.dashboard_heading.wait_for()
        current_url = self.page.url
        expected_url = url # Replace with your actual URL
        assert expected_url in current_url, f"Expected URL '{expected_url}', but got '{current_url}'"
        logger.info(f"Successfully navigated to page with URL: {current_url}")

    def click_on_new_dashboard(self):
        logger.info("Clicking on New Dashboard button")
        self.new_dashboard_button.click()
        logger.info("Clicked on New Dashboard button")

    def enter_dashboard_details(self, name: str, description: str):
        logger.info(f"Entering name: {name} and description: {description} for the new dashboard")
        self.dashboard_name_input.fill(name)  # Fill the name input field
        self.dashboard_description_input.fill(description)  # Fill the description input field

    def click_save_button(self):
        logger.info("Clicking on Save button")
        self.save_button.click()
        logger.info("Clicked on Save button")

    def verify_success_message(self, expected_message: str = "Dashboard added successfully."):
        logger.info(f"Verifying success message: '{expected_message}'")
        self.page.wait_for_timeout(3000)
        # Wait for the success message to appear
        self.success_message_locator.wait_for(state='visible', timeout=5000)  # Wait for up to 5 seconds for the message
        # Assert that the message text matches the expected message
        success_message_text = self.success_message_locator.text_content().strip()
        assert success_message_text == expected_message, f"Expected message '{expected_message}', but got '{success_message_text}'"
        logger.info(f"Success message verified: {success_message_text}")
        self.page.wait_for_timeout(3000)

    
    def add_panel(self,panel_name,page="dashboards/view"):
        # Wait for the frame to load
        frame = self.page.frame(url=re.compile(page))

        # Ensure frame is found
        assert frame is not None, "Dashboard view Frame not found"

        # Wait for the button inside the frame to be visible
        add_panel_button = frame.locator(self.add_dashboard_panel_locator_elem)
        add_panel_button.wait_for(state="visible", timeout=1000)

        # Optionally hover, scroll, then click
        add_panel_button.hover()
        add_panel_button.scroll_into_view_if_needed()
        add_panel_button.click()
        logger.info("Clicked on Add Panel button")        
        self.verify_current_page("web/dashboards/add_panel")
        panel_name_locator = frame.locator(self.panel_name)
        panel_name_locator.fill(panel_name)

    
    def select_stream_type(self, option_text: str = "logs",page="dashboards/add_panel"):
        frame = self.page.frame(url=re.compile(page))
        # Ensure frame is found
        assert frame is not None, "Dashboard view Add panel frame not found"
        stream_type_dropdown = frame.locator(self.stream_type_dropdown_elem)
        option_text = frame.locator(self.stream_type_logs)
        logger.info(f"Clicking on stream type dropdown and selecting '{option_text}'")
        self.select_from_custom_dropdown(stream_type_dropdown,option_text,frame="Present")
       
    
    def select_stream_input(self,option_text: str = "default",page="dashboards/add_panel"):
        frame = self.page.frame(url=re.compile(page))
        # Ensure frame is found
        assert frame is not None, "Dashboard view Add panel frame not found"
        stream_input_dropdown = frame.locator(self.stream_input_dropdown_elem)
        option_text = frame.locator(self.stream_input_default)
        logger.info(f"Clicking on stream input dropdown and selecting '{option_text}'")
        self.select_from_custom_dropdown(stream_input_dropdown,option_text,frame="Present")

    
    def add_elements_to_Y_axis(self, page="dashboards/add_panel"):
        logger.info("Locating frame with URL containing '%s'", page)
        frame = self.page.frame(url=re.compile(page))

        # Ensure frame is found
        assert frame is not None, "Dashboard view Add panel frame not found"
        logger.info("Frame found successfully")

        logger.info("Locating element: kubernetes_annotations_prometheus_io_path")
        kubernetes_annotations_prometheus_io_path = frame.locator(self.kubernetes_annotations_prometheus_io_path)
        kubernetes_annotations_prometheus_io_path.scroll_into_view_if_needed()
        kubernetes_annotations_prometheus_io_path.hover()
        logger.info("Hovering and clicking on kubernetes_annotations_prometheus_io_path")
        kubernetes_annotations_prometheus_io_path.click()

        logger.info("Locating element: code_field")
        code_field = frame.locator(self.code)
        code_field.scroll_into_view_if_needed()
        code_field.hover()
        logger.info("Hovering and clicking on code_field")
        code_field.click()

    def click_apply(self,page='dashboards/add_panel'):
        logger.info("Locating frame with URL containing '%s'", page)
        frame = self.page.frame(url=re.compile(page))
        self.apply_button = frame.locator(self.apply_button)
        self.apply_button.wait_for(timeout=1000)
        self.apply_button.click()
        logger.info("Clicked on Apply button")
    
    def save_panel(self,page='dashboards/add_panel'):
        logger.info("Locating frame with URL containing '%s'", page)
        frame = self.page.frame(url=re.compile(page))
        self.save_buton = frame.locator(self.save_buton)
        self.save_buton.wait_for(timeout=1000)
        self.save_buton.click()
        logger.info("Clicked on Save button")

    def add_chart_type(self,chart_type,page='dashboards/add_panel'):
        logger.info("Locating frame with URL containing '%s'", page)
        frame = self.page.frame(url=re.compile(page))
        if chart_type=='line':
            line_chart = frame.locator(self.line_chart_locator_elem)
        line_chart.click()
        logger.info(f"Added Chart type: {chart_type}")
        
    def select_toggle(self,toggle_name,page='dashboards/add_panel'):
        logger.info("Locating frame with URL containing '%s'", page)
        frame = self.page.frame(url=re.compile(page))
        if toggle_name=='Connect null values':
            connect_null = frame.locator(self.connect_all_null_toggle_elem)
        connect_null.click()
        logger.info(f"Clicked on: {toggle_name}")
    
    def go_to_config(self,page='dashboards/add_panel'):
        logger.info("Locating frame with URL containing '%s'", page)
        frame = self.page.frame(url=re.compile(page))
        config_button_locator_elem = frame.locator(self.config_button_locator_elem)
        config_button_locator_elem.click()
        logger.info(f"Clicked on: Config")




        