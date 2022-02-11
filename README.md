# Wordy Discord Bot

Wordy is a little Discord bot that plays a Wordle-like game. This repository accompanies a [tutorial blog post](https://thecodingchannel.hashnode.dev/full-tutorial-we-build-a-python-wordle-clone-discord-bot-with-disnake) on Hashnode which you can read to understand how it was made. A version with more features can be found at https://github.com/thecodingchannel/wordy-discord-bot.


## Setup & Requirements

Before running or working on this code you will need to install:

 * Python 3.10+
 * Pipenv


Then to get started:
```sh
pipenv sync --python 3.10
pipenv shell
```


## Run the Bot

Before you can run this you must first register a bot in Discord, give it the required permissions and add it to your server. Please see our blog post for details on how to do this, then make a file called `.env` with the following contents:
```
DISCORD_TOKEN=your_discord_bot_token_here
```


## The Coding Channel

Our mission is to help you understand code. Follow us on [Twitter](https://twitter.com/CodingChannel) or check out our [YouTube channel](https://www.youtube.com/channel/UCIzSzivWvtLIWrWoOVyvVKw).
