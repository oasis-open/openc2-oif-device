"""
Allow Target functions
"""
from ..utils import Dispatch, exceptions, valid_ip

Allow = Dispatch("allow")

ValidArgs = {
    "response_requested",
    "start_time",
    "end_time",
    "duration",
    "running",
    "direction",
    "insert_rule",
}


@Allow.register
def default(act, *extra_args, **extra_kwargs):
    return exceptions.target_not_implemented()


@Allow.register
def ipv4_addr(act, target="", args={}, *extra_args, **extra_kwargs):
    if not isinstance(args, dict) and len(set(args) - ValidArgs) > 0:
        print("Invalid Allow Args")
        return exceptions.bad_argument()

    ip = valid_ip(target)
    if ip:
        direction = args.get("direction", None)  # Apply to both INPUT and OUTPUT if None
        print(f"Allow ipv4: {ip} - {direction}")
        return exceptions.action_exception('allow', except_msg='target implementation TBD')

    print("Invalid Allow/IPv4_Addr target")
    return exceptions.bad_request(except_msg="Validation Error: Target: ipv4_addr")


@Allow.register
def ipv6_addr(act, target="", args={}, *extra_args, **extra_kwargs):
    if not isinstance(args, dict) and len(set(args) - ValidArgs) > 0:
        print("Invalid Allow Args")
        return exceptions.bad_argument()

    ip = valid_ip(target)
    if ip:
        direction = args.get("direction", None)  # Apply to both INPUT and OUTPUT if None
        print(f"Allow ipv6: {ip} - {direction}")
        return exceptions.action_exception('allow', except_msg='target implementation TBD')

    print("Invalid Allow/IPv6_Addr target")
    return exceptions.bad_request(except_msg="Validation Error: Target: ipv6_addr")


@Allow.register
def ipv4_connection(act, target={}, args={}, *extra_args, **extra_kwargs):
    if not isinstance(args, dict) and len(set(args) - ValidArgs) > 0:
        print("Invalid Allow Args")
        return exceptions.bad_argument()

    return exceptions.action_exception('allow', except_msg='target implementation TBD')


@Allow.register
def ipv6_connection(act, target={}, args={}, *extra_args, **extra_kwargs):
    if not isinstance(args, dict) and len(set(args) - ValidArgs) > 0:
        print("Invalid Allow Args")
        return exceptions.bad_argument()

    return exceptions.action_exception('allow', except_msg='target implementation TBD')