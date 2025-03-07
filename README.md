# Discord Webhook Tools
## Overview
This Python script allows you to manage Discord webhooks. You can:

- Modify webhook details (name, avatar, channel).
- Delete webhooks.
- Send messages (with or without embeds, username, avatar).
- Send infinite messages with custom delays (spamming).

## Prerequisites
- Python 3.6+
- `urllib3` library
Install `urllib3` with:

```bash

pip install urllib3
```

## Setup
The first time you run the script, you’ll be prompted to set a username, which will be saved in `config.json`.

Usage
Run the script:

```bash
python main.py
```
Available options:

- **Change Config**: Update username (How the program calls you).
- **Discord Webhook** Tools: Modify, delete, or send messages via a discord webhook.
- **Open GitHub Repository**: Open the project's GitHub.
- **Exit**: Close the program.
  
## Webhook Management
- Input a webhook URL to verify its validity.
- Modify the webhook's settings or delete it.
- Send messages with options to customize username, avatar, and attachments. (Embed supports)
  
## Contributing
Fork, improve, or report issues via GitHub.
