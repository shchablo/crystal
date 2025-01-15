import unittest
import sys


def ca_test():
    """

    Executes all unit tests in the 'tests' directory.

    This function uses the unittest module to discover and run all tests located in the "tests" directory.
    If any test fails, the function terminates the program with a non-zero exit code.

    :return: None

    """

    loader = unittest.TestLoader()
    suite = loader.discover("tests")

    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)

    if not result.wasSuccessful():
        sys.exit(1)