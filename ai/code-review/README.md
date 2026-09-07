# Review gates

| 维度 | 要求的证据 |
|---|---|
| 正确性 | 独立 oracle、误差阈值、dtype/shape 边界 |
| runtime | streaming、取消、失败恢复、多请求缓存隔离、TP/graph 支持 |
| 性能 | 生效 kernel、同协议 baseline、完整轮次、错误率、尾延迟 |
| 质量 | 独立验证集、关键切片、方向与阈值 |
| 结论 | 缺测/模拟/失败明确；无 silent fallback；不把相关当因果 |

AI 生成的测试不能仅复述实现。优先手算案例、已知 oracle 和负向测试。
