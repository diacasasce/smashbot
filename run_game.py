
#!/usr/bin/python3
import argparse
import signal
import sys
import melee
import bot
import random

# This example program demonstrates how to use the Melee API to run a console,
#   setup controllers, and send button presses over to a console

parser = argparse.ArgumentParser(description='Example of libmelee in action')

parser.add_argument('--debug', '-d', action='store_true',
                    help='Debug mode. Creates a CSV of all game states')
parser.add_argument('--address', '-a', default="127.0.0.1",
                    help='IP address of Slippi/Wii')
parser.add_argument('--dolphin_executable_path', '-e', default=None,
                    help='The directory where dolphin is')
parser.add_argument('--connect_code', '-t', default="",
                    help='Direct connect code to connect to in Slippi Online')

args = parser.parse_args()

Dolphin_executable_path = "/Users/DALEJ/AppData/Roaming/Slippi Launcher/netplay"

# This logger object is useful for retroactively debugging issues in your bot
#   You can write things to it each frame, and it will create a CSV file describing the match
log = None
if args.debug:
    log = melee.Logger()

# Create our Console object.
#   This will be one of the primary objects that we will interface with.
#   The Console represents the virtual or hardware system Melee is playing on.
#   Through this object, we can get "GameState" objects per-frame so that your
#       bot can actually "see" what's happening in the game
console = melee.Console(path=Dolphin_executable_path,
                        slippi_address=args.address,
                        logger=log,
                        fullscreen=False,
                        blocking_input=True
                        )

# Create our Controller object
#   The controller is the second primary object your bot will interact with
#   Your controller is your way of sending button presses to the game, whether
#   virtual or physical.
bot1 = bot.Bot(1, melee.Character.FOX, 0, console);
bot2 = bot.Bot(2, melee.Character.FOX, 0, console);
bot3 = bot.Bot(3, melee.Character.DK, 0, console);

#instantiate each object

# This isn't necessary, but makes it so that Dolphin will get killed when you ^C
def signal_handler(sig, frame):
    console.stop()
    if args.debug:
        log.writelog()
        print("") #because the ^C will be on the terminal
        print("Log file created: " + log.filename)
    print("Shutting down cleanly...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Run the console
console.run()

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
    print("ERROR: Failed to connect the controller 1.")
    sys.exit(-1)
if not bot2.connect():
    print("ERROR: Failed to connect the controller 2.")
    sys.exit(-1)
if not bot3.connect():
    print("ERROR: Failed to connect the controller 3.")
    sys.exit(-1)
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
        bot2.play(gamestate)
        if log:
            log.logframe(gamestate)
            log.writeframe()
    else:
        input("Press enter to continue to next match...")
        # select bot player
        melee.MenuHelper.menu_helper_simple(gamestate,
                                            bot1.controller,
                                            bot1.character,
                                            melee.Stage.RANDOM_STAGE,
                                            args.connect_code,
                                            costume=bot1.costume,
                                            autostart=True,
                                            swag=False)
        melee.MenuHelper.menu_helper_simple(gamestate,
                                            bot2.controller,
                                            bot2.character,
                                            melee.Stage.RANDOM_STAGE,
                                            args.connect_code,
                                            costume=bot2.costume,
                                            autostart=True,
                                            swag=False)
        
        # If we're not in game, don't log the frame
        if log:
            log.skipframe()
        