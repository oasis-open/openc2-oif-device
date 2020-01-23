"""
This is an example target registration for an action
- Initializing the Dispatch, it should receive a string as its namespace match the intended action
- Register a target function, create a function with a decorator of '@Example.register' or 'Example.register(FUNCTION)'
    Note: the function will be registered with its name unless an argument string is given specifying the registered name
"""

from ..utils import Dispatch, exceptions

Example = Dispatch("example")


@Example.register
def default(*extra_args, **extra_kwargs):
    return exceptions.target_not_implemented()


@Example.register(key="scan")
def example_scan(actuator, *extra_args, **extra_kwargs):
    """
    Example target function for example-scan
    Any parameter of an OpenC2-Command message can be used as an argument [action, actuator, args, id as cmd_id, target]
    Target will be the contents of the target object
    :param actuator: the instance of the actuator that called the function
    :param extra_args: positional arguments passed to the function - list
    :param extra_kwargs: keyword arguments passed to the function - dict
    :return: OpenC2 response message - dict
    """
    return dict(
        status=400,
        status_text='this is an example action, it returns this message'
    )


@Example.register
def locate(actuator, *extra_args, **extra_kwargs):
    """
    Example target function for example-locate
    Any parameter of an OpenC2-Command message can be used as an argument [action, actuator, args, id as cmd_id, target]
    Target will be the contents of the target object
    :param actuator: the instance of the actuator that called the function
    :param extra_args: positional arguments passed to the function - list
    :param extra_kwargs: keyword arguments passed to the function - dict
    :return: OpenC2 response message - dict
    """
    return dict(
        status=400,
        status_text='this is an example action, it returns this message'
    )


def example_allow(actuator, *extra_args, **extra_kwargs):
    """
    Example target function for example-allow
    Any parameter of an OpenC2-Command message can be used as an argument [action, actuator, args, id as cmd_id, target]
    Target will be the contents of the target object
    :param actuator: the instance of the actuator that called the function
    :param extra_args: positional arguments passed to the function - list
    :param extra_kwargs: keyword arguments passed to the function - dict
    :return: OpenC2 response message - dict
    """
    return dict(
        status=400,
        status_text='this is an example action, it returns this message'
    )


def update(actuator, *extra_args, **extra_kwargs):
    """
    Example target function for example-update
    Any parameter of an OpenC2-Command message can be used as an argument [action, actuator, args, id as cmd_id, target]
    Target will be the contents of the target object
    :param actuator: the instance of the actuator that called the function
    :param extra_args: positional arguments passed to the function - list
    :param extra_kwargs: keyword arguments passed to the function - dict
    :return: OpenC2 response message - dict
    """
    return dict(
        status=400,
        status_text='this is an example action, it returns this message'
    )


Example.register(example_allow, key="allow")
Example.register(update)
