import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import re
from dateutil import parser
from googletrans import Translator
import pandas as pd
import os


def write_to_excel(data, directory, filename):
    if not os.path.exists(directory):
        os.makedirs(directory)
    filepath = os.path.join(directory, filename)
    df = pd.DataFrame(data)
    df.to_excel(filepath, index=False)


def delete_user(user_to_delete, excel_file):
    df = pd.read_excel(excel_file)
    df = df[df["users"] != user_to_delete]
    df.to_excel(excel_file, index=False)


def fetch_all_users(excel_file):
    data = []
    df = pd.read_excel(excel_file)
    data = df["users"].tolist()
    return data


def parse_date(date_string):
    formatted_date = ''
    try:
        # Regular expressions to match relative date and time terms
        relative_datetime_regex = (
            r"(\d+)\s+(day|week|month|year|hr|hour)s?\s+(ago|from now)"
        )
        match = re.match(relative_datetime_regex, date_string.strip(), re.IGNORECASE)

        if match:
            # Extract the relative time components
            amount = int(match.group(1))
            unit = match.group(2).lower()
            direction = match.group(3).lower()

            # Calculate the relative delta
            delta = None
            if unit in ["day", "hr", "hour"]:
                delta = timedelta(days=amount)
            elif unit == "week":
                delta = timedelta(weeks=amount)
            elif unit == "month":
                delta = timedelta(days=amount * 30)  # Approximate months as 30 days
            elif unit == "year":
                delta = timedelta(days=amount * 365)  # Approximate years as 365 days

            if delta:
                # Calculate the actual date based on direction
                if direction == "ago":
                    parsed_date = datetime.now() - delta
                else:
                    parsed_date = datetime.now() + delta
                formatted_date = (
                    parsed_date.strftime("%d-%b-%y").lstrip("0").replace(" 0", " ")
                )
            else:
                raise ValueError("Error: Invalid relative time unit.")

        else:
            parsed_date = parser.parse(date_string, fuzzy=True)
            formatted_date = (
                parsed_date.strftime("%d-%b-%y").lstrip("0").replace(" 0", " ")
            )

        return formatted_date
    except ValueError as e:
        pass
        # print(str(e))
        # print(date_string)
        # print("Error: Date format is incorrect. Please provide a valid date.")


def parse_value_with_zeros(value_string):
    # Define a dictionary to map units to their multiplier
    units = {
        "K": 10**3,
        "M": 10**6,
        "B": 10**9,
        "T": 10**12,
    }

    # Use regular expressions to extract the numerical value and unit
    match = re.match(r"^(\d+(\.\d+)?)([KMBT])?$", value_string.strip(), re.IGNORECASE)

    if match:
        # Extract the numerical value and unit
        numeric_value = float(match.group(1))
        unit = match.group(3)

        # If the unit exists, multiply the numerical value by the corresponding multiplier
        if unit:
            multiplier = units[unit.upper()]
            numeric_value *= multiplier

        # Convert the numeric value to an integer and return
        return int(numeric_value)
    else:
        return int(0)


def translate_text(text, dest="en"):
    try:
        translator = Translator()
        translated = translator.translate(text, dest=dest)
        return translated.text
    except:
        return text


def configure_webdriver(
    open_browser=False, block_media=False, block_elements=["css", "img", "js"]
):
    options = webdriver.ChromeOptions()

    # Install the extension
    extension_path = "scraper/utils/pia.crx"

    if not open_browser:
        options.add_argument("--headless=new")
    if block_media:
        hide_elements = {
            "plugins": 2,
            "popups": 2,
            "geolocation": 2,
            "notifications": 2,
            "auto_select_certificate": 2,
            "fullscreen": 2,
            "mouselock": 2,
            "mixed_script": 2,
            "media_stream": 2,
            "media_stream_mic": 2,
            "media_stream_camera": 2,
            "protocol_handlers": 2,
            "ppapi_broker": 2,
            "automatic_downloads": 2,
            "midi_sysex": 2,
            "push_messaging": 2,
            "ssl_cert_decisions": 2,
            "metro_switch_to_desktop": 2,
            "protected_media_identifier": 2,
            "app_banner": 2,
            "site_engagement": 2,
            "durable_storage": 2,
        }
        if "cookies" in block_elements:
            hide_elements.update({"cookies": 2})
        if "js" in block_elements:
            hide_elements.update({"javascript": 2})
        if "img" in block_elements:
            hide_elements.update({"images": 2})
        prefs = {"profile.default_content_setting_values": hide_elements}
        options.add_argument("--disable-features=EnableNetworkService")
        options.add_argument("--blink-settings=imagesEnabled=false")
        options.add_experimental_option("prefs", prefs)
    options.add_argument("window-size=1200,1100")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    )

    # options.add_extension(extension_path)

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install())
    )

    if block_media:
        # Enable Chrome DevTools Protocol
        driver.execute_cdp_cmd("Page.enable", {})
        driver.execute_cdp_cmd("Network.enable", {})

        # Set blocked URL patterns to disable images and stylesheets
        blocked_patterns = []
        if "img" in block_elements:
            blocked_patterns.extend(
                [
                    "*.jpg",
                    "*.jpeg",
                    "*.png",
                    "*.gif",
                ]
            )
        if "css" in block_elements:
            blocked_patterns.extend(["*.css"])
        if "js" in block_elements:
            blocked_patterns.extend(["*.js"])
        driver.execute_cdp_cmd("Network.setBlockedURLs", {"urls": blocked_patterns})
    return driver


def configure_undetected_chrome_driver(open_browser=False):
    options = uc.ChromeOptions()
    my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
    # extension_path = 'scraper/utils/extensions/pia-unpacked'
    if not open_browser:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox --no-first-run --no-service-autorun --password-store=basic")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36")
    options.add_experimental_option('prefs', {"extensions.ui.developer_mode": True, })
    options.add_argument('--remote-debugging-port=9222')
    options.add_argument(f"user-agent={my_user_agent}")
    # options.add_argument(f'--load-extension={extension_path}')
    driver = uc.Chrome(driver_executable_path=ChromeDriverManager().install(), options=options, use_subprocess=False)
    return driver
