"""
A program to solve Ruzzle boards and write gesture commands to a file

Ensure that the files for BoardOCR, BoardSolver, and CommandWriter are in the 
same directory.

Author: David Chen
"""
from board_ocr import BoardOCR
from board_solver import BoardSolver
from command_writer import CommandWriter
    
if __name__ == '__main__':
    boardOCR = BoardOCR()
    board, word_mults = boardOCR.get_info()
    boardSolver = BoardSolver(board, word_mults)
    commandWriter = CommandWriter(boardSolver.words_info)
    