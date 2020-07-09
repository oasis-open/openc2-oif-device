"""
Deny Target functions
"""
from ..utils import Dispatch, exceptions, valid_ip

Deny = Dispatch("deny")

ValidArgs = {
    "response_requested",
    "start_time",
    "end_time",
    "duration",
    "running",
    "direction",
    "insert_rule",
    "drop_process",
}


@Deny.register
def default(act, *extra_args, **extra_kwargs):
    return exceptions.target_not_implemented()


@Deny.register
def ipv4_addr(act, target="", args={}, *extra_args, **extra_kwargs):
    if not isinstance(args, dict) and len(set(args) - ValidArgs) > 0:
        print("Invalid Deny Args")
        return exceptions.bad_argument()

    ip = valid_ip(target)
    if ip:
        direction = args.get("direction", None)  # Apply to both INPUT and OUTPUT if None
        print(f"Deny ipv4_addr: {ip} - {direction}")
        return exceptions.action_exception('deny', except_msg='target implementation TBD')

    print("Invalid Deny/IPv4_Addr target")
    return exceptions.bad_request(except_msg="Validation Error: Target: ipv4_addr")


@Deny.register
def ipv6_addr(act, target="", args={}, *extra_args, **extra_kwargs):
    if not isinstance(args, dict) and len(set(args) - ValidArgs) > 0:
        print("Invalid Deny Args")
        return exceptions.bad_argument()

    ip = valid_ip(target)
    if ip:
        direction = args.get("direction", None)  # Apply to both INPUT and OUTPUT if None
        print(f"Deny ipv6_addr: {ip} - {direction}")
        return exceptions.action_exception('deny', except_msg='target implementation TBD')

    print("Invalid Deny/IPv6_Addr target")
    return exceptions.bad_request(except_msg="Validation Error: Target: ipv6_addr")


@Deny.register
def ipvv4_connection(act, target={}, args={}, *extra_args, **extra_kwargs):
    if not isinstance(args, dict) and len(set(args) - ValidArgs) > 0:
        print("Invalid Deny Args")
        return exceptions.bad_argument()

    return exceptions.action_exception('deny', except_msg='target implementation TBD')


@Deny.register
def ipvv6_connection(act, target={}, args={}, *extra_args, **extra_kwargs):
    if not isinstance(args, dict) and len(set(args) - ValidArgs) > 0:
        print("Invalid Deny Args")
        return exceptions.bad_argument()

    return exceptions.action_exception('deny', except_msg='target implementation TBD')