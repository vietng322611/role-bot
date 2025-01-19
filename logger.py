import io

from datetime import datetime

DEFAULT_FORMAT = "[%s]" % str(datetime.now().strftime('%H:%M:%S'))

RED   = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
BLUE  = "\033[0;34m"
MAGENTA = "\033[0;95m"
CYAN  = "\033[0;96m"
RESET = "\033[0;0m"

__f = io.TextIOWrapper
_format = ""

def config(path: str, format: str = None) -> None:
    global __f, _format
    __f = open(path + str(datetime.now().date()) + '@' + str(datetime.now().strftime('%H.%M.%S')) + '.log',
                mode= "w", encoding='utf-8')
    if format == None: _format = DEFAULT_FORMAT
    else: _format = format

def to_file(__p: str, __s: str, _type: str) -> None:
    __f.write(f"{_format} {__p} -{_type.upper()}- {__s}\n")

def to_stdout(__p: str, __s: str, _type: str, _color: str):
    print(f"{GREEN}{_format} {RESET}{__p} {_color}-{_type.upper()}- {RESET}{__s}")

def info(__p: str, __s: str) -> None:
    to_stdout(__p, __s, "info", CYAN)
    to_file(__p, __s, "info")

def warning(__p: str, __s: str) -> None:
    to_stdout(__p, __s, "warning", YELLOW)
    to_file(__p, __s, "warning")

def error(__p: str, __s: str) -> None:
    to_stdout(__p, __s, "error", RED)
    to_file(__p, __s, "error")

def debug(__p: str, __s: str) -> None:
    to_stdout(__p, __s, "debug", MAGENTA)
    to_file(__p, __s, "debug")

def excepthook(type, value, traceback):
    error("%s: %s" % (type.__name__, value))