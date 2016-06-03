"""This module handles writing to the terminal or a log file with support
for coloring for warnings, errors, etc."""
from termcolor import cprint
verbosity = None
"""The verbosity level of messages being printed by the module."""
quiet = None
"""When in quiet mode, no text is ever printed to terminal unless its
verbosity level is explicitly specified.
"""
cenum = {
    "cerrs": 0,
    "cwarn": 1,
    "cinfo": 2,
    "cgens": 3,
    "cstds": 4,
    "cokay": 5
}
"""Dict of the various colors available for coloring specific
lines in the arb().
"""
icols = ["red", "yellow", "cyan", "blue", "white", "green"]

def arb(text, cols, split):
    """Prints a line of text in arbitrary colors specified by the numeric
    values contained in msg.cenum dictionary.
    """
    stext = text if text[-1] != split else text[0:-1]
    words = stext.split(split)
    for i, word in enumerate(words):
        col = icols[cols[i]]
        cprint(word, col, end="")
        if i < len(words)-1:
            cprint(split, end="")
        else:
            cprint(split)

def set_verbosity(level):
    """Sets the modules message verbosity level for *all* messages printed.

    :arg level: a positive integer (>0); higher levels including more detail.
    """
    global verbosity
    verbosity = level

def set_quiet(is_quiet):
    """Sets whether the messaging system is running in quiet mode. Quiet mode
    only prints messages with explicit verbosity specified. If verbosity==None
    and quiet==True, any message with level >= 0 is printed.
    """
    global quiet
    quiet = is_quiet

def will_print(level=1):
    """Returns True if the current global status of messaging would print a
    message using any of the printing functions in this module.
    """
    if level == 1:
        #We only affect printability using the quiet setting.
        return quiet is None or quiet == False
    else:
        return ((isinstance(verbosity, int) and level <= verbosity) or
                (isinstance(verbosity, bool) and verbosity == True))
    
def warn(msg, level=0, prefix=True):
    """Prints the specified message as a warning; prepends "WARNING" to
    the message, so that can be left off.
    """
    if will_print(level):
        cprint(("WARNING: " if prefix else "") + msg, "yellow")

def err(msg, level=-1, prefix=True):
    """Prints the specified message as an error; prepends "ERROR" to
    the message, so that can be left off.
    """
    if will_print(level) or verbosity is None:
        cprint(("ERROR: " if prefix else "") + msg, "red")

def info(msg, level=1):
    """Prints the specified message as information."""
    if will_print(level):
        cprint(msg, "cyan")

def okay(msg, level=1):
    """Prints the specified message as textual progress update."""
    if will_print(level):
        cprint(msg, "green")

def gen(msg, level=1):
    """Prints the message as generic output to terminal."""
    if will_print(level):
        cprint(msg, "blue")

def blank(n=1, level=2):
    """Prints a blank line to the terminal."""
    if will_print(level):
        for i in range(n):
            print("")

def std(msg, level=1):
    """Prints using the standard print() function."""
    if will_print(level):
        print(msg)