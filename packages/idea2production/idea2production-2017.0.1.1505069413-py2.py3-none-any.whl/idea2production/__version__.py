import time

hrl_logo = """
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
M                                                                                                  M
M    M""MMMMM""MM                   dP                                                             M
M    M  MMMMM  MM                   88                                                             M
M    M         `M .d8888b. 88d888b. 88d888b. .d8888b. 88d888b.                                     M 
M    M  MMMMM  MM 88'  `88 88'  `88 88'  `88 88'  `88 88'  `88                                     M 
M    M  MMMMM  MM 88.  .88 88       88.  .88 88.  .88 88                                           M 
M    M  MMMMM  MM `88888P8 dP       88Y8888' `88888P' dP                                           M     
M    MMMMMMMMMMMM                                                                                  M
M                                                                                                  M
M    MMMMMMMMMMMM                                                                                  M
M    MM        MM                                                       dP                         M
M    MM  mmmm,  M                                                       88                         M
M    MM'       .M .d8888b. .d8888b. .d8888b. .d8888b. 88d888b. .d8888b. 88d888b.                   M
M    MM  MMMb. "M 88ooood8 Y8ooooo. 88ooood8 88'  `88 88'  `88 88'  `"" 88'  `88                   M 
M    MM  MMMMM  M 88.  ...       88 88.  ... 88.  .88 88       88.  ... 88    88                   M
M    MM  MMMMM  M `88888P' `88888P' `88888P' `88888P8 dP       `88888P' dP    dP                   M
M    MMMMMMMMMMMM                                                                                  M
M                                                                                                  M
M    MMMMMMMMMMM                                                                                   M
M    M""MMMMMMMM          dP                                    dP                                 M
M    M  MMMMMMMM          88                                    88                                 M
M    M  MMMMMMMM .d8888b. 88d888b. .d8888b. 88d888b. .d8888b. d8888P .d8888b. 88d888b. dP    dP    M
M    M  MMMMMMMM 88'  `88 88'  `88 88'  `88 88'  `88 88'  `88   88   88'  `88 88'  `88 88    88    M
M    M  MMMMMMMM 88.  .88 88.  .88 88.  .88 88       88.  .88   88   88.  .88 88       88.  .88    M
M    M         M `88888P8 88Y8888' `88888P' dP       `88888P8   dP   `88888P' dP       `8888P88    M
M    MMMMMMMMMMM                                                                            .88    M
M                                                                                        d8888P    M
M                                                                                                  M
MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
"""
print(hrl_logo)
__version__ = '2017.0.1.{timestamp}'.format(timestamp=int(time.time()))
