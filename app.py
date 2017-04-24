import argparse

from arm.arm import run

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build Components Factory')
    parser.add_argument("-r", "--run", action="store_true")
    args = parser.parse_args()
    if args.run:
        run()