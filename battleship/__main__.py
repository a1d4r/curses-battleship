import curses
import os
import argparse
from curses import wrapper

from battleship.ui.menu import Menu


def main(stdscr, grid_height: int, grid_width: int) -> None:
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    menu = Menu(stdscr, grid_height, grid_width)
    menu.main_loop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Battleship console game')
    parser.add_argument('height', help='height of grid', type=int)
    parser.add_argument('width', help='width of grid', type=int)
    args = parser.parse_args()
    os.environ.setdefault('ESCDELAY', '25')
    wrapper(main, args.height, args.width)
