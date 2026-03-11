## mrxn jswz 抓取脚本

### 本地运行

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 默认参数（已包含限速 + 429 重试）
python scripts/crawl_mrxn_jswz.py --output output/jswz

# 如果仍被限流，可进一步放慢
python scripts/crawl_mrxn_jswz.py \
  --output output/jswz \
  --delay 1.0 \
  --min-interval 1.8 \
  --max-retries 8 \
  --base-backoff 2.0
```

抓取结果：
- `output/jswz/html/*.html`
- `output/jswz/markdown/*.md`
- `output/jswz/manifest.json`

### 抗限流策略

脚本内置：
- 请求最小间隔（`--min-interval`）
- 遇到 429 或网络异常时自动指数退避重试（`--max-retries`、`--base-backoff`）
- 随机抖动（`--jitter-max`）避免固定节奏触发风控

### GitHub Actions 自动执行

已提供工作流：`.github/workflows/crawl-mrxn-jswz.yml`。

- 支持手动触发（`workflow_dispatch`）
- 每周一自动执行一次
- 执行后会把抓取结果提交到 `mrxn-jswz-archive` 分支
- 工作流会自动检测并创建 `mrxn-jswz-archive` 分支（若不存在）
- 工作流会输出详细日志，并在 `manifest.json` 为空时直接失败，便于排查限流问题
- 工作流会在归档分支上执行时，强制使用触发该工作流的提交中的爬虫脚本，避免分支脚本版本落后导致参数不兼容
