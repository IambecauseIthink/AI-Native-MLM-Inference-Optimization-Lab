#!/usr/bin/env python3
"""CPU-only estimates and evidence-bounded benchmark analysis (stdlib)."""
import argparse
import json
import math
from pathlib import Path


def number(value, name, positive=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f'{name} must be finite numeric')
    if value < 0 or (positive and value == 0):
        raise ValueError(f'{name} out of range')
    return value


def integer(value, name, positive=False):
    number(value, name, positive)
    if int(value) != value:
        raise ValueError(f'{name} must be integral')
    return int(value)


def kv_bytes(layers, kv_heads, head_dim, tokens, batch, element_bytes):
    for name, value in [('layers', layers), ('kv_heads', kv_heads), ('head_dim', head_dim),
                        ('tokens', tokens), ('batch', batch)]:
        integer(value, name, True)
    number(element_bytes, 'element_bytes', True)
    return 2 * layers * kv_heads * head_dim * tokens * batch * element_bytes


def percentile(values, p):
    """Linear interpolation, equivalent to inclusive (n-1)*p quantile."""
    if not values:
        return None
    v = sorted(values)
    pos = (len(v) - 1) * p
    lo, hi = math.floor(pos), math.ceil(pos)
    return v[lo] + (v[hi] - v[lo]) * (pos - lo)


def distribution(values):
    return {'n': len(values), **{f'p{p}': percentile(values, p / 100) for p in [50, 95, 99]}}


def summarize(rows, duration):
    number(duration, 'duration', True)
    if not rows:
        raise ValueError('empty request set')
    ids, kinds = set(), set()
    e2e, ttft, tpot = [], [], []
    inputs = outputs = failed = 0
    for r in rows:
        rid = r['id']
        if not isinstance(rid, str) or not rid or rid in ids:
            raise ValueError('missing/duplicate request id')
        ids.add(rid)
        if r['kind'] not in ('synthetic', 'measured'):
            raise ValueError('unknown evidence kind')
        kinds.add(r['kind'])
        start = number(r['start_s'], 'start_s')
        end = number(r['end_s'], 'end_s')
        if not start <= end <= duration:
            raise ValueError('timestamps outside measurement window')
        if r['status'] not in ('ok', 'error'):
            raise ValueError('unknown request status')
        if r['status'] == 'error':
            failed += 1
            continue
        inp = integer(r['input_tokens'], 'input_tokens')
        out = integer(r['output_tokens'], 'output_tokens')
        times = r.get('token_times_s')
        if times is not None:
            if len(times) != out:
                raise ValueError('need one timestamp per token; chunk times are not token times')
            for t in times:
                number(t, 'token timestamp')
            if times != sorted(times) or any(t < start or t > end for t in times):
                raise ValueError('invalid token timeline')
            if times:
                ttft.append((times[0] - start) * 1000)
            if len(times) > 1:
                tpot.append((times[-1] - times[0]) / (len(times) - 1) * 1000)
        e2e.append((end - start) * 1000)
        inputs += inp
        outputs += out
    if len(kinds) != 1:
        raise ValueError('cannot mix synthetic and measured evidence')
    succeeded = len(e2e)
    return {'kind': next(iter(kinds)), 'requests': len(rows), 'succeeded': succeeded,
            'failed': failed, 'error_rate': failed / len(rows), 'duration_s': duration,
            'qps': succeeded / duration, 'input_tps': inputs / duration,
            'output_tps': outputs / duration, 'total_tps': (inputs + outputs) / duration,
            'ttft_ms': distribution(ttft), 'tpot_ms': distribution(tpot),
            'e2e_ms': distribution(e2e), 'quality': None,
            'note': 'Successful-request token rates over wall time; not isolated stage TPS. No quality or SLO recommendation.'}


CONTRACT_FIELDS = {'model_lineage', 'dataset_sha256', 'evaluator_sha256', 'runtime_commit',
                   'hardware', 'gpu_count', 'workload', 'sampling', 'measurement', 'quality_gate'}


def compare(records):
    """Fail closed: comparable, completed, measured, quality-gated Pareto set."""
    if not records:
        raise ValueError('empty run set')
    bases = [r for r in records if r.get('role') == 'baseline']
    if len(bases) != 1:
        raise ValueError('exactly one baseline required')
    base = bases[0]
    contract = base['contract']
    if set(contract) != CONTRACT_FIELDS:
        raise ValueError('contract fields missing or unexpected')
    integer(contract['gpu_count'], 'gpu_count', True)
    gate = contract['quality_gate']
    if gate['direction'] not in ('higher', 'lower') or gate['loss_mode'] not in ('absolute', 'relative'):
        raise ValueError('unsupported quality gate')
    number(gate['max_loss'], 'max_loss')
    rejected, eligible, seen = [], [], set()
    for r in records:
        if r['id'] in seen:
            raise ValueError('duplicate run id')
        seen.add(r['id'])
        reason = None
        if r.get('kind') != 'measured':
            reason = 'not-measured (synthetic/design cannot enter measured frontier)'
        elif r.get('contract') != contract:
            reason = 'not-comparable: contract mismatch'
        else:
            try:
                expected = integer(r['expected'], 'expected', True)
                succeeded = integer(r['succeeded'], 'succeeded')
                failed = integer(r['failed'], 'failed')
                rounds = integer(r['rounds'], 'rounds', True)
                if succeeded != expected or failed or r['exit_code'] != 0 or rounds < 3:
                    reason = 'incomplete or failed run'
                elif not r.get('evidence') or not r.get('quality_evidence') or r.get('fallback') is not False:
                    reason = 'missing evidence or unverified fallback'
                elif r.get('quality_slices_passed') is not True or r.get('slo_passed') is not True:
                    reason = 'quality slices or SLO gate not passed'
                else:
                    for field in ['quality', 'qps', 'e2e_p99_ms', 'peak_gpu_gib']:
                        number(r[field], field, positive=field != 'quality')
            except (KeyError, TypeError, ValueError) as exc:
                reason = f'invalid metrics: {exc}'
        if reason:
            rejected.append({'id': r['id'], 'reason': reason})
        else:
            eligible.append(r)
    if base not in eligible:
        return {'frontier': [], 'rejected': rejected, 'decision': 'baseline-invalid; no comparison'}
    accepted = []
    for r in eligible:
        loss = (base['quality'] - r['quality']) if gate['direction'] == 'higher' else (r['quality'] - base['quality'])
        if gate['loss_mode'] == 'relative':
            if base['quality'] == 0:
                raise ValueError('relative quality loss undefined for zero baseline; use absolute')
            loss /= abs(base['quality'])
        if loss > gate['max_loss'] + 1e-12:
            rejected.append({'id': r['id'], 'reason': 'quality loss exceeded'})
        else:
            accepted.append(r)
    def vector(r):
        quality = r['quality'] if gate['direction'] == 'higher' else -r['quality']
        return (quality, r['qps'] / contract['gpu_count'], -r['e2e_p99_ms'], -r['peak_gpu_gib'])
    def dominates(a, b):
        av, bv = vector(a), vector(b)
        return all(x >= y for x, y in zip(av, bv)) and any(x > y for x, y in zip(av, bv))
    frontier = [r['id'] for r in accepted if not any(dominates(o, r) for o in accepted)]
    return {'frontier': frontier, 'rejected': rejected,
            'dominated': [r['id'] for r in accepted if r['id'] not in frontier],
            'decision': 'descriptive Pareto only; uncertainty and production review still required'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    kv = sub.add_parser('kv')
    for flag in ['layers', 'kv-heads', 'head-dim', 'tokens', 'batch']:
        kv.add_argument('--' + flag, type=int, required=True)
    kv.add_argument('--bytes', type=float, required=True)
    w = sub.add_parser('workload')
    w.add_argument('--count', type=int, default=20)
    w.add_argument('--output', type=Path, required=True)
    s = sub.add_parser('summarize')
    s.add_argument('events', type=Path)
    s.add_argument('--duration', type=float, required=True)
    c = sub.add_parser('compare')
    c.add_argument('records', type=Path)
    a = parser.parse_args()
    try:
        if a.command == 'kv':
            n = kv_bytes(a.layers, a.kv_heads, a.head_dim, a.tokens, a.batch, a.bytes)
            result = {'kind': 'analytical-estimate', 'raw_kv_bytes': n, 'raw_kv_gib': n / 2**30,
                      'scope': 'Uniform full-attention logical KV only; excludes weights, state, scales, padding, workspace and TP replication.'}
        elif a.command == 'workload':
            integer(a.count, 'count', True)
            with a.output.open('x') as f:
                for i in range(a.count):
                    f.write(json.dumps({'id': f'synthetic-{i:05}', 'kind': 'synthetic',
                                        'prompt': 'Explain inference. ' * [8, 32, 128][i % 3],
                                        'max_tokens': [32, 128][i % 2]}, ensure_ascii=False) + '\n')
            result = {'output': str(a.output), 'count': a.count,
                      'note': 'Synthetic text lengths are not tokenizer token counts; tokenize with pinned model before benchmarking.'}
        elif a.command == 'summarize':
            rows = [json.loads(s) for s in a.events.read_text().splitlines() if s.strip()]
            result = summarize(rows, a.duration)
        else:
            result = compare(json.loads(a.records.read_text()))
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    main()
