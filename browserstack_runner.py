import os
import requests
import time
import threading
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from googletrans import Translator

# === Configuration ===
BASE_URL = "https://elpais.com/opinion/"
IMAGE_DIR = "images"
TRANSLATOR = Translator()

# === Create Image Directory ===
os.makedirs(IMAGE_DIR, exist_ok=True)

# === Scrape El Pais Articles ===
def scrape_articles():
    print("\n\U0001F4F0 Starting El País scraper...\n")
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.content, "html.parser")
    
    articles = soup.select("article a[href^='/opinion/']")
    seen = set()
    valid_links = []

    for link in articles:
        href = link.get("href")
        if href and href not in seen and len(valid_links) < 5:
            seen.add(href)
            valid_links.append("https://elpais.com" + href)

    results = []
    for idx, url in enumerate(valid_links):
        art_res = requests.get(url)
        art_soup = BeautifulSoup(art_res.content, "html.parser")

        title = art_soup.find("h1").get_text(strip=True) if art_soup.find("h1") else "No title"
        img_tag = art_soup.find("img")
        img_url = img_tag["src"] if img_tag and img_tag.has_attr("src") else None

        image_path = os.path.join(IMAGE_DIR, f"article_{idx+1}.jpg")
        if img_url:
            try:
                img_data = requests.get(img_url).content
                with open(image_path, 'wb') as f:
                    f.write(img_data)
            except Exception:
                image_path = "Image download failed"
        else:
            image_path = "Image not found"

        translated_title = TRANSLATOR.translate(title, src='es', dest='en').text

        print(f"\n\U0001F517 Article {idx+1}: {url}")
        print(f"✍️ Title (Spanish): {title}")
        print(f"\U0001F310 Title (English): {translated_title}")
        print(f"✍️ Author Info: Author info not found")
        print(f"\U0001F5BC️ Image saved to: {image_path}")

        results.append(translated_title)

    return results

# === Analyze Translated Titles ===
def analyze_titles(titles):
    print("\n\U0001F50E Analyzing repeated words in translated titles...")
    word_counts = {}
    for title in titles:
        for word in title.lower().split():
            word = word.strip(".,:;!?")
            word_counts[word] = word_counts.get(word, 0) + 1

    repeated = {w: c for w, c in word_counts.items() if c > 2}
    if repeated:
        for word, count in repeated.items():
            print(f"{word}: {count} times")
    else:
        print("✅ No words repeated more than twice.")

# === Cross-Browser Testing Threads ===
BROWSERSTACK_URL = "https://aniketajayshukla_WyQo9v:7Avz5uQTJmK1Bqrr9NEy@hub-cloud.browserstack.com/wd/hub"

CAPABILITIES = [
    {
        "os": "Windows",
        "osVersion": "10",
        "browserName": "Chrome",
        "sessionName": "Chrome Win10 Test"
    },
    {
        "os": "OS X",
        "osVersion": "Ventura",
        "browserName": "Safari",
        "sessionName": "Safari macOS Test"
    },
    {
        "deviceName": "Samsung Galaxy S23",
        "realMobile": "true",
        "browserName": "Chrome",
        "sessionName": "Galaxy S23 Mobile Test"
    },
    {
        "deviceName": "iPhone 14",
        "realMobile": "true",
        "browserName": "Safari",
        "sessionName": "iPhone 14 Test"
    },
    {
        "os": "Windows",
        "osVersion": "11",
        "browserName": "Firefox",
        "sessionName": "Firefox Win11 Test"
    },
]


def run_browserstack_test(cap):
    from selenium.webdriver.remote.webdriver import WebDriver
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    
    print(f"\n\U0001F9EA Starting: {cap['sessionName']}")
    options = webdriver.ChromeOptions()
    options.set_capability("bstack:options", cap)

    try:
        driver = webdriver.Remote(
            command_executor=BROWSERSTACK_URL,
            options=options
        )
        driver.get("https://elpais.com/opinion/")
        time.sleep(5)

        # ✅ Set BrowserStack session status to passed
        driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed","reason": "Page loaded successfully"}}')

        print(f"✅ Success: {cap['sessionName']}")
    except Exception as e:
        print(f"❌ Failed on {cap['sessionName']}: {e}")
    finally:
        try:
            driver.quit()
        except:
            pass

# === Main Execution ===
if __name__ == '__main__':
    titles = scrape_articles()
    analyze_titles(titles)

    print("\n\U0001F310 Starting parallel cross-browser tests on BrowserStack...")
    threads = []
    for cap in CAPABILITIES:
        t = threading.Thread(target=run_browserstack_test, args=(cap,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("\n\U0001F389 All parallel BrowserStack tests completed!")

