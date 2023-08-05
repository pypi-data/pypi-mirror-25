import os
import sys

if __package__ == '':
    path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, path)


from huzzer.huzz import main as huzzer_main  # NOQA


def main():
    huzzer_main()


if __name__ == '__main__':
    main()
