class Compiler:
    """
    Base compiler class.
    """

    def __init__(self, function):
        self.function = function

    def compile(self):
        """
        Compile function emiting code to the target language.
        """

        raise NotImplementedError
