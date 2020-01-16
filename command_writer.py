"""
Author: David Chen
"""
from pathlib import Path

""" Configure program settings """
MAIN_DIR = Path('./')
PATH_TO_COMMANDS = 'ruzzle_swipe.sh'

""" Gesture settings """
CHAR_MID_X0, CHAR_MID_Y0 = 145, 945  # coords of middle of top left letter
GAP_X, GAP_Y = 265, 264  # gap between letters


class CommandWriter:

    def __init__(self, words_info):
        self.words_info = words_info
        self.path_list = self.get_path_list(self.words_info)
        self.save_commands(self.path_list)


    def get_path_list(self, words_info):
        """get coords (0-3, 0-3) from words_info"""
        # add some initial swipes to 'warm up' sendinput, since it appears to be inaccurate when it first starts
        path_list = [
            [(-1,0), (-1,1), (-1,2), (-1,3)], 
            [(-1,0), (-1,1), (-1,2), (-1,3)],
            [(-1,0), (-1,1), (-1,2), (-1,3)],
            [(-1,2), (-1,1), (-1,0)],
            [(-1,2), (-1,1), (-1,0)]
        ]
        # sort by score (hi -> lo)
        high_scores = sorted(words_info.items(), key=lambda x: x[1])[::-1]
        for word, info in high_scores:
            path_list.append(info[1])
        return path_list

    @staticmethod
    def start_swipe(commands, x, y):
        # start swipe movement
        commands += 'sendevent /dev/input/event2 0003 57 570;'  # finger down
        commands += 'sendevent /dev/input/event2 0001 330 1;'
        # send coordinates
        commands += f'sendevent /dev/input/event2 0003 53 {x};'
        commands += f'sendevent /dev/input/event2 0003 54 {y};'
        # end command train
        commands += 'sendevent /dev/input/event2 0000 0 0;'
        return commands


    @staticmethod
    def mid_swipe(commands, x, y):
        # send coordinates
        commands += f'sendevent /dev/input/event2 0003 53 {x};'
        commands += f'sendevent /dev/input/event2 0003 54 {y};'
        # end command train
        commands += 'sendevent /dev/input/event2 0000 0 0;'
        return commands


    @staticmethod
    def end_swipe(commands):
        # end swipe movement
        commands += 'sendevent /dev/input/event2 0003 57 4294967295;'  # finger up
        commands += 'sendevent /dev/input/event2 0001 330 0;'
        # end command train
        commands += 'sendevent /dev/input/event2 0000 0 0;'
        return commands


    def save_commands(self, path_list):
        """ writes all sendevent commands to ruzzle_swipe.sh"""
        commands = ''
        for path in path_list:
            commands = CommandWriter.start_swipe(commands, CHAR_MID_X0+GAP_X*path[0][1], CHAR_MID_Y0+GAP_Y*path[0][0])  # initialize swipe
            for x, y in path[1:]:
                commands = CommandWriter.mid_swipe(commands, CHAR_MID_X0+GAP_X*y, CHAR_MID_Y0+GAP_Y*x)
            commands = CommandWriter.end_swipe(commands)
        
        with open(MAIN_DIR / PATH_TO_COMMANDS, 'w') as file:
            file.write(commands)

if __name__ == '__main__':
    commandWriter = CommandWriter({})