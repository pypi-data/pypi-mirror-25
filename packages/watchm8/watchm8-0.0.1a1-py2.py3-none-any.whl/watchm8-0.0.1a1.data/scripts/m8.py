import argparse
import sys
import logging

sys.path.append('.')
sys.path.append('..')
logging.basicConfig(level=logging.DEBUG)

from time import sleep
from threading import Thread
from watchm8.loaders import file_loader
from watchm8 import Watchm8

parser = argparse.ArgumentParser(description='Watchm8 CLI')
parser.add_argument('-f', '--file', required=True, help='Path to config file')


if __name__ == '__main__':
    args = parser.parse_args()
    config = file_loader(args.file)

    watchm8 = Watchm8(config)

    t = Thread(name='m8', target=watchm8.start)
    t.start()

    try:
        while 1:
            sleep(3)
    except KeyboardInterrupt:
        watchm8.stop()
        t.join()
