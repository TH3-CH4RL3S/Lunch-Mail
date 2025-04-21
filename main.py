import os
import requests
import shelve
import smtplib
import locale
from holidays import country_holidays
from datetime import date, timedelta
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from email.header import Header
from weather_api import get_coordinates, get_weather_from_smhi
from smhi_symbols import describe_weather_code

try:
    # Load .env
    load_dotenv(find_dotenv())
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API key is missing. Please set OPENAI_API_KEY in your .env file.")
    
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    if DEBUG:
        print("DEBUG mode is ON.")

    # Email setup
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    EMAIL_SENDER = os.getenv("EMAIL_SENDER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    EMAIL_RECIPIENTS = os.getenv("EMAIL_RECIPIENTS", "").split(",")
    FORMS_LINK = os.getenv("FORMS_LINK")

    # OpenAI client
    client = OpenAI(api_key=api_key)

    # Set locale for Swedish date formatting
    try:
        locale.setlocale(locale.LC_TIME, "sv_SE.UTF-8")
    except locale.Error:
        locale.setlocale(locale.LC_TIME, "sv_SE")

    today = date.today()
    weekday = today.weekday()
    swedish_holidays = country_holidays('SE')

    # Kontrollera om dagens datum är en röd dag
    if today in swedish_holidays and not DEBUG:
        # Avsluta programmet och därmed inte gör något utskick.
        raise SystemExit(f"Ingen lunchmeny skickas ut på röda dagar. Idag är det: {today}, {swedish_holidays[today]}.")
    
    else:

        # Standardvärden
        swedish_weekdays = ["Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag", "Lördag", "Söndag"]
        current_day = swedish_weekdays[weekday]
        target_week = today.isocalendar().week

        if weekday >= 5 or DEBUG:
            next_monday = today + timedelta(days=(7 - weekday))
            current_day = "Tisdag"
            target_week = next_monday.isocalendar().week

        # Hämta väderdata
        try:
            lat, lon = get_coordinates("Karlskoga") # Hämta latitud och longitud för en stad, exempelvis: Karlskoga
            temperature, wsymb_code, time = get_weather_from_smhi(lat, lon)
            weather_description = describe_weather_code(wsymb_code)
            weather_intro = f"📍 Vädret i Karlskoga just nu: {round(temperature)}°C och {weather_description}.\n"

        except Exception as e:
            weather_intro = "📍 Väderinformationen kunde inte hämtas just nu.\n\n"
            if DEBUG:
                print(f"[LunchBot WEATHER ERROR] {e}")

        # Restaurant URLs
        restaurant_urls = [
            "https://joans.se/lunch/lunch-karlskoga/",
            "https://boforshotel.se/ata/veckans-luncher/",
            "https://www.matochmat.se/lunch/karlskoga/karlskoga-hotell/",
            "https://hotellalfrednobel.se/ata/lunch/",
            "https://parltuppen.com/matsedel",
            "https://restauranghugo.se/dagens-lunch/",
            "https://indiancurry.nu/lunchbuffe/",
        ]

        # ------------------------
        def generate_lunch_email_html(client, menus):
            prompt_intro = (
                f"Du är en assistent som skickar ett dagligt lunchmejl till kollegor i HTML-format. "
                f"I varje menytext ska du endast visa lunchmenyn för {current_day} i vecka {target_week}. "
                "Om hemsidan anger lunch för flera veckor, se till att du väljer rätt vecka baserat på numret.\n\n"
                "För varje restaurang som nämns nedan ska du:\n"
                "- Skapa en rubrik med restaurangens namn som klickbar länk till hemsidan (<a href=\"...\">...<a>)\n"
                "- Lista dagens lunchrätter i punktform\n"
                "- Visa öppettider och pris om det finns\n"
                "- Om öppettider eller pris saknas, skriv något som 'se hemsidan för tider och priser.'\n"
                "- Lägg till en karta-länk med 📍-emoji som leder till Google Maps med restaurangens namn\n"
                "- Använd denna format för karta-länken:\n"
                "<p>📍 <a href='https://www.google.com/maps/search/RESTAURANGENS NAMN'>Visa på karta</a></p>\n"
                "- Använd HTML-taggar som <h2>, <h3>, <ul>, <li>, <p>, <em>, <a> för struktur\n"
                "- Lägg till en passande emoji i början av varje rätt som symboliserar vad det är (t.ex. 🐟, 🥩, 🌱)\n"
                "- Lägg till inbäddad CSS för enkel och professionell styling som fungerar i e-postklienter.\n\n"
                f"{weather_intro}"
                f"Använd väderinformationen i mejlets inledning för att skapa en personlig och trevlig hälsning. "
                f"Till exempel kan du föreslå att man sitter ute om det är soligt, eller rekommendera något varmt om det är kallt. "
                f"Var gärna lite humoristisk eller fyndig beroende på vädret.\n\n"
                "Inledningen (hälsning + väder) ska presenteras i en större stil än övrig text - t.ex. genom att använda en <div> med <strong> eller ökad fontstorlek (16–18px). "
                "Syftet är att skapa en varm och tydlig start på mejlet.\n\n"
                "Avsluta mejlet med en signatur från Lunch Bot 🤖 - byt gärna stil varje gång.\n\n"
                f"Avsluta allra sist med denna rad, med en fungerande HTML-länk:\n"
                f"<p style='font-size: 0.9em; text-align: center;'>Saknar du din favoritrestaurang? <a href='{FORMS_LINK}' target='_blank' style='color:#007bff;'>Tipsa Lunch-Bot Här!</a></p>\n\n"
                "<hr style='margin-top: 2em; margin-bottom: 0.5em;'>\n"
                "<p style='font-size: 0.75em; text-align: center; color: #888;'>"
                "* Detta utskick är automatiskt genererat av Lunch Bot med hjälp av "
                "<a href='https://openai.com' target='_blank' style='color: #888;'>OpenAI</a> "
                "och väderdata från <a href='https://opendata.smhi.se' target='_blank' style='color: #888;'>SMHI</a>."
                "</p>\n"
                "Här är menyerna:\n\n"
            )

            menu_texts = ""
            for url, raw_text in menus:
                trimmed_text = raw_text.strip()[:20000]
                menu_texts += f"---\nRestaurang: {url}\n\n{trimmed_text}\n\n"

            full_prompt = prompt_intro + menu_texts + "\nSvara endast med HTML och inbäddad CSS-utdata."

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Du är en assistent som skriver stilrena HTML-CSS-e-postmeddelanden med lunchmenyer."},
                    {"role": "user", "content": full_prompt}
                ]
            )

            return response.choices[0].message.content.strip().removeprefix("```html").removesuffix("```")

        # ------------------------

        results = []
        menus_for_gpt = []

        with shelve.open("menu_cache.db") as cache:
            today_str = today.isoformat()
            for url in restaurant_urls:
                cached = cache.get(url)
                if isinstance(cached, dict) and cached.get("date") == today_str:
                    print(f"Skipping {url}, already cached today.")
                    menu = cached["text"]
                    results.append(f"{url} (cached):\n{menu}")
                    menus_for_gpt.append((url, menu))
                    continue

                try:
                    html = requests.get(url, timeout=10).text
                    soup = BeautifulSoup(html, "html.parser")
                    text = soup.get_text(separator="\n", strip=True)[:20000]

                    # Save raw for GPT summarization
                    menus_for_gpt.append((url, text))
                    cache[url] = {"text": text, "date": today_str}
                    results.append(f"{url} (new):\n{text[:300]}...")
                except Exception as e:
                    error_msg = f"{url} (error): {str(e)}"
                    results.append(error_msg)
                    print(error_msg)

        subject_text = f"Dagens Lunch - V.{target_week} {current_day}"
        msg = MIMEMultipart("alternative")
        msg["From"] = formataddr(("Lunch Bot 🤖", EMAIL_SENDER))
        msg["To"] = "Lunchgruppen"
        msg["Subject"] = Header(subject_text, "utf-8")
        email_html = generate_lunch_email_html(client, menus_for_gpt)
        msg.attach(MIMEText("Se lunchmenyn i HTML-versionen av mejlet.", "plain"))
        msg.attach(MIMEText(email_html, "html"))

        if DEBUG:
            for url, _ in menus_for_gpt:
                if url not in email_html:
                    print(f"⚠️ VARNING: {url} verkar inte ha kommit med i GPT-svaret.")


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
    raise
