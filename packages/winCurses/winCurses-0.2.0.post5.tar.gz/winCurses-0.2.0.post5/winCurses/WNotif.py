import curses
from .Win import *

class WNotif(Win):
    def __init__(self, *args, **kwargs):
        """ Creates a one-line-high notification zone, only intended to display
        simple messages

        arguments and result are the same as winCurses.Win ones
        """
        args = list(args) # Because it is an inalterable tuple
        # Fixed height 
        if 'dim' in kwargs:
            kwargs['dim'].y = 1
            kwargs['dim'].relative_y = False
        else:
            args[2].y = 1
            args[2].relative_y = False

        # No borders, because of the limited height
        if 'borders' in kwargs:
            kwargs['borders'] = None
        else:
            if len(args) >= 5:
                args[4] = None

        Win.__init__(self, *args, **kwargs)
        
        self.text = ""
        _, self.line_length = self.get_content_dim().yx()
        
    def disp(self, text):
        """ Displays a notification

        text -- text to display (plain text, no tags)
        """
        self.text = text
        self.clear()
        self.refresh()

    def refresh(self, update=True, get_root_lock=True):
        """ Refreshes the window

        update -- transmitted to winCurses.Win.refresh()
        """
        disp_text = (self.text if len(self.text) <= self.line_length else self.text[:self.line_length])
        self.window.addstr(0, 1 , disp_text)
        Win.refresh(self, update, get_root_lock)

    def reset(self):
        """ Resets the content of the text field and clears the window """
        self.text = ""
        self.clear(True)
