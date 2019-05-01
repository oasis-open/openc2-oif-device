from .openc2 import openc2

# Python replacement for switch
TARGET_FUNCTIONS = dict(
    openc2=openc2
)


def query(self, cmd_id=0, action='query', target={}, *extra_args, **extra_kwargs):
    """
    Base function for the Query Action
    :param self: instance of the actuator that has called this function - object
    :param cmd_id: id of the command
    :param action: action of the command - query
    :param target: target of the command
    :param extra_args: positional arguments passed to the function - list
    :param extra_kwargs: keyword arguments passed to the function - dict
    :return: dict of of an OpenC2 response message
    """
    target_key0 = list(target.keys())[0]
    target_function = TARGET_FUNCTIONS.get(target_key0, None)

    if target_function is None:
        result = self.action_exception(cmd_id, action, except_msg='Invalid target type for action')
    else:
        nargs = [self]
        nargs.extend(extra_args)

        nkwargs = dict(extra_kwargs)
        nkwargs.update(
            cmd_id=cmd_id,
            target=target.get(target_key0, {})
        )
        result = target_function(*nargs, **nkwargs)

    return result
