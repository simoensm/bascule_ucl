import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageFilter
import pytesseract
from io import BytesIO
import re
import datetime

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
URL = "https://www.uclouvain.be/fr/resto-u/la-bascule"
TOKEN = "8398196144:AAEuz8or2MTRd8iCMlLUFvvX2OnzotlUxoA"  
CHAT_ID = "7005206249"      

page = requests.get(URL)
soup = BeautifulSoup(page.text, "html.parser")
selector = "#block-uclouvain-theme-content > article > div.node-content > div > div.col.col-12.text.text_default-500.rich-text.text_with-html > div > img"
img_tag = soup.select_one(selector)

if not img_tag or not img_tag.get("src"):
    print("⚠️ Impossible de trouver l'image du menu.")
    exit()

img_url = img_tag["src"]
response = requests.get(img_url)
img = Image.open(BytesIO(response.content))

img_gray = img.convert("L")
img_gray = img_gray.filter(ImageFilter.MedianFilter(size=3))
threshold = 150
img_bw = img_gray.point(lambda x: 0 if x < threshold else 255, '1')

left_lundi = 214
top = 170
right_lundi = 530
bottom = 380
horizontal_spacing = 25
col_width = right_lundi - left_lundi

jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
zones_plat_du_jour = {}
for i, jour in enumerate(jours):
    left = left_lundi + i * (col_width + horizontal_spacing)
    right = min(left + col_width, img.width)
    zones_plat_du_jour[jour] = (left, top, right, bottom)

def clean_text(text):
    text = re.sub(r'[^\w\séèàçùâêîôûëïüÉÈÀÇÙÂÊÎÔÛËÏÜ-]', ' ', text)
    lines = [line.strip() for line in text.splitlines() if len(line.strip()) > 2]
    return " ".join(lines)

menu = {}
for jour, coords in zones_plat_du_jour.items():
    cropped = img_bw.crop(coords)
    text = pytesseract.image_to_string(cropped, lang="fra").strip()
    menu[jour] = clean_text(text) or "Non trouvé"

aujourdhui = datetime.datetime.today().strftime("%A")
jours_fr = {"Monday": "Lundi", "Tuesday": "Mardi", "Wednesday": "Mercredi",
            "Thursday": "Jeudi", "Friday": "Vendredi"}
jour_fr = jours_fr.get(aujourdhui)

if jour_fr and jour_fr in menu:
    plat_du_jour = menu[jour_fr]
    message = f"Plat du jour de {jour_fr} : {plat_du_jour}"

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})
    requests.post(url, data={"chat_id": 2051726310, "text": message})
    print(f"✅ Notification envoyée pour {jour_fr}")
    requests.post("https://notify.run/wMprCYz7OnmaONmEIYbX", data=message.encode("utf-8")) 
else:
    print("⚠️ Aujourd'hui n'est pas un jour de menu ou jour introuvable")
