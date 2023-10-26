## import 
import melee
import configparser

import os
import platform

class SSBController:
  def __init__(self, console,port):
    self.console = console
    self.controller = melee.Controller(console=console,
                                       port=port,
                                       type=melee.ControllerType.GCN_ADAPTER)
    self.setup_keyboard_controller(port)

  def setup_keyboard_controller ( self , port ):
    print("Setting up keyboard controller for port " + str(port))
    # pipes_path = self.console.get_dolphin_pipes_path(port)
    # #Reads in dolphin's controller config file
    controller_config_path = self.console._get_dolphin_config_path() + "GCPadNew.ini"
    config = configparser.ConfigParser()
    config.read(controller_config_path)
    isWindows = platform.system() == "Windows"
    print(platform.system())

    # add keyboard Controller
    section = "GCPad" + str(port)
    if not config.has_section(section):
      config.add_section(section)
    config.set(section, 'Device','DInput/0/Keyboard Mouse' if isWindows else 'Quartz/0/Keyboard & Mouse')
    config.set(section, 'Buttons/A', 'X')
    config.set(section, 'Buttons/B', 'C')
    config.set(section, 'Buttons/X', 'Z')
    config.set(section, 'Buttons/Y', 'V')
    config.set(section, 'Buttons/Z', 'SPACE' if isWindows else 'Space')
    config.set(section, 'Buttons/L', 'Q')
    config.set(section, 'Buttons/R', 'E')
    config.set(section, 'Buttons/Threshold', '50.00000000000000')
    config.set(section, 'Main Stick/Up', 'UP' if isWindows else 'Up Arrow')
    config.set(section, 'Main Stick/Down', 'DOWN' if isWindows else 'Down Arrow')
    config.set(section, 'Main Stick/Left', 'LEFT' if isWindows else 'Left Arrow')
    config.set(section, 'Main Stick/Right', 'RIGHT' if isWindows else 'Right Arrow')
    config.set(section, 'Triggers/L', 'Q')
    config.set(section, 'Triggers/R', 'E')
    config.set(section, 'Main Stick/Radius', '100.000000000000000')
    config.set(section, 'D-Pad/Up', 'I')
    config.set(section, 'D-Pad/Down', 'K')
    config.set(section, 'D-Pad/Left', 'J')
    config.set(section, 'D-Pad/Right', 'L')
    config.set(section, 'Buttons/Start', 'RETURN' if isWindows else 'Return')
    config.set(section, 'C-Stick/Up', 'W')
    config.set(section, 'C-Stick/Down', 'S')
    config.set(section, 'C-Stick/Left', 'A')
    config.set(section, 'C-Stick/Right', 'S')
    config.set(section, 'C-Stick/Radius', '100.000000000000000')
    with open(controller_config_path, 'w') as configfile:
      config.write(configfile)
    dolphin_config_path = self.console._get_dolphin_config_path() + "Dolphin.ini"
    config = configparser.ConfigParser()
    config.read(dolphin_config_path)
    # Indexed at 0. "6" means standard controller, "12" means GCN Adapter
    #  The enum is scoped to the proper value, here
    config.set("Core", 'SIDevice'+str(port-1), '6')
    with open(dolphin_config_path, 'w') as dolphinfile:
      config.write(dolphinfile)

