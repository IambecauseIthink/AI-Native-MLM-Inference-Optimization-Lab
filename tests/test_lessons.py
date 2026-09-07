"""Hand-calculated teaching oracles; all inputs and results are synthetic/analytical."""
import itertools
import json
import math
from pathlib import Path
import re
import subprocess
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import lessons
import lab
import build_lesson_visuals


class LessonTests(unittest.TestCase):
    def test_01_same_requests_tradeoff(self):
        r=lessons.run('01')['data']
        self.assertEqual(r['A']['qps'],4)
        self.assertAlmostEqual(r['B']['qps'],8/1.8)
        self.assertEqual(r['A']['e2e_p50_ms'],1500)
        self.assertEqual(r['B']['e2e_p50_ms'],1800)
        self.assertEqual(r['A']['e2e_p99_ms'],2000)
        self.assertEqual(r['B']['e2e_p99_ms'],1800)

    def test_01_matches_existing_event_analyzer(self):
        for p in lessons.cases('01'):
            for r in lessons.run('01',p)['data'].values():
                measured=lab.summarize(r['requests'],r['window_s'])
                self.assertAlmostEqual(measured['qps'],r['qps'])
                for m in ['e2e','ttft','tpot']:
                    self.assertAlmostEqual(measured[m+'_ms']['p50'],r[m+'_p50_ms'])

    def test_02_hand_calculated_units(self):
        r=lessons.run('02',{'batch':1})['data']
        self.assertEqual(r['flops'],33554432)
        self.assertEqual(r['traffic_bytes'],33570816)
        self.assertAlmostEqual(r['memory_lower_ms'],.033570816)
        self.assertEqual(r['bottleneck_bound'],'HBM')

    def test_02_bottleneck_changes_and_reuse(self):
        a=lessons.run('02',{'batch':1})['data']
        b=lessons.run('02',{'batch':128,'compute_tflops':10})['data']
        self.assertEqual(b['bottleneck_bound'],'compute')
        self.assertLess(b['weight_bytes_per_row'],a['weight_bytes_per_row'])
        self.assertGreater(b['row_rate_upper'],a['row_rate_upper'])
        self.assertGreaterEqual(b['step_lower_ms'],b['compute_lower_ms'])
        self.assertGreaterEqual(b['step_lower_ms'],b['memory_lower_ms'])

    def test_03_rounding_boundary(self):
        p={'tokens':31,'block_size':16}
        r=lessons.run('03',p)['data']
        unit=2*32*8*128*2
        self.assertEqual(r['raw_bytes'],unit*31*4)
        self.assertEqual(r['allocated_bytes'],unit*32*4)
        self.assertEqual(r['waste_bytes'],unit*4)

    def test_03_gqa_and_dtype(self):
        a=lessons.run('03',{'kv_heads':8})['data']
        b=lessons.run('03',{'kv_heads':1})['data']
        c=lessons.run('03',{'kv_heads':8,'kv_bytes':1})['data']
        self.assertEqual(a['raw_bytes'],8*b['raw_bytes'])
        self.assertEqual(a['raw_bytes'],2*c['raw_bytes'])
        self.assertFalse(lessons.run('03',{'tokens':8193})['data']['fits_assumed_budget'])

    def test_04_budget_and_conservation_all_cases(self):
        for p in lessons.cases('04'):
            r=lessons.run('04',p)['data']
            self.assertTrue(all(0<t['used_tokens']<=p['budget'] for t in r['trace']))
            events=[e for t in r['trace'] for e in t['events']]
            self.assertEqual(sum(e['tokens'] for e in events),r['total_work_ticks'])
            if p['chunked'] or p['budget']>=12:
                self.assertEqual(r['status'],'completed')
                self.assertEqual(r['total_work_ticks'],23)
                self.assertEqual(len(r['finish_work_ticks']),3)
                self.assertEqual(sum(e['tokens'] for e in events if e['phase']=='prefill'),12)
            else:
                self.assertEqual(r['status'],'blocked-budget')
                self.assertNotIn('long',r['finish_work_ticks'])

    def test_04_priority_changes_short_finish(self):
        a=lessons.run('04',{'decode_first':1})['data']['finish_work_ticks']
        b=lessons.run('04',{'decode_first':0})['data']['finish_work_ticks']
        self.assertLess(a['short-1'],b['short-1'])

    def test_05_cold_warm_and_logits_recompute(self):
        hits=[r['hit_tokens'] for r in lessons.run('05')['data']['requests']]
        self.assertEqual(hits,[0,16,24,24])
        self.assertEqual(lessons.run('05',{'shared':7})['data']['requests'][1]['hit_tokens'],0)
        self.assertEqual(lessons.run('05',{'shared':8})['data']['requests'][1]['hit_tokens'],8)

    def test_05_eviction_and_zero_capacity(self):
        for capacity in [0,2]:
            r=lessons.run('05',{'capacity':capacity})['data']
            self.assertEqual(r['hit_tokens'],0)
            self.assertLessEqual(r['retained_blocks'],capacity)

    def test_05_token_conservation_all_presets(self):
        for p in lessons.cases('05'):
            r=lessons.run('05',p)['data']
            for req in r['requests']:
                self.assertEqual(req['hit_tokens']+req['recompute_tokens'],32)
                self.assertEqual(req['hit_tokens']%p['block_size'],0)
                self.assertLess(req['hit_tokens'],32)

    def test_06_hand_calculated_rounding(self):
        r=lessons.quantize([-.5,.5,1.5,7.0],4,4,7)
        self.assertEqual(r['scales'],[1])
        self.assertEqual(r['codes'],[0,0,2,7])
        self.assertEqual(r['mse'],.1875)

    def test_06_clipping(self):
        r=lessons.quantize([-10,10],4,2,7)
        self.assertEqual(r['codes'],[-7,7])
        self.assertEqual(r['clipped'],2)
        self.assertEqual(r['mse'],9)

    def test_06_zero_and_partial_group(self):
        r=lessons.quantize([0,0,0],4,2,7)
        self.assertEqual(r['dequantized'],[0,0,0])
        self.assertEqual(r['scales'],[1,1])

    def test_06_grouping_outlier_and_storage(self):
        a=lessons.run('06')['data'];b=lessons.run('06',{'group_size':4})['data']
        self.assertLess(b['small_values_mse'],a['small_values_mse'])
        self.assertGreater(b['toy_storage_bytes'],a['toy_storage_bytes'])
        self.assertEqual(a['weight_payload_vs_bf16'],.25)

    def test_all_presets_are_finite_and_not_measured(self):
        for id in lessons.SPECS:
            for p in lessons.cases(id):
                result=lessons.run(id,p)
                self.assertIn(result['kind'],['synthetic','analytical-estimate'])
                self.assertFalse(result['quality_verified'])
                self.assertIsNone(result['production_recommendation'])
                json.dumps(result,allow_nan=False)

    def test_visual_presets_exactly_match_python(self):
        for id in lessons.SPECS:
            fragment=(ROOT/f'courses/visuals/lesson-{id}.html').read_text()
            self.assertEqual(fragment,build_lesson_visuals.render(id))
            bundle=json.loads(re.search(r'<script type="application/json" data-presets>(.*?)</script>',fragment,re.S).group(1))
            self.assertEqual(len(bundle['records']),len(list(lessons.cases(id))))
            for r in bundle['records']:
                self.assertEqual(r,lessons.run(id,r['parameters']))
            self.assertLess(len(fragment.encode()),1_000_000)
            self.assertNotIn('fetch(',fragment)

    def test_invalid_parameters(self):
        for id,p in [('00',{}),('01',{'unknown':1}),('01',{'batch':True}),('02',{'batch':-1})]:
            with self.assertRaises(ValueError):lessons.run(id,p)

    def test_cli_all_lessons(self):
        for id in lessons.SPECS:
            process=subprocess.run([sys.executable,str(ROOT/'scripts/lab.py'),'lesson','--id',id],capture_output=True,text=True)
            self.assertEqual(process.returncode,0,process.stderr)
            self.assertEqual(json.loads(process.stdout),lessons.run(id))

    def test_cli_invalid_and_duplicate(self):
        for args in [['--set','batch=99'],['--set','batch=4','--set','batch=8'],['--set','bad']]:
            p=subprocess.run([sys.executable,str(ROOT/'scripts/lab.py'),'lesson','--id','01',*args],capture_output=True,text=True)
            self.assertEqual(p.returncode,2)

    def test_sources_pinned_and_all_lessons_present(self):
        lock=json.loads((ROOT/'courses/source-lock.json').read_text())
        self.assertRegex(lock['commit'],r'^[a-f0-9]{40}$')
        for id in lessons.SPECS:
            self.assertTrue(lock['lessons'][id])
            for source in lock['lessons'][id]:
                self.assertIn(lock['commit'],source['url'])
                self.assertGreater(source['line'],0)
                self.assertRegex(source['sha256'],r'^[a-f0-9]{64}$')
            for name in ['README.md','teacher.md','remote.md']:
                self.assertTrue((ROOT/f'courses/{id}/{name}').exists())

if __name__=='__main__':unittest.main()
