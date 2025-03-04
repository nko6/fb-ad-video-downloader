from flask import Flask, request, jsonify, render_template
import time
import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def get_facebook_ad_videos(search_query):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")  
    options.add_argument("--no-sandbox")  
    options.add_argument("--disable-dev-shm-usage")  

    # ✅ Use Render's pre-installed Chromium
    options.binary_location = "/usr/bin/chromium-browser"

    # ✅ Use Render's pre-installed ChromeDriver
    service = Service("/usr/lib/chromium-browser/chromedriver")

    logging.debug("Starting Chrome WebDriver...")
    driver = webdriver.Chrome(service=service, options=options)

    base_url = "https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&q="
    search_url = base_url + search_query.replace(" ", "%20")

    logging.debug(f"Fetching URL: {search_url}")
    driver.get(search_url)
    time.sleep(5)

    logging.debug("Parsing page source with BeautifulSoup")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    video_tags = soup.find_all("video")

    driver.quit()

    video_urls = [video.get("src") for video in video_tags if video.get("src")]

    if not video_urls:
        logging.warning("No videos found!")

    return video_urls

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    search_query = request.form.get("search_term")
    logging.info(f"User searched for: {search_query}")

    video_urls = get_facebook_ad_videos(search_query)

    if not video_urls:
        logging.warning("No videos found for the given query")
        return jsonify({"error": "No videos found"}), 404

    logging.info(f"Returning {len(video_urls)} video(s) to frontend")
    return jsonify({"videos": video_urls})

if __name__ == "__main__":
    app.run(debug=True)
