import datetime
from struct import unpack

from io import BytesIO

from mustaine.protocol import *

# Implementation of Hessian 1.0.2 deserialization
#   see: http://hessian.caucho.com/doc/hessian-1.0-spec.xtp

class ParseError(Exception):
    pass

class Parser(object):
    def parse_string(self, bypesarray):
        if isinstance(bypesarray, str):
            stream = BytesIO(bypesarray.encode('utf-8'))
        else:
            stream = BytesIO(bypesarray)

        return self.parse_stream(stream)

    def parse_stream(self, stream):
        self._refs   = []
        self._result = None

        if hasattr(stream, 'read') and hasattr(stream.read, '__call__'):
            self._stream = stream
        else:
            raise TypeError('Stream parser can only handle objects supporting read()')

        while True:
            code = self._read(1)

            if code == b'c':
                if self._result:
                    raise ParseError('Encountered duplicate type header')

                version = self._read(2)
                if version != b'\x01\x00':
                    raise ParseError("Encountered unrecognized call version %r" % (version,))

                self._result = Call()
                continue

            elif code == b'r':
                if self._result:
                    raise ParseError('Encountered duplicate type header')

                version = self._read(2)
                if version != b'\x01\x00':
                    raise ParseError("Encountered unrecognized reply version %r" % (version,))

                self._result = Reply()
                continue

            else:
                if not self._result:
                    raise ParseError("Invalid Hessian message marker: %r" % (code,))

                if   code == b'H':
                    key, value = self._read_keyval()
                    self._result.headers[key] = value
                    continue

                elif code == b'm':
                    if not isinstance(self._result, Call):
                        raise ParseError('Encountered illegal method name within reply')

                    if self._result.method:
                        raise ParseError('Encountered duplicate method name definition')

                    self._result.method = self._read(unpack('>H', self._read(2))[0])
                    continue

                elif code == b'f':
                    if not isinstance(self._result, Reply):
                        raise ParseError('Encountered illegal fault within call')

                    if self._result.value:
                        raise ParseError('Encountered illegal extra object within reply')

                    self._result.value = self._read_fault()
                    continue

                elif code == b'z':
                    break

                else:
                    if isinstance(self._result, Call):
                        self._result.args.append(self._read_object(code))
                    else:
                        if self._result.value:
                            raise ParseError('Encountered illegal extra object within reply')

                        self._result.value = self._read_object(code)

        # have to hit a 'z' to land here, TODO derefs?
        return self._result


    def _read(self, n):
        try:
            r = self._stream.read(n)
        except IOError:
            raise ParseError('Encountered unexpected end of stream')
        except:
            raise
        else:
            if len(r) == 0:
                raise ParseError('Encountered unexpected end of stream')

        return r

    def _read_object(self, code):
        if   code == b'N':
            return None
        elif code == b'T':
            return True
        elif code == b'F':
            return False
        elif code == b'I':
            return int(unpack('>l', self._read(4))[0])
        elif code == b'L':
            return int(unpack('>q', self._read(8))[0])
        elif code == b'D':
            return float(unpack('>d', self._read(8))[0])
        elif code == b'd':
            return self._read_date()
        elif code == b's' or code == b'x':
            fragment = self._read_string()
            next     = self._read(1)
            if next.lower() == code:
                return fragment + self._read_object(next)
            else:
                raise ParseError("Expected terminal string segment, got %r" % (next,))
        elif code == b'S' or code == b'X':
            return self._read_string()
        elif code == b'b':
            fragment = self._read_binary()
            next     = self._read(1)
            if next.lower() == code:
                return fragment + self._read_object(next)
            else:
                raise ParseError("Expected terminal binary segment, got %r" % (next,))
        elif code == b'B':
            return self._read_binary()
        elif code == b'r':
            return self._read_remote()
        elif code == b'R':
            return self._refs[unpack(">L", self._read(4))[0]]
        elif code == b'V':
            return self._read_list()
        elif code == b'M':
            return self._read_map()
        else:
            raise ParseError("Unknown type marker %r" % (code,))

    def _read_date(self):
        timestamp = unpack('>q', self._read(8))[0]
        return datetime.datetime.fromtimestamp(timestamp / 1000)

    def _read_string(self):
        len = unpack('>H', self._read(2))[0]

        bytes = []
        while len > 0:
            byte = self._read(1)
            if ord(byte) in range(0x00, 0x7F):
                bytes.append(byte)
            elif ord(byte) in range(0xC2, 0xDF):
                bytes.append(byte + self._read(1))
            elif ord(byte) in range(0xE0, 0xEF):
                bytes.append(byte + self._read(2))
            elif ord(byte) in range(0xF0, 0xF4):
                bytes.append(byte + self._read(3))
            len -= 1

        return b''.join(bytes).decode('utf-8')

    def _read_binary(self):
        len = unpack('>H', self._read(2))[0]
        return Binary(self._read(len))

    def _read_remote(self):
        r    = Remote()
        code = self._read(1)

        if code == b't':
            r.type = self._read(unpack('>H', self._read(2))[0])
            code   = self._read(1)
        else:
            r.type = None

        if code != b's' and code != b'S':
            raise ParseError("Expected string object while parsing Remote object URL")

        r.url = self._read_object(code)
        return r

    def _read_list(self):
        code = self._read(1)

        if code == b't':
            # read and discard list type
            self._read(unpack('>H', self._read(2))[0])
            code = self._read(1)

        if code == b'l':
            # read and discard list length
            self._read(4)
            code = self._read(1)

        result = []
        self._refs.append(result)

        while code != b'z':
            result.append(self._read_object(code))
            code = self._read(1)

        return result

    def _read_map(self):
        code = self._read(1)

        if code == b't':
            type_len = unpack('>H', self._read(2))[0]
            if type_len > 0:
                # a typed map deserializes to an object
                result = Object(self._read(type_len))
            else:
                result = {}

            code = self._read(1)
        else:
            # untyped maps deserialize to a dict
            result = {}

        self._refs.append(result)

        fields = {}
        while code != b'z':
            key, value  = self._read_keyval(code)

            if isinstance(result, Object):
                fields[str(key)] = value
            else:
                fields[key] = value

            code = self._read(1)

        if isinstance(result, Object):
            fields['__meta_type'] = result._meta_type
            result.__setstate__(fields)
        else:
            result.update(fields)

        return result

    def _read_fault(self):
        fault = self._read_map()
        return Fault(fault['code'], fault['message'], fault.get('detail'))

    def _read_keyval(self, first=None):
        key   = self._read_object(first or self._read(1))
        value = self._read_object(self._read(1))

        return key, value

