#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016, CESNET, z. s. p. o.
# Use of this source is governed by an ISC license, see LICENSE file.

import json
import typedcols
import re

try:
    unicode = unicode
except NameError:
    unicode = str

media_type_re = re.compile(r"^[a-zA-Z0-9_-]+/[a-zA-Z0-9_+\.-]+$")
charset_re = re.compile(r"^[a-zA-Z0-9\.:_()-]+$")
handle_re = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")
id_re = re.compile(r"^[a-zA-Z0-9\._-]+$")
uri_re = re.compile(r"^[a-zA-Z][a-zA-Z0-9+\.-]*:[][a-zA-Z0-9\._~:/?#@*'&'()*+,;=%-]*$")
nsid_re = re.compile(r"^(?:[a-z_][a-z0-9_]*\.)*[a-z_][a-z0-9_]*$")
mac_re = re.compile(r"^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$")
netname_re = re.compile(r"^[a-zA-Z][a-zA-Z0-9+\.-]*:[][a-zA-Z0-9\._~:/?#@*'&'()*+,;=%-]*$")
hash_re = re.compile(r"^[a-zA-Z][a-zA-Z0-9+\.-]*:[][a-zA-Z0-9\._~:/?#@*'&'()*+,;=%-]*$")
event_tag_re = re.compile(r"^[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)?$")
tag_re = re.compile(r"^[a-zA-Z0-9_-]+$")

timestamp_re = re.compile(r"^([0-9]{4})-([0-9]{2})-([0-9]{2})[Tt ]([0-9]{2}):([0-9]{2}):([0-9]{2})(?:\.([0-9]+))?([Zz]|(?:[+-][0-9]{2}:[0-9]{2}))$")
duration_re = re.compile("(?:([0-9]+)[Dd])?([0-9]{2}):([0-9]{2}):([0-9]{2})(?:\.([0-9]+))?$")


def source_target_dict_typedef(flavour, list_flavour, addon=None):
    source_target_def = {
        "Type": {
            "description": "List of source/target categories.",
            "type": list_flavour["SourceTargetTag"]
        },
        "Hostname": {
            "description": "List of hostnames of this source/target. Should be FQDN, but may not conform exactly, because values, extracted from logs, messages, DNS, etc. may themselves be malformed. Empty array can be used to explicitly indicate that value has been inquired and not found (missing DNS name).",
            "type": list_flavour["String"]
        },
        "IP4": {
            "description": "List of IPv4 addresses of this source/target.",
            "type": list_flavour["Net4"]
        },
        "MAC": {
            "description": "List of MAC addresses of this source/target.",
            "type": list_flavour["MAC"]
        },
        "IP6": {
            "description": "List of IPv6 addresses of this source/target.",
            "type": list_flavour["Net6"]
        },
        "Port": {
            "description": "List of source or destination ports affected.",
            "type": list_flavour["Port"]
        },
        "Proto": {
            "description": "List of protocols, concerning connections from/to this source/target.",
            "type": list_flavour["ProtocolName"]
        },
        "URL": {
            "description": "List of Unified Resource Locator of this source/target. Should be formatted according to [[http://tools.ietf.org/html/rfc1738|RFC 1738]], [[http://tools.ietf.org/html/rfc1808|RFC 1808]] and related, however may not conform exactly, because values, extracted from logs, messages, etc. may themselves be malformed.",
            "type": list_flavour["String"]
        },
        "Email": {
            "description": "List of email address (for example Reply-To address in phishing message). Should be formatted according to [[http://tools.ietf.org/html/rfc5322#section-3.4|RFC 5322, section 3.4]] and related, however may not conform exactly, because values, extracted from logs, messages, DNS, etc. may themselves be malformed.",
            "type": list_flavour["String"]
        },
        "AttachHand": {
            "description": "List of identifiers of attachments related to this source/target - contain \"Handle\"s of related attachments.",
            "type": list_flavour["Handle"]
        },
        "Note": {
            "description": "Free text human readable additional note.",
            "type": flavour["String"]
        },
        "Spoofed": {
            "description": "Establishes whether this source/target is forged.",
            "type": flavour["Boolean"]
        },
        "Imprecise": {
            "description": "Establishes whether this source/target is knowingly imprecise.",
            "type": flavour["Boolean"]
        },
        "Anonymised": {
            "description": "Establishes whether this source/target is willingly incomplete.",
            "type": flavour["Boolean"]
        },
        "ASN": {
            "description": "List of autonomous system numbers of this source/target.",
            "type": list_flavour["Integer"]
        },
        "Router": {
            "description": "List of router/interface path information. Intentionally organisation specific, router identifiers have usually no clear meaning outside organisational unit.",
            "type": list_flavour["String"]
        },
        "Netname": {
            "description": "List of RIR database reference network identifier (for example \"ripe:CESNET-BB2\" or \"arin:WETEMAA\"). Common network identifiers are: ripe, arin, apnic, lacnic, afrinic. Empty array can be used to explicitly indicate that value has been inquired and not found (IP address from unassigned block).",
            "type": list_flavour["Netname"]
        },
        "Ref": {
            "description": "List of references to known sources, related to attack and/or vulnerability, specific to this source/target. May be URL of the additional info, or URN (according to [[http://tools.ietf.org/html/rfc2141|RFC 2141]]) in registered namespace ([[http://www.iana.org/assignments/urn-namespaces/urn-namespaces.xhtml|IANA]]) or unregistered ad-hoc namespace bearing reasonable information value and uniqueness, such as \"urn:cve:CVE-2013-2266\".",
            "type": list_flavour["URI"]
        }
    }
    if addon is not None:
        source_target_def.update(addon)
    return source_target_def


def attach_dict_typedef(flavour, list_flavour, addon=None):
    attach_def = {
        "Handle": {
            "description": "Message unique identifier for reference through Attach elements.",
            "type": flavour["Handle"]
        },
        "FileName": {
            "description": "List of filenames of the attached file.",
            "type": list_flavour["String"]
        },
        "Type": {
            "description": "List of attachment type tags.",
            "type": list_flavour["AttachmentTag"]
        },
        "Hash": {
            "description": "Listof checksums of the content (for example \"sha1:794467071687f7c59d033f4de5ece6b46415b633\" or \"md5:dc89f0b4ff9bd3b061dd66bb66c991b1\").",
            "type": list_flavour["Hash"]
        },
        "Size": {
            "description": "Length of the content.",
            "type": flavour["Integer"]
        },
        "Ref": {
            "description": "List of references to known sources, related to attack and/or vulnerability, specific to this attachment. May be URL of the additional info, or URN (according to [[http://tools.ietf.org/html/rfc2141|RFC 2141]]) in registered namespace ([[http://www.iana.org/assignments/urn-namespaces/urn-namespaces.xhtml|IANA]]) or unregistered ad-hoc namespace bearing reasonable information value and uniqueness, such as \"urn:clamav:Win.Trojan.Banker-14334\".",
            "type": list_flavour["URI"]
        },
        "Note": {
            "description": "Free text human readable additional note.",
            "type": flavour["String"]
        },
        "ContentType": {
            "description": "Internet Media Type of the attachment, according to [[http://tools.ietf.org/html/rfc2046|RFC 2046]] and related. Along with [[http://www.iana.org/assignments/media-types/media-types.xhtml|types standardized by IANA]] also non standard but widely used media types can be used (for examples see [[http://www.freeformatter.com/mime-types-list.html|MIME types list at freeformatter.com]]).",
            "type": flavour["MediaType"]
        },
        "ContentCharset": {
            "description": "Name of the content character set according to [[http://www.iana.org/assignments/character-sets/character-sets.xhtml|IANA list]]. If key is not defined, unspecified binary encoding is assumed.",
            "type": flavour["Charset"]
        },
        "ContentEncoding": {
            "description": "Encoding of the content, if feasible. Nonexistent key means native JSON encoding.",
            "type": flavour["Encoding"]
        },
        "Content": {
            "description": "Attachment content.",
            "type": flavour["String"]
        },
        "ContentID": {
            "description": "If content of attachment is transferred separately (in underlaying container), this key contains list of external IDs of the content, so it can be paired back to message.",
            "type": list_flavour["String"]
        },
        "ExternalURI": {
            "description": "If content of attachment is available and/or recognizable from external source, this is list of defining URIs (usually URLs). May also be URN (according to [[http://tools.ietf.org/html/rfc2141|RFC 2141]]) in registered namespace ([[http://www.iana.org/assignments/urn-namespaces/urn-namespaces.xhtml|IANA]]) or unregistered ad-hoc namespace bearing reasonable information value and uniqueness, such as \"urn:mhr:55eaf7effadc07f866d1eaed9c64e7ee49fe081a\", \"magnet:?xt=urn:sha1:YNCKHTQCWBTRNJIV4WNAE52SJUQCZO5C\".",
            "type": list_flavour["URI"]
        }
    }
    if addon is not None:
        attach_def.update(addon)
    return attach_def


def node_dict_typedef(flavour, list_flavour, addon=None):
    node_def = {
        "Name": {
            "description": "Name of the detector, which must be reasonably unique, however still bear some meaningful sense. Usually denotes hierarchy of organisational units which detector belongs to and its own name.",
            "type": flavour["NSID"]
        },
        "Type": {
            "description": "List of tags, describing various facets of the detector.",
            "type": list_flavour["NodeTag"]
        },
        "SW": {
            "description": "List of the names of the detection software (optionally including version). For example \"labrea-2.5-stable-1\" or \"HP TippingPoint 7500NX\".",
            "type": list_flavour["String"]
        },
        "AggrWin": {
            "description": "The size of the aggregation window, if applicable.",
            "type": flavour["Duration"]
        },
        "Note": {
            "description": "Free text human readable additional description.",
            "type": flavour["String"]
        }
    }
    if addon is not None:
        node_def.update(addon)
    return node_def


def idea_typedef(flavour, list_flavour, defaults_flavour, source_list, target_list, attach_list, node_list, addon=None):
    idea_def = {
        "Format": {
            "description": "Identifier of the IDEA container.",
            "type": flavour["Version"],
            "required": True
        },
        "ID": {
            "description": "Unique message identifier.",
            "type": flavour["ID"],
            "required": True
        },
        "AltNames": {
            "description": "List of alternative identifiers; strings which help to pair the event to internal system information (for example tickets in request tracker systems).",
            "type": list_flavour["String"]
        },
        "CorrelID": {
            "description": "List of identifiers of messages, which are information sources for creation of this message in case the message has been created based on correlation/analysis/deduction of other messages.",
            "type": list_flavour["ID"]
        },
        "AggrID": {
            "description": "List of identifiers of messages, which are aggregated into more concise form by this message. Should be sent mostly by intermediary nodes, which detect duplicates, or aggregate events, spanning multiple detection windows, into one longer.",
            "type": list_flavour["ID"]
        },
        "PredID": {
            "description": "List of identifiers of messages, which are obsoleted and information in them is replaced by this message. Should be sent only by detection nodes to incorporate further data about ongoing event.",
            "type": list_flavour["ID"]
        },
        "RelID": {
            "description": "List of otherwise related messages identifiers.",
            "type": list_flavour["ID"]
        },
        "CreateTime": {
            "description": "Timestamp of the creation of the IDEA message. May point out delay between detection and processing of data.",
            "type": flavour["Timestamp"]
        },
        "DetectTime": {
            "description": "Timestamp of the moment of detection of event (not necessarily time of the event taking place). This timestamp is mandatory, because every detector is able to know when it detected the information - for example when line about event appeared in the logfile, or when its information source says the event was detected, or at least when it accepted the information from the source.",
            "type": flavour["Timestamp"],
            "required": True
        },
        "EventTime": {
            "description": "Deduced start of the event/attack, or just time of the event if its solitary.",
            "type": flavour["Timestamp"]
        },
        "CeaseTime": {
            "description": "Deduced end of the event/attack.",
            "type": flavour["Timestamp"]
        },
        "WinStartTime": {
            "description": "Beginning of aggregation window in which event has been observed.",
            "type": flavour["Timestamp"]
        },
        "WinEndTime": {
            "description": "End of aggregation window in which event has been observed.",
            "type": flavour["Timestamp"]
        },
        "ConnCount": {
            "description": "Number of individual connections attempted or taken place.",
            "type": flavour["Integer"]
        },
        "FlowCount": {
            "description": "Number of individual simplex (one direction) flows.",
            "type": flavour["Integer"]
        },
        "PacketCount": {
            "description": "Number of individual packets transferred.",
            "type": flavour["Integer"]
        },
        "ByteCount": {
            "description": "Number of bytes transferred.",
            "type": flavour["Integer"]
        },
        "Category": {
            "description": "Array of event categories.",
            "description": "List of event categories.",
            "type": list_flavour["EventTag"],
            "required": True
        },
        "Ref": {
            "description": "List of references to known sources, related to attack and/or vulnerability. May be URL of the additional info, or URN (according to [[http://tools.ietf.org/html/rfc2141|RFC 2141]]) in registered namespace ([[http://www.iana.org/assignments/urn-namespaces/urn-namespaces.xhtml|IANA]]) or unregistered ad-hoc namespace bearing reasonable information value and uniqueness, such as \"urn:cve:CVE-2013-5634\".",
            "type": list_flavour["URI"]
        },
        "Confidence": {
            "description": "Confidence of detector in its own reliability of this particular detection. (0 - surely false, 1 - no doubts). If key is not presented, detector does not know (or has no capability to estimate the confidence).",
            "type": flavour["ConfidenceFloat"],
        },
        "Description": {
            "description": "Short free text human readable description.",
            "type": flavour["String"]
        },
        "Note": {
            "description": "Free text human readable addidional note, possibly longer description of incident if not obvious.",
            "type": flavour["String"]
        },
        "Source": {
            "description": "List of dictionaries of information concerning particular source of the problem.",
            "type": source_list,
        },
        "Target": {
            "description": "List of dictionaries of information concerning particular target of the problem.",
            "type": target_list,
        },
        "Attach": {
            "description": "Array of additional attachments information and data.",
            "type": attach_list,
        },
        "Node": {
            "description": "Array of detector descriptions.",
            "description": "List of detector or possible intermediary (event aggregator, correlator, etc.) descriptions, last visited first (as in e-mail Received headers).",
            "type": node_list
        }
    }

    for d, val in defaults_flavour.items():
        idea_def[d]["default"] = val

    if addon is not None:
        idea_def.update(addon)

    return idea_def


def list_types(flavour, list_factory=None):
    if list_factory is None:
        def list_factory(name, item_type):
            return typedcols.typed_list(name, item_type)
    lists = {}
    for t in ("AttachmentTag", "EventTag", "Handle", "Hash", "ID", "Integer",
              "MAC", "Netname", "Net4", "Net6", "NodeTag", "Port",
              "ProtocolName", "SourceTargetTag", "String", "URI"):
        lists[t] = list_factory(t, flavour[t])
    return lists


class IdeaBase(typedcols.TypedDict):
    allow_unknown = True
    typedef = {}

    @staticmethod
    def json_default(o):
        if isinstance(o, typedcols.TypedDict):
            return o.data
        elif isinstance(o, typedcols.TypedList):
            return o.data
        else:
            raise ValueError(o)

    def to_json(self, *args, **kwargs):
        kwargs.setdefault('sort_keys', True)
        return json.dumps(self, default=self.json_default, *args, **kwargs)
