import time

from helpers import (
    configure_webdriver,
    configure_undetected_chrome_driver,
    translate_text,
    parse_date,
    parse_value_with_zeros,
    write_to_excel,
    fetch_all_users,
)

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def request_url(driver, url):
    driver.get(url)


def continue_as_guest(driver):
    time.sleep(5)
    element = driver.find_elements("css selector", "[data-e2e='channel-item']")
    if element:
        element[-1].click()
    return driver


def get_user_post_details(driver):
    user_details = []
    users = fetch_all_users(r"userCSVs\AI-USERS-1.xlsx")
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
            nickname = ""

        try:
            signature = driver.find_element(
                "css selector", "[data-e2e='user-bio']"
            ).text
        except Exception as e:
            signature = ""

        try:
            followingCount = driver.find_element(
                "css selector", "[data-e2e='following-count']"
            ).text
        except Exception as e:
            followingCount = ""

        try:
            followerCount = driver.find_element(
                "css selector", "[data-e2e='followers-count']"
            ).text
        except Exception as e:
            followerCount = ""

        try:
            heartCount = driver.find_element(
                "css selector", "[data-e2e='likes-count']"
            ).text
        except Exception as e:
            heartCount = ""

        try:
            avatarThumb = driver.find_element(By.CLASS_NAME, "css-1zpj2q-ImgAvatar")
            avatarThumb = avatarThumb.get_attribute("src")
        except Exception as e:
            avatarThumb = ""

        try:
            youtube_channel_id = driver.find_element(
                "css selector", "[data-e2e='user-link']"
            )
            youtube_channel_id = youtube_channel_id.get_attribute("href")
        except Exception as e:
            youtube_channel_id = ""

        user_detail = {
            "id": "",
            "uniqueId": user,
            "nickname": nickname,
            "avatarThumb": avatarThumb,
            "avatarMedium": avatarThumb,
            "avatarLarger": avatarThumb,
            "signature": signature,
            "verified ": False,
            "secUid": "",
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
            "ins_id": "",
            "twitter_id": "",
            "youtube_channel_title": youtube_channel_id,
            "youtube_channel_id": youtube_channel_id,
            "followingCount": parse_value_with_zeros(followingCount),
            "followerCount": parse_value_with_zeros(followerCount),
            "heartCount": parse_value_with_zeros(heartCount),
            "videoCount ": "",
            "diggCount": 0,
            "heart": parse_value_with_zeros(heartCount),
            "profileURL": url,
        }
        user_details.append(user_detail)
    return user_details


def get_tiktok_user():
    try:
        driver = configure_undetected_chrome_driver()
        driver.maximize_window()
        try:
            # driver.get(url)
            user_porofiles = get_user_post_details(driver)
            if user_porofiles:
                write_to_excel(
                    user_porofiles, "userCSVs", f"Ai_users_data-1000-new.xlsx"
                )
                # data.extend(user_posts)
        except Exception as e:
            print(f"Error : {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


get_tiktok_user()
