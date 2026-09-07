# 弹性 Sprint

当前带学主线已具体化为 [六节课程](courses/README.md)，先上第 01 课。下面保留长期 Sprint 组织方式，不作为另一个必须从头执行的入口。

每次只推进一个主要问题，Sprint 约 1 周，允许 1–3 周。忙碌时 Core 可拆成四次短会话，暂停后从最后的证据继续，不重排整年计划。

| 环节 | Core | 完成证据 | Stretch |
|---|---|---|---|
| Theory | 写一个因果解释和一个反例 | 自己写出的预测 | 推导/论文 |
| Source | 定位一个真实 symbol 和调用者 | commit、路径、调用链 | 修改实现 |
| Experiment | 设计至少一个可证伪实验 | 变量、控制、指标、停止条件 | 远程运行/消融 |
| Reflection | 回答为什么，标记未知 | 解释、替代假设、下一步 | 博客/图解 |

Core 的 experiment 是设计义务，不要求每周都取得 GPU。完成设计不代表已证明优化有效。

## 前六个 Sprint

| Sprint | 核心问题 | Source 目标 | 实验设计 | 交付 |
|---|---|---|---|---|
| 1 | 为什么 prefill/decode 瓶颈不同？ | scheduler/model runner | 输入长度与并发分开扫描 | [启动任务](sprints/001-prefill-decode.md) |
| 2 | Qwen 指定模型到底缓存什么？ | config + attention/state 层 | 手算与分配内存对照 | model-analysis |
| 3 | 为什么请求有显存却仍在等待？ | scheduler/KV allocator | token budget 与 block 容量分开调整 | 调用链笔记 |
| 4 | BF16 baseline 如何做到可比较？ | serving benchmark 与业务 evaluator | 冻结数据、采样、输出 cap、3 轮 | benchmark 合同 |
| 5 | 量化误差为何集中在少数层？ | scale/observer/linear dispatch | 校准切片与粒度消融 | quantization note |
| 6 | W4A16 何时比 W8A8 慢？ | quantized GEMM backend | batch × 输入输出长度 | 四维实验计划 |

## 结束与恢复

每次关闭工作前更新 `sprints/current.md` 的下一条可执行动作、未决问题和证据链接。两次 Sprint 都卡住时，缩小到一个 kernel/一个请求/一个质量切片，先证伪最便宜的假设。每四个完成的 Sprint 合并一份 Playbook，不搬运重复笔记。

判断是否学会：不用 AI 写出“如果改变 X，那么 Y 应该怎样变化，因为 Z”；让 AI 提供竞争解释，再用证据裁决。允许结果与预测相反。
