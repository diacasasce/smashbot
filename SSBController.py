## import 
import melee
import configparser

import os
import platform

class SSBController:
  def __init__(self, console,port, controller_name):
    self.console = console
    self.controller = melee.Controller(console=console,
                                       port=port,
                                       type=melee.ControllerType.GCN_ADAPTER)
    self.setup_keyboard_controller(port, controller_name)

  def setup_keyboard_controller ( self , port, controller_name ):
    print("Setting up keyboard controller for port " + str(port))
    # pipes_path = self.console.get_dolphin_pipes_path(port)
    # #Reads in dolphin's controller config file
    controller_config_path = self.console._get_dolphin_config_path() + "GCPadNew.ini"
    config = configparser.ConfigParser()
    config.read(controller_config_path)

    # add keyboard Controller
    section = "GCPad" + str(port)
    if not config.has_section(section):
      config.add_section(section)
    config.set(section, 'Device', controller_name)
    config.set(section, 'Buttons/A', 'SPACE')
    config.set(section, 'Buttons/B', 'LSHIFT')
    config.set(section, 'Buttons/X', 'RSHIFT')
    config.set(section, 'Buttons/Y', 'LMENU')
    config.set(section, 'Buttons/Z', 'Button Z')
    config.set(section, 'Buttons/L', 'Button L')
    config.set(section, 'Buttons/R', 'Button R')
    config.set(section, 'Buttons/Threshold', '50.00000000000000')
    config.set(section, 'Main Stick/Up', 'W')
    config.set(section, 'Main Stick/Down', 'S')
    config.set(section, 'Main Stick/Left', 'A')
    config.set(section, 'Main Stick/Right', 'D')
    config.set(section, 'Triggers/L', 'Button L')
    config.set(section, 'Triggers/R', 'Button R')
    config.set(section, 'Main Stick/Modifier', 'Shift_L')
    config.set(section, 'Main Stick/Modifier/Range', '50.000000000000000')
    config.set(section, 'Main Stick/Radius', '100.000000000000000')
    config.set(section, 'D-Pad/Up', 'up')
    config.set(section, 'D-Pad/Down', 'DOWN')
    config.set(section, 'D-Pad/Left', 'LEFT')
    config.set(section, 'D-Pad/Right', 'RIGHT')
    config.set(section, 'Buttons/Start', 'return')
    config.set(section, 'C-Stick/Up', 'Axis C Y +')
    config.set(section, 'C-Stick/Down', 'Axis C Y -')
    config.set(section, 'C-Stick/Left', 'Axis C X -')
    config.set(section, 'C-Stick/Right', 'Axis C X +')
    config.set(section, 'C-Stick/Radius', '100.000000000000000')
    config.set(section, 'Triggers/L-Analog', 'Axis L -+')
    config.set(section, 'Triggers/R-Analog', 'Axis R -+')
    config.set(section, 'Triggers/Threshold', '90.00000000000000')
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

