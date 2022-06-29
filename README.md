# Team MT – Metamorphic Testing Framework


## CI / CD Setup Steps
- People working on enabling CI / CD related features need access to the repository settings in GitLab so that they can enable runners.
- You need a standard Linux server instance to enable an own runner, as the LRZ doesn't provide one.
- Go to Settings > CI / CD and under Runners > Specific runners, follow the instruction on how to connect your server.
- You just need the `.gitlab-ci.yml` file to be in your project root for pipelines to appear in the navbar under CI/CD > Pipelines. For details on the CI configuration see the [GitLab documentation on this](https://docs.gitlab.com/ee/ci/yaml/gitlab_ci_yaml.html) or the [Quick Start Documentation for CI/CD](https://docs.gitlab.com/ee/ci/quick_start/). Some things you can do include
    * Run commands in a Docker container
    * Group them up by "services"
    * Run some services only on specific branches (e.g. only publish on the main branch)
    * Specify a JUnit output file to get failing tests and coverage info

## Publishing a New Version
- Increase the version number in pyproject.toml following the suggestions on https://semver.org/
- Push into your branch, then create a merge request into main
- Wait for the pipelines to finish, then let someone merge your PR
- After it's merged and the tests have run through again, go to CI/CD > Pipelines, then press the button to publish. This step has to be done manually so that you cannot publish on accident.

## License
[MIT License](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/blob/main/LICENSE)

