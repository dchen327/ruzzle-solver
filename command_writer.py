"""
A class for writing commands to a file, which can then be run on a phone.

Constants are defined in config.py, such as file paths and coordinates for
swiping. The class requires the dictionary words_info, which contains for each 
word a tuple (score, path).

Author: David Chen
"""
import config as cf
from pathlib import Path


class CommandWriter:

    def __init__(self, words_info):
        self.words_info = words_info
        self.path_list = self.get_path_list(self.words_info)
        self.save_commands(self.path_list)

    def get_path_list(self, words_info):
        """get coords (0-3, 0-3) from words_info"""
        # add some initial swipes to 'warm up' sendinput, since it appears to be inaccurate when it first starts
        path_list = [
            [(-1, 0), (-1, 1), (-1, 2), (-1, 3)],
            [(-1, 0), (-1, 1), (-1, 2), (-1, 3)],
            [(-1, 0), (-1, 1), (-1, 2), (-1, 3)],
            [(-1, 2), (-1, 1), (-1, 0)],
            [(-1, 2), (-1, 1), (-1, 0)]
        ]
        # sort by score (hi -> lo)
        high_scores = sorted(words_info.items(), key=lambda x: x[1])[::-1]
        for word, info in high_scores:
            path_list.append(info[1])
        return path_list

    @staticmethod
    def start_swipe(commands, x, y):
        # start swipe movement
        commands += 'sendevent /dev/input/event2 0003 57 50000;'  # finger down
        commands += 'sendevent /dev/input/event2 0001 330 1;'
        # send coordinates
        commands += f'sendevent /dev/input/event2 0003 53 {x};'
        commands += f'sendevent /dev/input/event2 0003 54 {y};'
        # end command train
        commands += 'sendevent /dev/input/event2 0000 0 0;'
        return commands

    @staticmethod
    def mid_swipe(commands, x=-1, y=-1):
        # send coordinates, if x is -1 send y and keep x from previous command
        if x != -1:
            commands += f'sendevent /dev/input/event2 0003 53 {x};'
        if y != -1:
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
            commands = CommandWriter.start_swipe(commands, cf.CHAR_MID_X0+cf.GAP_X *
                                                 path[0][1], cf.CHAR_MID_Y0+cf.GAP_Y*path[0][0])  # initialize swipe
            for i, (y, x) in enumerate(path[1:], start=1):
                if x == path[i-1][1]:  # same x coord, only send y
                    commands = CommandWriter.mid_swipe(commands, y=cf.CHAR_MID_Y0+cf.GAP_Y*y)
                elif y == path[i-1][0]:  # same y coord, only send x
                    commands = CommandWriter.mid_swipe(commands, x=cf.CHAR_MID_X0+cf.GAP_X*x)
                else:  # send (x, y)
                    commands = CommandWriter.mid_swipe(commands, cf.CHAR_MID_X0+cf.GAP_X*x, cf.CHAR_MID_Y0+cf.GAP_Y*y)
            commands = CommandWriter.end_swipe(commands)

        with open(cf.MAIN_DIR / cf.PATH_TO_COMMANDS, 'w') as file:
            file.write(commands)


if __name__ == '__main__':  # for testing - writes some gestures to ruzzle_swipe.sh
    commandWriter = CommandWriter({})
