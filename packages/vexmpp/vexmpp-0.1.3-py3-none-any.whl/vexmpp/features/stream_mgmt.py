# -*- coding: utf-8 -*-
from ..stanzas import Stanza
from ..errors import makeStanzaError
from ..protocols.stream_mgmt import NS_URI


async def handle(stream, feature_elem, sm_opts, timeout=None):
    assert(feature_elem is not None)
    nsmap = {"sm": NS_URI}

    enable_elem = Stanza("enable", nsmap={None: NS_URI})
    if sm_opts and sm_opts.resume:
        enable_elem.set("resume", "true")
    stream.send(enable_elem)

    resp = await stream.wait([("/sm:enabled", nsmap),
                              ("/sm:failed", nsmap)], timeout=timeout)
    if resp.name == "{%s}failed" % NS_URI:
        raise makeStanzaError(resp.xml)

    sm_opts.sm_id = resp.get("id")
    sm_opts.resume = bool(resp.get("resume") and
                          resp.get("resume") in ("1", "true"))
    sm_opts.resume_location = resp.get("location")
    sm_opts.max_resume_time = resp.get("max")

    return True
