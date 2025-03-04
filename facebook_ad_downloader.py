import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Set up Selenium WebDriver
options = Options()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def download_facebook_ad_video(search_query):
    """Search for a Facebook Ad and download the video"""
    base_url = "https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&q="
    search_url = base_url + search_query.replace(" ", "%20")

    # Open Facebook Ad Library search page
    driver.get(search_url)
    time.sleep(5)  # Allow time for the page to load

    # Scroll to load more ads (optional)
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
    time.sleep(2)

    # Extract page source and parse with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")
    video_tags = soup.find_all("video")

    if not video_tags:
        print("No videos found.")
        return

    # Extract video URL and download
    for index, video in enumerate(video_tags):
        video_url = video.get("src")
        if video_url:
            print(f"Downloading video {index + 1}: {video_url}")
            response = requests.get(video_url, stream=True)
            with open(f"facebook_ad_video_{index + 1}.mp4", "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Video {index + 1} downloaded successfully!")

# Example usage
search_term = "Uability"
download_facebook_ad_video(search_term)

# Close the browser
driver.quit()
