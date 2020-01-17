""" 
This configuration file provides settings for each of the classes and is split 
into three sections: BoardOCR settings, BoardSolver settings, and CommandWriter 
settings.

Author: David Chen
"""

from pathlib import Path

""" BoardOCR settings """
DEBUG = False  # save individual crops for tweaking widths/heights
MAIN_DIR = Path('./')
PATH_TO_IMG = 'ruzzletest.png'

# OCR constants
OCR_CONFIG = r'--psm 10'  # char only
LANG = 'Alte'  # custom pytesseract trained data
CHAR_X0, CHAR_Y0 = 80, 895  # coords of top left corner of top left letter
CHAR_WIDTH, CHAR_HEIGHT = 130, 100  # width and height of crops
GAP_X, GAP_Y = 265, 264  # gap between letters
MULT_X0, MULT_Y0 = 60, 890  # coords of multiplier of top left letter


""" BoardSolver settings """
PRINT_INFO = False  # prints info about board when writing words to file

# Ruzzle Rules
MIN_WORD_LEN = 2
MAX_WORD_LEN = 12
BOARD_SIZE = 4

# These options can be tweaked to improve performance if necessary.
PREFIX_LOWER_BOUND = 2
PREFIX_UPPER_BOUND = 8


""" CommandWriter settings """
PATH_TO_COMMANDS = 'ruzzle_swipe.sh'
CHAR_MID_X0, CHAR_MID_Y0 = 145, 945  # coords of middle of top left letter
