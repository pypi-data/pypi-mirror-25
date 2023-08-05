import unittest

import docker

from bblfsh import BblfshClient, filter
from bblfsh.github.com.bblfsh.sdk.protocol.generated_pb2 import ParseResponse
from github.com.bblfsh.sdk.uast.generated_pb2 import Node
from bblfsh.launcher import ensure_bblfsh_is_running

class BblfshTests(unittest.TestCase):
    BBLFSH_SERVER_EXISTED = None

    @classmethod
    def setUpClass(cls):
        cls.BBLFSH_SERVER_EXISTED = ensure_bblfsh_is_running()

    @classmethod
    def tearDownClass(cls):
        if not cls.BBLFSH_SERVER_EXISTED:
            client = docker.from_env(version="auto")
            client.containers.get("bblfsh").remove(force=True)
            client.api.close()

    def setUp(self):
        self.client = BblfshClient("0.0.0.0:9432")

    def testUASTDefaultLanguage(self):
        uast = self.client.parse(__file__)
        self._validate_uast(uast)

    def testUASTPython(self):
        uast = self.client.parse(__file__, language="Python")
        self._validate_uast(uast)

    def testUASTFileContents(self):
        with open(__file__) as fin:
            contents = fin.read()
        uast = self.client.parse("file.py", contents=contents)
        self._validate_uast(uast)
        self._validate_filter(uast)

    def testBrokenFilter(self):
        from sys import version_info
        if version_info[0:2] != (3, 4):
            # Skip test 3.4: cant capture SystemException from binary modules
            self.assertRaises(SystemError, filter, 0, "foo")

    def _validate_uast(self, uast):
        self.assertIsNotNone(uast)
        # self.assertIsInstance() does not work - must be some metaclass magic
        self.assertEqual(type(uast).DESCRIPTOR.full_name,
                         ParseResponse.DESCRIPTOR.full_name)
        self.assertEqual(len(uast.errors), 0)
        self.assertIsInstance(uast.uast, Node)

    def _validate_filter(self, uast):
        results = filter(uast.uast, "//Import[@roleImportDeclaration]//alias")
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].token, "unittest")
        self.assertEqual(results[1].token, "docker")


if __name__ == "__main__":
    unittest.main()
