# Mental models

- Roofline：局部 kernel 的计算/搬运上界；不包含队列和网络。
- Amdahl：只占 10% 总时间的阶段即使无限快，总加速最多约 1.11×。
- Little's law：稳定系统 L=λW；注意统一系统边界，不套用到无限增长队列。
- Capacity vs efficiency：能容纳更多请求与每个 token 算得更快是两件可独立测量的事。

使用前列出假设，使用后寻找违反假设的观测。
