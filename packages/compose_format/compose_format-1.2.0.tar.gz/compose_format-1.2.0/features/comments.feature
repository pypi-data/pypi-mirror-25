Feature: Format
  As a DevOps
  I want to add comments
  so that I can mark specialities

  Scenario: Comment at End of Line
    Given a file named "compose.yml" with:
      """
      foo:  # TODO: This service still uses hard-coded configuration
        image: bar
      """
    When I run `bin/compose_format compose.yml`
    Then it should pass with exactly:
      """
      foo:  # TODO: This service still uses hard-coded configuration
        image: bar
      """


  Scenario: Single Line Comment
    Given a file named "compose.yml" with:
      """
      foo:
        # Test
        image: bar
      """
    When I run `bin/compose_format compose.yml`
    Then it should pass with exactly:
      """
      foo:
        # Test
        image: bar
      """
