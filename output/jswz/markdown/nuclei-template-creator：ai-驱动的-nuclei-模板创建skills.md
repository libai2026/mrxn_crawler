---
title: "Nuclei Template Creator：AI 驱动的 Nuclei 模板创建skills"
source: https://mrxn.net/jswz/nuclei-template-creator.html
asset_dir: embedded-base64
---

## 简介

[Nuclei Template Creator](https://github.com/Mr-xn/nuclei-template-creator) 是一个全面的技能集，用于创建高质量的 [nuclei](https://mrxn.net/tag/nuclei "标签：nuclei") 安全[扫描](https://mrxn.net/tag/%E6%89%AB%E6%8F%8F "标签：扫描")模板。它涵盖了所有支持的协议和漏洞类型，帮助安全研究人员快速编写专业级的[扫描](#)模板。

机器学习与人工智能

## 核心特性

### 支持的协议类型（10 种）

| 协议 | 说明 | 应用场景 |
| --- | --- | --- |
| HTTP | Web 应用漏洞检测 | CVE、配置错误、信息泄露 |
| DNS | DNS 配置检测 | 子域名发现、DNS 劫持 |
| SSL/TLS | 证书安全检查 | 证书过期、弱加密 |
| Network/TCP | 网络服务扫描 | 服务识别、弱口令 |
| File | 本地文件扫描 | 敏感文件、配置泄露 |
| Headless | 浏览器自动化 | XSS、CSRF、DOM 漏洞 |
| JavaScript | JS 代码执行 | 复杂逻辑漏洞 |
| Code | 代码执行检测 | RCE、命令注入 |
| DAST | 模糊测试 | SQL 注入、XSS |
| Cloud | 云安全扫描 | AWS、Azure 配置错误 |

### 匹配器和提取器

**7 种匹配器类型**：

- `status` - HTTP 状态码匹配
- `size` - 响应大小匹配
- `word` - 关键词匹配
- `regex` - 正则表达式匹配
- `binary` - 二进制[数据](#)匹配
- `dsl` - DSL 表达式匹配
- `xpath` - XPath 表达式匹配

**5 种提取器类型**：

- `regex` - 正则提取
- `kval` - 键值提取
- `json` - JSON 提取
- `xpath` - XPath 提取
- `dsl` - DSL 表达式提取

### 强大的 DSL 函数库

提供 60+ 个 DSL 函数，涵盖：

C 与 C++

- **字符串处理**：`contains`, `replace`, `trim`, `split`
- **编码解码**：`base64`, `base64_decode`, `url_encode`, `html_encode`
- **哈希计算**：`md5`, `sha256`, `sha1`
- **压缩解压**：`gzip`, `gunzip`
- **随机生成**：`rand_char`, `rand_int`, `rand_text`
- **日期时间**：`date`, `time`, `year`, `month`
- **加密解密**：`aes_encrypt`, `aes_decrypt`

## 使用示例

### 1. CVE 漏洞检测模板

```
id: CVE-2024-1234
info:
  name: Example App RCE
  author: security-researcher
  severity: critical
  description: |
    Example App 存在远程代码执行漏洞
  reference:
    - https://nvd.nist.gov/vuln/detail/CVE-2024-1234
  tags: cve,rce,example

http:
  - method: POST
    path:
      - "{{BaseURL}}/api/deserialize"
    headers:
      Content-Type: application/json
    body: '{"data":"{{base64(marker)}}"}'

    matchers:
      - type: word
        words:
          - "{{marker}}"
        part: body
```

### 2. 配置错误检测

```
id: app-config-exposure
info:
  name: App Configuration Exposure
  author: security-researcher
  severity: high
  description: 检测应用配置文件泄露
  tags: misconfig,exposure

http:
  - method: GET
    path:
      - "{{BaseURL}}/config.yml"
      - "{{BaseURL}}/config.json"
      - "{{BaseURL}}/.env"
    stop-at-first-match: true

    matchers-condition: and
    matchers:
      - type: word
        words:
          - "database:"
          - "secret_key:"
          - "password:"
        condition: or

      - type: status
        status:
          - 200
```

### 3. SSRF 漏洞检测

```
id: ssrf-oob-detect
info:
  name: SSRF via OOB Detection
  author: security-researcher
  severity: high
  description: 通过 OOB 检测 SSRF 漏洞
  tags: ssrf,oob

http:
  - method: GET
    path:
      - "{{BaseURL}}/fetch?url={{interactsh-url}}"
      - "{{BaseURL}}/proxy?url={{interactsh-url}}"

    matchers:
      - type: word
        part: interactsh_protocol
        words:
          - "http"
```

## 模板验证清单

提交模板前请检查：

计算机安全

- ✅ ID 唯一、描述性强、小写连字符格式
- ✅ 信息块包含名称、作者、严重性
- ✅ 描述清楚解释了检测内容
- ✅ 包含参考链接（CVE、公告等）
- ✅ 标签全面且符合惯例
- ✅ 匹配器使用分层验证
- ✅ 模板能检测到漏洞
- ✅ 不会产生误报
- ✅ YAML 语法有效

**验证命令**：

```
nuclei -validate -t template.yaml
```

## 统计信息

| 指标 | 数量 |
| --- | --- |
| 总文件数 | 27 |
| 总行数 | ~5,100 |
| 协议文档 | 10 |
| 匹配器类型 | 7 |
| 提取器类型 | 5 |
| DSL 函数 | 60+ |
| JS 函数 | 35 |
| 示例模板 | 9 |

## 项目信息

- **作者**: Mr-xn
- **许可证**: MIT
- **GitHub**: [nuclei-template-creator](https://github.com/Mr-xn/nuclei-template-creator)

## 总结

[nuclei](https://mrxn.net/tag/nuclei "标签：nuclei") Template Creator 是一个强大的 Nuclei 模板创建工具，它：

黑客与破解

1. **覆盖全面** - 支持 10 种协议类型
2. **功能强大** - 60+ DSL 函数、35 个 JS 函数
3. **示例丰富** - 9 个真实世界模板示例
4. **文档完善** - 每个协议都有详细的参考文档

无论你是安全研究员、渗透测试工程师，还是安全工具开发者，这个技能集都能帮助你快速创建高质量的 Nuclei [扫描](https://mrxn.net/tag/%E6%89%AB%E6%8F%8F "标签：扫描")模板。

---
