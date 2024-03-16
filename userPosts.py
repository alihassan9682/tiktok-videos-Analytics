import time

from helpers import configure_webdriver, configure_undetected_chrome_driver

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import csv
import os


def request_url(driver, url):
    driver.get(url)

USERS = [
    "xxenni",
    "aleksandeer821",
    "beautyinbits",
    "bluefan20002023",
    "cars.bikes.ai",
    "cartoonscovers",
    "casos.basados",
    "celestial.muse",
    "celestialair_oficial",
    "charlyb_83",
    "chescosol",
    "corridones.ia",
    "cowieowie_",
    "crishxextrem",
    "croyances.superst",
    "cxaxrxexe",
    "cyberland.ai",
    "dautay.net",
    "davidross988",
    "diablesseguerriere",
    "digitart2050",
    "distopyanworld.ia",
    "drew_learning_ai",
    "duchessart",
    "el_moko_ke_kamina",
    "ellionz",
    "elpanaraul.2.0",
    "evilcorp.zima",
    "expandai",
    "f1covers",
    "fakeunivers1",
    "gbdowntown",
    "gpt_coderman",
    "gsm.ai",
    "gthvil",
    "halfblood.princesss",
    "iamso.hot",
    "idynkt",
    "ildeepfaker",
    "ilforonelmondo2",
    "ilyxoxohim",
    "imagine.if.ai1",
    "jane_morelli",
    "jorchhoffman",
    "killingdnyx",
    "kloverremix",
    "laliboall",
    "litficcreative",
    "luna_virtua",
    "makktu.b",
    "malfoy.mariamalfoy",
    "mangaain",
    "mb.art.nook",
    "mcantonio87",
    "miamizusan",
    "multandolphin",
    "nirasmiley",
    "otageekk",
    "outer_worlds.ai",
    "pahlawansuperai",
    "palimpalim228",
    "panorama.ia",
    "peetfrfr",
    "pinky.spider27",
    "pixelgenius8",
    "planet.ai",
    "rebirthai",
    "robin_lochmann",
    "ryan_.williams1",
    "sane.art",
    "scraggydog1",
    "sevsevseverus",
    "slava081984",
    "spdrgrleve",
    "summergram",
    "talesoftime1337",
    "techaivisions",
    "tenthousandscrolls",
    "theaibeatles",
    "thejasonpower_",
    "tomokoworks",
    "tonkenken.ai",
    "transeunte_prompts",
    "twanmillion",
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
        if previous_len == len(elements) or  len(elements) >= 250 :
            return elements
        previous_len = len(elements)


def get_user_post_details(driver):
    posts_details = []
    try:
        driver = continue_as_guest(driver)
    except:
        pass
    posts = load_all_posts(driver)
    print(len(posts))
    for post in posts:
        try:
            views_count = post.find_element("css selector", "[data-e2e='video-views']")
            post.click()
            time.sleep(1)
            try:
                post_desc = driver.find_element(
                    "css selector", "[data-e2e='browse-video-desc']"
                )
            except Exception as e:
                post_desc = None
            
            try:
                comments = driver.find_elements(
                    "css selector", "[data-e2e='comment-level-1']"
                )
            except Exception as e:
                comments = None
            
            try:
                digg_count = driver.find_element(
                    "css selector", "[data-e2e='browse-like-count']"
                )
            except Exception as e:
                digg_count = None
            
            try:
                comments_count = driver.find_element(
                    "css selector", "[data-e2e='browse-comment-count']"
                )
            except Exception as e:
                comments_count = None
            
            try:
                collect_count = driver.find_element(
                    "css selector", "[data-e2e='undefined-count']"
                )
            except Exception as e:
                collect_count = None
            
            try:
                video_url = driver.find_element(
                    "css selector", "[data-e2e='browse-video-link']"
                )
            except Exception as e:
                video_url = None

            comments = [i.text for i in comments]
            post_detail = {
                "videoUrl": video_url.text if video_url else '',
                "postDesc": post_desc.text if post_desc else '',
                "viewsCount": views_count.text if views_count else '',
                "diggCount": digg_count.text if digg_count else '',
                "commentsCount": comments_count.text if  comments_count else '',
                "collectCount": collect_count.text if collect_count else '',
                "comments": comments if comments else '',
            }
            posts_details.append(post_detail)
            close = driver.find_element("css selector", "[data-e2e='browse-close']")
            close.click()
        except Exception as e:
            print(f"Error in loading post details: {e}")
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
                user_posts = get_user_post_details(driver)
                if user_posts:
                    write_to_csv(user_posts, "userCSVs", f"{user}.csv")
                    data.extend(user_posts)
            except Exception as e:
                print(f"Error while scraping user '{user}': {e}")
        return data
    except Exception as e:
        print(f"An error occurred: {e}")
   


get_tiktok_user_posts()
