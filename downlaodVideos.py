from selenium import webdriver
from selenium.webdriver.common.by import By
from helpers import configure_webdriver, configure_undetected_chrome_driver
import time


def download_tiktok_video(url, filename):
    # Create a new instance of the Chrome driver
    driver = configure_webdriver(True)
    driver.maximize_window()
    # Open the TikTok URL

    driver.get("https://savetik.co/en")
    time.sleep(5)  # Wait for the page to load
    # Find the video element
    input = driver.find_element(By.CLASS_NAME, "search__input")
    input.send_keys(tiktok_url)
    btn = driver.find_element(By.CLASS_NAME, "btn-red")
    btn.click()
    time.sleep(1)
    btn = driver.find_elements(By.CLASS_NAME, "tik-button-dl")
    btn[0].click()
    time.sleep(1)
    import pdb

    pdb.set_trace()
    dismiss_button = driver.find_element(By.ID, "dismiss-button")
    dismiss_button.click()


# Example usage
tiktok_url = "https://www.tiktok.com/@ai.dreamcontent/video/7343320699689356549?is_from_webapp=1&sender_device=pc&web_id=7346423406504379911"
video_filename = "video.mp4"

download_tiktok_video(tiktok_url, video_filename)
