Before you begin, ensure you have met the following requirements:

- Python 3.8 or higher.
- `pyrofork` library.
- MongoDB database URI (MongoDB Atlas recommended).
- A Telegram bot token (you can get one from [@BotFather](https://t.me/BotFather) on Telegram).
- API ID and Hash: You can get these by creating an application on [my.telegram.org](https://my.telegram.org).

## Installation
To install `pyrofork` run the following command:
```bash
pip install pyrofork
```
**Note: If you previously installed `pyrogram`, uninstall it before installing `pyrofork`.**
## Configuration

1. Open the `config.py` file in your favorite text editor.
2. Replace the placeholders for `API_ID`, `API_HASH`, and `BOT_USERNAME` with your actual values:
   - **`API_ID`**: Your API ID from [my.telegram.org](https://my.telegram.org).
   - **`API_HASH`**: Your API Hash from [my.telegram.org](https://my.telegram.org).
   - **`BOT_TOKEN`**: The token you obtained from [@BotFather](https://t.me/BotFather).
   - **`BOT_USERNAME `**: Your Created Bot Username from [@BotFather](https://t.me/BotFather).
1. Open the `config.py` file in your preferred text editor.
2. Replace the following placeholders with your actual credentials:
* **`API_ID`** → Get it from [my.telegram.org](https://my.telegram.org?utm_source=chatgpt.com)
* **`API_HASH`** → Get it from [my.telegram.org](https://my.telegram.org?utm_source=chatgpt.com)
* **`BOT_TOKEN`** → Obtain it from [@BotFather](https://t.me/BotFather?utm_source=chatgpt.com)
* **`BOT_USERNAME`** → Your bot username created via [@BotFather](https://t.me/BotFather?utm_source=chatgpt.com)
* **`MONGO_URI`** → Your MongoDB connection URI from [MongoDB Atlas](https://www.mongodb.com/cloud/atlas?utm_source=chatgpt.com)

## How to Set Up Inline Mode

@@ -65,27 +57,30 @@
```sh
git clone https://github.com/bisnuray/WhisperBot
cd WhisperBot
pip install -r requirements.txt
python whisper.py
```

## Bot Commands

- **/start**: Sends a welcome message with instructions on how to use the bot.
- **Inline Query**: Use `@LockTextBot your message @username` in an inline query to send a whisper message. `@LockTextBot` Example Bot use your own bot.

## How to Use

1. **Inline Mode**:
   - Use the bot in inline mode by typing `@LockTextBot <your whisper> @<recipient_username> or userid`.
   - For example: `@LockTextBot hello this is a test messages @BisnuRay`.
   - Only the sender and the recipient will be able to view the secret message.

## Note

- **User ID Restriction**: If a user has not started the bot, you will not be able to send secret messages to them using their user ID. Ensure that the recipient has interacted with the bot at least once by clicking **Start**.

## Author

- Name: Bisnu Ray
- Telegram: [@itsSmartDev](https://t.me/itsSmartDev)
