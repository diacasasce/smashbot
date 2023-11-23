## import 
import melee
import random
## create bot class

class  Bot:

  def __init__(self, port, character, costume, console):
    self.port = port
    self.character = character
    self.costume = costume
    self.controller = melee.Controller(console=console,
                                       port=self.port,
                                       type=melee.ControllerType.STANDARD)

  def connect(self):
    return self.controller.connect()
  
  def play(self, gamestate):
    control = self.controller  # Local variable for easier access
    bot = gamestate.players[self.port]
    bot_position = bot.position
    opponent = gamestate.players[2]
    opponent_position = opponent.position
    size_stage = 50

    # Print the positions to the console
    print(f"My X={bot_position.x}, Y={bot_position.y} pika: X={opponent_position.x}, Y={opponent_position.y} game distance {gamestate.distance}")

    # dont jump of the stage!
    if abs(bot_position.x) > size_stage:
      direction = bot_position.x > 0
      control.tilt_analog(melee.enums.Button.BUTTON_MAIN, int(not direction), 0.5)
      if not bot.on_ground:
        control.press_button(melee.enums.Button.BUTTON_X)
    else:
      # follow the opponent
      follow = bot.x < opponent.x
      control.tilt_analog(melee.enums.Button.BUTTON_MAIN, int(follow), 0.5)

      control.release_button(melee.enums.Button.BUTTON_B)

      if bot.y < opponent.y and bot.on_ground:
        print(f"jump!")
        control.press_button(melee.enums.Button.BUTTON_X)
      else:
        control.release_button(melee.enums.Button.BUTTON_X)

      if gamestate.distance < 15 and gamestate.distance > 5:
        control.press_button(melee.enums.Button.BUTTON_B)
        control.tilt_analog(melee.enums.Button.BUTTON_MAIN, 0.5, 0.5)
      if gamestate.distance < 5:
        control.press_button(melee.enums.Button.BUTTON_A)
        control.tilt_analog(melee.enums.Button.BUTTON_MAIN, 0.5, 0.5)




      