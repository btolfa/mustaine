import datetime
import time
from struct import pack

from mustaine.protocol import *

# Implementation of Hessian 1.0.2 serialization
#   see: http://hessian.caucho.com/doc/hessian-1.0-spec.xtp

ENCODERS = {}
def encoder_for(data_type):
    def register(f):
        # register function `f` to encode type `data_type`
        ENCODERS[data_type] = f
        return f
    return register

def returns(data_type):
    def wrap(f):
        # wrap function `f` to return a tuple of (type,data)
        def wrapped(*args):
            return data_type, f(*args)
        return wrapped
    return wrap

def encode_object(obj):
    if type(obj) in ENCODERS:
        encoder = ENCODERS[type(obj)]
    else:
        raise TypeError("mustaine.encoder cannot serialize %s" % (type(obj),))

    return encoder(obj)[1]


@encoder_for(type(None))
@returns(b'null')
def encode_null(_):
    return b'N'

@encoder_for(bool)
@returns(b'bool')
def encode_boolean(value):
    if value:
        return b'T'
    else:
        return b'F'

@encoder_for(int)
@returns(b'int')
def encode_int(value):
    return pack('>cl', b'I', value)

@encoder_for(int)
@returns(b'long')
def encode_long(value):
    return pack('>cq', b'L', value)

@encoder_for(float)
@returns(b'double')
def encode_double(value):
    return pack('>cd', b'D', value)

@encoder_for(datetime.datetime)
@returns(b'date')
def encode_date(value):
    return pack('>cq', b'd', int(time.mktime(value.timetuple())) * 1000)

@encoder_for(bytes)
@returns(b'string')
def encode_string(value):
    encoded = b''

    while len(value) > 65535:
        encoded += pack('>cH', b's', 65535)
        encoded += value[:65535]
        value    = value[65535:]

    encoded += pack('>cH', b'S', len(value.decode('utf-8')))
    encoded += value
    return encoded

@encoder_for(str)
@returns(b'string')
def encode_unicode(value):
    encoded = b''

    while len(value) > 65535:
        encoded += pack('>cH', b's', 65535)
        encoded += value[:65535].encode('utf-8')
        value    = value[65535:]

    encoded += pack('>cH', b'S', len(value))
    encoded += value.encode('utf-8')
    return encoded

@encoder_for(list)
@returns(b'list')
def encode_list(obj):
    encoded = b''.join(map(encode_object, obj))
    return pack('>2cl', b'V', b'l', -1) + encoded + b'z'

@encoder_for(tuple)
@returns(b'list')
def encode_tuple(obj):
    encoded = b''.join(map(encode_object, obj))
    return pack('>2cl', b'V', b'l', len(obj)) + encoded + b'z'

def encode_keyval(pair):
    return b''.join((encode_object(pair[0]), encode_object(pair[1])))

@encoder_for(dict)
@returns(b'map')
def encode_map(obj):
    encoded = b''.join(map(encode_keyval, list(obj.items())))
    return pack('>c', b'M') + encoded + b'z'

@encoder_for(Object)
def encode_mobject(obj):
    encoded  = pack('>cH', b't', len(obj._meta_type)) + obj._meta_type
    members  = obj.__getstate__()
    del members['__meta_type'] # this is here for pickling. we don't want or need it

    encoded += b''.join(map(encode_keyval, list(members.items())))
    return (obj._meta_type.rpartition('.')[2], pack('>c', b'M') + encoded + b'z')

@encoder_for(Remote)
@returns(b'remote')
def encode_remote(obj):
    encoded = encode_string(obj.url)
    return pack('>2cH', b'r', b't', len(obj.type_name)) + obj.type_name + encoded

@encoder_for(Binary)
@returns(b'binary')
def encode_binary(obj):
    encoded = b''
    value   = obj.value

    while len(value) > 65535:
        encoded += pack('>cH', b'b', 65535)
        encoded += value[:65535]
        value    = value[65535:]

    encoded += pack('>cH', b'B', len(value))
    encoded += value

    return encoded

@encoder_for(Call)
@returns(b'call')
def encode_call(call):
    method    = call.method.encode('utf8')
    headers   = b''
    arguments = b''

    for header,value in list(call.headers.items()):
        if not isinstance(header, str):
            raise TypeError("Call header keys must be strings")

        headers += pack('>cH', b'H', len(header)) + header
        headers += encode_object(value)

    # TODO: this is mostly duplicated at the top of the file in encode_object. dedup
    for arg in call.args:
        if type(arg) in ENCODERS:
            encoder = ENCODERS[type(arg)]
        else:
            raise TypeError("mustaine.encoder cannot serialize %s" % (type(arg),))

        data_type, arg = encoder(arg)
        if call.overload:
            method    += b'_' + data_type
        arguments += arg

    encoded  = pack('>cBB', b'c', 1, 0)
    encoded += headers
    encoded += pack('>cH', b'm', len(method)) + method
    encoded += arguments
    encoded += b'z'

    return encoded

