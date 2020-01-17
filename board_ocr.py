"""
A class for grabbing information about a ruzzle board screenshot.

Constants are defined in config.py and vary for each device. A pretrained
pytesseract model is also required; this should be stored as 
/usr/share/tesseract-ocr/4.00/tessdata/Alte.traineddata. Alte is used because
it most nearly matches the font used in Ruzzle. If DEBUG is enabled in config.py, 
all 16 crops will be stored in MAIN_DIR with names of the format 'xy.png'. This 
is useful for finding the values of constants for cropping, since pytesseract can 
be inaccurate when the letters are improperly cropped.

Author: David Chen
"""
import config as cf
from PIL import Image
import pytesseract
from pathlib import Path


class BoardOCR:

    def __init__(self, file_path=cf.MAIN_DIR / cf.PATH_TO_IMG):
        """ Opens the screenshot, then gets letters and multipliers """
        self.image = Image.open(file_path)
        self.board = self.get_board()
        self.word_mults = self.get_mults()

    def get_board(self):
        """ Crops the 16 letters and stores values """
        board = [[None] * 4 for _ in range(4)]
        for x in range(4):
            for y in range(4):
                left = cf.CHAR_X0 + x * cf.GAP_X
                right = left + cf.CHAR_WIDTH
                top = cf.CHAR_Y0 + y * cf.GAP_Y
                bottom = top + cf.CHAR_HEIGHT
                imcrop = self.image.crop((left, top, right, bottom))
                if cf.DEBUG:
                    imcrop.save(f'{x}{y}.png')
                char = pytesseract.image_to_string(imcrop, lang=cf.LANG, config=cf.OCR_CONFIG)
                board[y][x] = char

        return board

    def get_mults(self):
        """ Gets multpliers by checking color of pixel """
        rgb_im = self.image.convert('RGB')
        word_mults = [[None] * 4 for _ in range(4)]
        for x in range(4):
            for y in range(4):
                pix_x, pix_y = cf.MULT_X0 + x*cf.GAP_X, cf.MULT_Y0 + y*cf.GAP_Y
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


if __name__ == '__main__':  # for testing
    boardOCR = BoardOCR(cf.MAIN_DIR / cf.PATH_TO_IMG)
    print(boardOCR.get_info())
