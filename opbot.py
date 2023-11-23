## import 
import melee
import random

from bot import Bot
## create bot class

class OPBot(Bot):

  def __init__(self, port, character, costume, console):
        super().__init__(port, character, costume, console)
        self.bot = None
        self.enemy = None
        self.framedata = melee.framedata.FrameData() 

  def play(self, gamestate):
    self.bot = gamestate.player[self.port]

    self.enemy = OPBot.findEnemy(self.port, gamestate.player)
    if self.enemy is None:
      return

    if self.bot.action == melee.enums.Action.EDGE_HANGING:
      OPBot.simplePressButton(self, 0.5, 0.5, melee.enums.Button.BUTTON_A)
      return

    if self.enemy.action == melee.enums.Action.EDGE_HANGING:
      if gamestate.distance > 15:
        OPBot.getClose(self, gamestate)
      else:
        self.controller.tilt_analog(melee.enums.Button.BUTTON_MAIN, 0.5, 0.5)
        OPBot.simplePressButton(self, 0.5, 0, melee.enums.Button.BUTTON_A)
      return

    if self.bot.off_stage:
      OPBot.survive(self, gamestate) 
      return 

    #attack
    if gamestate.distance <= 20:
      OPBot.attack(self, gamestate)
      return
	  
    #Fire projectile
    if OPBot.fireProjectile(self, gamestate):
      return

    if self.bot.position.y > 20 and random.uniform(0,1) < 0.2:
      self.controller.tilt_analog(melee.enums.Button.BUTTON_MAIN, 0.5, 0.1)
      return

    if not self.enemy.off_stage:
      OPBot.getClose(self, gamestate)
  
  ### Action Methods
       
  def getClose(self, gamestate):
    if self.bot.position.x > self.enemy.position.x:
      move = 0
    else: 
      move = 1
    if gamestate.distance > 10:
      self.controller.tilt_analog(melee.enums.Button.BUTTON_MAIN, move, 0.5)
      
  def survive(self, gamestate):
    if (self.bot.action in [melee.enums.Action.JUMPING_ARIAL_BACKWARD,melee.enums.Action.JUMPING_ARIAL_FORWARD,melee.enums.Action.JUMPING_BACKWARD,melee.enums.Action.JUMPING_FORWARD]):
      return
    if (OPBot.isOutsideLeftEdge(self, gamestate)):
      move = 1
    else: 
      move = 0
    if self.bot.jumps_left > 0:
      self.controller.tilt_analog(melee.enums.Button.BUTTON_MAIN, move, 1)
    else: 
      OPBot.simplePressButton(self, move, 1, melee.enums.Button.BUTTON_B)

  def isOutsideLeftEdge(self, gamestate):
    if self.bot.position.x < -melee.stages.EDGE_POSITION[gamestate.stage]:
      return True
    else: return False

  def fireProjectile(self, gamestate):
    if self.controller.prev.button[melee.enums.Button.BUTTON_B]:
      self.controller.release_button(melee.enums.Button.BUTTON_B)
    
    elif gamestate.distance > 10 and random.uniform(0,1)<0.015:
      self.controller.tilt_analog(melee.enums.Button.BUTTON_MAIN, 0.5, 0.5)
      self.controller.simple_press(0.5, 0.5, melee.enums.Button.BUTTON_B)
      return True
    return False

  def attack(self, gamestate):
    if OPBot.isEnemyOutsidePlatform(self, gamestate):
      return

    xVector = self.enemy.position.x - self.bot.position.x
    yVector = self.enemy.position.y - self.bot.position.y
    if xVector == 0 and yVector == 0:
      return
    xSign = -1 if xVector < 0 else 1
    ySign = -1 if yVector < 0 else 1
    maxValue = max(abs(xVector), abs(yVector))
    x = round(xSign * abs(xVector / maxValue), 1)
    y = round(ySign * abs(yVector / maxValue), 1)
    
    self.controller.tilt_analog_unit(melee.enums.Button.BUTTON_MAIN, x, y)
    if self.controller.prev.button[melee.enums.Button.BUTTON_A]:
      self.controller.release_button(melee.enums.Button.BUTTON_A)
    else:  
      self.controller.press_button(melee.enums.Button.BUTTON_A)

  def findEnemy(myPort, playersDict):
    ports = playersDict.keys()
    for port in ports:
      if port != myPort:
        return playersDict[port]
    return None
    
  def simplePressButton(self, x, y, button):
      if self.controller.prev.button[button]:
        self.controller.release_button(button)
    
      else:
        self.controller.simple_press(x, y, button)		

  def isEnemyOutsidePlatform(self, gamestate):
    if self.enemy.x < -melee.stages.EDGE_POSITION[gamestate.stage] or self.enemy.x > melee.stages.EDGE_POSITION[gamestate.stage]:
      return True
    else: 
      return False
