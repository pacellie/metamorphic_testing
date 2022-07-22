# Team MT – Metamorphic Testing Framework

## Introduction
`metamorphic` is a framework for metamorphic testing. It allows you to write your metamorphic tests and get the test reports.

## Requirements
Python >=3.8,<3.11

## Installation
- [Install the package](https://gitlab.lrz.de/help/user/packages/pypi_repository/index#install-a-pypi-package) with pip.
```shell
pip install metamorphic-test --extra-index-url https://__token__:<your_personal_token>@gitlab.lrz.de/api/v4/projects/114417/packages/pypi/simple
```

- Set or use your personal access token with `read_api` scope [here](https://gitlab.lrz.de/-/profile/personal_access_tokens).
- `__token__` is your personal token name.
- `<your_personal_token>` is your personal access token.

## Example: testing the sine function
### Create a metamorphic test
Create a file named `test_sin.py`:
```python
# content of test_sin.py
import math  
import pytest  
from metamorphic_test import (  # 1
    transformation,  
    relation,  
    metamorphic,  
    system,  
)  
  
A = metamorphic('shift')  # 2
  

@transformation(A)  # 3
def shift(x):  
    return x + 2 * math.pi  
  
  
@relation(A)  # 3
def approximately_equal(output_x, output_y):  
    return output_x == pytest.approx(output_y)  
  
  
@pytest.mark.parametrize('x', range(-1, 1))  # 4
@system(A)  # 5
def test_sin(x):  # 6
    return math.sin(x)
```
The code above defines a metamorphic test for the sine function with the input `x` which ranges from -1 to 1. Each input will be transformed to `x+2π`. The output relation is `sin(x)=sin(x+2π)`. Graphical representation:

<img src="https://latex.codecogs.com/svg.latex?\Large&space;\begin{array}{ccccc} & x & \longrightarrow & \sin (x) & \\ shift & \downarrow & & \updownarrow & approximately \ equal \\ & x+2 \pi & \longrightarrow & \sin (x+2 \pi) &\end{array}" title="example1_sin_A" />

1. Use the functions from `metamorphic_test` to configure a metamorphic test.
2. Register a metamorphic test with a customized name and assign the return value to a variable `A` by calling the `metamorphic` function.
3. Define the transformation and the relation functions that wanted to be tested with decorators `transformation` and `relation`. Specify these functions for test `A` which we have registered by passing the variable `A` to the decorators.
4. Determine the input variable `x` and parametrize its value.
5. Mark the `test_sine` function as the system under test with the `system` decorator and select test `A` to be tested.
6. The test function name should start with `test`.

### Run the test
Simply run
```shell
pytest
```

To see the logging messages in the console:
```shell
pytest -s
```

To generate an html report with graphical illustration for tests (should have `pytest-html` [installed](https://pytest-html.readthedocs.io/en/latest/installing.html)):
```shell
pytest --html=report.html --self-contained-html
```

## Example Upgrade

### Test with multiple metamorphic relations
Extend the content of `test_sin.py` to test with multiple metamorphic relations.
```python
# content of test_sin.py
import math  
import pytest  
from hypothesis import given  
import hypothesis.strategies as st

from metamorphic_test import (  
    transformation,  
    relation,  
    metamorphic,  
    system,  
    fixed,  
    randomized,  
)  
from metamorphic_test.generators import RandInt  
from metamorphic_test.relations import approximately
  
  
A = metamorphic('shift', relation=approximately) # 1 
B = metamorphic('negate')  
C = metamorphic('negate then shift')  
  
  
@transformation(A)  
@transformation(C, priority=0)  # 2
@randomized('n', RandInt(1, 10))  # 3
@fixed('c', 0)  # 3
def shift(x, n, c):  
    return x + 2 * n * math.pi + c  
  
  
@transformation(B)  
@transformation(C, priority=1)  # 2
def negate(x):  
    return -x  
  
  
@relation(B, C)  
def approximately_negate(x, y):  
    return approximately(-x, y)  
  
  
@pytest.mark.parametrize('x', range(-1, 1))  
@system(A, B, C)  
def test_sin(x):  
    return math.sin(x)


@given(st.floats(-1, 1))  # 4
@system(C)  
def test_sin_2(x):  
    return math.sin(x)
```
Now we have three tests `A`, `B`, and `C` for testing the sine function with the relations as follows:

`A`:\
<img src="https://latex.codecogs.com/svg.latex?\Large&space;\begin{array}{ccccc} & x & \longrightarrow & \sin (x) & \\ shift & \downarrow & & \updownarrow & approximately \\ & x+2n \pi +c & \longrightarrow & \sin (x+2n \pi + c) &\end{array}" title="example2_sin_A" />

`B`:\
<img src="https://latex.codecogs.com/svg.latex?\Large&space;\begin{array}{ccccc} & x & \longrightarrow & \sin (x) & \\ negate & \downarrow & & \updownarrow & approximately \ negate \\ & -x& \longrightarrow & \sin (-x) &\end{array}" title="example2_sin_B" />

`C`:\
<img src="https://latex.codecogs.com/svg.latex?\Large&space;\begin{array}{ccccc} & x & \longrightarrow & \sin (x) & \\ negate & \downarrow & & &  \\ & -x&  & \updownarrow & approximately \ negate \\ shift & \downarrow & &  &  \\ & -x + 2n \pi + c & \longrightarrow & \sin (-x + 2n \pi + c) & \end{array}" title="example1_sin_C" />

1. Optionally specify the predefined relation `relation=approximately` when registering the metamorphic test instead of repeatedly writing the same function. You can pass the keyword argument `transform=<some_transformation>` as well.
2. For test `C`, we want to first negate the input `x` and then shift it. Therefore, we assign the transformation `negate` with `priority=1` and the transformation `shift` with `priority=0`. The transformation with a higher priority number will be applied to the input `x` first.
3. The `randomized` decorator assigns the declared variable `n` a random number by `RandInt`. The `fixed` decorator simply sets `c` to a constant `0`. They provide a more flexible way to define the transformation function.
4. Also compatible with `hypothesis` `given` for the input.

## Individual Contributor Setup
- Run `poetry install` to install all requirements.
- Run `poetry run install-hook` to install a Git pre-commit hook which performs linting before you commit.

## CI / CD Setup Steps
- People working on enabling CI / CD related features need access to the repository settings in GitLab so that they can enable runners.
- You need a standard Linux server instance to enable an own runner, as the LRZ doesn't provide one.
- Go to Settings > CI / CD and under Runners > Specific runners, follow the instruction on how to connect your server.
- You just need the `.gitlab-ci.yml` file to be in your project root for pipelines to appear in the navbar under CI/CD > Pipelines. For details on the CI configuration see the [GitLab documentation on this](https://docs.gitlab.com/ee/ci/yaml/gitlab_ci_yaml.html) or the [Quick Start Documentation for CI/CD](https://docs.gitlab.com/ee/ci/quick_start/). Some things you can do include
    * Run commands in a Docker container
    * Group them up by "services"
    * Run some services only on specific branches (e.g. only publish on the main branch)
    * Specify a JUnit output file to get failing tests and coverage info


## Available poetry Scripts
- `poetry install`: Install all dependencies
- `poetry run test`: Run tests (with outputs)
- `poetry run example <which>`: Run tests on example
- `poetry run cov`: Run tests with coverage and show results
- `poetry run lint`: Run linters. Equivalent to `poetry run prospector`. This will automatically check with mypy, pylint, bandit and some other tools.
- `poetry run install-hook`: Install Git pre-commit hook to lint before committing


## Linting in VSCode
- You can have Visual Studio Code check your linting automatically by adding the following to `.vscode/settings.json` (which is .gitignore-d):
    ```json
    "python.linting.mypyEnabled": false,
    "python.linting.enabled": true,
    "python.linting.prospectorEnabled": true
    ```

This way you should see linting and typing errors directly in your editor, which is way more convenient.


## Create a new example
- Create a new directory in the `examples` directory.
- Put your test files in there like normal (e.g. `test_example.py`, files to be checked by Pytest need to have their names start with `test_`).
- Install development dependencies using `poetry add --D <package name>`.
- Run `poetry run example <which>` to run the tests locally.
- Create a new job for your example: Assuming your example is called `hello_world`, add this to the `.gitlab-ci.yml` file in the repository root:
```
hello_world_example:
    stage: examples
    needs: []
    allow_failure: true
    script:
        - poetry run example hello_world
```
- Explanation: This will declare a job called `hello_world_example` and run the example `hello_world` when it is triggered, independently of other jobs and not blocking the pipeline on failure.


## Publishing a New Version
- Increase the version number in pyproject.toml following the suggestions on https://semver.org/
- Push into your branch, then create a merge request into main
- Wait for the pipelines to finish, then let someone merge your PR
- After it's merged and the tests have run through again, go to CI/CD > Pipelines, then press the button to publish. This step has to be done manually so that you cannot publish on accident.

## License
[MIT License](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/blob/main/LICENSE)

