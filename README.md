# Team MT – Metamorphic Testing Framework


## CI / CD Setup Steps
- People working on enabling CI / CD related features need access to the repository settings in GitLab so that they can enable runners.
- You need a standard Linux server instance to enable an own runner, as the LRZ doesn't provide one.
- Go to Settings > CI / CD and under Runners > Specific runners, follow the instruction on how to connect your server.
- You just need the `.gitlab-ci.yml` file to be in your project root for pipelines to appear in the navbar under CI/CD > Pipelines. For details on the CI configuration see the [GitLab documentation on this](https://docs.gitlab.com/ee/ci/quick_start/). Some things you can do include
    * Run commands in a Docker container
    * Group them up by "services"
    * Run some services only on specific branches (e.g. only publish on the main branch)
    * Specify a JUnit output file to get failing tests and coverage info

## License
[MIT License](https://gitlab.lrz.de/pypracticum/team-mt-metamorphic-testing-framework/-/blob/main/LICENSE)

