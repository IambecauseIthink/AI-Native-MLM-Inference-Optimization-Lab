"""Six deterministic, CPU-only teaching experiments; never GPU measurements."""
import itertools
import math

SPECS = {
 '01': {'title': '两个服务，谁真的更快？', 'kind': 'synthetic',
        'params': {'batch': ('服务 B 的 batch', [2, 4, 8], 8),
                   'service_ms': ('B 每批服务时间 (ms)', [600, 1000, 1800], 1800),
                   'first_ms': ('B 批内首 token 时间 (ms)', [100, 200, 500], 500)}},
 '02': {'title': 'GPU 带宽已满，还能提速吗？', 'kind': 'analytical-estimate',
        'params': {'batch': ('batch / 行数', [1, 8, 32, 128], 8),
                   'weight_bytes': ('每权重元素 bytes', [1, 2, 4], 2),
                   'bandwidth_gbs': ('HBM 带宽 GB/s', [100, 1000, 2000], 1000),
                   'compute_tflops': ('计算上限 TFLOP/s', [10, 100], 100)}},
 '03': {'title': '权重放得下，为什么还 OOM？', 'kind': 'analytical-estimate',
        'params': {'tokens': ('每请求 cached tokens', [31, 127, 1025, 8193], 1025),
                   'kv_heads': ('KV heads', [1, 8, 32], 8),
                   'kv_bytes': ('KV 元素 bytes', [1, 2], 2),
                   'block_size': ('每 block 的 tokens', [16, 32, 64], 16)}},
 '04': {'title': '一个长请求，为什么拖慢其他人？', 'kind': 'synthetic',
        'params': {'budget': ('每轮 token 预算', [4, 8, 16], 8),
                   'chunked': ('是否切分 prefill', [0, 1], 1),
                   'decode_first': ('是否优先服务活跃 decode', [0, 1], 1)}},
 '05': {'title': '相似提示词，为什么没有缓存收益？', 'kind': 'synthetic',
        'params': {'shared': ('精确共同前缀 tokens', [0, 7, 8, 16, 31], 16),
                   'block_size': ('每 block 的 tokens', [4, 8, 16], 8),
                   'capacity': ('缓存容量 blocks', [0, 2, 8, 32], 8),
                   'repeats': ('目标前缀后续出现次数', [1, 3, 6], 3)}},
 '06': {'title': 'INT4 更小，为什么不一定更快？', 'kind': 'synthetic',
        'params': {'bits': ('有符号量化位宽', [4, 8], 4),
                   'outlier': ('单个 outlier 的值', [2, 20, 100], 20),
                   'group_size': ('每组元素数', [4, 12], 12),
                   'calibration_max': ('校准绝对上界', [2, 20, 100], 20)}}
}


def parameters(lesson_id, overrides=None):
    if lesson_id not in SPECS:
        raise ValueError('lesson id must be 01..06')
    spec = SPECS[lesson_id]['params']
    values = {k: v[2] for k, v in spec.items()}
    for k, v in (overrides or {}).items():
        if k not in spec:
            raise ValueError(f'unknown parameter: {k}')
        if isinstance(v, bool) or v not in spec[k][1]:
            raise ValueError(f'{k} must be one of {spec[k][1]}')
        values[k] = v
    return values


def cases(lesson_id):
    spec = SPECS[lesson_id]['params']
    for vals in itertools.product(*(v[1] for v in spec.values())):
        yield dict(zip(spec, vals))


def quantile(xs, p):
    xs = sorted(xs)
    pos = (len(xs) - 1) * p
    a, b = math.floor(pos), math.ceil(pos)
    return xs[a] + (xs[b] - xs[a]) * (pos - a)


def metric(label, value, unit=''):
    return {'label': label, 'value': value, 'unit': unit}


def lane(label, segments, unit):
    return {'label': label, 'segments': [{'label': n, 'value': v} for n, v in segments], 'unit': unit}


def request_batch(batch, service_ms, first_ms):
    """Same eight simultaneous requests, 3 tokens each; sequential batch service."""
    if first_ms > service_ms:
        raise ValueError('first token must precede completion')
    rows = []
    for i in range(8):
        begin = (i // batch) * service_ms
        end = begin + service_ms
        first = begin + first_ms
        rows.append({'id': str(i), 'kind': 'synthetic', 'status': 'ok',
                     'start_s': 0, 'end_s': end / 1000, 'input_tokens': 32,
                     'output_tokens': 3, 'token_times_s': [first / 1000, (first + end) / 2000, end / 1000]})
    return rows


def lesson01(p):
    configs = [('A', 4, 1000, 200), ('B', p['batch'], p['service_ms'], p['first_ms'])]
    results, lanes, metrics = {}, [], []
    for name, batch, service, first in configs:
        rows = request_batch(batch, service, first)
        window = max(r['end_s'] for r in rows)
        e2e = [r['end_s'] * 1000 for r in rows]
        ttft = [r['token_times_s'][0] * 1000 for r in rows]
        tpot = [(r['token_times_s'][-1] - r['token_times_s'][0]) * 500 for r in rows]
        results[name] = {'requests': rows, 'window_s': window, 'qps': 8 / window,
                         'e2e_p50_ms': quantile(e2e, .5), 'e2e_p99_ms': quantile(e2e, .99),
                         'ttft_p50_ms': quantile(ttft, .5), 'tpot_p50_ms': quantile(tpot, .5)}
        for i in [0, 7]:
            wait = i // batch * service
            lanes.append(lane(f'{name} 请求 {i+1}', [('排队', wait), ('批内首 token', first),
                                                     ('后续生成', service-first)], 'ms'))
        metrics.extend([metric(f'{name} QPS', 8 / window, 'req/s'),
                        metric(f'{name} E2E P50', quantile(e2e, .5), 'ms'),
                        metric(f'{name} E2E P99', quantile(e2e, .99), 'ms'),
                        metric(f'{name} TTFT P50', quantile(ttft, .5), 'ms'),
                        metric(f'{name} TPOT P50', quantile(tpot, .5), 'ms')])
    return results, lanes, metrics, '同 8 请求在 t=0 到达；每请求生成 3 token；批处理示例，不是 vLLM 模拟器。QPS 用各自完整排空窗口。'


def lesson02(p):
    b, k, n = p['batch'], 4096, 4096
    flops = 2 * b * k * n
    traffic = k * n * p['weight_bytes'] + 2 * b * (k + n)
    compute_s = flops / (p['compute_tflops'] * 1e12)
    memory_s = traffic / (p['bandwidth_gbs'] * 1e9)
    floor_s = max(compute_s, memory_s)
    r = {'flops': flops, 'traffic_bytes': traffic, 'intensity_flop_per_byte': flops / traffic,
         'compute_lower_ms': compute_s*1000, 'memory_lower_ms': memory_s*1000,
         'step_lower_ms': floor_s*1000, 'row_rate_upper': b/floor_s,
         'bottleneck_bound': 'compute' if compute_s >= memory_s else 'HBM',
         'weight_bytes_per_row': k*n*p['weight_bytes']/b}
    return r, [lane('计算时间下界', [('计算', r['compute_lower_ms'])], 'ms'),
               lane('搬运时间下界', [('HBM', r['memory_lower_ms'])], 'ms')], [
        metric('算术强度', r['intensity_flop_per_byte'], 'FLOP/B'),
        metric('单步时间下界', r['step_lower_ms'], 'ms'),
        metric('行吞吐上界', r['row_rate_upper'], 'row/s')], '单层 X[B,4096]×W[4096,4096]；每步权重读一次，输入输出各一次且为 2 bytes；忽略 KV、scale、反量化、launch、排队。带宽 GB/s 为十进制；不预测模型 TPS。'


def lesson03(p):
    layers, dim, batch = 32, 128, 4
    unit = 2 * layers * p['kv_heads'] * dim * p['kv_bytes']
    padded = math.ceil(p['tokens']/p['block_size'])*p['block_size']
    raw = unit*p['tokens']*batch
    allocated = unit*padded*batch
    weights, other, budget = 54, 6, 64
    total = weights+other+allocated/2**30
    r = {'raw_bytes': raw, 'allocated_bytes': allocated, 'waste_bytes': allocated-raw,
         'blocks': padded//p['block_size']*batch, 'total_gib': total, 'budget_gib': budget,
         'fits_assumed_budget': total <= budget, 'fixed_weights_gib': weights, 'other_gib': other}
    return r, [lane('raw KV', [('有效 KV', raw/2**20)], 'MiB'),
               lane('分页 KV', [('有效 KV', raw/2**20), ('尾块空槽', (allocated-raw)/2**20)], 'MiB')], [
        metric('全体 KV 分配', allocated/2**30, 'GiB'), metric('假定总占用', total, 'GiB'),
        metric('假定容量', budget, 'GiB')], '32 层 full attention，head_dim=128，4 请求；假定权重 54 GiB、其他 6 GiB、容量 64 GiB。无 prefix 共享、TP 复制和 allocator 元数据；混合 Qwen 必须另算 state。'


def schedule(budget, chunked, decode_first):
    """Token work ticks, not wall time: one long prefill + 2 active decodes."""
    requests = [{'id':'long', 'prefill':12, 'decode':3},
                {'id':'short-1', 'prefill':0, 'decode':4},
                {'id':'short-2', 'prefill':0, 'decode':4}]
    trace, finish, now = [], {}, 0
    for step in range(100):
        alive = [r for r in requests if r['prefill'] or r['decode']]
        if not alive:
            return {'status':'completed', 'trace':trace, 'finish_work_ticks':finish, 'total_work_ticks':now}
        ordered = sorted(alive, key=lambda r: bool(r['prefill'])) if decode_first else alive
        left, used, events = budget, 0, []
        for r in ordered:
            if r['prefill']:
                take = min(r['prefill'], left) if chunked else (r['prefill'] if r['prefill'] <= left else 0)
                phase = 'prefill'
            else:
                take = min(1, left)
                phase = 'decode'
            if not take:
                continue
            r[phase] -= take
            left -= take
            used += take
            events.append({'id':r['id'], 'phase':phase, 'tokens':take})
        if not used:
            return {'status':'blocked-budget', 'trace':trace, 'finish_work_ticks':finish,
                    'total_work_ticks':now, 'reason':'Unchunked prefill cannot fit this toy budget; not a vLLM failure prediction.'}
        now += used  # Explicit simplified equal cost for every prefill/decode token.
        for r in requests:
            if not r['prefill'] and not r['decode'] and r['id'] not in finish:
                finish[r['id']] = now
        trace.append({'step':step, 'used_tokens':used, 'end_work_tick':now, 'events':events})
    raise AssertionError('scheduler did not terminate')


def lesson04(p):
    r = schedule(p['budget'], p['chunked'], p['decode_first'])
    lanes = [lane(name, [('完成所需工作刻度', end)], 'work ticks') for name,end in r['finish_work_ticks'].items()]
    return r, lanes, [metric('调度轮数', len(r['trace']), 'steps'),
                      metric('完成请求', len(r['finish_work_ticks']), '/3')], '每 token 假设花费 1 work tick；prefill/decode 等成本仅为教学。请求在每轮结束完成；活跃短请求的 prefill 已在窗口前完成。不能据此预测 TTFT 或证明实际调度收益；不模拟真实抢占。'


def cache_sim(shared, block_size, capacity, repeats):
    from collections import OrderedDict
    cache = OrderedDict()
    original = list(range(32))
    target = original[:shared] + list(range(1000+shared, 1032))
    requests = [original] + [target for _ in range(repeats)]
    records = []
    for i, tokens in enumerate(requests):
        keys = [tuple(tokens[:end]) for end in range(block_size, len(tokens)+1, block_size)]
        hit = 0
        for key in keys:
            # v0.19.0 generation needs a final token recomputation for logits.
            if len(key) > len(tokens)-1:
                break
            if key not in cache:
                break
            hit += block_size
            cache.move_to_end(key)
        # Cache population happens after the request; full-prefix keys model ancestry.
        for key in keys:
            cache[key] = True
            cache.move_to_end(key)
            while len(cache) > capacity:
                cache.popitem(last=False)
        records.append({'request':i+1, 'hit_tokens':hit, 'recompute_tokens':32-hit})
    return {'requests':records, 'hit_tokens':sum(x['hit_tokens'] for x in records),
            'total_tokens':32*len(records), 'retained_blocks':len(cache)}


def lesson05(p):
    r = cache_sim(p['shared'],p['block_size'],p['capacity'],p['repeats'])
    lanes = [lane(f"请求 {x['request']}", [('命中',x['hit_tokens']),('需计算',x['recompute_tokens'])], 'tokens') for x in r['requests']]
    return r, lanes, [metric('累计命中',r['hit_tokens'],'tokens'),
                     metric('累计输入',r['total_tokens'],'tokens'),
                     metric('保留块',r['retained_blocks'],'blocks')], '32 个合成 token；请求 1 冷缓存，之后请求共享所选前缀且彼此完全相同；完整块+带祖先前缀的 key，LRU 教学策略；最后 token 为 logits 重算，命中长度向下对齐 block。只估算可复用 prefill tokens，不换算速度、不模拟 decode、隔离盐和多模态缓存。'


def quantize(values, bits, group_size, calibration_max):
    """Symmetric signed integers, ties-to-even; per-group observed max capped by calibration."""
    qmax = 2**(bits-1)-1
    output, codes, scales, clipped = [], [], [], 0
    for i in range(0,len(values),group_size):
        group = values[i:i+group_size]
        bound = min(max(abs(x) for x in group), calibration_max)
        scale = bound/qmax if bound else 1.0
        scales.append(scale)
        for x in group:
            clipped += int(abs(x)>bound)
            q = max(-qmax,min(qmax,round(x/scale)))
            codes.append(q)
            output.append(q*scale)
    mse = sum((x-y)**2 for x,y in zip(values,output))/len(values)
    return {'original':values, 'dequantized':output, 'codes':codes, 'scales':scales,
            'mse':mse, 'clipped':clipped, 'max_abs_error':max(abs(x-y) for x,y in zip(values,output))}


def lesson06(p):
    values = [-1.2,-.7,-.2,.1,.3,.8,1.1,1.7,-.4,.5,1.3,p['outlier']]
    r = quantize(values,p['bits'],p['group_size'],p['calibration_max'])
    r['weight_payload_vs_bf16'] = p['bits']/16
    r['small_values_mse'] = sum((x-y)**2 for x,y in zip(values[:-1],r['dequantized'][:-1]))/11
    r['toy_storage_bytes'] = math.ceil(len(values)*p['bits']/8)+len(r['scales'])*4
    return r, [lane('普通值 MSE', [('误差',r['small_values_mse'])], 'value²'),
               lane('全部值 MSE', [('误差',r['mse'])], 'value²')], [metric('普通值 MSE',r['small_values_mse']),
             metric('截断元素',r['clipped']), metric('含 FP32 scale 的存储',r['toy_storage_bytes'],'bytes')], '12 个合成值；对称整数范围 ±(2^(bits−1)−1)，ties-to-even；每组观测上界受校准上界限制。BF16 权重 payload 比例仅是搬运理想比例，不含真实 packing/反量化开销；MSE 不是业务质量，也不实现 AWQ/GPTQ。'


RUNNERS = {'01':lesson01,'02':lesson02,'03':lesson03,'04':lesson04,'05':lesson05,'06':lesson06}


def run(lesson_id, overrides=None):
    p = parameters(lesson_id, overrides)
    data, lanes, metrics, assumption = RUNNERS[lesson_id](p)
    return {'lesson_id':lesson_id, 'title':SPECS[lesson_id]['title'], 'kind':SPECS[lesson_id]['kind'],
            'parameters':p, 'assumptions':assumption, 'data':data, 'view':{'lanes':lanes,'metrics':metrics},
            'quality_verified':False, 'production_recommendation':None}
