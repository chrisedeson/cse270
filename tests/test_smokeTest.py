import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestSmokeTest():
    def setup_method(self, method):
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_1_logo_header_title(self):
        """Test #1 - Logo Header and Title"""
        self.driver.get("http://127.0.0.1:5500/teton/1.6/index.html")
        # Verify site logo is displayed
        logo = self.driver.find_element(By.CSS_SELECTOR, ".header-logo img")
        assert logo.is_displayed()
        # Verify website heading
        h1 = self.driver.find_element(By.CSS_SELECTOR, ".header-title h1")
        assert h1.text == "Teton Idaho"
        h2 = self.driver.find_element(By.CSS_SELECTOR, ".header-title h2")
        assert h2.text == "Chamber of Commerce"
        # Verify browser tab title
        assert self.driver.title == "Teton Idaho CoC"

    def test_2_home_page_spotlights_and_join(self):
        """Test #2 - Home Page - Spotlights and Join Feature"""
        self.driver.get("http://127.0.0.1:5500/teton/1.6/index.html")
        # Set window size large enough to show full nav
        self.driver.set_window_size(1920, 1080)
        # Wait for spotlights to load (populated via JS fetch)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".main-spotlight .spotlight1")))
        # Verify two spotlights are present
        spotlight1 = self.driver.find_element(By.CSS_SELECTOR, ".main-spotlight .spotlight1")
        assert spotlight1.is_displayed()
        spotlight2 = self.driver.find_element(By.CSS_SELECTOR, ".main-spotlight .spotlight2")
        assert spotlight2.is_displayed()
        # Verify Join Us link is present
        join_link = self.driver.find_element(By.LINK_TEXT, "Join Us!")
        assert join_link.is_displayed()
        # Click Join Us link and verify navigation to join page
        join_link.click()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".join-wizard-main")))
        assert "join.html" in self.driver.current_url

    def test_3_directory_grid_and_list(self):
        """Test #3 - Directory Grid and List feature"""
        self.driver.get("http://127.0.0.1:5500/teton/1.6/directory.html")
        wait = WebDriverWait(self.driver, 10)
        # Wait for business data to load
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#directory-data"), "Teton Turf and Tree"))
        # Click Grid button
        grid_btn = self.driver.find_element(By.ID, "directory-grid")
        grid_btn.click()
        # Verify Teton Turf and Tree is shown in cards
        directory_data = self.driver.find_element(By.ID, "directory-data")
        assert "Teton Turf and Tree" in directory_data.text
        assert "directory-cards" in directory_data.get_attribute("class")
        # Click List button
        list_btn = self.driver.find_element(By.ID, "directory-list")
        list_btn.click()
        # Verify Teton Turf and Tree is still displayed in list view
        directory_data = self.driver.find_element(By.ID, "directory-data")
        assert "Teton Turf and Tree" in directory_data.text
        assert "directory-list" in directory_data.get_attribute("class")

    def test_4_join_page_data_entry(self):
        """Test #4 - Join Page Data Entry"""
        self.driver.get("http://127.0.0.1:5500/teton/1.6/join.html")
        # Verify First Name input is present
        fname = self.driver.find_element(By.NAME, "fname")
        assert fname.is_displayed()
        # Fill in the form
        fname.send_keys("John")
        self.driver.find_element(By.NAME, "lname").send_keys("Doe")
        self.driver.find_element(By.NAME, "bizname").send_keys("Test Business")
        self.driver.find_element(By.NAME, "biztitle").send_keys("Manager")
        # Click Next Step
        self.driver.find_element(By.NAME, "submit").click()
        # Verify Email input is present on step 2
        wait = WebDriverWait(self.driver, 10)
        email_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
        assert email_input.is_displayed()

    def test_5_admin_page_login(self):
        """Test #5 - Admin Page Username/Password"""
        self.driver.get("http://127.0.0.1:5500/teton/1.6/admin.html")
        # Verify Username input is present
        username = self.driver.find_element(By.ID, "username")
        assert username.is_displayed()
        # Fill in incorrect credentials
        username.send_keys("wronguser")
        self.driver.find_element(By.ID, "password").send_keys("wrongpassword")
        # Click Login button
        self.driver.find_element(By.CSS_SELECTOR, ".mysubmit").click()
        # Wait for error message
        wait = WebDriverWait(self.driver, 10)
        error_msg = wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, ".errorMessage"), "Invalid username and password."
        ))
        # Verify error message
        error_element = self.driver.find_element(By.CSS_SELECTOR, ".errorMessage")
        assert error_element.text == "Invalid username and password."
