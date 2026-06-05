import io
import sqlite3
import unittest
from pathlib import Path

from tests._demo_suite import TMP_DIRS, CONNS, InnerPass, InnerFail, InnerError, InnerSetupError


class TestCleanupProof(unittest.TestCase):
    def test_cleanup_happens_on_success_fail_error(self):
        TMP_DIRS.clear()
        CONNS.clear()

        suite = unittest.TestSuite()
        loader = unittest.defaultTestLoader
        suite.addTests(loader.loadTestsFromTestCase(InnerPass))
        suite.addTests(loader.loadTestsFromTestCase(InnerFail))
        suite.addTests(loader.loadTestsFromTestCase(InnerError))
        suite.addTests(loader.loadTestsFromTestCase(InnerSetupError))

        stream = io.StringIO()
        result = unittest.TextTestRunner(stream=stream, verbosity=0).run(suite)

        self.assertGreaterEqual(len(result.failures), 1)
        self.assertGreaterEqual(len(result.errors), 1)

        leaked = [p for p in TMP_DIRS if Path(p).exists()]
        self.assertEqual(leaked, [], msg=f"Остались временные директории: {leaked}")

        not_closed = []
        for i, conn in enumerate(CONNS):
            try:
                conn.execute("SELECT 1")
            except sqlite3.ProgrammingError:
                pass
            else:
                not_closed.append(i)

        self.assertEqual(not_closed, [], msg=f"Есть незакрытые соединения (индексы): {not_closed}")