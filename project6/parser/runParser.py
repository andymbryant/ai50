import subprocess
import os
import parser
import sys

def main():
    cwd = os.getcwd()
    filenames = os.listdir(cwd + '/sentences')
    for filename in filenames:
        # cmd_raw = "python parser.py " + 'sentences/' + filename
        # cmd = cmd_raw.split()
        # result = subprocess.call(cmd)
        print(sys.argv)
        parser.main()


if __name__ == '__main__':
    main()
