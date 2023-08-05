import sys

ANSI_COLOR_ERR = "\x1b[31m"
ANSI_COLOR_WARN = "\x1b[33m"
ANSI_COLOR_OK = "\x1b[32m"
ANSI_COLOR_RESET = "\x1b[0m"

def info(*arg):
    print("", *arg)

def error(*arg):
    print(ANSI_COLOR_ERR, *arg, file=sys.stderr, end='%s\n' % ANSI_COLOR_RESET)

def warn(*arg):
    print(ANSI_COLOR_WARN, *arg, file=sys.stderr, end='%s\n' % ANSI_COLOR_RESET)

def ok(*arg):
    print(ANSI_COLOR_OK, *arg, file=sys.stderr, end='%s\n' % ANSI_COLOR_RESET)
