import sys
import os
from pick import pick
from getopt import getopt

arg_pretty_prompt = ""


def print_help():
    print("usage: start-with {-i command} [option]")
    print("Options:")
    print("-h        : print this help message and exit (also --help)")
    print("-d        : do a dry run and print the command this would've executed")
    print("-p prompt : message to display in the option picker")
    print("-i command: REQUIRED, command to run. Include a %s in this command to replace running this with an argument which is the picked option, with the option being run as %s. %q may be used to substitute a quotation mark")
    print("-w args   : REQUIRED, potential arguments to run the command with")
    print("-t text   : user-friendly text which accompanies a -w option. This will be written in the picker instead of the argument(s)")
    sys.exit(0)


def parseargs():
    class Output:
        def __init__(self):
            self.args_string = sys.argv[1:]
            self.set_options = True
            self.dry_run = False

    opts, args = getopt(sys.argv[1:], "hdnp:i:w:t:", ["--help"])
    enum = 0
    with_text_dict = {}
    with_list = []
    pretty_list = []
    output = Output()
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_help()
        elif opt == "-p":
            global arg_pretty_prompt
            arg_pretty_prompt = arg
        elif opt == "-i":
            output.initial_path = arg
        elif opt == "-w":
            with_list += [arg]
        elif opt == "-t":
            pretty_list += [arg]
        elif opt == "-d":
            output.dry_run = True
        enum += 1

    if enum == 0:
        print_help()

    if not hasattr(output, "initial_path"):
        raise Exception("No initial command (-i) set.")
    if len(with_list) == 0:
        raise Exception("No potential arguments (-w arg) set.")
    if len(pretty_list) == 0:
        for current_with in with_list:
            with_text_dict.update({current_with: current_with})
        pretty_list = with_list
    else:
        for current_with, current_pretty in zip(with_list, pretty_list):
            with_text_dict.update({current_pretty: current_with})

    output.with_text_dict = with_text_dict
    output.with_list = with_list
    output.pretty_list = pretty_list

    return output


parsed_args = parseargs()
picked_arg = pick(parsed_args.pretty_list, arg_pretty_prompt if not arg_pretty_prompt == "" else "Choose an argument")
if "%s" in parsed_args.initial_path:
    parsed_args.initial_path = parsed_args.initial_path.replace("%s", parsed_args.with_text_dict[picked_arg[0]])
    parsed_args.set_options = False

parsed_args.initial_path = parsed_args.initial_path.replace("%q", "\"")

if parsed_args.dry_run:
    command = print
else:
    command = os.system

if parsed_args.set_options:
    command(f"{parsed_args.initial_path} {parsed_args.with_text_dict[picked_arg[0]]}")
else:
    command(parsed_args.initial_path)