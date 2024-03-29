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


def fetch_all_users():
    csv_file = "userCSVs\Ai_users.csv"
    data = []
    with open(csv_file, "r", newline="") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(row["username"])
    return data


def get_user_post_details(driver):
    user_details = []
    users = fetch_all_users()
    url = f"https://www.tiktok.com/@{users[0]}"
    driver.get(url)
    try:
        driver = continue_as_guest(driver)
    except:
        pass
    print(len(users))
    for user in users:
        url = f"https://www.tiktok.com/@{user}"
        print(f"Scraping user: {user}")
        driver.get(url)
        try:
            nickname = driver.find_element(
                "css selector", "[data-e2e='user-subtitle']"
            ).text
        except Exception as e:
            nickname = "N/A"

        try:
            signature = driver.find_element(
                "css selector", "[data-e2e='user-bio']"
            ).text
        except Exception as e:
            signature = "N/A"

        try:
            followingCount = driver.find_element(
                "css selector", "[data-e2e='following-count']"
            ).text
        except Exception as e:
            followingCount = "N/A"

        try:
            followerCount = driver.find_element(
                "css selector", "[data-e2e='followers-count']"
            ).text
        except Exception as e:
            followerCount = "N/A"

        try:
            heartCount = driver.find_element(
                "css selector", "[data-e2e='likes-count']"
            ).text
        except Exception as e:
            heartCount = "N/A"

        try:
            avatarThumb = driver.find_element(By.CLASS_NAME, "css-1zpj2q-ImgAvatar")
            avatarThumb = avatarThumb.get_attribute("src")
        except Exception as e:
            avatarThumb = "N/A"

        try:
            youtube_channel_id = driver.find_element(
                "css selector", "[data-e2e='user-link']"
            )
            youtube_channel_id = youtube_channel_id.get_attribute("href")
        except Exception as e:
            youtube_channel_id = "N/A"

        user_detail = {
            "profile_URL":url,
            "UniqueID": user,
            "nickname": nickname,
            "avatarThumb": avatarThumb,
            "avatarMedium": avatarThumb,
            "avatarLarger": avatarThumb,
            "signature ": signature,
            "verified ": False,
            "secret": False,
            "ftc": False,
            "relation": 0,
            "openFavorite": False,
            "commentSetting": "None",
            "duetSetting": "None",
            "stitchSetting": "None",
            "privateAccount": False,
            "isADVirtual": False,
            "isUnderAge18": False,
            "insta_id": "N/A",
            "twitter_id": "N/A",
            "youtube_channel_title": youtube_channel_id,
            "youtube_channel_id": youtube_channel_id,
            "followingCount": followingCount,
            "followerCount": followerCount,
            "heartCount": heartCount,
            "diggCount": 0,
            "heart": heartCount,
        }
        user_details.append(user_detail)
    return user_details


def get_tiktok_user():
    try:
        driver = configure_undetected_chrome_driver(True)
        driver.maximize_window()
        try:
            # driver.get(url)
            user_porofiles = get_user_post_details(driver)
            if user_porofiles:
                write_to_csv(user_porofiles, "userCSVs", f"Ai_users_data.csv")
                # data.extend(user_posts)
        except Exception as e:
            print(f"Error : {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


get_tiktok_user()
