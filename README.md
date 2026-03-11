## mrxn jswz 抓取脚本（Playwright）

使用无头浏览器抓取 `https://mrxn.net/jswz`，导出为 **Markdown**，并把文章内图片下载到本地（Markdown 引用本地图片）。

### 本地运行

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install --with-deps chromium

python scripts/crawl_mrxn_jswz.py --output output/jswz
```

### 输出结果

- `output/jswz/markdown/*.md`（按文章标题清洗后命名）
- `output/jswz/assets/<title>/images/*`（每篇文章对应图片目录）
- `output/jswz/manifest.json`
- `output/jswz/crawl_report.json`

### 说明

- 仅导出 Markdown，不再输出 HTML 文件。
- 每次抓取前会清理旧的 `output/jswz`，避免历史 md/html 混入新结果。
- 图片会优先读取 `src/data-src/data-original/srcset` 并下载到本地，下载请求会携带 `Referer/Origin/User-Agent`（兼容防盗链）；成功后 Markdown 改写为本地图片路径，失败则保留原始图片链接。
- 工作流会把 `output/jswz` 打包为 `jswz-output.tgz` 并上传 artifact，同时推送到 `mrxn-jswz-archive` 分支。

### 快速验证工作流（仅抓 10 篇）

已新增：`.github/workflows/crawl-mrxn-jswz-smoke-10.yml`

- 仅支持手动触发（`workflow_dispatch`）
- 最多抓取 10 篇文章（`--max-articles 10`）
- 不推送归档分支，只上传测试 artifact（`jswz-smoke10-output`）

本地也可快速验证：

```bash
python scripts/crawl_mrxn_jswz.py --output output/jswz-smoke10 --max-articles 10
```
