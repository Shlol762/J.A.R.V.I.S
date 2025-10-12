import discord


class PreStartException(Exception):
    """Exception occured before the Bot was initialised."""

    def __init__(self, message, *args):
        super().__init__(message, *args)


class NotImportableError(PreStartException, ImportError):
    """Bot initiating file was run as a module."""


    def __init__(self, message, *args):
        super().__init__(message=message, *args )


class InvalidToken(ValueError):
    """String does not match valid Discord Bot token pattern."""

    def __init__(self, *args):
        super().__init__(*args)

