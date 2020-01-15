"""
Author: David Chen
"""
from PIL import Image
import pytesseract
from pathlib import Path

""" Configure program settings """
MAIN_DIR = Path('./')
PATH_TO_IMG = 'boards/board6.png'
DEBUG = False  # save individual crops for tweaking widths/heights

""" OCR settings """
OCR_CONFIG = r'--psm 10'  # char only
LANG = 'Alte'  # custom pytesseract trained data
CHAR_X0, CHAR_Y0 = 80, 895  # coords of top left corner of top left letter
CHAR_WIDTH, CHAR_HEIGHT = 130, 100  # width and height of crops
GAP_X, GAP_Y = 265, 264  # gap between letters
MULT_X0, MULT_Y0 = 60, 890  # coords of multiplier of top left letter


class BoardOCR:

    def __init__(self, file_path=MAIN_DIR / PATH_TO_IMG):
        self.image = Image.open(file_path)
        self.board = self.get_board()
        self.word_mults = self.get_mults()


    def get_board(self):
        """ Crops the 16 letters and stores values """
        board = [[None] * 4 for _ in range(4)]
        for x in range(4):
            for y in range(4):
                left = CHAR_X0 + x * GAP_X
                right = left + CHAR_WIDTH
                top = CHAR_Y0 + y * GAP_Y
                bottom = top + CHAR_HEIGHT
                imcrop = self.image.crop((left, top, right, bottom))
                if DEBUG:
                    imcrop.save(f'{x}{y}.png')
                char = pytesseract.image_to_string(imcrop, lang=LANG, config=OCR_CONFIG)
                board[y][x] = char

        return board


    def get_mults(self):
        """ Gets multpliers by checking color of pixel """
        rgb_im = self.image.convert('RGB')
        word_mults = [[None] * 4 for _ in range(4)] 
        for x in range(4):
            for y in range(4):
                pix_x, pix_y = MULT_X0 + x*GAP_X, MULT_Y0 + y*GAP_Y
                rgb = rgb_im.getpixel((pix_x, pix_y))
                mult = self.get_multiplier(rgb)
                word_mults[y][x] = mult
        return word_mults


    @staticmethod
    def distance(p1, p2):
        """ Squared distance between 2 points """
        return sum([(p1[i] - p2[i])**2 for i in range(3)])


    @staticmethod
    def get_multiplier(rgb):
        """ Find the multiplier based on color (minimum distance between rgb values) """
        multipliers = {
            (236, 236, 236): '-',
            (11, 131, 12): 'D', 
            (9, 74, 139): 'T', 
            (255, 158, 0): '2', 
            (175, 6, 6): '3'
        }
        min_d = 1000000
        for color in multipliers:
            if BoardOCR.distance(rgb, color) < min_d:
                min_d = BoardOCR.distance(rgb, color)
                mult = multipliers[color]

        return mult


    def get_info(self):
        """ Returns all information about the board """
        return self.board, self.word_mults


if __name__ == '__main__':
    boardOCR = BoardOCR(MAIN_DIR / PATH_TO_IMG)
    print(boardOCR.get_info())