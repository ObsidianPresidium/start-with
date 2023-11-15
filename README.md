# start-with

A Python script which prompts the user to make a choice about which app to open and with which parameters/options, based on its own options.

---
## Usage

`start-with {-i command} [option]`

Options:

    -h        : print this help message and exit (also --help)
    -d        : do a dry run and print the command this would've executed
    -p prompt : message to display in the option picker
    -i command: REQUIRED, command to run. Include a %s in this command to replace running this with an argument which is the picked option, with the option being run as %s.
    -w args   : REQUIRED, potential arguments to run the command with
    -t text   : user-friendly text which accompanies a -w option. This will be written in the picker instead of the argument(s)

---
## Examples

### Example 1:

start-with command:  
`start-with -p "Which pet should have its picture opened?" -i xviewer -w "cat.jpg" -t Cat -w "dog.jpg" -t Dog`

TUI argument picker menu:

    Which pet should have its picture opened?
      
    * Cat
      Dog

Upon selecting Cat, for example, this command will then be executed:  
`xviewer cat.jpg`

### Example 2:

start-with command:
`start-with -p "Start PHP server in this directory:" -i "cd '%s'; php -S 127.0.0.1:8000" -w "/home/emil/Homework" -t "Homework folder" -w "/home/emil/Documents/my-website" -t "My Website"`

TUI argument picker menu:

    Start PHP server in this directory:
    
    * Homework folder
      My Website

Upon selecting My Website, for example, this command will then be executed:
`cd '/home/emil/Documents/my-website'; php -S 127.0.0.1:8000`