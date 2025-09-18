import os
from dotenv import load_dotenv
import gspread
from datetime import datetime, timedelta
from telegram import Bot
import logging
import asyncio
import traceback
import requests

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, filename='script.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')

# Load sensitive information
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
SPREADSHEET_URL = os.getenv("GOOGLE_SHEET_URL")

if not BOT_TOKEN or not CHAT_ID or not SPREADSHEET_URL:
  raise ValueError("Missing required environment variables in .env file.")

# Initialize the Telegram bot
bot = Bot(token=BOT_TOKEN)

# Notification thresholds (in days)
NOTIFY_DAYS = [60, 45, 30, 15, 7, 3, 1]


async def send_notification(subscription, days_left):
  """Send a subscription notification via Telegram bot."""
  message = (
    f"🔔 Subscription Reminder 🔔\n\n"
    f"**Name**: {subscription['Name']}\n"
    f"**Ends On**: {subscription['End Date']}\n"
    f"**Days Remaining**: {days_left} days\n\n"
    f"**Remarks**: {subscription['Remarks']}\n\n"
  )
  await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
  logging.info(f"Subscription notification sent for {subscription['Name']}: {days_left} days left.")


async def send_error_notification(error_message):
  """Send an error notification via Telegram bot."""
  message = (
    f"🚨 **Subscription Checker Error** 🚨\n\n"
    f"An error occurred while running the script:\n\n"
    f"```\n{error_message}\n```"
  )
  await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
  logging.error(f"Error notification sent: {error_message}")


async def send_ip_change_notification(new_ip, old_ip=None):
  """Sends a notification when the IP address changes."""
  if old_ip:
    message = (
      f"✨ **IP Address Changed!** ✨\n\n"
      f"Your public IP address has changed from `{old_ip}` to `{new_ip}`."
    )
  else:
    message = (
      f"✨ **IP Address Detected!** ✨\n\n"
      f"Your current public IP address is `{new_ip}`."
    )
  await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
  logging.info(f"IP change notification sent. New IP: {new_ip}")

def get_current_ip_address():
  """Fetches the current public IP address."""
  try:
    response = requests.get("https://api.ipify.org?format=json")
    response.raise_for_status()  # Raise an exception for HTTP errors
    ip_data = response.json()
    return ip_data["ip"]
  except requests.exceptions.RequestException as e:
    logging.error(f"Error fetching IP address: {e}")
    return None

def read_last_ip_address(file_path="last_ip.txt"):
  """Reads the last known IP address from a file."""
  try:
    with open(file_path, "r") as f:
      return f.read().strip()
  except FileNotFoundError:
    return None

def write_last_ip_address(ip_address, file_path="last_ip.txt"):
  """Writes the current IP address to a file."""
  with open(file_path, "w") as f:
    f.write(ip_address)


def fetch_spreadsheet_data():
  """Fetch data from the public Google Sheets."""
  gc = gspread.service_account(filename='service_account.json')
  sheet = gc.open_by_url(SPREADSHEET_URL).sheet1
  return sheet.get_all_records()


async def check_subscriptions():
  """Check subscriptions and send notifications."""
  try:
    logging.info("Start checking subscriptions!")
    data = fetch_spreadsheet_data()
    today = datetime.today()

    for subscription in data:
      try:
        # Parse the subscription end date
        end_date = datetime.strptime(subscription['End Date'], "%d-%m-%Y")
      except ValueError:
        logging.error(
          f"Invalid date format for subscription: {subscription['Subscription']}")
        continue

      # Calculate days left
      days_left = (end_date - today).days + 1

      # Notify if the subscription matches any threshold
      if days_left in NOTIFY_DAYS:
        await send_notification(subscription, days_left)

  except Exception as e:
    # Capture and send error details
    error_message = traceback.format_exc()
    await send_error_notification(error_message)


if __name__ == "__main__":
  asyncio.run(check_subscriptions())

  async def main():
    logging.info("Script started.")
    current_ip = get_current_ip_address()
    if current_ip:
      last_ip = read_last_ip_address()

      if last_ip != current_ip:
        await send_ip_change_notification(current_ip, last_ip)
        write_last_ip_address(current_ip)
      else:
        logging.info(f"IP address has not changed: {current_ip}")
    else:
      logging.error("Could not retrieve current IP address.")
    logging.info("Script finished.")
  
  asyncio.run(main())
