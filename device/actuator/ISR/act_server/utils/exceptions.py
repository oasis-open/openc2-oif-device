"""
Actuator Error/Exception Functions
"""


def action_not_implemented(*args: tuple, **kwargs: dict) -> dict:
    """
    Default function if no action function is found
    :return: OpenC2 response message - dict
    """
    return dict(
        status=501,
        status_text=f"Action not implemented"
    )


def target_not_implemented(*args: tuple, **kwargs: dict) -> dict:
    """
    Default function if no target function is found
    :return: OpenC2 response message - dict
    """
    return dict(
        status=501,
        status_text=f"Target type not implemented"
    )


def not_implemented(*args: tuple, **kwargs: dict) -> dict:
    """
    Default responce if pair is valid, bot no action is taken
    :return: OpenC2 response message - dict
    """
    return dict(
        status=501,
        status_text=f"command valid, no action taken"
    )


def bad_argument(*args: tuple, **kwargs: dict) -> dict:
    """
    Bad Option exception response
    :return: OpenC2 response message - dict
    """
    return dict(
        status=501,
        status_text="Option not supported"
    )


# Temporary error/exceptions
def action_exception(action="ACTION", status: int = 400, except_msg: str = "", *args: tuple, **kwargs: dict) -> dict:
    """
    Action exception message creation for errors
    :param action: action of command
    :param status: status code of the error
    :param except_msg: message stating the error
    :param args: positional arguments passed to the function - list
    :param kwargs: keyword arguments passed to the function - dict
    :return: OpenC2 response message - dict
    """
    return dict(
        status=status,
        status_text=f"Action '{action}' received an invalid command" if except_msg == "" else except_msg
    )


def server_exception(except_msg: str = "", *args: tuple, **kwargs: dict) -> dict:
    """
    Server exception response
    :param except_msg: message stating the error
    :param args: positional arguments passed to the function - list
    :param kwargs: keyword arguments passed to the function - dict
    :return: OpenC2 response message - dict
    """
    msg = "The Consumer encountered an unexpected condition that prevented it from performing the Command." if except_msg == "" else except_msg
    return dict(
        status=500,
        status_text=f"Internal Error - {msg}"
    )


def bad_request(except_msg: str = "", *args: tuple, **kwargs: dict) -> dict:
    """
    Bad Request exception response
    :param except_msg: message stating the error
    :param args: positional arguments passed to the function - list
    :param kwargs: keyword arguments passed to the function - dict
    :return: OpenC2 response message - dict
    """
    msg = "The Consumer cannot process the Command due to something that is perceived to be a Producer error (e.g., malformed Command syntax)" if except_msg == "" else except_msg
    return dict(
        status=400,
        status_text=f"Bad Request - {msg}"
    )
