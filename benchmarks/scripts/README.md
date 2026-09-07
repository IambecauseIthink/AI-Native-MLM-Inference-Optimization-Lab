# Runtime adapters

当前执行入口为 [capture_command.py](capture_command.py)，在选定远程 Linux 环境捕获用户提供的固定版本 benchmark 命令、stdout/stderr、超时、退出码和 hash。它不是负载驱动，不自动启动服务，不适配未知版本参数。

```bash
# 仅在已选定的远程 Linux GPU 环境执行；ARGS 来自冻结协议和该版本 --help
python3 benchmarks/scripts/capture_command.py --out artifacts/run-001 --timeout 1800 -- YOUR_PINNED_BENCHMARK ARGS
```

vLLM adapter：保存实际 benchmark CLI 版本/help/命令，规范化请求级事件；Triton adapter：使用现有业务 gRPC/stream 客户端，固定长连接策略、服务发现和重试，保存 raw response 与状态。两种协议不可直接混成一个 baseline/candidate 比较。

接入顺序：固定版本→短样本正确性→完整 warmup/3 轮→转换 events→独立质量 evaluator→回执校验。缺少逐 token 时间时填 null。业务 HTTP/gRPC adapter 与 quality evaluator 是后续工作，未假称已实现。
