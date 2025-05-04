# 🍽️ LunchBot – Daily Restaurant Lunch Emailer

**LunchBot** is a powerful Python-based automation tool designed to simplify and enhance your lunch planning experience. It automatically fetches daily lunch menus from restaurant websites, processes them using OpenAI's GPT models (tested with versions as low as GPT-4o-mini), and delivers beautifully formatted HTML emails to your inbox. Whether you're coordinating lunch for a team or just want to stay informed, LunchBot ensures you never miss a delicious meal.

---

## 🚀 Features

- ✅ Fetches menus from one or more restaurant websites  
- 🤖 Uses GPT to extract **only today's lunch**, even if the full week's menu is listed  
- 💸 Extracts and mentions **lunch price and serving time**  
- 📬 Sends a formatted HTML email with a friendly greeting and inbedded CSS  
- 🕵️ **Lunchmysterium**: Includes a daily riddle, rebus, or math puzzle to engage recipients  
- ⏰ Perfect for **automated daily scheduling** using `cron` — set it and forget it!
- 💾 Caches websites to avoid reprocessing  
- 📅 Skips sending emails on **Swedish public holidays** using the `holidays` package  

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
DEBUG=true/false
```

---

## 🕒 Automating LunchBot with `cron` (Linux / Raspberry Pi)

This section explains how to automatically run LunchBot on a **Linux-based system**, such as a **Raspberry Pi**, using `cron` — the built-in task scheduler. This allows LunchBot to run at a specific time every day without any manual intervention.

We use a shell script called `run_task.sh` to manage environment setup, logging, and shutting down the Pi after the task completes.

---

### 🔧 What is `run_task.sh`?

The `run_task.sh` script:

- ✅ Activates the virtual environment for the LunchBot project.
- ✅ Executes the Python script to fetch, parse, and email the lunch menu.
- ✅ Logs both standard output and errors to timestamped log files.
- ✅ Sends an email with the error log if anything goes wrong.
- ✅ Shuts down the Raspberry Pi afterward to save energy.

This script handles all the behind-the-scenes logic and ensures errors are logged and notified properly.

---

### 📅 How to Schedule LunchBot with `cron`

#### 1. Open the crontab editor (in the terminal)

```bash
crontab -e
```

The first time you do this, it may ask you to choose an editor — select nano for simplicity.

#### 2. Add this line to run the script Monday–Friday at 11:00 AM:
```bash
0 11 * * 1-5 /home/pi/Lunch-Mail/run_task.sh
```
**Replace** ***/home/pi/LunchBot/*** with the actual path to your LunchBot project if it's different.

#### 3. Save and exit:
- In nano, press ***Ctrl + O*** to save.

- Then press ***Enter*** to confirm.

- Finally, press ***Ctrl + X*** to exit the editor.


#### 4. Cron Security & Best Practices

- **Ensure your `run_task.sh` is executable:**
  
  ```bash
  chmod +x /home/pi/Lunch-Mail/run_task.sh
  ```

- Your Pi will shut down after sending the email, so make sure it is powered back on each morning.

- You can use a smart plug with scheduled power cycles to get the full automation experience.

- Or manually turn it on each day, depending on your use case.

#### 5. Test your setup manually: 
Before relying on the automatic schedule, run the task manually to confirm that everything works:
```bash
bash /home/pi/Lunch-Mail/run_task.sh
```
Check the **cron.log**, **output_*.log**, and **error_*.log** files for results. You should receive the email and see no errors in the logs.

#### 6. Done! LunchBot is now scheduled and running:
You're all set! LunchBot will now automatically run every weekday at the time you specified, fetch the latest lunch menus, send them via email, and then shut down your server🎉

### ℹ️ Need more help with cron syntax?
Check out [crontab.guru](https://crontab.guru) — a helpful site for building and understanding cron schedules.

---

## ✉️ Setting Up Email on Linux / Raspberry Pi (for Notifications)

LunchBot uses your Raspberry Pi to send emails, including the formatted lunch menu and any error logs. To make this work reliably, you'll configure the Pi to send email via a real mail server (like Gmail) using a lightweight tool called `msmtp`.

---

### 🔧 1. Install msmtp and mail tools:

In the terminal, run:

```bash
sudo apt update
sudo apt install msmtp msmtp-mta mailutils
```
This installs the tools required to send email from the command line.

### 📄 2. Create the ~/.msmtprc configuration file:
Run:
```bash
nano ~/.msmtprc
```

Paste the following configuration, replacing the placeholders with your own Gmail info:
```ini
defaults
auth           on
tls            on
tls_trust_file /etc/ssl/certs/ca-certificates.crt
logfile        ~/.msmtp.log

account        gmail
host           smtp.gmail.com
port           587
from           your_email@gmail.com
user           your_email@gmail.com
password       your_app_password_here

account default : gmail
```
🔐 **Important:** You must use a [Gmail App Password](https://support.google.com/accounts/answer/185833) — not your normal password.

### 🔒 3. Secure the email config file:
```bash
chmod 600 ~/.msmtprc
```

### ✅ 4. Test email sending:
Send a test email:
```bash
echo "This is a test email from my Raspberry Pi" | mail -s "Test Email" your_email@gmail.com
```
Check your inbox. If the message arrives, you're good to go!

### 🪵 5. Check logs if it fails:
If no email arrives, check the log:
```bash
cat ~/.msmtp.log
```

📧 Once email is working, LunchBot can notify you of errors, send daily menus, and shut down automatically with confidence.