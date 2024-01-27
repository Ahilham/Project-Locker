# IP-based security location retrieval

## Overview

The program uses Tkinter to create a simple password input UI. It allows user to create or change password if needed. The script communicates with a server to send the device's location via telegram bot in case of multipke incorrect attempts.

## Table of Contents

1. [Telegram Bot with Location Tracking](#1-telegram-bot-with-location-tracking)
2. [Tkinter-based Password Management](#2-tkinter-based-password-management)

## 1. Telegram Bot with Location Tracking

### Overview

This Python script implements a Telegram bot that provides location information of the device running the bot. The bot supports various commands such as `/start`, `/send_loc`, and `/send_chat_id`.

### Features

- **Location Tracking**: Utilizes the `get_location` module to fetch the device's location.
- **Socket Server**: Implements a simple socket server to handle incoming connections and trigger events.
- **Telegram Commands**: Supports commands for interacting with the bot.

### Getting Started

- **Prerequisites**: Python 3.x
- **Setup**: Clone the repository, install dependencies, and update script variables.

### Usage

1. Go to "https://sendpulse.com/knowledge-base/chatbot/telegram/create-telegram-chatbot" to create a bot token and its username.
2. Create a groupchat without the bot first and then add the bot after it has been created.
3. Start a conversation with the bot using the `/start` command. 
4. Use `/send_loc` to receive the device's current location.
5. Use `/send_chat_id` to receive the chat ID associated with the conversation.

### Additional Information

- **Dependencies**: Ensure required dependencies are installed using `pip install -r requirements.txt`.
- **Security**: Take precautions with sensitive information, such as the bot token.

## 2. Tkinter-based Password input UI

### Overview

This Python script uses Tkinter to create a simple password input UI. It allows users to enter a password and, if needed, create or change the password. The script communicates with the telegram bot server to send the device's location in case of multiple incorrect attempts.

### Features

- **Password Management**: Users can enter a password and create/change it.
- **Socket Communication**: The script communicates with a server to send a warning message in case of repeated incorrect attempts.

### Getting Started

- **Prerequisites**: Python 3.x
- **Setup**: Clone the repository, install dependencies, and update script variables.

### Usage

1. Make sure the '/start' command has been initialized in the telegram group that contains the telegram bot.
2. Enter a password using the entry field.
3. Use the "Enter" button to check the password.
4. Use the "Create Password" button to create or change the password.

## Contributing

Contributions are welcome! If you have suggestions or bug reports, please create an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Author

Ahmad Nur Ilham






