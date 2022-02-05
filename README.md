# Discord Trivia Bot

This Discord Bot allows users to play interactive trivia games that are fetched from the [opentdb trivia API](https://opentdb.com/).

## Description

Before the trivia game begins, users are able to select what category of trivia they would like to answer and the difficulty of the questions. Then a sequence of multiple-choice questions is asked by the Trivia Bot, to which the user responds with their answer choices. 

The bot keeps a score of how many questions are answered correctly/incorrectly and displays this score to the user. The bot only responds to input from the user who invokes the bot. All other users' messages in the channel are ignored during the duration of the trivia game.

## Getting Started

### Dependencies

* Python3 (developed using 3.8.12)
  * Pip package [discordpy](https://discordpy.readthedocs.io/en/stable/)

### Installing

* Install python dependencies by running `poetry install` in the project directory.

### Executing program

* You will notice an environment variable set that contains the discord bot's token. You will need to either set this environment variable yourself or replace it with your bot token. Instructions to do so are [here](https://discordpy.readthedocs.io/en/stable/discord.html).

* Ultimately, the bot will be invoked with the following simple command:
  ```python
  python3 main.py
  ```

## Authors

Contributors names and contact info

ex. Dominique Pizzie  
ex. [@DomPizzie](https://twitter.com/dompizzie)

## Version History

* 0.1
    * Initial Release

## Acknowledgments

Inspiration, code snippets, etc.
* [discordpy](https://discordpy.readthedocs.io/en/stable/discord.html)
* [CodeCamp Tutorial](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/)