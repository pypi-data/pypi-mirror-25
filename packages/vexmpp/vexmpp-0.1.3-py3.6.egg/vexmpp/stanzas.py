# -*- coding: utf-8 -*-
import uuid
import functools
from copy import deepcopy
from lxml import etree
from .namespaces import (XML_NS_URI, STREAM_NS_URI,
                         CLIENT_NS_URI, SERVER_NS_URI,
                         STANZA_ERROR_NS_URI, STREAM_ERROR_NS_URI)
from .jid import Jid

XML_LANG = "{%s}lang" % XML_NS_URI
STANZA_ERROR_TAG = "{%s}error" % STANZA_ERROR_NS_URI
STREAM_ERROR_TAG = "{%s}error" % STREAM_ERROR_NS_URI


class ElementWrapper:
    _NEXT_ID = 1
    _UUID = str(uuid.uuid4()).split("-")[0]

    def __init__(self, xml):
        if isinstance(xml, ElementWrapper):
            self.xml = xml.xml
        else:
            self.xml = xml

    def _getChildText(self, child):
        e = self.xml.xpath("child::%s" % child)
        return e[0].text if e else None

    def _setChildText(self, child, s):
        matches = self.xml.xpath("child::%s" % child)
        e = matches[0] if matches else None

        if s is None:
            if e is not None:
                self.xml.remove(e)
            return

        if e is None:
            e = etree.Element(child)
            self.xml.append(e)
        e.text = s

    def toXml(self, pprint=False, encoding="utf-8"):
        return etree.tostring(self.xml, pretty_print=pprint, encoding=encoding)

    @property
    def name(self):
        return self.xml.tag

    @property
    def type(self):
        return self.get("type")

    @type.setter
    def type(self, t):
        self.set("type", t)

    @property
    def id(self):
        return self.get("id")

    @id.setter
    def id(self, i):
        self.set("id", i)

    def setId(self, prefix=None):
        id_str = ""

        if prefix and ':' in prefix:
            raise ValueError("Prefix cannot contain ':'")
        elif prefix:
            id_str += "%s:" % prefix

        id_str += "%s-" % ElementWrapper._UUID
        id_str += str(ElementWrapper._NEXT_ID)
        ElementWrapper._NEXT_ID += 1
        self.id = id_str

    def x(self, ns):
        x = self.getChild("x", ns)
        return ElementWrapper(x) if (x is not None) else None

    def getChild(self, name, ns):
        child = self.xml.find("{%s}%s" % (ns, name))
        return child

    # ----- etree Element interface begin -----
    def find(self, *args, **kwargs):
        e = self.xml.find(*args, **kwargs)
        return ElementWrapper(e) if e is not None else None

    def xpath(self, *args, **kwargs):
        matches = self.xml.xpath(*args, **kwargs)
        retval = []
        for m in matches:
            if isinstance(m, str):
                retval.append(m)
            else:
                retval.append(ElementWrapper(m))
        return retval

    def get(self, key, default=None, as_jid=False):
        value = self.xml.get(key, default=default)
        if value:
            return value if not as_jid else Jid(value)
        else:
            return None

    def set(self, attr, s):
        if not s:
            if attr in self.xml.attrib:
                del self.xml.attrib[attr]
        else:
            if isinstance(s, Jid):
                s = s.full
            self.xml.attrib[attr] = s

    def append(self, child_elem):
        if isinstance(child_elem, ElementWrapper):
            child_elem = child_elem.xml
        return self.xml.append(child_elem)

    def remove(self, child_elem):
        if isinstance(child_elem, ElementWrapper):
            child_elem = child_elem.xml
        return self.xml.remove(child_elem)

    def findtext(self, *args, **kwargs):
        return self.xml.findtext(*args, **kwargs)

    def findall(self, *args, **kwargs):
        all_ = self.xml.findall(*args, **kwargs)
        return [ElementWrapper(e) for e in all_]

    def __iter__(self):
        return iter(self.xml)

    @property
    def attrib(self):
        return self.xml.attrib

    @property
    def text(self):
        return self.xml.text

    @text.setter
    def text(self, txt):
        self.xml.text = txt

    @property
    def tag(self):
        return self.xml.tag

    def clear(self):
        return self.xml.clear()

    def getchildren(self):
        return self.xml.getchildren()

    # ----- etree Element interface end -----

    @staticmethod
    def _makeTagName(tag, ns):
        return "{%s}%s" % (ns, tag)

    def appendChild(self, name, ns=None):
        if not ns:
            nsmap = self.xml.nsmap
            # None represents the unprefixed default namespace. Top-level stanza
            # types don't have this.
            ns = nsmap[None] if None in nsmap else None
        else:
            nsmap = {None: ns}

        c = etree.Element("{%s}%s" % (ns, name), nsmap=nsmap)
        self.xml.append(c)
        return ElementWrapper(c)


class Stanza(ElementWrapper):
    XPATH = (None, None)

    TYPE_GET = "get"
    TYPE_SET = "set"
    TYPE_ERROR = "error"
    TYPE_RESULT = "result"

    def __init__(self, tag=None, nsmap=None, xml=None, attrs=None):

        if xml is None and tag:
            xml = etree.Element(tag, nsmap=nsmap)
        elif xml is None:
            raise ValueError("'tag' or 'xml' argument is required")

        super().__init__(xml)

        for name, value in (attrs or {}).items():
            self.set(name, value)

    def _initAttributes(self, to=None, frm=None, type=None, id=None):
        if to:
            self.to = to
        if frm:
            self.frm = frm
        if type:
            self.type = type
        if id:
            self.id = id

    @property
    def to(self):
        return self.get("to", as_jid=True)

    @to.setter
    def to(self, j):
        self.set("to", j)

    @property
    def frm(self):
        return self.get("from", as_jid=True)

    @frm.setter
    def frm(self, j):
        self.set("from", j)

    @property
    def error(self):
        from . import errors
        error = self.xml.xpath("/*/error")
        if error:
            return errors.makeStanzaError(error[0])
        return None

    @error.setter
    def error(self, err):
        from . import errors
        curr = self.xml.xpath("/*/error")
        if curr:
            self.xml.remove(curr[0])

        if err is not None:
            if not isinstance(err, errors.StanzaError):
                raise ValueError("error attribute must be of type StanzaError")
            self.xml.append(err.xml)

    def swapToFrom(self):
        tmp_to = self.to
        tmp_from = self.frm
        if tmp_from:
            self.to = tmp_from
        if tmp_to:
            self.frm = tmp_to

    def errorResponse(self, err):
        err_stanza = deepcopy(self)
        err_stanza.type = "error"
        for c in err_stanza.xml.getchildren():
            err_stanza.xml.remove(c)
        err_stanza.error = err
        err_stanza.swapToFrom()
        return err_stanza

    def resultResponse(self, clear=False):
        res_stanza = deepcopy(self)
        res_stanza.type = "result"
        res_stanza.error = None
        res_stanza.swapToFrom()
        if clear:
            for c in res_stanza.xml.getchildren():
                res_stanza.xml.remove(c)
        return res_stanza


class StreamHeader(Stanza):
    XPATH = ("/stream:stream", {"stream": STREAM_NS_URI})

    def __init__(self, ns=CLIENT_NS_URI, to=None, frm=None, version="1.0",
                 lang="en", id=None, xml=None):
        if xml is not None:
            assert(xml.tag == "{%s}stream" % STREAM_NS_URI)
            assert(xml.nsmap["stream"] == STREAM_NS_URI)
            assert(xml.nsmap[None] in [CLIENT_NS_URI, SERVER_NS_URI])
            super().__init__(xml=xml)
        else:
            assert(ns in [CLIENT_NS_URI, SERVER_NS_URI])
            super().__init__("{%s}stream" % STREAM_NS_URI,
                             nsmap={"stream": STREAM_NS_URI, None: ns})
            self._initAttributes(to=to, frm=frm, id=id)
            self.version = version
            self.lang = lang

    @property
    def version(self):
        return self.get("version")

    @version.setter
    def version(self, v):
        self.set("version", v)

    @property
    def lang(self):
        return self.get(XML_LANG)

    @lang.setter
    def lang(self, l):
        self.set(XML_LANG, l)

    @property
    def defaultNamespace(self):
        return self.xml.nsmap[None]

    def toXml(self, pprint=False, encoding="utf-8"):
        # Special serialization since it must be an open tag.
        header = u"<stream:stream xmlns:stream='%s' xmlns='%s' " % \
                 (STREAM_NS_URI, self.defaultNamespace)
        if self.lang:
            header += u"xml:lang='%s' " % self.lang
        if self.version:
            header += "version='%s'" % self.version
        if self.to:
            header += " to='%s'" % self.to.full
        if self.frm:
            header += " from='%s'" % self.frm.full
        if self.id is not None:
            header += " id='%s'" % self.id
        header += ">\n"
        return header.encode(encoding)


class StreamFeatures(Stanza):
    XPATH = ("/stream:features", {"stream": STREAM_NS_URI})

    def __init__(self, xml=None):
        if xml is not None:
            assert(xml.tag == "{%s}features" % STREAM_NS_URI)
            assert(xml.nsmap["stream"] == STREAM_NS_URI)
            super().__init__(xml=xml)
        else:
            super().__init__("{%s}features" % STREAM_NS_URI,
                             nsmap={"stream": STREAM_NS_URI})

    def getFeature(self, name, ns):
        for feature in self.xml:
            if feature.tag == "{%s}%s" % (ns, name):
                return feature
        return None


class StreamError(Stanza, RuntimeError):
    XPATH = ("/stream:error", {"stream": STREAM_NS_URI})

    def __init__(self, error=None, xml=None):
        assert(error is not None or xml is not None)

        if xml is not None:
            assert(xml.tag == "{%s}error" % STREAM_NS_URI)
            assert(xml.nsmap["stream"] == STREAM_NS_URI)
            super().__init__(xml=xml)
        else:
            super().__init__("{%s}error" % STREAM_NS_URI,
                             nsmap={"stream": STREAM_NS_URI})
            self.error = error

    @property
    def error(self):
        from . import errors
        return errors.makeStreamError(self.xml)

    @error.setter
    def error(self, err):
        from . import errors
        if not isinstance(err, errors.StreamError):
            raise ValueError("error attribute must be of type "
                             "hiss.xmpp.errors.StreamError")
        self.xml = err.xml


class Iq(Stanza):
    XPATH = ("/iq", None)

    def __init__(self, to=None, frm=None, type="get", id=None, request=None,
                 xml=None, id_prefix=None, attrs=None):
        if xml is not None:
            assert(xml.tag == "iq")
            assert(None not in xml.nsmap)
            super().__init__(xml=xml, attrs=attrs)
        else:
            super().__init__("iq", attrs=attrs)
            self._initAttributes(to=to, frm=frm, id=id, type=type)
            if id is None:
                # Iqs most of all need id values
                self.setId(prefix=id_prefix)
            if request:
                name, ns = request
                self.xml.append(etree.Element("{%s}%s" % (ns, name),
                                              nsmap={None: ns}))

    @property
    def request(self):
        for e in self.xml.getchildren():
            if e.tag != STANZA_ERROR_TAG:
                return ElementWrapper(e)
        return None
    query = request


@functools.total_ordering
class Presence(Stanza):
    XPATH = ("/presence", None)

    TYPE_AVAILABLE = 'available'
    TYPE_UNAVAILABLE = 'unavailable'
    TYPE_SUBSCRIBE = 'subscribe'
    TYPE_SUBSCRIBED = 'subscribed'
    TYPE_UNSUBSCRIBE = 'unsubscribe'
    TYPE_UNSUBSCRIBED = 'unsubscribed'
    TYPE_PROBE = 'probe'

    SHOW_AWAY = 'away'
    SHOW_CHAT = 'chat'
    SHOW_DND = 'dnd'
    SHOW_XA = 'xa'

    ORDERED_SHOWS = [SHOW_CHAT, None, SHOW_AWAY, SHOW_XA, SHOW_DND]

    def __init__(self, to=None, frm=None, type=TYPE_AVAILABLE, priority=None,
                 show=None, status=None, xml=None, attrs=None):
        if xml is not None:
            assert(xml.tag == "presence")
            assert(None not in xml.nsmap)
            super().__init__(xml=xml, attrs=attrs)
        else:
            super().__init__("presence", attrs=attrs)
            self._initAttributes(to=to, frm=frm, type=type)
            self.priority = priority
            self.show = show
            self.status = status

    def __gt__(self, rhs):
        # Must implement even with total_ordering to make !lt != gt
        if self < rhs:
            return False
        else:
            if self.priority == rhs.priority and self.show == rhs.show:
                return False
            else:
                return True

    def __lt__(self, rhs):
        if self.priority < rhs.priority:
            return True
        elif self.priority > rhs.priority:
            return False
        else:
            if (self.ORDERED_SHOWS.index(self.show) <=
                    self.ORDERED_SHOWS.index(rhs.show)):
                return False
            else:
                return True

    @property
    def type(self):
        t = self.get("type")
        return t if t else Presence.TYPE_AVAILABLE

    @type.setter
    def type(self, t):
        if t == Presence.TYPE_AVAILABLE:
            if "type" in self.xml.attrib:
                del self.xml.attrib["type"]
        else:
            self.set("type", t)

    @property
    def priority(self):
        t = self._getChildText("priority")
        return int(t) if t is not None else None

    @priority.setter
    def priority(self, i):
        if i is None:
            self._setChildText("priority", None)
        else:
            i = int(i)
            if -128 < i < 127:
                self._setChildText("priority", str(i))
            else:
                raise ValueError("out of range: -128 < priority > 127")

    @property
    def show(self):
        return self._getChildText("show")

    @show.setter
    def show(self, s):
        if s not in self.ORDERED_SHOWS:
            raise ValueError("Invald show: %s" % s)
        self._setChildText("show", s)

    @property
    def status(self):
        return self._getChildText("status")

    @status.setter
    def status(self, s):
        self._setChildText("status", s)


class Message(Stanza):
    XPATH = ("/message", None)

    TYPE_CHAT = "chat"
    TYPE_ERROR = "error"
    TYPE_GC = "groupchat"
    TYPE_HEADLINE = "headline"
    TYPE_NORMAL = "normal"

    def __init__(self, to=None, frm=None, type=TYPE_CHAT, subject=None,
                 body=None, thread=None, xml=None, attrs=None):
        if xml is not None:
            assert(xml.tag == "message")
            assert(None not in xml.nsmap)
            super().__init__(xml=xml, attrs=attrs)
        else:
            super().__init__("message", attrs=attrs)
            self._initAttributes(to=to, frm=frm, type=type)
            self.subject = subject
            self.body = body
            self.thread = thread

    @property
    def type(self):
        t = self.get("type")
        return t if t else Message.TYPE_NORMAL

    @type.setter
    def type(self, t):
        if not t or t == Message.TYPE_NORMAL:
            if "type" in self.xml.attrib:
                del self.xml.attrib["type"]
        else:
            self.set("type", t)

    @property
    def subject(self):
        return self._getChildText("subject")

    @subject.setter
    def subject(self, s):
        self._setChildText("subject", s)

    @property
    def body(self):
        return self._getChildText("body")

    @body.setter
    def body(self, s):
        self._setChildText("body", s)

    @property
    def thread(self):
        return self._getChildText("thread")

    @thread.setter
    def thread(self, s):
        self._setChildText("thread", s)


def makeStanza(elem):
    if elem.tag == "presence":
        return Presence(xml=elem)
    elif elem.tag == "message":
        return Message(xml=elem)
    elif elem.tag == "iq":
        return Iq(xml=elem)
    elif elem.tag == "{%s}stream" % STREAM_NS_URI:
        return StreamHeader(xml=elem)
    elif elem.tag == "{%s}features" % STREAM_NS_URI:
        return StreamFeatures(xml=elem)
    elif elem.tag == "{%s}error" % STREAM_NS_URI:
        return StreamError(xml=elem)
    else:
        return Stanza(xml=elem)
