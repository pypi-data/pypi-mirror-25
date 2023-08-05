import unittest
import json
import os
from json_pointer import evaluate, JsonPointerException
from tests import TEST_DIR

JSON_FILE = os.path.join(TEST_DIR, 'test.json')


class EvaluateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(JSON_FILE) as json_file:
            cls.json = json.load(json_file)

    def test_evaluate_positives(self):
        self.assertEqual(evaluate('', self.json), self.json)
        self.assertEqual(evaluate('/foo/0', self.json), 'bar')
        self.assertEqual(evaluate('/foo/-', self.json), 'baz')
        self.assertEqual(evaluate('/', self.json), 0)
        self.assertEqual(evaluate('/a~1b', self.json), 1)
        self.assertEqual(evaluate('/c%d', self.json), 2)
        self.assertEqual(evaluate('/e^f', self.json), 3)
        self.assertEqual(evaluate('/g|h', self.json), 4)
        self.assertEqual(evaluate('/i\\j', self.json), 5)
        self.assertEqual(evaluate('/k\"l', self.json), 6)
        self.assertEqual(evaluate('/ ', self.json), 7)
        self.assertEqual(evaluate('/m~0n', self.json), 8)
        self.assertEqual(evaluate('/0/1', self.json), 9)

        # Testing URI Fragments
        self.assertEqual(evaluate('/c%25d', self.json), 2)
        self.assertEqual(evaluate('/e%5Ef', self.json), 3)
        self.assertEqual(evaluate('/g%7Ch', self.json), 4)
        self.assertEqual(evaluate('/i%5Cj', self.json), 5)
        self.assertEqual(evaluate('/k%22l', self.json), 6)
        self.assertEqual(evaluate('/%20', self.json), 7)

    def test_evaluate_negatives(self):
        self.assertRaises(JsonPointerException, evaluate, '/foo/22', self.json)
        self.assertRaises(JsonPointerException, evaluate, '/unresolvable', self.json)
        self.assertRaises(JsonPointerException, evaluate, '/foo/unresolvable', self.json)
        self.assertRaises(JsonPointerException, evaluate, 'garbage', self.json)
        self.assertRaises(JsonPointerException, evaluate, '/foo/000001', self.json)
