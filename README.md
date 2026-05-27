<h1 align="center">Whisper Bot</h1>

<p align="center">
  <a href="https://github.com/bisnuray/WhisperBot/stargazers"><img src="https://img.shields.io/github/stars/bisnuray/WhisperBot?color=blue&style=flat" alt="GitHub Repo stars"></a>
  <a href="https://github.com/bisnuray/WhisperBot/issues"><img src="https://img.shields.io/github/issues/bisnuray/WhisperBot" alt="GitHub issues"></a>
  <a href="https://github.com/bisnuray/WhisperBot/pulls"><img src="https://img.shields.io/github/issues-pr/bisnuray/WhisperBot" alt="GitHub pull requests"></a>
  <a href="https://github.com/bisnuray/WhisperBot/graphs/contributors"><img src="https://img.shields.io/github/contributors/bisnuray/WhisperBot?style=flat" alt="GitHub contributors"></a>
  <a href="https://github.com/bisnuray/WhisperBot/network/members"><img src="https://img.shields.io/github/forks/bisnuray/WhisperBot?style=flat" alt="GitHub forks"></a>
</p>

<p align="center">
  <em>Whisper Bot: Send secret, encrypted messages in Telegram groups via inline mode. Easy-to-use, supports private messaging without being part of the group.</em>
</p>
<hr>

## Features

- 🌐 **Inline Mode Support**: Send whisper messages without adding the bot to a group.
- 💬 **Secret Messaging**: Messages are only visible to the sender and the intended recipient.
- 🔄 **Help and Back Button**: Easily access the help menu and navigate back with built-in buttons.
- 📎 **User-Friendly**: Simply use the bot in the inline mode to send private messages easily.

## Requirements

Before you begin, ensure you have met the following requirements:

- Python 3.8 or higher.
- MongoDB database URI (MongoDB Atlas recommended).
- A Telegram bot token (you can get one from [@BotFather](https://t.me/BotFather) on Telegram).
- API ID and Hash: You can get these by creating an application on [my.telegram.org](https://my.telegram.org).

## Configuration

1. Open the `config.py` file in your preferred text editor.
2. Replace the following placeholders with your actual credentials:

* **`API_ID`** → Get it from [my.telegram.org](https://my.telegram.org?utm_source=chatgpt.com)
* **`API_HASH`** → Get it from [my.telegram.org](https://my.telegram.org?utm_source=chatgpt.com)
* **`BOT_TOKEN`** → Obtain it from [@BotFather](https://t.me/BotFather?utm_source=chatgpt.com)
* **`BOT_USERNAME`** → Your bot username created via [@BotFather](https://t.me/BotFather?utm_source=chatgpt.com)
* **`MONGO_URI`** → Your MongoDB connection URI from [MongoDB Atlas](https://www.mongodb.com/cloud/atlas?utm_source=chatgpt.com)

## How to Set Up Inline Mode

To enable inline mode for your bot, follow these steps:

   - Open a chat with **BotFather** in Telegram.
   - Send the command `/setinline` to BotFather.
   - Choose the bot for which you want to enable inline mode.
   - After that, send a sample text like: `Hi` or `Hello`.

For more information on inline bots, refer to the [Telegram Bot Documentation](https://core.telegram.org/bots/inline).


## Deploy the Bot

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

✨ **Note**: If you found this repo helpful, please fork and star it. Also, feel free to share with proper credit!
