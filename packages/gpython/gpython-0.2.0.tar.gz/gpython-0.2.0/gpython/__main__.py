import argparse

from .core import install, uninstall

FUNCTION_MAP = {
    'install': install,
    'uninstall': uninstall,
}

parser = argparse.ArgumentParser()
parser.add_argument('command', choices=FUNCTION_MAP.keys())
args = parser.parse_args()

func = FUNCTION_MAP[args.command]
func()
