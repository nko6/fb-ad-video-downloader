from flask import Flask, request, jsonify, render_template
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_facebook_ad_videos(search_query):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    base_url = "https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&q="
    search_url = base_url + search_query.replace(" ", "%20")

    driver.get(search_url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    video_tags = soup.find_all("video")

    driver.quit()

    return [video.get("src") for video in video_tags if video.get("src")]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    search_query = request.form.get("search_term")
    video_urls = get_facebook_ad_videos(search_query)

    if not video_urls:
        return jsonify({"error": "No videos found"}), 404

    return jsonify({"videos": video_urls})

if __name__ == "__main__":
    app.run(debug=True)
