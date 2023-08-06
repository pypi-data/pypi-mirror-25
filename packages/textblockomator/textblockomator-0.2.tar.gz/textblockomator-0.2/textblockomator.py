'''
    Text block automator
    Written by: Joseph Jones

    Notes:
        The keywords must be proceeded by an = and ended with an enter
        in order to paste out given text
'''
from pynput import keyboard

DEBUG_MODE = False   # Enables debug output and easily closing script
WORDS = {
    # Keyword:  Text to paste out when keyword is seen
    "help":     "https://example.com/help"
}

class TextAuto:
    ''' Class implementation of the text block automator '''
    cur_word = ""
    word_listening = False
    kbctrl = keyboard.Controller()  # Handles keyboard output

    def __init__(self):
        print("Starting text block automator")
        with keyboard.Listener(       # Listens to keyboard events
            on_press=self.on_press,
            on_release=self.on_release) as listener:
            listener.join()

    def on_press(self, key):
        ''' Execute on key press '''
        try:                        # Catches alphanumeric keys such as c and 3
            if DEBUG_MODE:
                print('alphanumeric key {0} pressed'.format(
                    key.char))

            if self.word_listening:
                self.cur_word += key.char

            # Wait for the press of = before listening to individual keys
            if key.char == '=' and not self.word_listening:
                if DEBUG_MODE:
                    print("DEBUG: Starting word")
                self.cur_word = ""
                self.word_listening = True

        except AttributeError:      # Catches special keys such as enter and control
            # If enter is pressed and we are currently listening to individual keys,
            # stop listening and check if the keyword exists, if so then paste out
            # the given text
            if key == keyboard.Key.enter and self.word_listening:
                if DEBUG_MODE:
                    print("DEBUG: Ending word")
                self.word_listening = False

                if self.cur_word in WORDS.keys():
                    if DEBUG_MODE:
                        print("DEBUG: found '%s'!" % self.cur_word)
                    for i in range(len(self.cur_word) + 2):
                        self.kbctrl.press(keyboard.Key.backspace)
                    self.kbctrl.type(WORDS[self.cur_word])

    def on_release(self, key):
        ''' Execute on key release '''
        if key == keyboard.Key.esc and DEBUG_MODE:
            return False

MAIN = TextAuto()
