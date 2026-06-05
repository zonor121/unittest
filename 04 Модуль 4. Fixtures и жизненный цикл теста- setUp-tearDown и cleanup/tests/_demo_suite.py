import sqlite3
import tempfile
import unittest

TMP_DIRS = []
CONNS = []


class _BaseWithResources(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        TMP_DIRS.append(tmp.name)
        self.addCleanup(tmp.cleanup)

        conn = sqlite3.connect(":memory:")
        CONNS.append(conn)
        self.addCleanup(conn.close)

        conn.execute("CREATE TABLE t(x INTEGER)")
        conn.execute("INSERT INTO t(x) VALUES (1)")


class InnerPass(_BaseWithResources):
    def test_ok(self):
        self.assertEqual(1, 1)


class InnerFail(_BaseWithResources):
    def test_fail(self):
        self.assertEqual(1, 2)


class InnerError(_BaseWithResources):
    def test_error(self):
        raise RuntimeError("boom")


class InnerSetupError(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        TMP_DIRS.append(tmp.name)
        self.addCleanup(tmp.cleanup)

        conn = sqlite3.connect(":memory:")
        CONNS.append(conn)
        self.addCleanup(conn.close)

        raise RuntimeError("boom in setUp")

    def test_never_runs(self):
        self.assertTrue(False)