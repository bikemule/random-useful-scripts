#!/usr/local/bin/python3

import subprocess
import sys
import re

DEBUG = False

def get_man_descriptions(flag, man_page):

    # Check for correctness
    if flag[0] != '-':
        return "Invalid flag."

    flag_re_prefix = "\W*"

    flags = []

    if len(flag) > 2:
        if flag[1] == '-':
            flags.append(flag)
        else:
            for char in flag:
                if char != '-':
                    flags.append('-' + char)
    else:
        flags.append(flag)

    relevant_lines = []

    for f in flags:
        flag_re = re.compile(flag_re_prefix + f)
        for counter, line in enumerate(man_page):
            if re.match(flag_re, line):
                current_line = line
                current_counter = counter
                while current_counter < len(man_page) - 1:
                    current_counter += 1
                    if not re.match("\W*", man_page[current_counter]):
                        current_line += "\n" + man_page[current_counter]

                relevant_lines.append(current_line)
                continue

    return relevant_lines


if __name__ == '__main__':

    # Perhaps first scrub input for security? Whitelisted commands?
    # Add a check to see if it requires sudo?

    if DEBUG:
        print(sys.argv)

    command = sys.argv[1]
    flags = sys.argv[2:]

    # TODO: figure out encoding from command line
    # Run `man _command_` and capture output
    # Split output on double newlines to separate paragraphs
    man_page = subprocess.check_output(["man", command]).decode("utf-8").split("\n\n")

    # Go through each flag/argument and find each line of the man page that
    # contains it.
    for flag in flags:
        print(flag)
        man_descriptions = get_man_descriptions(flag, man_page)
        if len(man_descriptions):
            for m in man_descriptions:
                print(m)
        else:
            print("No valid flags detected")
