import os
import requests
import shelve
import smtplib
import locale
from datetime import date
from datetime import timedelta
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

# Load .env
load_dotenv(find_dotenv())
api_key = os.getenv("OPENAI_API_KEY")

# Email setup
SMTP_SERVER = "smtp.gmail.com"  # Change to your SMTP server
SMTP_PORT = 587
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECIPIENTS = os.getenv("EMAIL_RECIPIENTS", "").split(",")

# OpenAI client
client = OpenAI(api_key=api_key)

# Set locale for Swedish date formatting
locale.setlocale(locale.LC_TIME, "sv_SE.UTF-8")
today = date.today()
weekday = today.weekday()  # 0 = Måndag, 6 = Söndag

# Standardvärden
current_day = today.strftime("%A").capitalize()
target_week = today.isocalendar().week

# Om helg – simulera måndag nästa vecka
if weekday >= 5:
    next_monday = today + timedelta(days=(7 - weekday))  # kommande måndag
    current_day = "Måndag"
    target_week = next_monday.isocalendar().week

# Restaurant URLs to scrape
# Add your restaurant URLs here
restaurant_urls = [
    "https://joans.se/lunch/lunch-karlskoga/",
    "https://boforshotel.se/ata/veckans-luncher/",
    "https://www.matochmat.se/lunch/karlskoga/karlskoga-hotell/",
    "https://hotellalfrednobel.se/ata/lunch/",
    "https://parltuppen.com/matsedel",
    "https://restauranghugo.se/dagens-lunch/",
    "https://www.matochmat.se/lunch/karlskoga/pacos-karlskoga/",
]

# ------------------------
# Function to generate full HTML email using GPT in Swedish
def generate_lunch_email_html(client, menus):
    prompt_intro = (
        f"Du är en assistent som skickar ett dagligt lunchmejl till kollegor. "
        f"I varje menytext ska du endast visa lunchmenyn för {current_day} i vecka {target_week}. "
        "Om hemsidan anger lunch för flera veckor, se till att du väljer rätt vecka baserat på numret.\n\n"
        "För varje restaurang som nämns nedan ska du:\n"
        "- Skapa en rubrik med restaurangens namn som länk till hemsidan\n"
        "- Lista dagens lunchrätter i punktform\n"
        "- Försök alltid att visa öppettider och pris\n"
        "- Om öppettider eller pris saknas, skriv istället något i stil med 'se hemsidan för tider och priser.'\n"
        "- Använd HTML-taggar som <h2>, <h3>, <ul>, <li>, <p> och <em> för struktur\n\n"
        "Inled mejlet med en vänlig hälsning och avsluta alltid med en signatur från Lunch Bot – "
        "gör det roligt, kreativt och gärna med emojis. Använd olika stilar varje gång.\n\n"
        "Här är menyerna:\n\n"
    )


    menu_texts = ""
    for url, raw_text in menus:
        trimmed_text = raw_text.strip()[:20000]
        menu_texts += f"---\nRestaurang: {url}\n\n{trimmed_text}\n\n"

    full_prompt = prompt_intro + menu_texts + "\nSvara endast med HTML-mejltexten, utan förklaringar."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Du är en assistent som skriver e-postmeddelanden med lunchmenyer i HTML-format."},
            {"role": "user", "content": full_prompt}
        ]
    )

    return response.choices[0].message.content.strip().removeprefix("```html").removesuffix("```")

# ------------------------

results = []
menus_for_gpt = []

with shelve.open("menu_cache.db") as cache:
    for url in restaurant_urls:
        if url in cache:
            print(f"Skipping {url}, already cached.")
            menu = cache[url]
            results.append(f"{url} (cached):\n{menu}")
            menus_for_gpt.append((url, menu))
            continue

        try:
            html = requests.get(url, timeout=10).text
            soup = BeautifulSoup(html, "html.parser")
            text = soup.get_text(separator="\n", strip=True)[:20000]

            # Save raw for GPT summarization
            menus_for_gpt.append((url, text))
            cache[url] = text  # Cache raw, not formatted GPT result
            results.append(f"{url} (new):\n{text[:300]}...")  # Preview in console
        except Exception as e:
            error_msg = f"{url} (error): {str(e)}"
            results.append(error_msg)
            print(error_msg)

# Prepare email content
email_subject = f"Dagens Lunch - V.{target_week} {current_day} 🍽️"


# Generate HTML email body with GPT
email_html = generate_lunch_email_html(client, menus_for_gpt)

# Email message
msg = MIMEMultipart("alternative")
msg["From"] = formataddr(("Lunch Bot 🤖", EMAIL_SENDER))
msg["To"] = ", ".join(EMAIL_RECIPIENTS)
msg["Subject"] = email_subject

# Attach both plain fallback and HTML version
msg.attach(MIMEText("Se lunchmenyn i HTML-versionen av mejlet.", "plain"))
msg.attach(MIMEText(email_html, "html"))

# Send email
try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENTS, msg.as_string())
        print("Email sent successfully.")
except Exception as e:
    print("Failed to send email:", str(e))

except Exception as e:
    print(f"[LunchBot ERROR] {e}")
    raise  # re-raise so cron sees it