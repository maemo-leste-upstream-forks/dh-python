import unittest
from os.path import exists
from dhpython.version import Version
from dhpython.interpreter import Interpreter

class TestInterpreter(unittest.TestCase):

    @unittest.skipUnless(exists('/usr/bin/pypy'), 'pypy is not installed')
    def test_pypy(self):
        sorted(Interpreter.parse('pypy').items()) == \
            [('debug', None), ('name', 'pypy'), ('options', ()), ('path', ''), ('version', None)]
        sorted(Interpreter.parse('#! /usr/bin/pypy --foo').items()) == \
            [('debug', None), ('name', 'pypy'), ('options', ('--foo',)), ('path', '/usr/bin/'), ('version', None)]
        Interpreter('pypy').sitedir(version='2.0') == '/usr/lib/pypy/dist-packages/'

    @unittest.skipUnless(exists('/usr/bin/python3.1'), 'python3.1 is not installed')
    def test_python31(self):
        i = Interpreter('python3.1')
        self.assertEqual(i.soabi(), '')
        self.assertIsNone(i.check_extname('foo.so'))
        self.assertIsNone(i.check_extname('foo.abi3.so'))
        self.assertIsNone(i.check_extname('foo/bar/bazmodule.so'))

    @unittest.skipUnless(exists('/usr/bin/python3.1-dbg'), 'python3.1-dbg is not installed')
    def test_python31dbg(self):
        i = Interpreter('python3.1-dbg')
        self.assertEqual(i.soabi(), '')
        self.assertIsNone(i.check_extname('foo.so'))
        self.assertIsNone(i.check_extname('foo.abi3.so'))
        self.assertIsNone(i.check_extname('foo/bar/bazmodule.so'))

    @unittest.skipUnless(exists('/usr/bin/python3.2'), 'python3.2 is not installed')
    def test_python32(self):
        i = Interpreter('python3.2')
        self.assertEqual(i.soabi(), 'cpython-32mu')
        self.assertRegex(i.check_extname('foo.so'), r'foo.cpython-32mu.*\.so')
        self.assertIsNone(i.check_extname('foo.abi3.so'))
        self.assertRegex(i.check_extname('foo/bar/bazmodule.so'), r'foo/bar/bazmodule.cpython-32mu.*\.so')

    @unittest.skipUnless(exists('/usr/bin/python3.2-dbg'), 'python3.2-dbg is not installed')
    def test_python32dbg(self):
        i = Interpreter('python3.2-dbg')
        self.assertEqual(i.soabi(), 'cpython-32dmu')
        self.assertRegex(i.check_extname('foo.so'), r'foo.cpython-32dmu.*\.so')
        self.assertIsNone(i.check_extname('foo.abi3.so'))
        self.assertRegex(i.check_extname('foo/bar/bazmodule.so'), r'foo/bar/bazmodule.cpython-32dmu.*\.so')

    @unittest.skipUnless(exists('/usr/bin/python3.3'), 'python3.3 is not installed')
    def test_python33(self):
        i = Interpreter('python3.3')
        self.assertEqual(i.soabi(), 'cpython-33m')
        self.assertRegex(i.check_extname('foo.so'), r'foo.cpython-33m.*\.so')
        self.assertIsNone(i.check_extname('foo.abi3.so'))
        self.assertRegex(i.check_extname('foo/bar/bazmodule.so'), r'foo/bar/baz.cpython-33m.*\.so')

    @unittest.skipUnless(exists('/usr/bin/python3.3-dbg'), 'python3.3-dbg is not installed')
    def test_python33dbg(self):
        i = Interpreter('python3.3-dbg')
        self.assertEqual(i.soabi(), 'cpython-33dm')
        self.assertRegex(i.check_extname('foo.so'), r'foo.cpython-33dm.*\.so')
        self.assertIsNone(i.check_extname('foo.abi3.so'))
        self.assertRegex(i.check_extname('foo/bar/bazmodule.so'), r'foo/bar/baz.cpython-33dm.*\.so')

    def test_version(self):
        i = Interpreter(impl='cpython2')
        self.assertEqual(str(i), 'python')
        self.assertEqual(i.binary('2.7'), '/usr/bin/python2.7')

if __name__ == '__main__':
    unittest.main()