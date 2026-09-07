"""Synthetic unit fixtures only; no actual model or GPU results."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('lab', ROOT / 'scripts/lab.py')
lab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lab)


class AnalysisTests(unittest.TestCase):
    def setUp(self):
        self.rows = [json.loads(s) for s in (ROOT / 'benchmarks/workloads/synthetic-events.jsonl').read_text().splitlines()]
        self.runs = json.loads((ROOT / 'benchmarks/workloads/synthetic-runs.json').read_text())

    def eligible_fixture(self):
        # Simulates measured metadata to test gates; never a measured repository result.
        for r in self.runs:
            r['kind'] = 'measured'
        return self.runs

    def test_hand_calculated_kv(self):
        self.assertEqual(lab.kv_bytes(32, 8, 128, 8192, 4, 2), 4 * 2**30)
        self.assertEqual(lab.kv_bytes(32, 8, 128, 8192, 4, 1), 2 * 2**30)

    def test_invalid_formula_input(self):
        for x in [0, -1, True, float('nan'), 1.5]:
            with self.subTest(x=x), self.assertRaises(ValueError):
                lab.kv_bytes(x, 8, 128, 8192, 4, 2)

    def test_hand_calculated_metrics(self):
        out = lab.summarize(self.rows, 4)
        self.assertEqual((out['qps'], out['input_tps'], out['output_tps'], out['total_tps']), (.5, 5, 1, 6))
        self.assertAlmostEqual(out['error_rate'], 1/3)
        self.assertEqual(out['ttft_ms']['p50'], 750)
        self.assertEqual(out['tpot_ms']['n'], 1)
        self.assertEqual(out['tpot_ms']['p50'], 500)
        self.assertEqual(out['e2e_ms']['p99'], 2000)
        self.assertEqual(out['kind'], 'synthetic')

    def test_missing_stream_metrics_not_invented(self):
        for r in self.rows:
            r['token_times_s'] = None
        self.assertIsNone(lab.summarize(self.rows, 4)['ttft_ms']['p50'])

    def test_duplicate_request_rejected(self):
        with self.assertRaises(ValueError):
            lab.summarize(self.rows + [self.rows[0]], 4)

    def test_chunk_count_rejected(self):
        self.rows[0]['token_times_s'] = [.5]
        with self.assertRaises(ValueError):
            lab.summarize(self.rows, 4)

    def test_invalid_timeline(self):
        for times in [[1, .5, 1.5], [.5, 1, 5], [.5, 1, float('nan')]]:
            self.rows[0]['token_times_s'] = times
            with self.assertRaises(ValueError):
                lab.summarize(self.rows, 4)

    def test_window_must_cover_requests(self):
        with self.assertRaises(ValueError):
            lab.summarize(self.rows, 3)

    def test_mixed_evidence_rejected(self):
        self.rows[0]['kind'] = 'measured'
        with self.assertRaises(ValueError):
            lab.summarize(self.rows, 4)

    def test_synthetic_frontier_empty(self):
        self.assertEqual(lab.compare(self.runs)['frontier'], [])

    def test_dominance_and_equal_ties(self):
        runs = self.eligible_fixture()
        self.assertEqual(lab.compare(runs)['frontier'], ['candidate'])
        runs[1]['qps'] = runs[0]['qps']
        self.assertEqual(lab.compare(runs)['frontier'], ['baseline', 'candidate'])

    def test_quality_loss_excluded(self):
        runs = self.eligible_fixture()
        runs[1]['quality'] = .8
        self.assertEqual(lab.compare(runs)['frontier'], ['baseline'])

    def test_quality_latency_tradeoff_preserved(self):
        runs = self.eligible_fixture()
        runs[1]['e2e_p99_ms'] = 120
        self.assertEqual(lab.compare(runs)['frontier'], ['baseline', 'candidate'])

    def test_lower_is_better(self):
        runs = self.eligible_fixture()
        for r in runs:
            r['contract']['quality_gate'].update(direction='lower', loss_mode='absolute', max_loss=.01)
        runs[1]['quality'] = .8
        self.assertEqual(lab.compare(runs)['frontier'], ['candidate'])

    def test_mismatched_contract_rejected(self):
        runs = self.eligible_fixture()
        runs[1]['contract']['workload']['max_tokens'] = 32
        self.assertEqual(lab.compare(runs)['frontier'], ['baseline'])

    def test_failure_gates(self):
        for field, value in [('succeeded', 29), ('failed', 1), ('rounds', 2), ('exit_code', 1),
                             ('fallback', True), ('quality_slices_passed', False),
                             ('slo_passed', False), ('evidence', ''), ('quality_evidence', ''),
                             ('qps', float('nan'))]:
            runs = copy.deepcopy(self.eligible_fixture())
            runs[1][field] = value
            with self.subTest(field=field):
                self.assertEqual(lab.compare(runs)['frontier'], ['baseline'])

    def test_invalid_baseline_blocks_all(self):
        runs = self.eligible_fixture()
        runs[0]['exit_code'] = 1
        self.assertEqual(lab.compare(runs)['frontier'], [])

    def test_zero_baseline_relative_undefined(self):
        runs = self.eligible_fixture()
        runs[0]['quality'] = 0
        with self.assertRaises(ValueError):
            lab.compare(runs)

    def test_missing_contract_field(self):
        del self.runs[0]['contract']['sampling']
        with self.assertRaises(ValueError):
            lab.compare(self.runs)


if __name__ == '__main__':
    unittest.main()
