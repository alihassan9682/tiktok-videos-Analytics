import time

from helpers import configure_webdriver, configure_undetected_chrome_driver

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import csv
import os


def request_url(driver, url):
    driver.get(url)


def write_to_csv(data, directory, filename):
    fieldnames = list(data[0].keys())
    if not os.path.exists(directory):
        os.makedirs(directory)
    filepath = os.path.join(directory, filename)
    with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            writer.writerow(item)


def continue_as_guest(driver):
    time.sleep(5)
    element = driver.find_elements("css selector", "[data-e2e='channel-item']")
    if element:
        element[-1].click()
    return driver


def load_all_users(driver):
    time.sleep(9)
    previous_len = len(
        driver.find_elements("css selector", "[data-e2e='search-user-unique-id']")
    )
    while True:
        try:
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        except:
            pass
        time.sleep(15)
        elements = driver.find_elements(
            "css selector", "[data-e2e='search-user-unique-id']"
        )
        if previous_len == len(elements) or len(elements) >= 1000:
            ele = [i.text for i in elements]
            return ele
        previous_len = len(elements)


def get_user_post_details(driver):
    user_details = []
    try:
        driver = continue_as_guest(driver)
    except:
        pass
    users = load_all_users(driver)
    print(len(users))
    for user in users:
        user_detail = {
                "username": user,
            }
        user_details.append(user_detail)
    return user_details
    
def get_tiktok_user():
    try:
        driver = configure_undetected_chrome_driver(True)
        driver.maximize_window()
        url = "https://www.tiktok.com/search/user?q=artificial%20intelligence&t=1711741088459"
        try:
            driver.get(url)
            user_porofiles = get_user_post_details(driver)
            if user_porofiles:
                write_to_csv(user_porofiles, "userCSVs", f"Ai_users1.csv")
                # data.extend(user_posts)
        except Exception as e:
            print(f"Error : {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


get_tiktok_user()
