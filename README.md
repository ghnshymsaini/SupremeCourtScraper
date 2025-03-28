# Supreme Court Case Scraper

## Overview
This project is a web scraper that downloads Supreme Court case PDFs from [Indian Kanoon](https://indiankanoon.org) for specified years. It automates browsing, extracting case links, and downloading PDFs using **Selenium**.

## Features
- Scrapes case links for Supreme Court cases from 1950 to the latest year.
- Automates CAPTCHA handling and PDF downloads.
- Saves PDFs in a structured directory.
- Deployable on **Render** for remote access.
- Secured API access with an authentication key.

## Requirements
Ensure you have the following installed:
- Python 3.x
- Google Chrome
- ChromeDriver
- Selenium
- Flask
- Git

## Setup Instructions
### 1️⃣ Clone the Repository
```sh
git clone https://github.com/ghnshymsaini/SupremeCourtScraper.git
cd SupremeCourtScraper
```

### 2️⃣ Create a Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Run the Scraper Locally
```sh
python app.py
```

### 5️⃣ Deploy on Render
1. Push your code to GitHub:
   ```sh
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```
2. Go to [Render](https://render.com/) and create a **New Web Service**.
3. Select your **GitHub repository** and deploy.
4. Set **Environment Variables**:
   ```
   SCRAPER_API_KEY = your_secret_key
   ```
5. Deploy and monitor logs for success.

### 6️⃣ Test the API
Once deployed, test the scraper using:
```sh
curl -X POST "https://your-render-app-url/scrape" \
     -H "Authorization: Bearer your_secret_key" \
     -H "Content-Type: application/json" \
     -d '{"year": "2020"}'
```

## License
This project is open-source and free to use.

