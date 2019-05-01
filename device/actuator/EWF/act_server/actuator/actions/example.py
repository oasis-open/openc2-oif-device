"""
This is an example function for an action
The function name should match the filename and be a valid action
The target functions do not need to follow a naming convention, they do need to be paired to a target key in the TARGET_FUNCTIONS dict
"""

"""
The actions can be written as python packages names as the action - see query
The main action function should within the __init__.py
    - If action is query, a function named query is needed in the __init__.py
    - The TARGET_FUNCTIONS dict should be located in the __init__.py as well
"""


def example_scan(self, cmd_id=0, *extra_args, **extra_kwargs):
    """
    Example target function for example-scan
    Any parameter of an OpenC2-Command message can be used as an argument [action, actuator, args, id as cmd_id, target]
    Target will be the contents of the target object
    :param self: the instance of the actuator that called the function
    :param cmd_id: id of the command
    :param extra_args: positional arguments passed to the function - list
    :param extra_kwargs: keyword arguments passed to the function - dict
    :return: dict of of an OpenC2 response message
    """
    return dict(
        id=cmd_id,
        status=400,
        status_text='this is an example action, it returns this message'
    )


# Python replacement for switch
# Key/Value pairing - Target Name/Target Function
TARGET_FUNCTIONS = dict(
    scan=example_scan
)


def example(self, cmd_id=0, action='example', target={}, *extra_args, **extra_kwargs):
    """
    Base function for the Example Action
    :param self: instance of the actuator that has called this function - object
    :param cmd_id: id of the command
    :param action: action of the command - example
    :param target: target of the command
    :param args: args of the command
    :param extra_args: positional arguments passed to the function - list
    :param extra_kwargs: keyword arguments passed to the function - dict
    :return: dict of of an OpenC2 response message
    """
    target_function = TARGET_FUNCTIONS.get(list(target.keys())[0], None)

    if target_function is None:
        result = self._action_exception(cmd_id, action, except_msg='Invalid target type for action')
    else:
        nargs = [self]
        nargs.extend(extra_args)

        nkwargs = dict(extra_kwargs)
        nkwargs.update(
            cmd_id=cmd_id,
            target=target.get(list(target.keys())[0], {})
        )
        result = target_function(*nargs, **nkwargs)

    return result
