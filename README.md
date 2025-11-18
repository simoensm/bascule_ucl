# bascule_ucl

Daily Menu Scraper and Telegram Notifier

This script scrapes the daily menu image from UCLouvain’s restaurant La Bascule, extracts text using OCR, identifies the dish for the current weekday, and sends it through a Telegram bot.

Requirements

Install the required Python packages:

pip install requests beautifulsoup4 pillow pytesseract


Install Tesseract OCR:

Windows users can download it from: https://github.com/tesseract-ocr/tesseract

Update the path inside the script if necessary:

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

Configuration

Edit these constants in the script:

URL = "https://www.uclouvain.be/fr/resto-u/la-bascule"
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"


You can add more recipients by sending additional POST requests.

How It Works

Downloads the webpage containing the weekly menu.

Extracts the image using a CSS selector.

Preprocesses the image (grayscale, filter, threshold).

Crops predefined image areas corresponding to each weekday.

Uses Tesseract OCR to read the text in each area.

Determines today’s weekday.

Sends the corresponding dish to the configured Telegram chat.

Usage

Run:

python menu_scraper.py


The script will print whether the menu was successfully retrieved and whether the notification was sent.
