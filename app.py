from flask import Flask, request, jsonify, render_template
import time
import logging
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
    logging.info(f"Received search query: {search_query}")  # Step 1: Confirm query received

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    base_url = "https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&q="
    search_url = base_url + search_query.replace(" ", "%20")

    logging.info(f"Opening URL: {search_url}")  # Step 2: Verify correct URL
    driver.get(search_url)

    time.sleep(5)  # Allow time for page to load

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Log the page source length (if it’s empty, something is wrong)
    logging.info(f"Page source length: {len(driver.page_source)}")

    video_tags = soup.find_all("video")
    video_urls = [video.get("src") for video in video_tags if video.get("src")]

    logging.info(f"Found {len(video_urls)} video(s)")  # Step 3: Confirm videos found

    driver.quit()

    return video_urls

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    search_query = request.form.get("search_term")
    logging.info(f"User searched for: {search_query}")  # Step 1: Confirm input received

    video_urls = get_facebook_ad_videos(search_query)

    if not video_urls:
        logging.warning("No videos found for the given query")
        return jsonify({"error": "No videos found"}), 404

    logging.info(f"Returning {len(video_urls)} video(s) to frontend")  # Step 4: Confirm response
    return jsonify({"videos": video_urls})

if __name__ == "__main__":
    app.run(debug=True)
