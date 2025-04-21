# smhi_symbols.py
# https://opendata.smhi.se/metfcst/pmp/parameters#weather-symbol
wsymb_descriptions = {
    1: "Klart ☀️",
    2: "Nästan klart 🌤️",
    3: "Växlande molnighet 🌥️",
    4: "Molnigt ☁️",
    5: "Mycket moln ☁️",
    6: "Mulet ☁️",
    7: "Dimma 🌫️",
    8: "Lätt regnskur 🌦️",
    9: "Måttlig regnskur 🌧️",
    10: "Kraftig regnskur 🌧️",
    11: "Åska med regn ⛈️",
    12: "Lätt blötsnöskur 🌨️",
    13: "Måttlig blötsnöskur 🌨️",
    14: "Kraftig blötsnöskur ❄️",
    15: "Lätt snöskur ❄️",
    16: "Måttlig snöskur 🌨️",
    17: "Kraftig snöskur 🌨️",
    18: "Lätt regn 🌦️",
    19: "Måttligt regn 🌧️",
    20: "Kraftigt regn 🌧️",
    21: "Åska ⚡️",
    22: "Lätt blötsnö 🌨️",
    23: "Måttlig blötsnö 🌨️",
    24: "Kraftig blötsnö ❄️",
    25: "Lätt snöfall ❄️",
    26: "Måttligt snöfall 🌨️",
    27: "Kraftigt snöfall 🌨️"
}


def describe_weather_code(code: int) -> str:
    """Returnerar väderbeskrivning med emoji för en Wsymb2-kod."""
    return wsymb_descriptions.get(code, f"Okänt väder ({code}) ❓")
