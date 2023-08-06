Feature: Stack
  As a DevOps
  I want to format docker stack files
  so that 

  Scenario: Compose Version 3
    Given a file named "compose.yml" with:
      """
      version: "3"
      services:
        foo:
          image: bar
      """
    When I run `bin/compose_format compose.yml`
    Then it should pass with exactly:
      """
      version: '3'
      services:
        foo:
          image: bar
      """

  Scenario: Healthcheck
    Given a file named "compose.yml" with:
      """
      version: "3"
      services:
        foo:
          image: bar
          healthcheck:
            interval: 1m30s
            timeout: 10s
            retries: 3
            test: ["CMD", "/bin/true"]
      """
    When I run `bin/compose_format compose.yml`
    Then it should pass with exactly:
      """
      version: '3'
      services:
        foo:
          image: bar
          healthcheck:
            test: [CMD, /bin/true]
            interval: 1m30s
            timeout: 10s
            retries: 3
      """

  Scenario: Deploy
    Given a file named "compose.yml" with:
      """
      version: "3"
      services:
        foo:
          image: bar
          deploy:
            replicas: 7
            mode: global
      """
    When I run `bin/compose_format compose.yml`
    Then it should pass with exactly:
      """
      version: '3'
      services:
        foo:
          image: bar
          deploy:
            replicas: 7
            mode: global
      """
