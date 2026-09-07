# Debugging decision tree

1. 请求未完成：先区分客户端传输、HTTP/gRPC、队列、进程与 CUDA 错误。
2. OOM：区分权重加载、KV 预分配、峰值激活、graph/workspace；读取日志而非猜测。
3. QPS 不升：先检查样本长度、并发、缓存和实际 backend，再看 profile。
4. 尾延迟恶化：检查到达率、队列、长输入干扰与错误重试。
5. 质量下降：复核模板/processor/解码参数，再查 calibration、scale 和敏感切片。

保留失败 run；修复后重跑同协议完整样本，不用补一条请求拼成完整结果。
