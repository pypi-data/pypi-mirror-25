#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016, CESNET, z. s. p. o.
# Use of this source is governed by an ISC license, see LICENSE file.

import typedcols
from . import base
import uuid
import re
import time
import struct
import datetime
import ipranges
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
    if isinstance(s, uuid.UUID):
        return s
    if base.id_re.match(s) is None:
        raise ValueError("Wrong ID")
    return s


def Timestamp(t):
    if isinstance(t, datetime.datetime):
        return t
    try:
        # Try numeric type
        return datetime.datetime.fromtimestamp(float(t))
    except (TypeError, ValueError):
        pass
    # Try RFC3339 string
    res = base.timestamp_re.match(t)
    if res is not None:
        year, month, day, hour, minute, second = (int(n or 0) for n in res.group(*range(1, 7)))
        us_str = (res.group(7) or "0")[:6].ljust(6, "0")
        us = int(us_str)
        zonestr = res.group(8)
        zonespl = (0, 0) if zonestr in ['z', 'Z'] else [int(i) for i in zonestr.split(":")]
        zonediff = datetime.timedelta(minutes = zonespl[0]*60+zonespl[1])
        return datetime.datetime(year, month, day, hour, minute, second, us) - zonediff
    else:
        raise ValueError("Wrong Timestamp")


def Duration(t):
    if isinstance(t, datetime.timedelta):
        return t
    try:
        # Ok, try numeric type
        return datetime.timedelta(seconds=float(t))
    except (TypeError, ValueError):
        pass
    # Try definition match
    res = base.duration_re.match(t)
    if res is not None:
        day, hour, minute, second = (int(n or 0) for n in res.group(*range(1, 5)))
        ms_str = (res.group(5) or "0")[:6].ljust(6, "0")
        ms = int(ms_str)
        return datetime.timedelta(days=day, hours=hour, minutes=minute, seconds=second, microseconds=ms)
    else:
        raise ValueError("Wrong Duration")


def URI(s):
    if base.uri_re.match(s) is None:
        raise ValueError("Wrong URI")
    return s


def Net4(ip):
    for t in ipranges.IP4Net, ipranges.IP4Range, ipranges.IP4:
        try:
            return t(ip)
        except ValueError:
            pass
    raise ValueError("%s does not appear as IPv4 address, network or range string" % ip)


def Net6(ip):
    for t in ipranges.IP6Net, ipranges.IP6Range, ipranges.IP6:
        try:
            return t(ip)
        except ValueError:
            pass
    raise ValueError("%s does not appear as IPv6 address, network or range string" % ip)


def NSID(s):
    if base.nsid_re.match(s) is None:
        raise ValueError("Wrong NSID")
    return s


def MAC(s):
    if base.mac_re.match(s) is None:
        raise ValueError("Wrong MAC")
    return s


def Port(s):
    return int(s)


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
    return float(s)


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

idea_defaults = {
    "Format": "IDEA0",
    "ID": lambda: uuid.uuid4()
}

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

    @staticmethod
    def json_default(o):
        if isinstance(o, (ipranges.IPBase, uuid.UUID)):
            return str(o)
        elif isinstance(o, datetime.datetime):
            return o.isoformat() + "Z"
        elif isinstance(o, datetime.timedelta):
            hours = o.seconds // 3600
            mins = (o.seconds % 3600) // 60
            secs = o.seconds % 60
            return "%s%02i:%02i:%02i%s" % (("%iD" % o.days) if o.days else "", hours, mins, secs, (".%i" % o.microseconds) if o.microseconds else "")
        else:
            return base.IdeaBase.json_default(o)
