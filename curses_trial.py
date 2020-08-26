import curses
from curses.ascii import isprint
import sys
from typing import Any


class ChatScreen:

    height = 0
    width = 0
    messages = []
    stdscr: Any = ...
    input_msg = ''
    new_message = ''

    def __init__(self):
        curses.wrapper(self.main)

    def drawScreen(self):
        """Draw the main structure of the client's chat screen"""

        self.height, self.width = self.stdscr.getmaxyx()

        self.stdscr.addstr(self.height-2, 0, '-' * self.width)
        self.stdscr.move(self.height-1, 0)

        # show the last (h-2) messages
        for i, message in enumerate(self.messages[-(self.height-2):]):
            self.stdscr.addstr(i, 0, message)

        self.stdscr.refresh()

    def clearMessageInput(self):
        """Clear the bottom lines used for inputting the message"""

        # clear bottom line
        self.stdscr.addstr(self.height-1, 0, ' ' * (self.width-1))
        # reset cursor position
        self.stdscr.move(self.height-1, 0)
        # clear input string
        self.input_msg = ''

    @property
    def new_message(self):
        return self.new_message

    @new_message.setter
    def new_message(self, message):
        self.messages.append(message)
        self.drawScreen()

    def main(self, stdscr):
        """Event loop resides here"""

        self.stdscr = stdscr

        curses.echo()           # display on keypress
        stdscr.nodelay(1)
        stdscr.timeout(100)
        # curses.cbreak()

        self.drawScreen()

        # event loop of chat client
        while True:
            key = stdscr.getch()

            # stdscr.addstr(0, 0, str(key))
            if isprint(key):
                self.input_msg += chr(key)

            # ENTER was pressed, send message (or exit)
            if key == 10:
                if self.input_msg == "bye":
                    break

                self.input_msg = self.input_msg.ljust(self.width-1, ' ')
                self.messages.append(self.input_msg)

                # # show the last (h-2) messages
                # for i, message in enumerate(self.messages[-(self.height-2):]):
                #     self.stdscr.addstr(i, 0, message)

                self.drawScreen()
                self.clearMessageInput()

    def endMain(self):
        sys.exit(0)


if __name__ == "__main__":
    chat_screen = ChatScreen()
