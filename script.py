import os
from dotenv import load_dotenv
import gspread
from datetime import datetime, timedelta
from telegram import Bot
import logging
import asyncio
import traceback

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

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


async def send_error_notification(error_message):
  """Send an error notification via Telegram bot."""
  message = (
    f"🚨 **Subscription Checker Error** 🚨\n\n"
    f"An error occurred while running the script:\n\n"
    f"```\n{error_message}\n```"
  )
  await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")


def fetch_spreadsheet_data():
  """Fetch data from the public Google Sheets."""
  gc = gspread.service_account(filename='service_account.json')
  sheet = gc.open_by_url(SPREADSHEET_URL).sheet1
  return sheet.get_all_records()


async def check_subscriptions():
  """Check subscriptions and send notifications."""
  try:
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
