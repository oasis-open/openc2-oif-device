"""
osquery Field Consts
"""
from typing import Any, Tuple


def getChoiceDisplay(choices: Tuple[Tuple[Any, str], ...], val: Any) -> str:
    for value, display in choices:
        if value == val:
            return display
    return None


SocketFamily = [
    (0, "Reserved"),
    (1, "IP (IP version 4)"),
    (2, "IP6 (IP version 6)"),
    (3, "NSAP"),
    (4, "HDLC (8-bit multidrop)"),
    (5, "BBN 1822"),
    (6, "802 (includes all 802 media plus Ethernet 'canonical format')"),
    (7, "E.163"),
    (8, "E.164 (SMDS, Frame Relay, ATM)"),
    (9, "F.69 (Telex)"),
    (10, "X.121 (X.25, Frame Relay)"),
    (11, "IPX"),
    (12, "Appletalk"),
    (13, "Decnet IV"),
    (14, "Banyan Vines"),
    (15, "E.164 with NSAP format subaddress"),
    (16, "DNS (Domain Name System)"),
    (17, "Distinguished Name"),
    (18, "AS Number"),
    (19, "XTP over IP version 4"),
    (20, "XTP over IP version 6"),
    (21, "XTP native mode XTP"),
    (22, "Fibre Channel World-Wide Port Name"),
    (23, "Fibre Channel World-Wide Node Name"),
    (24, "GWID"),
    (25, "AFI for L2VPN information [RFC4761][RFC6074]"),
    (26, "MPLS-TP Section Endpoint Identifier [RFC7212]"),
    (27, "MPLS-TP LSP Endpoint Identifier [RFC7212]"),
    (28, "MPLS-TP Pseudowire Endpoint Identifier [RFC7212]"),
    (29, "MT IP: Multi-Topology IP version 4 [RFC7307]"),
    (30, "MT IPv6: Multi-Topology IP version 6 [RFC7307]"),
    (31, "BGP SFC [RFC9015]"),
    *[(v, "Unassigned") for v in range(32, 16384)],
    (16384, "EIGRP Common Service Family"),
    (16385, "EIGRP IPv4 Service Family"),
    (16386, "EIGRP IPv6 Service Family"),
    (16387, "LISP Canonical Address Format (LCAF)"),
    (16388, "BGP-LS [RFC7752]"),
    (16389, "48-bit MAC [RFC7042]"),
    (16390, "64-bit MAC [RFC7042]"),
    (16391, "OUI [RFC7961]"),
    (16392, "MAC/24 [RFC7961]"),
    (16393, "MAC/40 [RFC7961]"),
    (16394, "IPv6/64 [RFC7961]"),
    (16395, "RBridge Port ID [RFC7961]"),
    (16396, "TRILL Nickname [RFC7455]"),
    (16397, "Universally Unique Identifier (UUID)"),
    (16398, "Routing Policy AFI [draft-ietf-idr-rpd-02]"),
    (16399, "MPLS Namespaces [draft-kaliraj-bess-bgp-sig-private-mpls-labels-03]"),
    *[(v, "Unassigned") for v in range(16400, 65535)],
    (65535, "Reserved")
]
