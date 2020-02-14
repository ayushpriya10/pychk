import argparse
import sys

class Parser(argparse.ArgumentParser):
    def error(self, message):
        print(f'[ERR] You supplied {message}. Please use valid syntax.')
        self.print_help()
        sys.exit(1)