import time
import random
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumbase import Driver
from selenium.common.exceptions import TimeoutException, WebDriverException
from dotenv import load_dotenv

# Load environment variables from a .env file for local development
load_dotenv()

# --- Configuration ---
BASE_URL = "https://www.clashchamps.com/i-need-a-base/"
ACCOUNTS = [
    {"username": os.getenv("ACCOUNT_1_USER"), "password": os.getenv("ACCOUNT_1_PASS")},
    {"username": os.getenv("ACCOUNT_2_USER"), "password": os.getenv("ACCOUNT_2_PASS")},
    {"username": os.getenv("ACCOUNT_3_USER"), "password": os.getenv("ACCOUNT_3_PASS")},
    {"username": os.getenv("ACCOUNT_4_USER"), "password": os.getenv("ACCOUNT_4_PASS")},
    {"username": os.getenv("ACCOUNT_5_USER"), "password": os.getenv("ACCOUNT_5_PASS")},
    {"username": os.getenv("ACCOUNT_6_USER"), "password": os.getenv("ACCOUNT_6_PASS")},
    {"username": os.getenv("ACCOUNT_7_USER"), "password": os.getenv("ACCOUNT_7_PASS")},
    {"username": os.getenv("ACCOUNT_8_USER"), "password": os.getenv("ACCOUNT_8_PASS")},
    {"username": os.getenv("ACCOUNT_9_USER"), "password": os.getenv("ACCOUNT_9_PASS")},
    {"username": os.getenv("ACCOUNT_10_USER"), "password": os.getenv("ACCOUNT_10_PASS")},
    {"username": os.getenv("ACCOUNT_11_USER"), "password": os.getenv("ACCOUNT_11_PASS")},
    {"username": os.getenv("ACCOUNT_12_USER"), "password": os.getenv("ACCOUNT_12_PASS")},
    {"username": os.getenv("ACCOUNT_13_USER"), "password": os.getenv("ACCOUNT_13_PASS")},
    {"username": os.getenv("ACCOUNT_14_USER"), "password": os.getenv("ACCOUNT_14_PASS")},
    {"username": os.getenv("ACCOUNT_15_USER"), "password": os.getenv("ACCOUNT_15_PASS")},
    {"username": os.getenv("ACCOUNT_16_USER"), "password": os.getenv("ACCOUNT_16_PASS")},
    {"username": os.getenv("ACCOUNT_17_USER"), "password": os.getenv("ACCOUNT_17_PASS")},
    {"username": os.getenv("ACCOUNT_18_USER"), "password": os.getenv("ACCOUNT_18_PASS")},
    {"username": os.getenv("ACCOUNT_19_USER"), "password": os.getenv("ACCOUNT_19_PASS")},
    {"username": os.getenv("ACCOUNT_20_USER"), "password": os.getenv("ACCOUNT_20_PASS")},
]

# --- Functions ---
def login(driver, username, password):
    """Logs into the website and verifies success."""
    print(f"Attempting to log in as {username}...")
    try:
        driver.uc_open_with_reconnect("https://www.clashchamps.com/my-account/", 4)

        print("Page loaded. Entering credentials...")
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "username")))
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.NAME, "login").click()

        # Verify login by checking for the "My Account" menu item.
        print("Verifying login success...")
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "menu-item-3650"))
        )
        print("Login successful and verified.")
        return True
    except TimeoutException:
        print("Login failed. Could not verify login success or the page timed out.")
        driver.save_screenshot("login_error.png")
        print("A screenshot of the login error was saved as 'login_error.png'")
        return False
    except Exception as e:
        print(f"An unexpected error occurred during login: {e}")
        driver.save_screenshot("login_error.png")
        return False

def download_first_base(driver):
    """Navigates to the base page and attempts to initiate a download."""
    print("\nNavigating to the base download page...")
    driver.get(BASE_URL)

    try:
        print("Looking for the first 'DOWNLOAD' button...")
        download_button_selector = (By.CSS_SELECTOR, ".baseItem_footer .btn_primary")

        download_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(download_button_selector)
        )
        print("Found the DOWNLOAD button. Clicking it...")
        driver.execute_script("arguments[0].click();", download_button)
        print("Clicked the DOWNLOAD button via JavaScript.")

        # Handle optional pop-up
        try:
            print("Checking for the confirmation pop-up (will wait up to 5 seconds)...")
            ok_button_selector = (By.CSS_SELECTOR, "#modalSupport_Download button.wantSupport")
            ok_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(ok_button_selector)
            )
            print("Pop-up found! Clicking the 'Ok' button.")
            ok_button.click()
            print("Successfully clicked 'Ok' in the pop-up.")
        except TimeoutException:
            print("Pop-up did not appear. This is okay. Continuing...")
            pass

        print("Download process initiated successfully.")
        time.sleep(2)
        return True

    except TimeoutException:
        print("\n--- ERROR ---")
        print("Script timed out waiting for an element on the base page.")
        print("This usually means the page didn't load correctly or the element could not be found.")
        driver.save_screenshot("error_screenshot.png")
        print("A screenshot of the error has been saved as 'error_screenshot.png'")
        print("-------------\n")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        driver.save_screenshot("error_screenshot.png")
        return False

# --- Main Execution Logic ---
def process_accounts():
    """Loops through accounts and performs the download task."""
    for account in ACCOUNTS:
        username = account["username"]
        password = account["password"]

        # Skip invalid accounts
        if not username or not password:
            print(f"⚠️ Skipping account - missing username or password in env vars.")
            continue

        print("=" * 50)
        print(f"Processing account: {username}")

        driver = None
        try:
            driver = Driver(uc=True, headless=True)  # Keep headless for cloud
            if login(driver, username, password):
                if download_first_base(driver):
                    print(f"\n✅ Task completed for {username}.")
                else:
                    print(f"\n❌ Task failed for {username}.")
            else:
                print(f"🚫 Could not proceed with task for {username} due to login failure.")

        except (WebDriverException, ConnectionRefusedError) as e:
            print(f"A browser or connection error occurred: {e}")
            print("Please ensure your internet connection is stable.")
        except Exception as e:
            print(f"A critical script error occurred: {e}")
        finally:
            if driver:
                print("Closing the browser for this account.")
                driver.quit()

        # Add random delay before next account
        delay = random.uniform(5, 12)
        print(f"⏳ Waiting {delay:.1f} seconds before next account...\n")
        time.sleep(delay)

# --- Entry Point ---
if __name__ == "__main__":
    print("🚀 Script starting process...")
    process_accounts()
    print("✅ All accounts processed. Script finished.")
