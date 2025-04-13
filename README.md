# 🍽️ LunchBot – Daily Restaurant Lunch Emailer

**LunchBot** is a Python-based tool that automatically fetches daily lunch menus from restaurant websites, uses OpenAI's GPT-4o-mini model to extract and format them beautifully in HTML, and emails the result to a group of recipients.

---

## 🚀 Features

- ✅ Fetches menus from one or more restaurant websites
- 🤖 Uses GPT to extract **only today's lunch**, even if the full week's menu is listed
- 🕵️ Validates correct **week number** (even if testing on a Sunday!)
- 💸 Extracts or mentions **lunch price and serving time**
- 📬 Sends a formatted HTML email with a friendly greeting and a funny Lunch Bot signature
- 💾 Caches websites to avoid reprocessing
- 📅 Configured for testing: simulates **Monday of next week** if script is run on a weekend

---

## 📦 Requirements

- Python 3.8+
- An [OpenAI API key](https://platform.openai.com/)
- A E-mail account that you have access to. E.g: A Gmail account with [App Passwords enabled](https://support.google.com/accounts/answer/185833)
- The following Python packages installed:
  - `openai`
  - `requests`
  - `beautifulsoup4`
  - `python-dotenv`

Install dependencies with:

### 🪟 Windows

```bash
pip install openai requests beautifulsoup4 python-dotenv
```

## 🐧 Linux Setup Instructions

Follow these steps to install dependencies and set up the LunchBot environment on a Linux system (e.g. Raspberry Pi):

### 📦 1. Update & Upgrade the System

```bash
sudo apt update && sudo apt upgrade -y
```

### 🐍 2. Install Python and Virtual Environment Tools
```bash
sudo apt install -y python3 python3-pip python3-venv
```

### ☁️ 3. Create and Activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install openai requests beautifulsoup4 python-dotenv
```