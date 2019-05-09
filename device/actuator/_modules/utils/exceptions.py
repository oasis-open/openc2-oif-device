"""
Actuator Error/Exception Functions
"""


def action_not_implemented() -> dict:
    """
    Default function if no action function is found
    :return: OpenC2 response message - dict
    """
    return dict(
        status=501,
        status_text=f"Action not supported"
    )


def target_not_implemented() -> dict:
    """
    Default function if no action function is found
    :return: OpenC2 response message - dict
    """
    return dict(
        status=501,
        status_text=f"Target type not supported"
    )


def bad_argument() -> dict:
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
    return dict(
        status=500,
        status_text="Server Error. The server encountered an unexpected condition that prevented it from fulfilling the request" if except_msg == "" else except_msg
    )


def bad_request(except_msg: str = "", *args: tuple, **kwargs: dict) -> dict:
    """
    Bad Request exception response
    :param except_msg: message stating the error
    :param args: positional arguments passed to the function - list
    :param kwargs: keyword arguments passed to the function - dict
    :return: OpenC2 response message - dict
    """
    return dict(
        status=400,
        status_text="Bad Request. The server cannot process the request due to something that is perceived to be a client error (e.g., malformed request syntax.)" if except_msg == "" else except_msg
    )
