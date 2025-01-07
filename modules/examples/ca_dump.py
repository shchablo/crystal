class CaDump:
    """
    A basic class example to demonstrate initialization, representation, and default parameter handling.
    """

    def init(self, value1, value2):
        """
        Initializes the CaDump instance with provided values.

        Args:
            value1: The first parameter.
            value2: The second parameter.
        """
        self.param1 = value1
        self.param2 = value2
        self.param3 = 0  # Default value

    def repr(self):
        """
        Returns a string representation of the object for debugging purposes.

        Returns:
            str: A string representation of the CaDump object.
        """
        return f"CaDump(param1={self.param1}, param2={self.param2}, param3={self.param3})"