import os
import csv
import time
from helpers import (
    configure_webdriver,
    configure_undetected_chrome_driver,
    translate_text,
    parse_date,
    parse_value_with_zeros,
    fetch_all_users,
    write_to_excel,
    delete_user,
)

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


USERS = fetch_all_users(r"userCSVs\test-AI-USERS-1.xlsx")


def continue_as_guest(driver):
    time.sleep(5)
    element = driver.find_elements("css selector", "[data-e2e='channel-item']")
    if element:
        element[-1].click()
    return driver


def load_all_posts(driver):
    previous_len = len(
        driver.find_elements("css selector", "[data-e2e='user-post-item']")
    )
    while True:
        try:
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        except:
            pass
        time.sleep(5)
        elements = driver.find_elements("css selector", "[data-e2e='user-post-item']")
        if previous_len == len(elements) or len(elements) >= 100:
            return elements
        previous_len = len(elements)


def load_all_comments(driver):
    previous_len = len(
        driver.find_elements(By.CLASS_NAME, "css-1i7ohvi-DivCommentItemContainer")
    )
    while True:
        try:
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        except:
            pass

        elements = driver.find_elements(
            By.CLASS_NAME, "css-1i7ohvi-DivCommentItemContainer"
        )
        if previous_len == len(elements) or len(elements) >= 80:
            return elements
        previous_len = len(elements)


def get_user_post_details(driver, username):
    posts_details = []
    try:
        driver = continue_as_guest(driver)
    except:
        pass
    posts = load_all_posts(driver)
    print(len(posts))
    for post in posts:
        try:
            original_window = driver.current_window_handle
            try:
                views_count = post.find_element(
                    "css selector", "[data-e2e='video-views']"
                ).text
            except:
                views_count = ""
            url = post.find_element(By.TAG_NAME, "a")
            url = url.get_attribute("href")
            driver.switch_to.new_window("tab")
            driver.get(url)
            time.sleep(3)

            try:
                post_desc = driver.find_element(
                    "css selector", "[data-e2e='browse-video-desc']"
                ).text
            except Exception as e:
                post_desc = ""

            try:
                digg_count = driver.find_element(
                    "css selector", "[data-e2e='like-count']"
                ).text
            except Exception as e:
                digg_count = ""
            try:
                comments_count = driver.find_element(
                    "css selector", "[data-e2e='comment-count']"
                ).text
            except Exception as e:
                comments_count = ""

            try:
                collect_count = driver.find_element(
                    "css selector", "[data-e2e='undefined-count']"
                ).text
            except Exception as e:
                collect_count = ""

            try:
                postedDate = driver.find_element(
                    "css selector", "[data-e2e='browser-nickname']"
                )
                postedDate = postedDate.text.split("\n")[-1]
            except Exception as e:
                postedDate = ""

            try:
                share_count = driver.find_element(
                    "css selector", "[data-e2e='share-count']"
                ).text
            except Exception as e:
                share_count = ""

            try:
                generatedByAi = driver.find_element(
                    By.CLASS_NAME, "css-1483eyc-DivAnchorTagWrapper"
                )
                generatedByAi = generatedByAi.text.find("AI-generated")
            except:
                generatedByAi = -1

            try:
                comments = load_all_comments(driver)
            except Exception as e:
                comments = None
            comments = [i.text for i in comments]
            if comments:
                for comment in comments:
                    post_detail = {
                        "username": username,
                        "videoUrl": driver.current_url if driver.current_url else "",
                        "postedDate": parse_date(postedDate),
                        "postDesc": post_desc,
                        "viewsCount": parse_value_with_zeros(views_count),
                        "diggCount": parse_value_with_zeros(digg_count),
                        "commentsCount": len(comments),
                        "collectCount": parse_value_with_zeros(collect_count),
                        "shareCount": parse_value_with_zeros(share_count),
                        "commentedDate": parse_date(comment.split("\n")[2]),
                        "comments": comment.split("\n")[1],
                        "generated by AI": "NO" if generatedByAi == -1 else "YES",
                        "postDec-eng": translate_text(post_desc),
                        "comments-eng": translate_text(comment.split("\n")[1]),
                    }
                    posts_details.append(post_detail)
            else:
                post_detail = {
                    "username": username,
                    "videoUrl": driver.current_url if driver.current_url else "",
                    "postedDate":parse_date(postedDate),
                    "postDesc": post_desc,
                    "viewsCount": parse_value_with_zeros(views_count),
                    "diggCount": parse_value_with_zeros(digg_count),
                    "commentsCount": "0",
                    "collectCount": parse_value_with_zeros(collect_count),
                    "shareCount": parse_value_with_zeros(share_count),
                    "commentedDate": "",
                    "comments": "",
                    "generated by AI": "NO" if generatedByAi == -1 else "YES",
                    "postDec-eng": translate_text(post_desc),
                    "comments-eng": "",
                }
                # print(post_detail)
                posts_details.append(post_detail)

            driver.close()
            driver.switch_to.window(original_window)
        except Exception as e:
            print(f"Error in loading post details: {e}")
            driver.close()
            driver.switch_to.window(original_window)
    return posts_details


def get_tiktok_user_posts():
    try:
        driver = configure_undetected_chrome_driver()
        driver.maximize_window()
        for user in USERS:
            url = f"https://www.tiktok.com/@{user}"
            print(f"Scraping user: {user}")
            try:
                driver.get(url)
                user_posts = get_user_post_details(driver, user)
                if user_posts:
                    write_to_excel(user_posts, "userPostsDetail-1000-updated", f"{user}.xlsx")
                    delete_user(user, r"userCSVs\test-AI-USERS-1.xlsx")
            except Exception as e:
                print(f"Error while scraping user '{user}': {e}")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")


get_tiktok_user_posts()
