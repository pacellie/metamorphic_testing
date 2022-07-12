from subprocess import CalledProcessError, run  # nosec
import webbrowser
from os import getcwd
import sys


def html_coverage():
    try:
        run(
            ["poetry", "run", "coverage", "run", "-m", "pytest"],
            check=True
        )
    except CalledProcessError:
        print("Tests failed")
        sys.exit(1)
    run(
        ["poetry", "run", "coverage", "html"],
        check=True
    )
    webbrowser.open(f"file://{getcwd()}/htmlcov/index.html")
