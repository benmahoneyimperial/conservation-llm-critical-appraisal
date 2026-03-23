import os
import sys

ROOT = os.path.dirname(os.path.dirname(__file__))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from your_package.cli import run


def test_run_smoke():
    # smoke call to ensure `run` executes without error
    run("smoke-test")
