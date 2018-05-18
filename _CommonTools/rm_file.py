__author__ = 'lr9371'
import sys
import os
import re

if __name__ == "__main__":
    if(len(sys.argv) == 2):
        filename = sys.argv[1]
        os.system("del %s"%filename)

