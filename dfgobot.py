## import 
import melee
import random
import time
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
    
    if gamestate.player[1].y > gamestate.player[2].y or gamestate.player[2].stock == 0:
        self.controller.tilt_analog(melee.enums.Button.BUTTON_MAIN, 0.5, 0)
        
    elif gamestate.distance < 3:
        self.controller.press_button(melee.enums.Button.BUTTON_B)
        self.controller.tilt_analog(melee.enums.Button.BUTTON_MAIN, 0.5, 0)
    else:
        left = gamestate.player[1].x < gamestate.player[2].x
        self.controller.tilt_analog(melee.enums.Button.BUTTON_MAIN, int(left), 0.5)
        self.controller.release_button(melee.enums.Button.BUTTON_B)
        
        if gamestate.player[1].y < gamestate.player[2].y:
          self.controller.press_button(melee.enums.Button.BUTTON_X)
          self.controller.tilt_analog(melee.enums.Button.BUTTON_MAIN, 0.5, 0)
          self.controller.press_button(melee.enums.Button.BUTTON_B)
        else:
          self.controller.release_button(melee.enums.Button.BUTTON_X)
          
        self.controller.release_button(melee.enums.Button.BUTTON_B)
        
