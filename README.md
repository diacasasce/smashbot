# Bot Installation and Setup Guide

Follow these steps to install and run the bot for playing Super Smash Bros. Melee with Slippi:

## Step 1: Slippi Launcher

Download and install the Slippi Launcher from [slippi.gg](https://slippi.gg).

## Step 2: Download ISO Image

Download the game's ISO image from [vimm.net](https://vimm.net/vault/7818).

## Step 3: Replace Gecko Code File

Replace the `GALE01r2.ini` Gecko code file in your Slippi Dolphin with the one provided in the this repository.

## Step 4: Create a .env File Set Environment Variables

Create a `.env` file to store your environment variables and set the following environment variables:

- `DOLPHIN_EXEC_PATH` to your Slippi Dolphin executable path.
- `ISO_PATH` to the location of your game's `.ciso` file.

## Step 5: Install libmelee

Install the `libmelee` library by running the following command:

```bash
   pip install libmelee
```

## Step 6: Install dotenv

Install the `dotenv` library by running the following command:

```bash
   pip install python-dotenv
```

## Step 7: Run the game

Run the game by running the following command:

```bash
   python run_game.py
```

## Keyboard Controller Setup

If you want to play the bot, you can set up a keyboard controller. The button mapping configuration can be found in the `run_game` script and is based on the provided image.

![controlmappingg](./ControlMapping.png)

**IMPORTANT**: When setting up the bot, make sure to only modify the bot file.

That's it! You should now have the environment set upand configured to play Super Smash Bros. Melee with Slippi, and run the bot.

for additional information on the libmellee options be sure to check the [libmelee documentation](https://libmelee.readthedocs.io/)

# Happy smashing!
