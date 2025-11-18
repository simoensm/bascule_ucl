# bascule_ucl

This Python script automatically scrapes the daily menu image from UCLouvain’s restaurant La Bascule, extracts the text using OCR, identifies the meal for the current weekday, and sends it as a Telegram notification.

Features

Scrapes the daily menu image from UCLouvain
Preprocesses the image for better OCR results
Uses Tesseract OCR to read the daily meals
Extracts only the menu for today
Sends notifications via Telegram Bot API
Optional push notification using notify.run

Requirements

Python Packages

Install all dependencies:

pip install requests beautifulsoup4 pillow pytesseract

Tesseract OCR

You must install Tesseract OCR on your system.

Windows:
Download the installer from:
https://github.com/tesseract-ocr/tesseract

Then ensure the script points to the correct installation path:

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

🔧 How It Works

Fetches the UCLouvain menu webpage.

Detects and extracts the weekly menu image.

Preprocesses the image: grayscale, filtering, thresholding.

Crops the areas corresponding to each weekday.

OCR is performed on each cropped zone.

The script compares today’s date with the weekday.

Sends the detected dish to Telegram and notify.run.

🗂 Configuration

Edit these values at the top of the script:

URL = "https://www.uclouvain.be/fr/resto-u/la-bascule"
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"


To notify multiple users, add more POST requests:

requests.post(url, data={"chat_id": ANOTHER_CHAT_ID, "text": message})

Usage

Run the script:

python menu_scraper.py


Expected output on success:

Notification envoyée pour Mardi


If no menu is found or it's a weekend:

Aujourd'hui n'est pas un jour de menu ou jour introuvable

Project Structure
menu-scraper
 ├── menu_scraper.py
 └── README.md

Notes & Limitations

OCR accuracy depends on the menu image quality.

If UCLouvain changes their page layout, the CSS selector or crop coordinates may need to be updated.

Image coordinates are tailored to the current design of the menu.

Contributions

Contributions, issues, and feature requests are welcome!
Feel free to open a pull request.
