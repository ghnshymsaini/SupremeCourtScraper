import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Set up Chrome options for automatic downloads
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True  # Avoid opening PDFs in browser
})
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid detection
chrome_options.add_argument("--log-level=3")  # Reduce logging noise
chrome_options.add_argument("--disable-popup-blocking")  # Prevent popups
chrome_options.add_argument("--start-maximized")

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Iterate through years 1950 to 2025
for year in range(1950, 2026):
    print(f"\n🔍 Scraping cases for the year {year}...")

    # Create a directory for each year
    year_dir = os.path.join(os.getcwd(), f"SupremeCourt_{year}_PDFs")
    os.makedirs(year_dir, exist_ok=True)

    # Update Chrome download directory for this year
    chrome_options.add_experimental_option("prefs", {"download.default_directory": year_dir})
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Base URL for the year (pagination handled dynamically)
    base_url = f"https://indiankanoon.org/search/?formInput=doctypes%3A%20supremecourt%20year%3A%20{year}&pagenum={{}}"

    # Extract case links from all pages
    page_num = 0
    case_links = []

    while True:
        driver.get(base_url.format(page_num))
        time.sleep(2)  # Allow page to load

        case_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/docfragment/')]")
        if not case_elements:  # Stop when no more cases found
            break

        for case in case_elements:
            href = case.get_attribute("href")
            if href:
                case_links.append(href)

        print(f"📄 Extracted {len(case_elements)} case links from page {page_num} ({year})")
        page_num += 1

    print(f"🔗 Found {len(case_links)} cases for {year}.")

    # Download PDFs for each case
    '''for case_link in case_links:
        driver.get(case_link)
        time.sleep(5)  # Allow the page to load

        # Handle CAPTCHA if present
        try:
            captcha_iframe = driver.find_element(By.CSS_SELECTOR, "iframe[src*='captcha']")
            driver.switch_to.frame(captcha_iframe)
            checkbox = driver.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
            checkbox.click()  # Click "I’m not a robot" checkbox
            driver.switch_to.default_content()
            time.sleep(10)  # Wait for CAPTCHA to verify
        except:
            pass  # If no CAPTCHA, continue normally

        # Click "Get this document in PDF"
        try:
            pdf_button = driver.find_element(By.ID, "pdfdoc")
            pdf_button.click()
            print(f"📥 Downloading PDF from: {case_link}")
            time.sleep(10)  # Wait for download to complete
        except Exception as e:
            print(f"❌ Failed to download PDF from {case_link}: {e}")
'''
    print(f"✅ Finished scraping {year}. PDFs saved to: {year_dir}")

# Close the browser
driver.quit()
print("\n🎉 All years processed successfully!")
