import logging

from permute import build

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    with open('example.py', mode="r") as f:
        build(f.read())
