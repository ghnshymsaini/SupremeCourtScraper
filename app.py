import os
import time
import threading
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

# API Key for Security
API_KEY = os.getenv("SCRAPER_API_KEY", "default_secure_key")


# Function to run the scraper
def scrape_supreme_court(year):
    download_dir = os.path.join(os.getcwd(), f"SupremeCourt_{year}_PDFs")
    os.makedirs(download_dir, exist_ok=True)

    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {"download.default_directory": download_dir})
    chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    base_url = f"https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%20{year}&pagenum={{}}"
    page_num = 0
    case_links = []

    while True:
        driver.get(base_url.format(page_num))
        time.sleep(5)
        case_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/docfragment/')]")
        if not case_elements:
            break
        case_links.extend([case.get_attribute("href") for case in case_elements])
        page_num += 1

    for case_link in case_links:
        driver.get(case_link)
        time.sleep(5)
        try:
            pdf_button = driver.find_element(By.ID, "pdfdoc")
            pdf_button.click()
            time.sleep(10)
        except:
            continue

    driver.quit()
    print(f"✅ Finished scraping {year}. PDFs saved to: {download_dir}")


# API Endpoint to trigger the scraper
@app.route("/scrape", methods=["POST"])
def scrape():
    api_key = request.headers.get("Authorization")
    if api_key != f"Bearer {API_KEY}":
        return jsonify({"error": "Unauthorized"}), 403

    year = request.json.get("year")
    if not year or not (1950 <= int(year) <= 2025):
        return jsonify({"error": "Invalid year"}), 400

    threading.Thread(target=scrape_supreme_court, args=(year,)).start()
    return jsonify({"message": f"Scraping started for year {year}. PDFs will be stored securely."})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
