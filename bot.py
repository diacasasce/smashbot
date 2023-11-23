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
    if gamestate.distance < 5:
      self.controller.press_button(melee.enums.Button.BUTTON_B)
      self.controller.tilt_analog(melee.enums.Button.BUTTON_MAIN, 0.5, 0)
    else:
      randX = random.uniform(0,1)
      randY = random.uniform(0,1)
      randJ = random.uniform(0,1) > 0.5
      
      self.controller.release_button(melee.enums.Button.BUTTON_B)
      if randJ:
        self.controller.press_button(melee.enums.Button.BUTTON_X)
      else:
        self.controller.release_button(melee.enums.Button.BUTTON_X)

      self.controller.tilt_analog(melee.enums.Button.BUTTON_MAIN, randX, randJ)
      