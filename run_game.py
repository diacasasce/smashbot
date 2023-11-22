#!/usr/bin/python3
import argparse
import signal
import sys
import melee

import os
from dotenv import load_dotenv

# 
import bot
import bot_impl
import SSBController

load_dotenv() 

Dolphin_executable_path = os.getenv("DOLPHIN_EXEC_PATH")
ISO_Path = os.getenv("ISO_PATH")



# This example program demonstrates how to use the Melee API to run a console,
#   setup controllers, and send button presses over to a console

parser = argparse.ArgumentParser(description='Example of libmelee in action')


# Create our Console object.
#   This will be one of the primary objects that we will interface with.
#   The Console represents the virtual or hardware system Melee is playing on.
#   Through this object, we can get "GameState" objects per-frame so that your
#       bot can actually "see" what's happening in the game
console = melee.Console(path=Dolphin_executable_path,
                        dolphin_home_path=Dolphin_executable_path,
                        fullscreen=False,
                        blocking_input=True
                        )

# Create our Controller object or bots
#   The controller is the second primary object your bot will interact with
#   Your controller is your way of sending button presses to the game, whether
#   virtual or physical.
#   Add a Bot object for each port you want to use
bot1 = bot_impl.BotImpl(1, melee.Character.LINK, 0, console)
# you can add additional bot agents
# be sure to keep it at maximum 4 players over all (bots and keyboard)
# to add them just create a new class instance like this:
# bot2 = bot.Bot( [player port ], [player character], 0, console)
#   Add a controller object if oyu want to use a physical controller
print("Connecting to keyboard controller...")
# if you want to use the keboard to play leave 
# the following line uncommented to play in port 2
human_controller = SSBController.SSBController(console,2)

# be sure to check the maximum player instances should be 4 
# and each instance should have a different port assign to it


# This isn't necessary, but makes it so that Dolphin will get killed when you ^C
def signal_handler(sig, frame):
    console.stop()
    print("Shutting down cleanly...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Run the console
console.run(iso_path=ISO_Path)

# Connect to the console
print("Connecting to console...")
if not console.connect():
    print("ERROR: Failed to connect to the console.")
    sys.exit(-1)
print("Console connected")

# Plug our controller in
#   Due to how named pipes work, this has to come AFTER running dolphin
#   NOTE: If you're loading a movie file, don't connect the controller,
#   dolphin will hang waiting for input and never receive it
print("Connecting controller to console...")
if not bot1.connect():
    print("ERROR: Failed to connect the Bot to port 1.")
    sys.exit(-1)
# if additional bots are added, connect them here the same way as above


print("Controller connected")

costume = 0
framedata = melee.framedata.FrameData()

# Main loop
while True:
    # "step" to the next frame
    gamestate = console.step()
    if gamestate is None:
        continue
    # The console object keeps track of how long your bot is taking to process frames
    #   And can warn you if it's taking too long
    if console.processingtime * 1000 > 12:
        print("WARNING: Last frame took " + str(console.processingtime*1000) + "ms to process.")
    # What menu are we in?
    if gamestate.menu_state in [melee.Menu.IN_GAME, melee.Menu.SUDDEN_DEATH]:
        ## move function of each bot 
        bot1.play(gamestate)
        # if additional bots are added, call their play function here the same way as above

    else:
        # select bot player
        melee.MenuHelper.menu_helper_simple(gamestate,
                                            bot1.controller,
                                            bot1.character,
                                            melee.Stage.RANDOM_STAGE,
                                            '',
                                            costume=bot1.costume,
                                            autostart=True,
                                            swag=False)
        # if additional bots are added, select them here the same way as above
