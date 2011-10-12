'''
Created on 12.10.2011

@author: Tengiz Sharafiev <btolfa@gmail.com>
'''
import unittest
from mustaine.client import HessianProxy
from mustaine import protocol


class Test(unittest.TestCase):
    
    def setUp(self):
        self.test = HessianProxy("http://hessian.caucho.com/test/test")
    
    def test_encode_double_0_0(self):
        self.assertTrue(self.test.argDouble_0_0(0.0))

    def test_encode_double_0_001(self):
        self.assertTrue(self.test.argDouble_0_001(0.001))

    def test_encode_double_1_0(self):
        self.assertTrue(self.test.argDouble_1_0(1.0))

    def test_encode_double_127_0(self):
        self.assertTrue(self.test.argDouble_127_0(127.0))

    def test_encode_double_128_0(self):
        self.assertTrue(self.test.argDouble_128_0(128.0))

    def test_encode_double_2_0(self):
        self.assertTrue(self.test.argDouble_2_0(2.0))

    def test_encode_double_3_14159(self):
        self.assertTrue(self.test.argDouble_3_14159(3.14159))

    def test_encode_double_32767_0(self):
        self.assertTrue(self.test.argDouble_32767_0(32767.0))

    def test_encode_double_65_536(self):
        self.assertTrue(self.test.argDouble_65_536(65.536))

    def test_encode_double_m0_001(self):
        self.assertTrue(self.test.argDouble_m0_001(-0.001))

    def test_encode_double_m128_0(self):
        self.assertTrue(self.test.argDouble_m128_0(-128.0))

    def test_encode_double_m129_0(self):
        self.assertTrue(self.test.argDouble_m129_0(-129.0))

    def test_encode_double_m32768_0(self):
        self.assertTrue(self.test.argDouble_m32768_0(-32768.0))

    def test_encode_false(self):
        self.assertTrue(self.test.argFalse(False))

    def test_encode_int_0(self):
        self.assertTrue(self.test.argInt_0(0))

    def test_encode_int_0x30(self):
        self.assertTrue(self.test.argInt_0x30(0x30))

    def test_encode_int_0x3ffff(self):
        self.assertTrue(self.test.argInt_0x3ffff(0x3ffff))

    def test_encode_int_0x40000(self):
        self.assertTrue(self.test.argInt_0x40000(0x40000))

    def test_encode_int_0x7ff(self):
        self.assertTrue(self.test.argInt_0x7ff(0x7ff))

    def test_encode_int_0x7fffffff(self):
        self.assertTrue(self.test.argInt_0x7fffffff(0x7fffffff))

    def test_encode_int_0x800(self):
        self.assertTrue(self.test.argInt_0x800(0x800))

    def test_encode_int_1(self):
        self.assertTrue(self.test.argInt_1(1))

    def test_encode_int_47(self):
        self.assertTrue(self.test.argInt_47(47))

    def test_encode_int_m0x40000(self):
        self.assertTrue(self.test.argInt_m0x40000(-0x40000))

    def test_encode_int_m0x40001(self):
        self.assertTrue(self.test.argInt_m0x40001(-0x40001))

    def test_encode_int_m0x800(self):
        self.assertTrue(self.test.argInt_m0x800(-0x800))

    def test_encode_int_m0x80000000(self):
        self.assertTrue(self.test.argInt_m0x80000000(-0x80000000))

    def test_encode_int_m0x801(self):
        self.assertTrue(self.test.argInt_m0x801(-0x801))

    def test_encode_int_m16(self):
        self.assertTrue(self.test.argInt_m16(-16))

    def test_encode_int_m17(self):
        self.assertTrue(self.test.argInt_m17(-17))

    def test_encode_long_0(self):
        self.assertTrue(self.test.argLong_0(0))

    def test_encode_long_0x10(self):
        self.assertTrue(self.test.argLong_0x10(0x10))

    def test_encode_long_0x3ffff(self):
        self.assertTrue(self.test.argLong_0x3ffff(0x3ffff))

    def test_encode_long_0x40000(self):
        self.assertTrue(self.test.argLong_0x40000(0x40000))
    
    def test_encode_long_0x7ff(self):
        self.assertTrue(self.test.argLong_0x7ff(0x7ff))
    
    def test_encode_long_0x7fffffff(self):
        self.assertTrue(self.test.argLong_0x7fffffff(0x7fffffff))
    
    def test_encode_long_0x800(self):
        self.assertTrue(self.test.argLong_0x800(0x800))
    
    def test_encode_long_0x80000000(self):
        self.assertTrue(self.test.argLong_0x80000000(0x80000000))
    
    def test_encode_long_1(self):
        self.assertTrue(self.test.argLong_1(1))
    
    def test_encode_long_15(self):
        self.assertTrue(self.test.argLong_15(15))
    
    def test_encode_long_m0x40000(self):
        self.assertTrue(self.test.argLong_m0x40000(-0x40000))
    
    def test_encode_long_m0x40001(self):
        self.assertTrue(self.test.argLong_m0x40001(-0x40001))
    
    def test_encode_long_m0x800(self):
        self.assertTrue(self.test.argLong_m0x800(-0x800))
    
    def test_encode_long_m0x80000000(self):
        self.assertTrue(self.test.argLong_m0x80000000(-0x80000000))
    
    def test_encode_long_m0x80000001(self):
        self.assertTrue(self.test.argLong_m0x80000001(-0x80000001))
    
    def test_encode_long_m0x801(self):
        self.assertTrue(self.test.argLong_m0x801(-0x801))
    
    def test_encode_long_m8(self):
        self.assertTrue(self.test.argLong_m8(-8))
    
    def test_encode_long_m9(self):
        self.assertTrue(self.test.argLong_m9(-9))
    
    def test_encode_null(self):
        self.assertTrue(self.test.argNull(None))
    
    def test_encode_object_0(self):
        payload = protocol.Object('com.caucho.hessian.test.A0')
        self.assertTrue(self.test.argObject_0(payload))
    
    def test_encode_object_1(self):
        payload = protocol.Object('com.caucho.hessian.test.TestObject', _value=0)
    
        self.assertTrue(self.test.argObject_1(payload))
    
    def test_encode_object_16(self):
        payload = [
            protocol.Object('com.caucho.hessian.test.A0'),
            protocol.Object('com.caucho.hessian.test.A1'),
            protocol.Object('com.caucho.hessian.test.A2'),
            protocol.Object('com.caucho.hessian.test.A3'),
            protocol.Object('com.caucho.hessian.test.A4'),
            protocol.Object('com.caucho.hessian.test.A5'),
            protocol.Object('com.caucho.hessian.test.A6'),
            protocol.Object('com.caucho.hessian.test.A7'),
            protocol.Object('com.caucho.hessian.test.A8'),
            protocol.Object('com.caucho.hessian.test.A9'),
            protocol.Object('com.caucho.hessian.test.A10'),
            protocol.Object('com.caucho.hessian.test.A11'),
            protocol.Object('com.caucho.hessian.test.A12'),
            protocol.Object('com.caucho.hessian.test.A13'),
            protocol.Object('com.caucho.hessian.test.A14'),
            protocol.Object('com.caucho.hessian.test.A15'),
            protocol.Object('com.caucho.hessian.test.A16')
        ]
    
        self.assertTrue(self.test.argObject_16(payload))
    
    def test_encode_object_2(self):
        payload = [
            protocol.Object('com.caucho.hessian.test.TestObject', _value=0),
            protocol.Object('com.caucho.hessian.test.TestObject', _value=1)
        ]
    
        self.assertTrue(self.test.argObject_2(payload))
    
    def test_encode_object_2a(self):
        payload = protocol.Object('com.caucho.hessian.test.TestObject', _value=0)
    
        self.assertTrue(self.test.argObject_2a([payload, payload]))
    
    def test_encode_object_2b(self):
        payload = [
            protocol.Object('com.caucho.hessian.test.TestObject', _value=0),
            protocol.Object('com.caucho.hessian.test.TestObject', _value=0)
        ]
    
        self.assertTrue(self.test.argObject_2b(payload))
    
    ### argObject_3 causes a stack pop. BOOM, recursion.
    # def disabled_test_encode_object_3(self):
    #     payload = protocol.Object('com.caucho.hessian.test.TestCons', _first = 'a', _rest = None)
    #     payload._rest = payload
    #
    #     self.assertTrue(self.test.argObject_3(payload))
    
    def test_encode_string_0(self):
        self.assertTrue(self.test.argString_0(""))
    
    def test_encode_string_1(self):
        self.assertTrue(self.test.argString_1("0"))
    
    def test_encode_string_31(self):
        payload = "0123456789012345678901234567890"
        self.assertTrue(self.test.argString_31(payload))
    
    def test_encode_string_32(self):
        payload = "01234567890123456789012345678901"
        self.assertTrue(self.test.argString_32(payload))
    
    ### here, we have to generate big convoluted strings. later.
    # def test_encode_string_1023(self):
    #     self.assertTrue(self.test.argString_1023("x" * 1023))
    #
    # def test_encode_string_1024(self):
    #     self.assertTrue(self.test.argString_1024("x" * 1024))
    #
    # def test_encode_string_65536(self):
    #     self.assertTrue(self.test.argString_65536("x" * 65536))
    
    def test_encode_true(self):
        self.assertTrue(self.test.argTrue(True))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()