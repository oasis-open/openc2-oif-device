from ..enums import EnumBase


class MessageType(str, EnumBase):
    """
    The type of OpenC2 Message
    """
    Request = "request"       # The initiator of a two-way message exchange.
    Response = "response"      # A response linked to a request in a two-way message exchange.
    Notification = "ntf"  # A (one-way) message that is not a request or response.  (Placeholder)
