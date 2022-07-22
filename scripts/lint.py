from subprocess import CalledProcessError, run  # nosec
import sys


def lint():
    try:
        run(
            [
                "poetry", "run", "prospector", "metamorphic_test",
                *sys.argv[1:]
            ],
            check=True
        )
    except CalledProcessError:
        print("Linting failed")
        sys.exit(1)
