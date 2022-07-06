from subprocess import call  # nosec
import webbrowser
from os import getcwd


def html_coverage():
    call(["poetry", "run", "coverage", "run", "-m", "pytest"])
    call(["poetry", "run", "coverage", "html"])
    webbrowser.open(f"file://{getcwd()}/htmlcov/index.html")
