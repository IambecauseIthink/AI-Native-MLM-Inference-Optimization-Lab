"""Harmless CPU subprocess tests, never a model/profiler/benchmark run."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('capture', ROOT / 'benchmarks/scripts/capture_command.py')
capture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(capture)


class CaptureTests(unittest.TestCase):
    def run_fixture(self, code):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'run'
            argv = ['capture', '--out', str(out), '--timeout', '1', '--', sys.executable, '-c', code]
            with patch.object(sys, 'argv', argv), patch.object(capture.platform, 'system', return_value='Linux'):
                with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(SystemExit) as result:
                    capture.main()
            return result.exception.code, json.loads((out / 'receipt.json').read_text())

    def test_completed_receipt_has_hash_and_no_quality_claim(self):
        code, receipt = self.run_fixture('print("fixture")')
        self.assertEqual(code, 0)
        self.assertEqual(receipt['status'], 'command-completed')
        self.assertEqual(len(receipt['sha256']['stdout.log']), 64)
        self.assertFalse(receipt['quality_verified'])

    def test_failure_receipt_preserves_exit_code(self):
        code, receipt = self.run_fixture('raise SystemExit(7)')
        self.assertEqual(code, 1)
        self.assertEqual(receipt['exit_code'], 7)
        self.assertEqual(receipt['status'], 'command-failed')

    def test_timeout_stops_cpu_fixture(self):
        code, receipt = self.run_fixture('import time; time.sleep(5)')
        self.assertEqual(code, 1)
        self.assertEqual(receipt['status'], 'timed-out')
        self.assertLess(receipt['elapsed_s'], 4)

    def test_mac_execution_rejected_before_launch(self):
        argv = ['capture', '--out', '/unused', '--timeout', '1', '--', 'unused']
        with patch.object(sys, 'argv', argv), patch.object(capture.platform, 'system', return_value='Darwin'):
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as result:
                capture.main()
        self.assertEqual(result.exception.code, 2)
