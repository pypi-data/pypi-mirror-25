#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016, CESNET, z. s. p. o.
# Use of this source is governed by an ISC license, see LICENSE file.

import typedcols
from . import base
import re
import struct
import socket

from .base import unicode


def Version(s):
    if s != "IDEA0":
        raise ValueError("Wrong ID string")
    return s


def MediaType(s):
    if base.media_type_re.match(s) is None:
        raise ValueError("Wrong MediaType")
    return s


def Charset(s):
    if base.charset_re.match(s) is None:
        raise ValueError("Wrong Charset")
    return s


def Encoding(s):
    s = s.lower()
    if s != "base64":
        raise ValueError("Wrong Encoding")
    return s


def Handle(s):
    if base.handle_re.match(s) is None:
        raise ValueError("Wrong Handle")
    return s


def ID(s):
    if base.id_re.match(s) is None:
        raise ValueError("Wrong ID")
    return s


def Timestamp(t):
    if base.timestamp_re.match(t) is None:
        raise ValueError("Wrong Timestamp")
    return t


def Duration(t):
    if base.duration_re.match(t) is None:
        raise ValueError("Wrong Duration")
    return t


def URI(s):
    if base.uri_re.match(s) is None:
        raise ValueError("Wrong URI")
    return unicode(s)


def ip4_to_int(ip):
    return struct.unpack(">L", socket.inet_pton(socket.AF_INET, ip))[0]


def Net4(s):
    try:
        # CIDR notation?
        net, cidr = s.split("/")
    except ValueError:
        pass
    else:
        ip = ip4_to_int(net)
        mask = int(cidr)
        if not 0 < mask < 32:
            raise ValueError("Wrong CIDR")
        return s

    try:
        # Range?
        ip1, ip2 = s.split("-")
        rng = (ip4_to_int(ip1), ip4_to_int(ip2))
    except Exception:
        pass
    else:
        return s

    # Single IP?
    ip4_to_int(s)
    return s


def ip6_to_int(ip):
    hi, lo = struct.unpack(">QQ", socket.inet_pton(socket.AF_INET6, ip))
    return hi << 64 | lo


def Net6(s):
    try:
        # CIDR notation?
        net, cidr = s.split("/")
    except ValueError:
        pass
    else:
        ip = ip6_to_int(net)
        mask = int(cidr)
        if not 0 < mask < 128:
            raise ValueError("Wrong CIDR")
        return s

    try:
        # Range?
        ip1, ip2 = s.split("-")
        rng = (ip6_to_int(ip1), ip6_to_int(ip2))
    except Exception:
        pass
    else:
        return s

    # Single IP?
    ip6_to_int(s)
    return s


def NSID(s):
    if base.nsid_re.match(s) is None:
        raise ValueError("Wrong NSID")
    return s


def MAC(s):
    if base.mac_re.match(s) is None:
        raise ValueError("Wrong MAC")
    return s


def Port(s):
    int(s)
    return s


def Netname(s):
    if base.netname_re.match(s) is None:
        raise ValueError("Wrong Netname")
    return s


def Hash(s):
    if base.hash_re.match(s) is None:
        raise ValueError("Wrong Hash")
    return s


def EventTag(s):
    if base.event_tag_re.match(s) is None:
        raise ValueError("Wrong EventTag")
    return s


def ProtocolName(s):
    return s


def ConfidenceFloat(s):
    f = float(s)
    if not 0.0 <= f <= 1:
        raise ValueError("Confidence out of bounds")
    return s


def SourceTargetTag(s):
    if base.tag_re.match(s) is None:
        raise ValueError("Wrong Type")
    return s


NodeTag = SourceTargetTag
AttachmentTag = SourceTargetTag


idea_types = {
    "Boolean": bool,
    "Integer": int,
    "String": unicode,
    "Binary": str,
    "ConfidenceFloat": float,
    "Version": Version,
    "MediaType": MediaType,
    "Charset": Charset,
    "Encoding": Encoding,
    "Handle": Handle,
    "ID": ID,
    "Timestamp": Timestamp,
    "Duration": Duration,
    "URI": URI,
    "Net4": Net4,
    "Net6": Net6,
    "Port": Port,
    "NSID": NSID,
    "MAC": MAC,
    "Netname": Netname,
    "Hash": Hash,
    "EventTag": EventTag,
    "ProtocolName": ProtocolName,
    "SourceTargetTag": SourceTargetTag,
    "NodeTag": NodeTag,
    "AttachmentTag": AttachmentTag
}

idea_defaults = {}

idea_lists = base.list_types(idea_types)


class SourceTargetDict(typedcols.TypedDict):
    allow_unknown = True
    typedef = base.source_target_dict_typedef(idea_types, idea_lists)


class AttachDict(typedcols.TypedDict):
    allow_unknown = True
    typedef = base.attach_dict_typedef(idea_types, idea_lists)


class NodeDict(typedcols.TypedDict):
    allow_unknown = True
    typedef = base.node_dict_typedef(idea_types, idea_lists)


class Idea(base.IdeaBase):
    typedef = base.idea_typedef(
        idea_types,
        idea_lists,
        idea_defaults,
        typedcols.typed_list("SourceList", SourceTargetDict),
        typedcols.typed_list("TargetList", SourceTargetDict),
        typedcols.typed_list("AttachList", AttachDict),
        typedcols.typed_list("NodeList", NodeDict))
