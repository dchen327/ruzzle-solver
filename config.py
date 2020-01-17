from pathlib import Path

""" OCR settings """
DEBUG = False  # save individual crops for tweaking widths/heights
MAIN_DIR = Path('./')
PATH_TO_IMG = 'boards/board6.png'
OCR_CONFIG = r'--psm 10'  # char only
LANG = 'Alte'  # custom pytesseract trained data
CHAR_X0, CHAR_Y0 = 80, 895  # coords of top left corner of top left letter
CHAR_WIDTH, CHAR_HEIGHT = 130, 100  # width and height of crops
GAP_X, GAP_Y = 265, 264  # gap between letters
MULT_X0, MULT_Y0 = 60, 890  # coords of multiplier of top left letter



""" CommandWriter settings """
PATH_TO_COMMANDS = 'ruzzle_swipe.sh'
CHAR_MID_X0, CHAR_MID_Y0 = 145, 945  # coords of middle of top left letter
