from apt.help import init, choco_run

import sys


def main():
    init()
    path, *cmds = sys.argv
    choco_run(cmds)
