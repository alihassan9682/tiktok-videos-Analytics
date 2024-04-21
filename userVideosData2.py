import os
import csv
import time

from helpers import configure_webdriver, configure_undetected_chrome_driver

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


USERS = [
    "vikthor_stone",
    "wanderingweb",
    "wiwispiderm4noc",
    "worldofwondev",
    "xcwenty",
    "xxheichouxx",
    "zo6262",
    "ai4klivewallpapers",
]


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
        if previous_len == len(elements) or len(elements) >= 200:
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
        time.sleep(3)
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
                views_count = 'N/A'
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
                post_desc = 'N/A'

            try:
                digg_count = driver.find_element(
                    "css selector", "[data-e2e='like-count']"
                ).text
            except Exception as e:
                digg_count = 'N/A'
            try:
                comments_count = driver.find_element(
                    "css selector", "[data-e2e='comment-count']"
                ).text
            except Exception as e:
                comments_count = 'N/A'

            try:
                collect_count = driver.find_element(
                    "css selector", "[data-e2e='undefined-count']"
                ).text
            except Exception as e:
                collect_count = 'N/A'

            try:
                postedDate = driver.find_element(
                    "css selector", "[data-e2e='browser-nickname']"
                )
                postedDate = postedDate.text.split("\n")[-1]
            except Exception as e:
                postedDate = 'N/A'

            try:
                share_count = driver.find_element(
                    "css selector", "[data-e2e='share-count']"
                ).text
            except Exception as e:
                share_count = 'N/A'

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
                        "username":username,
                        "videoUrl": driver.current_url if driver.current_url else "",
                        "postedDate": postedDate,
                        "postDesc": post_desc,
                        "viewsCount": views_count,
                        "diggCount": digg_count,
                        "commentsCount": comments_count,
                        "collectCount": collect_count,
                        "shareCount": share_count,
                        "commentedDate": comment.split("\n")[2],
                        "comments": comment.split("\n")[1],
                        "generated by AI": "NO" if generatedByAi == -1 else "YES",
                    }
                    # print(post_detail)
                    posts_details.append(post_detail)
            else:
                post_detail = {
                    "username": username,
                    "videoUrl": driver.current_url if driver.current_url else "",
                    "postedDate": postedDate,
                    "postDesc": post_desc,
                    "viewsCount": views_count,
                    "diggCount": digg_count,
                    "commentsCount": comments_count,
                    "collectCount": collect_count,
                    "shareCount": share_count,
                    "commentedDate": "N/A",
                    "comments": "N/A",
                    "generated by AI": "NO" if generatedByAi == -1 else "YES",
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
        data = []
        for user in USERS:
            url = f"https://www.tiktok.com/@{user}"
            print(f"Scraping user: {user}")
            try:
                driver.get(url)
                user_posts = get_user_post_details(driver,user)
                if user_posts:
                    write_to_csv(user_posts, "userPostsDetail-updated", f"{user}.csv")
                    data.extend(user_posts)
            except Exception as e:
                print(f"Error while scraping user '{user}': {e}")
        return data
    except Exception as e:
        print(f"An error occurred: {e}")


get_tiktok_user_posts()
