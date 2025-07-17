# BrowserStack Round 2 Technical Assignment – Aniket Ajay Shukla

## 📌 Overview

This project is a submission for the **Customer Engineering Role – Round 2 Assignment** at **BrowserStack**. It demonstrates web scraping, translation API integration, text processing, and cross-browser automated testing using Selenium and BrowserStack Automate.

---

## 🔧 Technologies Used

- Python 3
- Selenium WebDriver
- BrowserStack Automate
- BeautifulSoup (bs4)
- Google Translate (via `googletrans`)
- Requests
- Threading

---

## ✅ Problem Statement

The objective is to:

1. Scrape the top 5 articles from the **Opinion** section of [El País](https://elpais.com/opinion/).
2. Extract the article title, content (Spanish), and cover image.
3. Translate the Spanish titles into English using a translation API.
4. Analyze repeated words across all translated titles.
5. Execute cross-browser testing in **5 parallel threads** using **BrowserStack Automate**.

---

## 📁 Project Structure

├── browserstack_runner.py # Main script with scraping + BrowserStack testing
├── requirements.txt # Python dependencies
├── README.md # Project documentation
└── images/ # Folder containing downloaded article images



---

## 🚀 Features Implemented

### 1. Web Scraping
- Visited `https://elpais.com/opinion/`
- Extracted 5 unique article URLs
- Fetched:
  - Spanish Title
  - Article content (headings only for demonstration)
  - Cover image (if available)

### 2. Translation
- Translated all titles from **Spanish → English**
- Used the `googletrans` package (Google Translate unofficial API)

### 3. Text Analysis
- Analyzed translated titles
- Identified **repeated words (occurring more than twice)** across all titles

### 4. Cross-Browser Parallel Testing
- Executed using `threading` in Python
- Run on 5 different browser environments:
  - Chrome on Windows 10
  - Firefox on Windows 11
  - Safari on macOS Ventura
  - Chrome on Samsung Galaxy S23
  - Safari on iPhone 14
- Used BrowserStack Automate with custom session names and status reporting.

---

## 🧪 How to Run

### 1. Setup bash


pip install -r requirements.txt
Run Locally
bash
Copy
Edit
python3 browserstack_runner.py

This will:

Scrape articles

Translate and analyze

Trigger BrowserStack tests in 5 parallel threads

🌐 BrowserStack Automate Details
Build Screenshot & Results:
📸 Screenshot of Build Dashboard: Google Drive Link

✅ Automate Build Link: BrowserStack Dashboard

Build Status: Passed

Total Tests: 5

Failure: None

Duration: ~49 seconds

👨‍💻 Author
Aniket Ajay Shukla
Email: [aniketshukla454@gmail.com]
GitHub: github.com/aniketajayshukla
