## mrxn jswz 抓取脚本

### 本地运行

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/crawl_mrxn_jswz.py --output output/jswz
```

抓取结果：
- `output/jswz/html/*.html`
- `output/jswz/markdown/*.md`
- `output/jswz/manifest.json`

### GitHub Actions 自动执行

已提供工作流：`.github/workflows/crawl-mrxn-jswz.yml`。

- 支持手动触发（`workflow_dispatch`）
- 每周一自动执行一次
- 执行后会把抓取结果提交到 `mrxn-jswz-archive` 分支

> 首次使用前请先在仓库创建 `mrxn-jswz-archive` 分支。
