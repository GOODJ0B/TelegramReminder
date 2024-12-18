# Telegram Subscription Reminder

This project is a Telegram bot that sends subscription reminders based on data from a Google Sheets document.

## Prerequisites

- Python 3.9 or higher
- A Google Cloud project with a service account
- A Telegram bot token

## Setup

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/TelegramReminder.git
cd TelegramReminder
```

### 2. Install Dependencies

Install the required Python packages using `pip`:

```sh
pip install python-dotenv gspread google-auth python-telegram-bot
```

### 3. Create the `.env` File

Create a `.env` file in the project directory with the following content:

```dotenv
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
GOOGLE_SHEET_URL=your_google_sheet_url
```

Replace `your_telegram_bot_token`, `your_telegram_chat_id`, and `your_google_sheet_url` with your actual values.

### 4. Create the `service_account.json` File

Create a `service_account.json` file in the project directory with your Google Cloud service account credentials. The file should look like this:

```json
{
  "type": "service_account",
  "project_id": "your_project_id",
  "private_key_id": "your_private_key_id",
  "private_key": "your_private_key",
  "client_email": "your_client_email",
  "client_id": "your_client_id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "your_client_x509_cert_url",
  "universe_domain": "googleapis.com"
}
```

Replace the placeholders with your actual service account details.

### 5. Update the Script

Ensure the `script.py` file has the correct import statements and logic as shown in the provided code.

### 6. Run the Script

You can run the script manually using:

```sh
python3 script.py
```

Alternatively, you can use the `update_and_run.sh` script to update the repository and run the script:

```sh
./update_and_run.sh
```

Make sure the `update_and_run.sh` script has execute permissions:

```sh
chmod +x update_and_run.sh
```

## Usage

The script will fetch subscription data from the specified Google Sheets document and send reminders via the Telegram bot based on the defined notification thresholds.

## Troubleshooting

- Ensure all dependencies are installed in the correct Python environment.
- Verify that the `.env` and `service_account.json` files contain the correct information.
- Check the logs for any error messages and address them accordingly.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.