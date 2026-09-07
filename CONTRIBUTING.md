# Maintenance

每个变更聚焦一个问题；笔记从模板创建，实验协议先于结果。提交说明写问题、改变、验证与局限。模型和 runtime 版本变更后，新建 baseline，保留旧结果。

运行测试、Markdown 链接检查和 `git diff --check`。GitHub Actions 在 push/PR 时运行 CPU 测试与文档检查，不拉权重、不运行 GPU benchmark。没有 LICENSE 文件时不推定仓库授予开源许可；许可证后续由所有者选择。

课程公式修改后运行 `python3 scripts/build_lesson_visuals.py` 重新生成图，并用 `bash scripts/check.sh` 验证。不要只改生成后的 HTML 数据。CPU 预设是教学证据，不可提升为 measured。
