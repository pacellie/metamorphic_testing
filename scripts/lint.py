from subprocess import call  # nosec


def lint():
    call(["poetry", "run", "prospector", "-w", "mypy", "-w", "bandit"])