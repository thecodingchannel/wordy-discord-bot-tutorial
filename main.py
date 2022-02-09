'''
This file contains the Discord interaction, implemented using the Disnake library.
'''
from dotenv import load_dotenv
load_dotenv()

import os
from typing import Callable

import disnake
from disnake.ext import commands

from wordy_types import EndResult
from game_store import clear_game, get_info_for_user, set_info_for_user
from wordy_chat import begin_game, enter_guess, render_result
from dictionary import get_acceptable_words, get_alphabet, get_solution_words


# Create the bot

bot = commands.Bot(command_prefix="/", description="Wordy Guessing Game", help_command=None,
    activity=disnake.Game(name='with dictionaries'))


# Add the prefix commands

@bot.command(name='wordy', description='Guess a word in your own personal Wordy game!')
async def wordy_prefix(ctx: commands.Context, guess: str):
    await handle_new_guess(guess, ctx.author, ctx.reply)

@bot.command(name='surrender', help="Give up and reveal the word!")
async def surrender_prefix(ctx: commands.Context):
    await handle_surrender(ctx.author, ctx.reply)

@bot.command(name='help', help="How to play Wordy")
async def help_prefix(ctx: commands.Context):
    await handle_help(ctx.author, ctx.reply)

@bot.command(name='show', help="Show current board state")
async def show_prefix(ctx: commands.Context):
    await handle_show(ctx.author, ctx.reply)


# Add the new-style slash commands

@bot.slash_command(name='wordy', description='Guess a word in your own personal Wordy game!')
async def wordy_slash(inter, guess:str):
    await handle_new_guess(guess, inter.author, inter.response.send_message)

@bot.slash_command(name='surrender', description="Give up and reveal the word!")
async def surrender_slash(inter):
    await handle_surrender(inter.user, inter.response.send_message)

@bot.slash_command(name='help', description="How to play Wordy")
async def help_slash(inter):
    inter: disnake.Interaction = inter
    await handle_help(inter.user, inter.response.send_message)

@bot.slash_command(name='show', description="Show current board state")
async def show_slash(inter):
    await handle_show(inter.user, inter.response.send_message)


# Common functionality

HELP_TEXT = """**Wordy is a Wordle-like clone that let's you play within Discord.**

Start a game by typing `/wordy <guess>` (replace <guess> with your word) and guess the word the game has secretly chosen. If Wordy returns a gray icon ⬛ the letter does not exist. If it returns a yellow icon 🟨 the letter exists but is on the wrong spot. If Wordy returns a green icon 🟩 the letter is on the correct spot.

New games are started automatically.

To re-show your current board type `/show`.
To give up use `/surrender`.
"""


async def handle_help(user: disnake.User|disnake.Member|None, reply: Callable):
    '''
    Show the help text.
    '''
    await reply(f"Hey {user.mention}, we got the help you need...", embed=disnake.Embed(description=HELP_TEXT))


async def handle_show(user: disnake.User|disnake.Member, reply: Callable):
    '''
    Show the current board state.
    '''
    game = get_info_for_user(user.id)

    if game is None:
        await reply("You haven't started a game yet!")
        return

    # Render the results
    description = "Your board:\n"
    description += "```"
    for result,word in zip(game.results, game.board_state):
        description += f"{render_result(result)} {word}\n"
    description += "```"

    await reply(description)


async def handle_surrender(user: disnake.User | disnake.Member, reply: Callable):
    '''
    Give up and reveal the word.
    '''
    game = get_info_for_user(user.id)
    if game is None:
        await reply("You haven't started a game yet!")
        return

    answer = game.answer
    game = None
    set_info_for_user(user.id, game)

    await reply(f"You coward! 🙄\nYour word was `{answer}`!")


async def handle_new_guess(guess: str, user: disnake.User|disnake.Member, reply: Callable):
    '''
    Enter a new guess, starting a new game automatically.
    '''
    # Validate input
    if not guess:
        await reply(f"To play Wordy simply type `/wordy <guess>` to start or continue your own personal game.")
        return

    guess = guess.lower()
    guess = guess.removeprefix('guess:') # handles Discord mobile oddness
    if len(guess) != 5:
        await reply("Guess must be 5 letters long")
        return

    # Make sure the word is valid
    if guess not in get_solution_words() and guess not in get_acceptable_words():
        await reply("That's not a valid word!")
        return

    # Gather text to return to the user
    description = ''

    # Make sure we have a game running, starting a new one if not
    game = get_info_for_user(user.id)
    if not game or game.state != EndResult.PLAYING:
        description += "Starting a new game...\n"
        game = begin_game()
        set_info_for_user(user.id, game)

    # Make sure the user hasn't already guessed this word
    if guess in game.board_state:
        await reply("You've already guessed that word!")
        return

    # Make sure the guess uses only letters from the dictionary
    dictionary = get_alphabet()
    if any(char not in dictionary for char in guess):
        await reply(f"You can only use the following letters: `{dictionary}`")
        return

    # Process the guess
    enter_guess(guess, game)

    # Render the results
    description += "Your results so far:\n"
    description += "```"
    for result,word in zip(game.results, game.board_state):
        description += f"{render_result(result)} {word}\n"
    description += "```"

    # See if the game is over
    if game.state == EndResult.WIN:
        description += f"\nCongratulations! 🎉\nCompleted in {len(game.board_state)} guesses!\n"
        clear_game(user.id)
    elif game.state == EndResult.LOSE:
        description += f"\nNo more guesses! 😭\nYour word was `{game.answer}`!\n"
        clear_game(user.id)

    # Send the response
    embed = disnake.Embed(title="Wordy", description=description.strip('\n'))
    await reply(embed=embed)



if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))
