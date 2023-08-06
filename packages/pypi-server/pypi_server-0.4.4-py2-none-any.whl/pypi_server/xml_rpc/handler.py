# encoding: utf-8
import base64
import datetime
import logging
from types import NoneType
import os
from tornado.gen import coroutine, maybe_future
from tornado.web import RequestHandler, HTTPError
from lxml import etree

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

try:
    unicode
except NameError:
    unicode = str


class Binary(str):
    pass


log = logging.getLogger(__name__)


class XMLRPCHandler(RequestHandler):
    SCHEMA = etree.XMLParser(
        schema=etree.XMLSchema(
            file=os.path.join(CURRENT_DIR, 'xmlrpc.xsd')
        )
    )

    METHOD_PREFIX = "rpc_"

    TIME_FORMAT = "%Y%m%dT%H:%M:%S"

    RPC_METHODS = set([])

    @coroutine
    def post(self, *args, **kwargs):
        if 'xml' not in self.request.headers.get('Content-Type', ''):
            raise HTTPError(400)

        try:
            xml_request = etree.fromstring(self.request.body, self.SCHEMA)
        except etree.XMLSyntaxError:
            raise HTTPError(400)

        method_name = xml_request.xpath('//methodName[1]')[0].text
        method = getattr(self, "{0}{1}".format(self.METHOD_PREFIX, method_name), None)
        if not callable(method):
            log.warning("Can't find method %s%s in ", self.METHOD_PREFIX, method_name, self.__class__.__name__)
            raise HTTPError(404)

        log.info("RPC Call: %s => %s.%s.%s", method_name, method.__module__, method.__class__.__name__, method.__name__)

        args = map(
            self._process_param,
            xml_request.xpath('//params/param/value/*')
        )

        try:
            root = etree.Element("methodResponse")
            el_params = etree.Element("params")
            el_param = etree.Element("param")
            el_value = etree.Element("value")
            el_param.append(el_value)
            el_params.append(el_param)
            root.append(el_params)

            result = yield maybe_future(method(*args))

            el_value.append(
                self._process_result(result)
            )
        except Exception as e:
            root = etree.Element('methodResponse')
            xml_fault = etree.Element('fault')
            xml_value = etree.Element('value')

            root.append(xml_fault)
            xml_fault.append(xml_value)

            xml_value.append(self._process_result({
                "faultCode": getattr(e, 'code', -32500),
                "faultString": repr(e),
            }))

            log.exception(e)

        self.set_header("Content-Type", "text/xml; charset=utf-8")
        xml = etree.tostring(root, xml_declaration=True, encoding="utf-8")
        self.finish(xml)

    @classmethod
    def _process_result(cls, result):
        def xml_string(x):
            el = etree.Element('string')
            el.text = str(x)
            return el

        def xml_float(x):
            el = etree.Element('double')
            el.text = str(x)
            return el

        def xml_datetime(x):
            el = etree.Element('dateTime.iso8601')
            el.text = x.strftime(cls.TIME_FORMAT)
            return el

        def xml_int(x):
            el = etree.Element('i4')
            el.text = str(x)
            return el

        def xml_binary(x):
            el = etree.Element('base64')
            el.text = base64.b64encode(x)
            return el

        def xml_bool(x):
            el = etree.Element('boolean')
            el.text = "1" if x else "0"
            return el

        def xml_none(x):
            return etree.Element('nil')

        def xml_list(x):
            array = etree.Element('array')
            data = etree.Element('data')
            array.append(data)

            for i in x:
                el = etree.Element('value')
                el.append(cls._process_result(i))
                data.append(el)

            return array

        def xml_dict(x):
            struct = etree.Element('struct')

            for key, value in x.items():
                member = etree.Element('member')
                struct.append(member)

                key_el = etree.Element('name')
                key_el.text = str(key)
                member.append(key_el)

                value_el = etree.Element('value')
                value_el.append(cls._process_result(value))
                member.append(value_el)

            return struct

        types = {
            str: xml_string,
            unicode: xml_string,
            tuple: xml_list,
            list: xml_list,
            int: xml_int,
            float: xml_float,
            datetime.datetime: xml_datetime,
            Binary: xml_binary,
            bool: xml_bool,
            NoneType: xml_none,
            dict: xml_dict
        }

        func = types.get(type(result))
        if not func:
            raise RuntimeError("Can't serialise type: %s", type(result))

        return func(result)

    @classmethod
    def _process_param(cls, value):
        def from_struct(p):
            return dict(
                map(
                    lambda x: (x[0].text, x[1]),
                    zip(
                        p.xpath(".//member/name"),
                        map(cls._process_param, p.xpath(".//member/value/*"))
                    )
                )
            )

        def from_array(p):
            return list(map(cls._process_param, p.xpath(".//data/value/*")))

        types = {
            'string': lambda x: str(x.text),
            'struct': from_struct,
            'array': from_array,
            'base64': lambda x: base64.b64decode(x.text),
            'boolean': lambda x: bool(int(x.text)),
            'dateTime.iso8601': lambda x: datetime.datetime.strptime(x.text, cls.TIME_FORMAT),
            'double': lambda x: float(x.text),
            'integer': lambda x: int(x.text),
            'nil': lambda x: None,
        }

        return types.get(value.tag)(value)
