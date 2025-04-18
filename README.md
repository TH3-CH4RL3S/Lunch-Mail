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
- 📅 Skips sending emails on **Swedish public holidays** using the `holidays` package
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
  - `holidays`

Install dependencies with:

### 🪟 Windows

```bash
pip install openai requests beautifulsoup4 python-dotenv holidays
```

### 🐧 Linux Setup Instructions

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
pip install openai requests beautifulsoup4 python-dotenv holidays
```

---

## 🔑 Setting Up the `.env` File

The `.env` file is used to securely store sensitive information, such as API keys and email credentials, that the LunchBot script needs to run. This approach keeps your sensitive data out of the source code and ensures it is not accidentally shared or exposed.

### Why You Need a `.env` File

1. **API Key**: The script uses OpenAI's API to process and format the lunch menus. You need to provide your OpenAI API key.
2. **Email Credentials**: LunchBot sends the formatted lunch menu via email. You need to provide your email account credentials (e.g., Gmail App Password) to enable this functionality.
3. **Environment Variables**: Using a `.env` file allows you to easily manage and update these values without modifying the code.

### How to Create and Configure the `.env` File

1. Create a file named `.env` in the root directory of the project.
2. Add the following variables to the file, replacing the placeholders with your actual values:

```python
OPENAI_API_KEY=your_openai_api_key_here
EMAIL_SENDER=sender_email_address_here
EMAIL_PASSWORD=your_email_app_password_here
EMAIL_RECIPIENTS=list_of_recipients_email_adresses_here
FORMS_LINK=your_forms_link_here
```