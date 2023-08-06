# Deployment Director

Plug this utility in your CI/CD pipeline and customise your deployment flow
with advanced logic using simple yaml configuration.

Docker support required.

## How to run

```
Usage: deployment-director [OPTIONS] RULES_FILE

Options:
  --ci-name TEXT      Name of the CI product deployment director is running
                      under
  -n, --dry-run TEXT  Do not actually execute any actions, just print them out
  -v, --verbose
  --help              Show this message and exit.
```

## The rules file

Sample:

```
version: "1"
rules:
  when:
    branch: [ master, development ]
  then:
    - add_action:
        name: deploy
        class_name: CommandAction
        arguments:
          command: deploy.sh {server_ip}
        parameters:
          server_ip:
            key: branch
            map:
              master: 10.0.0.1
              development: 10.0.1.1
```

## Available action classes

TODO

## Documentation

TODO

## Which CI/CD are supported

- Codeship