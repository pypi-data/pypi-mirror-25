import unittest

from json_pointer import JsonPointer, JsonPointerException


class JsonPointerTest(unittest.TestCase):

    def setUp(self):
        self.pointer = JsonPointer('/foo/1')

    def test_move_pointer_forward(self):
        self.pointer.move_pointer_forward('baz')
        self.assertEqual(str(self.pointer), '/foo/1/baz')

        self.pointer.move_pointer_forward(0)
        self.assertEqual(str(self.pointer), '/foo/1/baz/0')

    def test_move_pointer_backward(self):
        attr = self.pointer.move_pointer_backward()
        self.assertEqual(attr, '1')
        self.assertEqual(str(self.pointer), '/foo')

        attr = self.pointer.move_pointer_backward()
        self.assertEqual(attr, 'foo')
        self.assertEqual(str(self.pointer), '')

        attr = self.pointer.move_pointer_backward()
        self.assertEqual(attr, None)
        self.assertEqual(str(self.pointer), '')

    def test_equals(self):
        self.assertTrue(self.pointer == JsonPointer('/foo/1'))
        self.assertFalse(self.pointer == JsonPointer('/foo'))

    def test_hash(self):
        self.assertTrue(self.pointer.__hash__() == JsonPointer('/foo/1').__hash__())
        self.assertFalse(self.pointer.__hash__() == JsonPointer('/foo').__hash__())

    def test_init_validation(self):
        self.assertRaises(JsonPointerException, JsonPointer, 0)
        self.assertRaises(JsonPointerException, JsonPointer, 'invalid')
