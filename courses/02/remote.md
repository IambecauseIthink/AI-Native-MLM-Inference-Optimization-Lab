# 02 远程验证 · GPU 带宽已满，还能提速吗？

状态：**designed / not-run**。本课 CPU 实验不依赖此步骤。此文件是待具体化的课程验证协议，不是已冻结的业务 RunRecord。

## 问题与单变量

你最初判断“并发 1 已经拉满，增加并发可能无收益”。现在只讨论权重读取带宽：它满了还可能有收益吗？

自变量：并发或输入长度，二者分开扫描。预先写出方向预测与竞争解释，禁止用量化/数据/并发多个变化共同解释单一原因。

## 执行前门槛

未来实际执行前读取两份本机 GPU inventory，过期一小时或长任务前按用户规定顺序刷新；本次不 SSH、不启动 GPU。选定 exact checkpoint/processor/template hash、镜像、vLLM commit、硬件/GPU数及数据与 evaluator 后，复制 [实验模板](../../templates/experiment.md) 为独立协议，锁定参数、质量阈值和资源期限。

## 最小设计

对同一 checkpoint 冻结输入输出后分组扫描并发；先采非 profiler 性能，再单独采目标 GEMM/attention 时间线。核对有效 batch、实际 dtype 和 kernel，计算每层字节与算力上界。

baseline/candidate 同数据、采样、输出 cap、EOS、缓存定义和计时边界；10 个固定 warmup 不计入统计，3 轮完整样本。交错运行，profiler 单独采集；客户端和采样实现也记录版本。

## 应收证据

实际 batch、TTFT/TPOT、QPS、kernel shape/dtype、可取得的 HBM/计算计数器；权限不足明确缺测。保存命令、PID/PGID、退出码、样本 expected/success/failure、原始 evidence hash 和清理回执。输入 TPS、输出 TPS、总 TPS 分列。

## 停止与解释

OOM、缺样本、质量失败、意外 fallback、未授权资源或环境改变时停止并保留失败证据。无标签仅能做一致性/机制检查；不得选择生产候选。即使预测正确也检查其他解释；真实结果可与 toy 趋势不同。
