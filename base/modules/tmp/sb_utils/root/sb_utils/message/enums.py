from ..enums import EnumBase


class MessageType(str, EnumBase):
    """
    The type of OpenC2 Message
    """
    Request = "req"       # The initiator of a two-way message exchange.
    Response = "rsp"      # A response linked to a request in a two-way message exchange.
    Notification = "ntf"  # A (one-way) message that is not a request or response.  (Placeholder)
