from bot import Bot
import melee

class BotImpl(Bot):

  def __init__(self, port, character, costume, console):
    self.character = melee.Character.LINK
    super().__init__(port, character, costume, console)
  
  def play(self, gamestate):
    self.reviewDistance(gamestate)  

  def reviewDistance(self, gamestate):
    if gamestate.distance < 20:
      self.spinAttack(gamestate)
    elif gamestate.distance > 40 and gamestate.distance < 60 :    
      self.throwBoomerang(gamestate)
    else:
      self.controller.release_all()
  
  def spinAttack(self, gamestate):
    self.controller.tilt_analog(melee.enums.Button.BUTTON_MAIN, 0.5, 1)
    self.controller.press_button(melee.enums.Button.BUTTON_B)

  def throwBoomerang(self, gamestate):
    if  self.reviewOponentPosition(gamestate):
      self.controller.tilt_analog(melee.enums.Button.BUTTON_MAIN, 1, 0.5)
    else:
      self.controller.tilt_analog(melee.enums.Button.BUTTON_MAIN, 0, 0.5)
    self.controller.press_button(melee.enums.Button.BUTTON_B)
  
  def reviewOponentPosition(self, gamestate):
    return gamestate.player[1].x < gamestate.player[2].x

 
