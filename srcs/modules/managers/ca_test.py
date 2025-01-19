import unittest
import sys


def ca_test():
    """
    Execute all unit tests in the 'tests' directory.

      This command discovers and runs all unit tests located in the "tests" directory using the unittest module.
      If any test fails, the program exits with a non-zero status code.
    """

    loader = unittest.TestLoader()
    suite = loader.discover("tests")

    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)

    if not result.wasSuccessful():
        sys.exit(1)