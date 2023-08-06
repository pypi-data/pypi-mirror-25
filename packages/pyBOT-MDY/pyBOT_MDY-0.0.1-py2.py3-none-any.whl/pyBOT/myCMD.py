import cmd
import shlex
import sys

class MyCmd(cmd.Cmd):
    def do_add(self, arguments):
        '''add - Adds two numbers the print the sum'''
        x, y = shlex.split(arguments)
        x, y = int(x), int(y)
        print( x + y)

    def do_quit(self, s):
        '''quit - quit the program'''
        sys.exit(0)

if __name__ == '__main__':
    cmd = MyCmd()
    cmd.cmdloop('type help for a list of valid commands')
