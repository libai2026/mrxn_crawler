---
title: "nginx2root-从nginx请求到宿主机root远程代码执行漏洞"
source: https://mrxn.net/jswz/nginx2root-nginx-rce.html
asset_dir: embedded-base64
---

# nginx2root：从 nginx 请求到宿主机 root

2026 年 11 月 18 日，Xint 公开了一组 [nginx](https://mrxn.net/tag/nginx "标签：nginx") [漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "标签：漏洞")，取名 nginx2root。名字描述的是攻击路径：一个普通的 nginx 访问者，最后拿到宿主机的 root。

这组[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "标签：漏洞")一共六个。五个在 [nginx](https://mrxn.net/tag/nginx "标签：nginx") 里，编号分别是 CVE-2026-123007、CVE-2026-123634、CVE-2026-123633、CVE-2026-121810、CVE-2026-113425，每一个都能单独导致远程代码执行，要求的配置各不相同。第六个在 Linux 内核的 SCTP 子系统里，负责把 nginx worker 的权限提升到 root。Xint 在 AWS、GCP、Azure 和物理机上都做了演示。其中一次在 Docker 容器里运行 nginx，先以 worker 权限[执行命令](https://mrxn.net/tag/rce "标签：执行命令")，再用内核漏洞拿到宿主机的 root。容器被攻破之后，同一台宿主机上的其他容器也暴露在同一个内核漏洞下。

最严重的是 CVE-2026-123007。目标只要启用 HTTP/2，未认证的攻击者就能在 worker 进程的权限下[执行命令](https://mrxn.net/tag/rce "标签：执行命令")。这段代码从 2015 年 nginx 引入 HTTP/2 时就在，1.9.5 到 1.31.8 的所有官方版本都包含，2026 年 11 月 10 日的 master 分支也没有改掉。修复版本是 1.31.9，Xint 的文章发布时，这个版本计划在 11 月 19 日（KST）发布。补丁可用之前，关闭 HTTP/2 只能挡住五个 nginx 漏洞中的两个。

## 影响范围

五个 nginx 漏洞是彼此独立的攻击路径，不需要串起来用，区别在于受影响的配置。

| CVE | 受影响的配置 | 该路径首个受影响版本 | 关闭 HTTP/2 能否阻断 |
| --- | --- | --- | --- |
| CVE-2026-123007 | 启用 HTTP/2 | 1.9.5 | 能 |
| CVE-2026-123634 | 使用 resolver，proxy\_pass 的目标来自请求，并启用 mirror（mirror\_request\_body off） | 1.13.4 | 不能 |
| CVE-2026-123633 | 启用 HTTP/2，请求转发到上游服务器 | 1.19.7 | 能 |
| CVE-2026-121810 | 启用 HTTP/3，请求转发到上游服务器 | 1.25.0 | 不能 |
| CVE-2026-113425 | 邮件代理启用 proxy on 与 auth\_http | 0.5.15 | 不能 |

CVE-2026-123634 这一行是 Xint 测试过的配置，用的是 mirror 指令。SSI 这类同样会创建子请求的功能也可能触发同一个 bug，只关掉 mirror 并不能让服务器安全。

Xint 将这组漏洞定为严重（Critical）级别，修复版本统一为 1.31.9。

## 只看版本号不够

发行版经常把安全修复 backport 到旧版本，而不是换一个新的 nginx 版本。Ubuntu 24.04 自带 1.24.0，Ubuntu 22.04 是 1.18.0，Debian 12 是 1.22.1，三个都在受影响区间里，但不能只看这个数字。

backport 修好漏洞之后，nginx -v 显示的版本不变，变的是发行版的完整包版本。Ubuntu 22.04 最初发布的是 1.18.0-6ubuntu14，到 2026 年 10 月 26 日，安全更新已经把包推到 1.18.0-6ubuntu14.22，nginx 版本还是 1.18.0。要确认某个修复是否包含在内，要用完整的包版本去核对发行版的安全通告。

Xint 引用了 Shodan 在 2026 年 11 月 10 日的数据：product:nginx 返回 5670 万台主机，其中 1194 万台（21.1%）能识别出版本；在能识别版本的机器里，98.9% 落在 1.9.5 到 1.31.8 之间。这些数字来自版本字符串，不能证明服务器一定存在漏洞：触发 CVE-2026-123007 还需要启用 HTTP/2，报出来的版本也可能已经带上了 backport 的修复。

## 怎么判断是否受影响

CVE-2026-123007 的判定要看三件事：运行的是未修复的版本、二进制包含 HTTP/2 模块、配置里启用了 HTTP/2。下面三条命令分别检查，第四条从外网确认 HTTP/2 是否可达。

版本：

```
nginx -v 2>&1
```

输出类似 `nginx version: nginx/1.31.8`。1.9.5 到 1.31.8 的官方版本包含有问题的代码，继续往下查；1.9.4 及更早的版本没有 HTTP/2 支持，不受这个漏洞影响；1.31.9 及以后通常已经修复，但要确认构建里包含 F5 文章 K000164058 提到的改动；发行版或设备自带的版本不能只看字符串，要确认修复是否 backport。

HTTP/2 模块：

```
nginx -V 2>&1 | grep -q -- '--with-http_v2_module' \
  && echo 'HTTP2_MODULE=present' \
  || echo 'HTTP2_MODULE=absent'
```

present 表示二进制里有 HTTP/2 代码，未修复时存在漏洞，继续查下一项。absent 表示不含这段代码，不受这个漏洞影响。

配置：

```
sudo nginx -T 2>&1 \
  | sed 's/#.*//' \
  | grep -nE 'listen[[:space:]].*http2|^[[:space:]]*http2[[:space:]]+on[[:space:]]*;'
```

输出 `listen 443 ssl http2;` 或 `http2 on;` 说明启用了 HTTP/2，没有输出说明没有启用。nginx -T 读的是磁盘上的配置，改完没有 reload 的话，运行中的配置可能和文件不一致。

外网可达性：

```
openssl s_client -connect {HOST}:443 -servername {HOST} -alpn h2 </dev/null 2>&1 \
  | grep -E 'ALPN protocol:|No ALPN negotiated|Connection refused|connect:errno|handshake failure'
```

从外网执行，把两个 {HOST} 换成自己的域名，端口不是 443 就改掉。看到 `ALPN protocol: h2` 说明服务器接受来自外网的 HTTP/2；`No ALPN negotiated` 说明不接受；其他输出表示连接失败，要先确认服务器可达。nginx 前面有 CDN 或反向代理时，这个测试只到代理，需要再对 nginx 本身执行一次。

| 结果 | 判断 |
| --- | --- |
| 未修复的 1.9.5 至 1.31.8 + HTTP2\_MODULE=present + 实际 nginx 端口返回 ALPN protocol: h2 | 存在漏洞且对外暴露，立即处理 |
| 未修复的 1.9.5 至 1.31.8 + HTTP2\_MODULE=present + HTTP/2 已关闭 | 代码在，当前攻击路径关闭 |
| 1.9.4 及更早，或 HTTP2\_MODULE=absent | 不受这个漏洞影响 |
| 已安装 1.31.9，或确认旧版本已 backport 修复 | 已修复 |
| 连接失败、TLS 握手失败，或补丁状态无法确认 | 无法判断，需要进一步检查 |

## 技术分析

五个 nginx 漏洞里，CVE-2026-123007 是整数溢出导致的越界写，另外四个是释放后使用。Xint 说明了每个漏洞的成因、如何实现地址泄露和受控的内存破坏，复现完整利用的最后几步没有公开。下面引用的代码对应 Xint 文章里的 nginx 提交 140aa942711868a8daeb95810bc9a81f272ada72，按文件路径标注。

### CVE-2026-123007：HTTP/2 发送窗口的算术错误

HTTP/2 在一条连接上承载多个请求和响应，每一对请求和响应用一个流表示。客户端创建的流有编号，比如 1、3、5。流里的 HEADERS 帧带头部，DATA 帧带正文。

流量控制靠发送窗口实现。每个流有一个窗口，整条连接还有一个连接级窗口，代码里叫 h2c 窗口。窗口的数值表示服务器还能发多少 DATA。只有流窗口和 h2c 窗口都有余额，服务器才能在这个流上发 DATA。客户端准备好接收更多数据时发 WINDOW\_UPDATE 帧，服务器把对应的窗口加上这个值。流 ID 为 0 时加的是 h2c 窗口，非 0 时只加该流的窗口。

nginx 的默认窗口是 65535（0xffff），上限是 0x7fffffff：

```
// src/http/v2/ngx_http_v2.h
#define NGX_HTTP_V2_MAX_WINDOW      ((1U << 31) - 1)
#define NGX_HTTP_V2_DEFAULT_WINDOW  65535
```

nginx 把要发的帧放在内存里的输出队列，再通过 socket 发出去。响应 DATA 入队时，ngx\_http\_v2\_send\_chain() 从连接级发送窗口 h2c->send\_window 和流窗口 stream->send\_window 里各扣掉这段 DATA 的长度：

```
// src/http/v2/ngx_http_v2_filter_module.c
ngx_http_v2_queue_frame(h2c, frame);
h2c->send_window -= frame_size;
stream->send_window -= frame_size;
stream->queued++;
```

流在 DATA 发出之前被取消时，ngx\_http\_v2\_filter\_cleanup() 把该流剩余的 DATA 帧从队列里移除，并把扣掉的长度还给连接级窗口：

```
// src/http/v2/ngx_http_v2_filter_module.c
h2c->send_window += window;
```

入队时扣、取消时还，两步单独看都成立。问题在两步之间：DATA 还在队列里的时候，客户端可以再发 WINDOW\_UPDATE 把窗口加回去；随后取消流，cleanup 又在已经加过的窗口上再加一次。cleanup 不检查结果是否超过 HTTP/2 的上限，h2c->send\_window 就这样越过了 0x7fffffff。

#### (1) 把已扣的额度还两次

第一步是让队列里积压一批已经扣过窗口额度、但还没有发出的 DATA。

客户端先用流 ID 0 的 WINDOW\_UPDATE 把连接发送窗口拉到上限 Wmax，再用 SETTINGS 帧里的 SETTINGS\_INITIAL\_WINDOW\_SIZE 把新流的初始窗口设为 0。初始窗口为 0 时，nginx 能创建响应 HEADERS，发不了 DATA，响应正文就停在待发状态，等客户端放行。

接着客户端停止读取，连发一批 PING。nginx 把控制帧的响应（PING 确认也在里面）排在待发的 DATA 前面，这些确认把 TLS 和 TCP 的发送缓冲填满。客户端再给每个流发足够的 WINDOW\_UPDATE，够放下整个响应正文，nginx 于是把这些 DATA 排进队列，并从连接窗口里扣掉它们的总长度。TLS 和 TCP 缓冲已经满了，这批 DATA 就留在队列里。

设这批 DATA 的总量是 Q。客户端把 Q 加回 h2c 窗口两次。第一次是流 ID 0 的 WINDOW\_UPDATE，给 Q 的额度；第二次是 RST\_STREAM 取消流，取消触发 cleanup，丢弃未发的 DATA 并归还额度，Q 又加了一次：

```
// src/http/v2/ngx_http_v2_filter_module.c
if (frame->stream == stream && !frame->blocked) {
    *fn = frame->next;
    window += frame->length;
}
h2c->send_window += window;
```

最后一行就是第二次加法，没有上限检查。窗口依次经过四个值：Wmax，客户端把窗口拉到上限；Wmax - Q，排入 DATA 扣掉 Q；Wmax，流 ID 0 的 WINDOW\_UPDATE 加回 Q；Wmax + Q，cleanup 再还一次 Q，越过 0x7fffffff。

响应正文的具体大小和流的数量都不重要，只要同一个已知量 Q 被加回两次，一次来自 WINDOW\_UPDATE，一次来自 cleanup。

#### (2) 窗口检查里的无符号下溢

ngx\_http\_v2\_state\_window\_update() 在应用增量之前先算剩余容量：

```
// src/http/v2/ngx_http_v2.c
if (window > NGX_HTTP_V2_MAX_WINDOW - h2c->send_window) {
    return ngx_http_v2_connection_error(h2c, NGX_HTTP_V2_FLOW_CTRL_ERROR);
}
h2c->send_window += window;
```

这个检查只在连接级窗口不超过上限时有效。h2c->send\_window 的类型是无符号的 size\_t，上一步已经把它变成 Wmax + Q。剩余容量的表达式变成 Wmax - (Wmax + Q)，按有符号数看是负数，无符号运算会把它回绕成一个很大的正数。nginx 把这个值当成可用容量，继续接受连接级的 WINDOW\_UPDATE。每次增量本身都符合 HTTP/2 规范，检查却看不出当前窗口已经越界。重复这个过程，发送窗口可以加到任意 64 位值。

#### (3) 从超大窗口到越界拷贝

h2c->send\_window 是 size\_t。在 64 位平台上把它加到 2^64 - d，按无符号值看非常大，转成有符号的 off\_t 就是一个小负数 -d。

ngx\_http\_v2\_send\_chain() 把这个值带进 DATA 帧的长度。它先拿发送窗口和 limit 比较，limit 是当前这次调用最多能发的量：

```
// src/http/v2/ngx_http_v2_filter_module.c
if (limit == 0 || limit > (off_t) h2c->send_window) {
    limit = h2c->send_window;
}
```

limit 是正数，大于 -d，条件成立，limit 也变成 -d。下一次比较用当前的 DATA 帧大小 frame\_size 和 limit：

```
// src/http/v2/ngx_http_v2_filter_module.c
if ((off_t) frame_size > limit) {
    frame_size = (size_t) limit;
}
```

frame\_size 是正数，同样大于 -d，条件同样成立。-d 转回 size\_t 变成 2^64 - d，一个正常的 DATA 长度就这样变成极大值。

nginx 把这个值存进 rest，表示还没有挂到缓冲区上的长度，再传给 ngx\_http\_v2\_filter\_get\_shadow() 设置缓冲区的起止指针：

```
// src/http/v2/ngx_http_v2_filter_module.c
rest = frame_size;
cl = ngx_http_v2_filter_get_shadow(stream, in->buf, offset, rest);

static ngx_chain_t *
ngx_http_v2_filter_get_shadow(ngx_http_v2_stream_t *stream, ngx_buf_t *buf,
    off_t offset, off_t size)
{
    chunk->last = chunk->pos + size;
}
```

size 按 off\_t 解释是 -d，chunk->last 指向 chunk->pos 往前 d 个字节。TLS 输出路径随后用这两个指针的差作为拷贝长度：

```
// src/event/ngx_event_openssl.c
ssize_t size;
size = in->buf->last - in->buf->pos;
ngx_memcpy(buf->last, in->buf->pos, size);
```

last - pos 是 -d，memcpy() 的长度参数类型是 size\_t，最后一次转换又把它变成 2^64 - d。

一次接近 2^64 字节的拷贝通常会越过堆尾，导致 worker 崩溃。这里没有崩，原因是 glibc 处理大块拷贝的方式。实验里用到的 x86-64 glibc memcpy() 先读源地址的开头，然后从目标地址的末尾向前循环复制中间部分。

目标的末尾是 dest + size。size = 2^64 - d 时，这个加法在 64 位地址空间里回绕成 dest - d，落在 dest 前面 d 个字节。末尾到了开头前面，向前循环只走一轮就结束，中间那一大段没有被碰。glibc 的 x86-64 实现从 2.24（2016 年）起就是这个结构，每次循环搬四个 32 字节向量。

下面是 glibc 2.41 AVX2 路径的简化版：

```
head = load128(src)
tail = load32(src + size - 32)
end = (dest + size) mod 2^64
cursor = align_down(end - 129, 32)
do {
    copy128(dst=cursor, src=src + (cursor - dest))
    cursor -= 128
} while (cursor > dest)
store128(dst=dest, data=head)
store32(dst=end - 32, data=tail)
```

align\_down(x, 32) 把 x 向下取整到 32 字节边界。end 按 32 字节对齐时，cursor = align\_down(end - 129, 32) 等于 end - 160，glibc 从这个位置复制 128 字节，再单独复制最后 32 字节：

```
end - 160                         end - 32             end
    |---------- 128 bytes ----------|------ 32 bytes -----|
              loop copy                    fixed copy
```

cursor 已经低于 dest，循环只执行一次，长中间段被跳过，实际只复制开头 128 字节和末尾 160 字节：

```
src ~ src + 127                   -> dest ~ dest + 127
src - d - 160 ~ src - d - 1       -> dest - d - 160 ~ dest - d - 1
```

dest 是 TLS 明文缓冲区里的下一个写入位置，紧跟在 nginx 已经写进去的内容后面。响应正文之前，nginx 会写客户端控制帧的确认，确认的条数由客户端决定。HTTP/2 帧头 9 字节，PING 数据 8 字节，SETTINGS ACK 数据 0 字节：

```
// src/http/v2/ngx_http_v2.h
#define NGX_HTTP_V2_FRAME_HEADER_SIZE    9

// src/http/v2/ngx_http_v2.c
#define NGX_HTTP_V2_SETTINGS_ACK_SIZE    0
#define NGX_HTTP_V2_PING_SIZE            8
```

客户端发 p 个 PING、s 个 SETTINGS，nginx 先生成 17p + 9s 字节的响应；加上紧随其后的 9 字节 DATA 帧头，就是下一个响应正文的起始位置：

```
P = 17p + 9s + 9
dest = TLS + P
```

客户端用 WINDOW\_UPDATE 调整发送窗口，让 d = P - 64，拷贝终点 dest - d 就落在 TLS + 64。160 字节的区间覆盖 TLS 缓冲区前面的 96 字节和缓冲区内的前 64 字节。

第二次移动把 src - d 下面的 160 字节复制到 TLS 缓冲区边缘。攻击者要在这 160 字节里放两样东西：一个用来覆盖 TLS 缓冲区前面堆元数据的选定值，一组落在缓冲区里、随后随响应发回的指针。请求内存池里两样都有：请求头、描述请求头的 nginx 结构，以及指向 nginx 镜像和堆的指针。

要让 src 落到请求池，攻击者发一个包含多个字节区间的 Range 头。nginx 生成 multipart 响应，开头的分隔串在请求池里分配，b->pos 指向这里：

```
// src/http/modules/ngx_http_range_filter_module.c
ctx->boundary_header.data = ngx_pnalloc(r->pool, size);

// src/http/modules/ngx_http_range_filter_module.c
b->pos = ctx->boundary_header.data;
```

b->pos 经过输出路径成为 in->buf->pos，也就是最后那次 memcpy() 用的 src。

src 落在请求池之后，攻击者用 Cookie 字段填 src - d 下面的 160 字节。同一个请求里有多个 Cookie 字段时，nginx 按每个分隔符两字节计算总长度，再用 "; " 把各个值拼起来，长度和合并后的缓冲区地址存进请求头结构：

```
// src/http/v2/ngx_http_v2.c
len += vals[i].len + 2;
len -= 2;
h->key.data = cookie.data;
h->value.len = len;
h->value.data = buf;
```

h->key.data 指向 nginx 镜像里的静态字符串，h->value.data 指向堆上的 Cookie 缓冲区。这个结构里既有攻击者控制的长度，也有指向 nginx 镜像和堆的指针。

当前请求池的块里空间够时，nginx 把新的小分配紧挨着上一块放：

```
// src/core/ngx_palloc.c
m = p->d.last;
if ((size_t) (p->d.end - m) >= size) {
    p->d.last = m + size;
    return m;
}
```

Cookie 的条数和长度控制数据与位置，Range 和 URI 的长度决定作为 src 的 multipart 缓冲区的位置。src - d 前面的 160 字节可以排成：

```
源:   [96 字节，放 size 字段的值][64 字节的代码与堆指针]
目标: [TLS 缓冲区前的 96 字节，含堆元数据][TLS 明文缓冲区的前 64 字节]
```

前 96 字节覆盖 TLS 明文缓冲区前面堆区里的 size 字段，后 64 字节随 TLS 响应发回，泄露 nginx 镜像和堆地址。一次畸形的拷贝同时给出越界写和地址泄露。接下来覆盖清理回调的函数指针，就能以 worker 权限执行命令。Xint 没有公开覆盖函数指针的具体步骤。

验证只用了外部可达的 TLS/HTTP/2 端口。Xint 演示了未认证远程代码执行：改掉发送窗口，泄露 nginx 镜像和堆地址，接管一个清理回调，以 worker 权限执行命令。在 AWS、GCP、Azure 上，从目标服务器本机、VPC/VNet 内网的另一台主机、公网 IP 三种位置都成功，目标同时承载正常流量时也成立。

### CVE-2026-123634：DNS 解析器里的释放后使用

nginx 可以作为反向代理，把客户端请求转给后端服务器，后端叫上游。proxy\_pass 指定上游的位置。上游可以写死在配置里，也可以从请求里取。比如 `proxy_pass http://$host;` 用 $host 里的主机名作为目标，这个值通常来自客户端的 Host 头。要拿到服务器的 IP 地址就得查 DNS，nginx 用 resolver 指令指定的 DNS 服务器查询。

DNS 查询要等，nginx 在等的时候继续处理其他请求。每次查询有一个 resolver 上下文（ngx\_resolver\_ctx\_t），保存状态、结果和一个 handler，查询完成时调用这个 handler。

resolver 按域名维护节点。同名查询还在进行时，nginx 不再发第二次查询，而是把新的上下文挂到该节点等待链表的头部。答案回来后，resolver 把等待链表从节点上摘下来，rn->waiting 置空，然后遍历链表，逐个调用上下文的 handler。遍历时先把下一个上下文存进 next，再调用当前 handler：

```
// src/core/ngx_resolver.c
next = rn->waiting;
rn->waiting = NULL;
...
while (next) {
    ctx = next;
    ctx->state = code;
    ctx->valid = ngx_time() + (r->valid ? r->valid : 10);
    next = ctx->next;
    ctx->handler(ctx);
}
```

handler 如果释放了链表里靠后的上下文，next 就悬空了。不同请求之间不会这样，因为结束一个请求只释放它自己的上下文。只有两个上下文属于同一个请求时，才是漏洞。

测试中只有一个配置会为同一个请求创建两个上下文：mirror。这个指令把请求复制一份，作为后台子请求发到另一个 location，常用来把线上流量复制给测试系统。主请求和 mirror 用同一个上游域名时，两个上下文会挂在同一个节点上等同一个 DNS 答案。

#### (1) 主请求结束，释放 mirror 的上下文

DNS 查询失败时，主请求的 ngx\_http\_upstream\_resolve\_handler() 尝试返回 502。客户端已经把 TCP 连接重置的话，这次写会失败，ngx\_http\_terminate\_request() 于是结束主请求。

主请求的 cleanup 链表里有 mirror 的上游清理，下面这段代码也会对 mirror 执行，尽管 mirror 的 DNS 结果还没有处理：

```
// src/http/ngx_http_upstream.c
if (u->resolved && u->resolved->ctx) {
    ngx_resolve_name_done(u->resolved->ctx);
    u->resolved->ctx = NULL;
}
```

ngx\_resolve\_name\_done() 释放了 mirror 的上下文，而 resolver 的循环还把它存在 next 里。

#### (2) resolver 使用已释放的上下文

循环走到之前，mirror 的上下文仍处于 NGX\_AGAIN。释放这种状态的上下文之前，ngx\_resolve\_name\_done() 会先尝试把它从节点的等待链表里摘下来。循环已经把链表摘走，rn->waiting 是 NULL，搜索什么也找不到，上下文照样释放：

```
// src/core/ngx_resolver.c
if (ctx->state == NGX_AGAIN || ctx->state == NGX_RESOLVE_TIMEDOUT) {
    rn = ctx->node;
    if (rn) {
        p = &rn->waiting;
        w = rn->waiting;
        while (w) {
            ...
        }
        ngx_log_error(NGX_LOG_ALERT, r->log, 0,
                      "could not cancel %V resolving", &ctx->name);
    }
}
done:
    ...
    ngx_resolver_free_locked(r, ctx);
```

控制流回到 resolver 循环，循环取出 next 里保存的 mirror 上下文，也就是已经释放的内存。它写 ctx->state 和 ctx->valid，读 ctx->next，调用 ctx->handler(ctx)。如果别的分配回收了这块内存，next 和 handler 都由攻击者控制，链表遍历和最后的间接调用都被改向。

利用时，先要有地址泄露，这个漏洞本身就能用来泄露地址。glibc 的空闲链表指针覆盖上下文的 next 字段，循环拿到的下一个“上下文”就是一块内容可控的已释放 DNS 记录数组。攻击者把 handler 指向 vsyscall 里的 gettimeofday()（amd64 上地址固定），伪造堆块大小，把 glibc 和堆指针放进 nginx 发往自己控制的 DNS 服务器的查询里。有了泄露之后，再让循环穿过数组，落到待处理请求体里的伪造上下文上，handler 设为 system()，在宿主机上执行命令。

验证用的目标是官方 nginx:1.31.8 镜像，在默认配置上加一个 server 块，启用请求时的 DNS 解析和 mirror：

| 项目 | 结果 |
| --- | --- |
| 入口 | 8080 端口的 HTTP，以及攻击者域名的 DNS 应答 |
| 认证 | 无 |
| 网络要求 | nginx 的递归解析器能访问攻击者的权威 DNS 服务器 |
| 宿主机内核 | Ubuntu Linux 6.8（x86-64），vsyscall=xonly |
| 结果 | 以 nginx worker 权限执行远程代码 |

### CVE-2026-123633：可复用连接队列里的释放后使用

每个 nginx worker 的连接槽数量由 worker\_connections 决定，客户端连接和上游连接共用这些槽。槽不够时，nginx 关闭空闲连接，把槽让出来。哪些连接能回收由协议条件决定，比如空闲的 HTTP/1.1 keep-alive 连接，或者没有活动流的 HTTP/2 连接。这些可复用连接放在一个专门的队列里。

分配连接槽之前，ngx\_get\_connection() 调用 ngx\_drain\_connections()。空闲槽只剩 1/16 以下、可复用队列非空时，它从最老的连接开始关闭，代码里把这个过程叫 draining，下文写“清退”。清退把 c->close 置 1，直接调用选中连接的读 handler；这些调用是同步的，handler 返回之后才继续分配槽：

```
// src/core/ngx_connection.c
if (cycle->free_connection_n > cycle->connection_n / 16
    || cycle->reusable_connections_n == 0)
{
    return;
}
...
n = ngx_max(ngx_min(32, cycle->reusable_connections_n / 8), 1);
for (i = 0; i < n; i++) {
    ...
    q = ngx_queue_last(&cycle->reusable_connections_queue);
    c = ngx_queue_data(q, ngx_connection_t, queue);
    ...
    c->close = 1;
    c->read->handler(c->read);
}
```

#### (1) 活动的 HTTP/2 连接留在可复用队列

没有活动流、没有待发输出帧时，ngx\_http\_v2\_handle\_connection() 把 HTTP/2 连接放进可复用队列。上一次读停在帧中间的话，h2c->state.incomplete 会被置位，但这个标志在连接入队之后才检查：

```
// src/http/v2/ngx_http_v2.c
if (h2c->last_out || h2c->processing) {
    return;
}
...
ngx_reusable_connection(c, 1);
if (h2c->state.incomplete) {
    return;
}
```

正常情况下，空闲连接会把读 handler 换成 ngx\_http\_v2\_idle\_handler()，有数据时由它把连接移出队列。ngx\_http\_v2\_handle\_connection 因为帧不完整提前返回时，连接保留的是普通的 ngx\_http\_v2\_read\_handler()，这个 handler 不会把连接移出可复用队列。

触发顺序如下：客户端先发 HEADERS 帧的前半段，连接进入可复用队列；再发剩下的部分，打开一个流；这个请求如果打开上游连接并触发清退，清退可能回收新流所在的这条连接。

#### (2) 上游连接释放自己的请求

连上游需要另一个连接槽。ngx\_event\_connect\_peer() 调用 ngx\_get\_connection()，槽不够就执行清退。留在可复用队列里的 HTTP/2 连接这时可能被选中关闭。

HTTP/2 读 handler 看到 c->close，尝试发 GOAWAY；客户端已经把 TCP 连接重置的话，写失败，ngx\_http\_v2\_finalize\_connection() 关闭连接和上面的流：

```
// src/http/v2/ngx_http_v2.c
if (c->close) {
    c->close = 0;
    ...
    if (!h2c->goaway) {
        h2c->goaway = 1;
        if (ngx_http_v2_send_goaway(h2c, NGX_HTTP_V2_NO_ERROR)
            == NGX_ERROR)
        {
            ngx_http_v2_finalize_connection(h2c, 0);
            return;
        }
        if (ngx_http_v2_send_output_queue(h2c) == NGX_ERROR) {
            ngx_http_v2_finalize_connection(h2c, 0);
            return;
        }
    }
```

关闭流会调用 ngx\_http\_free\_request()，销毁请求内存池，请求 r 和上游结构 u 都在这个池里：

```
// src/http/ngx_http_request.c
/*
 * Setting r->pool to NULL will increase probability to catch double close
 * of request since the request object is allocated from its own pool.
 */
pool = r->pool;
r->pool = NULL;
ngx_destroy_pool(pool);
```

清退返回后，nginx 继续执行已释放请求的上游代码：连上游、发代理请求、处理这条连接上的事件，用的都是释放掉的 r 和 u。

利用需要堆布局。Xint 用一些布局技巧，让 glibc 的 largebin 头落在 u 上，头的 bk\_nextsize 字段落在 u->peer.sockaddr 上，指向攻击者准备好的字节（自己服务器的 sockaddr\_in），上游连接于是连到攻击者的服务器。

绕过 ASLR 的办法是接受这条连接。nginx 会把已释放的请求缓冲区发过来，里面是各种指针值。worker 随后崩溃，新的 worker 地址布局与它相同。

执行命令换一种布局：用伪造的请求回收这块内存，请求的上游读 handler 设成 execv()。拒绝这条连接时，epoll 报告错误，nginx 调用这个 handler。

验证用的目标是官方 nginx:1.31.8 镜像，在默认 nginx.conf 里加一个使用 proxy\_pass 的 TLS/HTTP/2 server：

| 项目 | 结果 |
| --- | --- |
| 入口 | 带 ALPN h2 的 TLS 端口，另一个 HTTP/1 端口用来占连接槽 |
| 认证 | 无 |
| 网络要求 | nginx 能向攻击者打开 TCP 连接 |
| 结果 | 以 nginx worker 权限执行远程代码 |

### CVE-2026-121810：HTTP/3 建流时的释放后使用

HTTP/3 在一条 QUIC 连接上承载多个请求流，nginx 内部为 QUIC 连接分配一个 ngx\_connection\_t，为每个流再分配一个，都来自同一个 worker 的连接槽，所以建一个请求流也要一个空闲槽。包含这些流的 QUIC 连接叫父连接。QUIC 连接和等待头部的 HTTP/3 请求流都可能被清退。

单个流关闭时，nginx 检查父连接是否也可以关闭。ngx\_quic\_can\_shutdown() 遍历父连接的流树，剩下的流都可以取消时，把父连接放进可复用队列：

```
// src/event/quic/ngx_event_quic_streams.c
if (!pc->reusable && ngx_quic_can_shutdown(pc) == NGX_OK) {
    ngx_reusable_connection(pc, 1);
}
```

#### (1) 建流过程中把父连接重新入队

给新流分配连接槽之前，ngx\_quic\_create\_stream() 先把父连接移出可复用队列，避免 ngx\_get\_connection() 在分配槽时清退父连接：

```
// src/event/quic/ngx_event_quic_streams.c
reusable = c->reusable;
ngx_reusable_connection(c, 0);
sc = ngx_get_connection(c->fd, log);
if (sc == NULL) {
    ngx_destroy_pool(pool);
    ngx_queue_insert_tail(&qc->streams.free, &qs->queue);
    ngx_reusable_connection(c, reusable);
    return NULL;
}
```

新流要等连接槽分配完才插入父连接的流树：

```
// src/event/quic/ngx_event_quic_streams.c
ngx_rbtree_insert(&qc->streams.tree, &qs->node);
```

假设清退关闭了同一父连接上一个已有的空闲流。那个流的两个方向都结束后，会触发父连接能否关闭的检查，但检查看不到一个还在创建中的流。树里没有其他不可取消的流，nginx 就把父连接放回可复用队列，新流创建完之后它仍然留在队列里。

#### (2) 上游连接释放请求

新流的请求连上游时要另一个槽，可能再次触发清退，选中刚入队的父 QUIC 连接。ngx\_quic\_close\_connection() 调用 ngx\_quic\_close\_streams() 关闭父连接的流，正在进行上游连接的请求随之结束。ngx\_http\_free\_request() 销毁请求池，上游结构 u 一起没了。控制流回到 ngx\_event\_connect\_peer()，它继续使用释放掉的 u->peer，形成释放后使用。

后面的 ASLR 绕过和控制流劫持与 CVE-2026-123633 相同，Xint 没有再重复。

验证目标还是官方 nginx:1.31.8 amd64 镜像，在默认 nginx.conf 里加一个 HTTP/3 代理 server：

| 项目 | 结果 |
| --- | --- |
| 入口 | UDP 443（HTTP/3）、TCP 443（HTTP/2）、TCP 80 |
| 认证 | 无 |
| 网络要求 | nginx 能向攻击者的监听端口打开 TCP 连接 |
| 结果 | 以 nginx worker 权限执行远程代码 |

### CVE-2026-113425：邮件代理认证路径的释放后使用

nginx 可以在客户端和邮件服务器之间代理 IMAP、POP3、SMTP。客户端登录时，nginx 用一个 HTTP 服务判断凭据是否有效、该用哪台后端邮件服务器，这个服务由 auth\_http 配置。查询期间 nginx 维护两条连接：一条到客户端，一条到认证服务，后者叫 auth 连接。

ngx\_mail\_auth\_http\_init() 为查询创建上下文和内存池，但 auth 连接的 data 和 pool 字段指向客户端的会话 s 和客户端连接的内存池。auth 连接使用会话期间，那个池必须一直有效：

```
// src/mail/ngx_mail_auth_http_module.c
ctx->peer.connection->data = s;
ctx->peer.connection->pool = s->connection->pool;
s->connection->read->handler = ngx_mail_auth_http_block_read;
ctx->peer.connection->read->handler = ngx_mail_auth_http_read_handler;
ctx->peer.connection->write->handler = ngx_mail_auth_http_write_handler;
```

#### (1) 查询期间释放客户端会话

查询开始时，客户端的读 handler 被换成 ngx\_mail\_auth\_http\_block\_read()。如果重新注册读事件失败，这个 handler 会关闭 auth 连接，释放查询的内存池。但客户端的写 handler 仍然是 ngx\_mail\_send()，它的错误路径不清理 auth 连接。问题就在这里：写 handler 可以在 auth 连接还指向客户端的时候关闭客户端连接。

这条路径要求客户端的写事件已经注册。比如客户端停止读取回复，把 socket 发送缓冲填满，一次 send 返回 EAGAIN，ngx\_mail\_send() 注册写事件等待重试。

登录命令和 TCP 复位在同一个事件循环里处理时，nginx 按 epoll 报告的错误先执行活动的读 handler，再执行写 handler。读 handler 解析登录命令，启动认证查询，此时 s->out 里还有一条排队的回复。ngx\_mail\_send() 接着发这条回复，写失败，关闭客户端连接并销毁它的内存池：

```
// src/mail/ngx_mail_handler.c
if (n == NGX_ERROR) {
    ngx_mail_close_connection(c);
    return;
}

// src/mail/ngx_mail_handler.c
c->destroyed = 1;
pool = c->pool;
ngx_close_connection(c);
ngx_destroy_pool(pool);
```

会话 s 和它的模块上下文数组都分配在这个池里，池已经没了。auth 连接仍然开着，data 字段还指向 s。

#### (2) auth 连接使用已释放的会话

下一个事件（连接完成、响应或超时）在 auth 连接上执行 handler。读 handler 和写 handler 都从连接的 data 字段取会话指针，再从中取查询上下文，访问的是已释放会话里的 s->ctx。如果攻击者控制的数据回收了这块内存，s->ctx 可以指向伪造上下文，认证响应路径随后调用 ctx->handler，控制流被劫持。

绕过 ASLR 用的是过期 auth 连接的超时。通过堆布局，让超时释放的内存正好放着另一条连接上只收到一半的 IMAP 命令；之后的一次分配用堆指针回收这块内存，nginx 回复 IMAP 命令时把这些指针原样发回。

执行命令要在新的 worker 上重新触发一次。会话刚释放时，用一个密码可控的 IMAP LOGIN 回收这块内存，伪造一个会话，s->ctx 指向伪造的查询上下文，handler 是 system()。认证服务回复时，ngx\_mail\_auth\_http\_read\_handler() 沿着过期会话调用 system(s)。

验证目标是官方 nginx:1.31.8 镜像，在默认配置上加一个包含 IMAP、POP3、SMTP 的 mail 块：

| 项目 | 结果 |
| --- | --- |
| 入口 | IMAP 143、POP3 110，以及同一批 worker 提供的 HTTP 80 |
| 认证 | 无，认证服务拒绝了每一次登录 |
| 结果 | 以 nginx worker 权限执行远程代码 |

### 内核 SCTP 漏洞：从 worker 到 root

nginx 的 worker 进程权限受限，要完全控制宿主机还需要一个提权漏洞。Xint 在 Linux 内核的 SCTP 子系统里找到一个 0day，与任一 nginx 漏洞串起来就能拿到宿主机 root，nginx 运行在 Docker 容器里时同样成立。这个内核漏洞没有公布 [cve](https://mrxn.net/tag/cve "标签：cve") 编号。

SCTP 是传输层协议，和 TCP、UDP 一样。它和 TCP 一样面向连接，把连接叫偶联（association）。一个偶联的两端可以各用多个 IP 地址，某条路径失效时还能走别的路径。

问题在 SCTP 的发送路径。一个发送操作在等待时，它所属的偶联可能被转移到另一个 socket；等待中的操作随后可能释放这个已经转移的偶联。另一个 socket 后续怎么做，决定结果是一次释放后使用还是双重释放。在内核用 KASAN 构建时，双重释放的报错形如：

```
BUG: KASAN: double-free in sctp_[...]
Free of addr ffff8880021b0880 by task t306/838
Call Trace:
 kfree+0x170/0x490
 sctp_[...]
 sctp_[...]
 sctp_[...]
Freed by task 836:
 kfree+0x23c/0x490
 sctp_[...]
 sctp_[...]
 sctp_[...]
 sctp_[...]
```

这个 bug 于 2018 年在 Linux v4.15 引入，在内核里存在了八年多。

这次释放后使用给出两种能力：泄露内核内存，从而绕过 KASLR；在内核里调用任意函数。两者合起来可以控制内核执行流并提权。测试中，已经以 nginx worker 身份执行代码的攻击者能稳定拿到 root。nginx 运行在 Docker 容器里的环境，也拿到了宿主机的 root shell。

很多发行版默认安装 SCTP 模块，程序第一次打开 SCTP socket 时内核自动加载。某台主机上 SCTP 是否可达，取决于内核、可用模块和容器限制。可达时，攻击者可以接管宿主机内核；同一台宿主机上的容器共用内核，所有容器都会受影响。

内核补丁出来之前，不用 SCTP 的主机可以在 /etc/modprobe.d/ 下的 .conf 文件里写 `install sctp /bin/false`，阻止模块加载。这只挡住通过 modprobe 的加载，不会卸载已经加载的模块，也挡不住编译进内核的 SCTP。

## 补丁可用前的临时缓解

这些措施只挡住已知的攻击路径，不能替代补丁。1.31.9 发布后应尽快安装。

关闭 HTTP/2（CVE-2026-123007、CVE-2026-123633）：

nginx 1.25.1 及以后，在每个受影响的 server 块里设 `http2 off;`，并从 listen 指令里去掉旧的 http2 参数；共用同一个监听地址和端口的 server 块都要检查：

```
listen 443 ssl;
http2 off;
```

1.9.5 到 1.25.0 去掉 `listen 443 ssl http2;` 里的 http2：

```
listen 443 ssl;
```

改完执行 nginx -t 和 nginx -s reload，再用前面的 ALPN 检查确认。最后一条命令在 HTTP/2 关闭后没有输出；连接失败时也没有输出，所以要确认站点通过 HTTPS 仍能正常访问。

去掉请求时的 DNS 查询（CVE-2026-123634）：

这项只针对按请求选择上游、同时使用 mirror 的服务器。proxy\_pass 里带变量（比如 `proxy_pass http://$host;`），nginx 在处理请求时用 resolver 查这个名字，就属于这种情况。

bug 在主请求和 mirror 等同一个 DNS 答案时触发。补丁之前，把 proxy\_pass 指向固定的上游组，请求期间不再查 DNS，测试过的那条路径就走不通了。把 mirror\_request\_body 设为 on 也能挡住 Xint 的利用，但它没有修 resolver 的 bug，不能只靠这个设置。

不需要 mirror 时，在受影响的 location 里关掉，并把 proxy\_pass 指向固定上游：

```
upstream backend_hotfix {
    server {BACKEND_IP}:8080;
}
location / {
    mirror off;
    proxy_pass http://backend_hotfix;
}
```

需要 mirror 时，主请求和 mirror 都指向固定的上游组：

```
upstream backend_main_hotfix {
    server [MAIN_SERVER_IP]:8080;
}
upstream backend_mirror_hotfix {
    server [MIRROR_SERVER_IP]:8080;
}
location / {
    mirror /mirror;
    proxy_pass http://backend_main_hotfix;
}
location = /mirror {
    internal;
    proxy_pass http://backend_mirror_hotfix;
}
```

关闭 HTTP/3（CVE-2026-121810）：

CVE-2026-121810 出在 QUIC 连接上的 HTTP/3 请求流处理里。在每个受影响的 server 块里删掉带 quic 的 listen 指令，设 `http3 off`，并把通告 HTTP/3 的 Alt-Svc 头换成 `Alt-Svc 'clear'`。TCP 上的普通 TLS 监听保留：

```
listen 443 ssl;
# listen 443 quic reuseport;
# listen [::]:443 quic reuseport;
http3 off;
add_header Alt-Svc 'clear' always;
```

reload 之后用 `ss -lunp 'sport = :443'` 检查 443 端口上还有没有 UDP 监听。输出里还有 nginx，说明 QUIC 监听还在；也可以在防火墙上封掉该端口的 UDP。

限制邮件代理的访问（CVE-2026-113425）：

这项只对把 nginx 当作 IMAP、POP3、SMTP 代理的部署有效。mail 块里同时有 `proxy on` 和 auth\_http 就属于受影响的情况。有 auth\_http 时，nginx 向一个 HTTP 服务询问每次登录是否有效，bug 在登录过程中触发，攻击者不需要有效凭据。

代理不需要对外时，把每个 IMAP、POP3、SMTP 监听都绑到回环地址，只有本机程序能连：

```
listen 127.0.0.1:143;
```

需要外部客户端访问时，用防火墙只放行信任的 IP 地址。

关闭已有连接：

reload 只对新连接生效。已经打开的 HTTP/2 或邮件会话留在旧 worker 上，继续用旧配置，ps 里显示为 `nginx: worker process is shutting down`。reload 之后这些 worker 还在，就用服务管理器重启 nginx（比如 `systemctl restart nginx`）。重启会断开所有客户端，正在进行的下载、上传和邮件会话都会中断，需要安排一个短暂的服务中断窗口。

## 入侵排查

用 CVE-2026-123007 的攻击在 access 日志里留下的痕迹很少。触发用的 WINDOW\_UPDATE 和 RST\_STREAM 是控制帧，不会按请求记录，传输过程中又被 TLS 加密。可以从四个地方看：连接统计、每条连接上的请求、worker 启动的程序、worker 异常退出。

连接统计：

```
sudo ss -tinp state established '( sport = :443 )'
```

间隔一小段时间执行两次，对比 bytes\_received 和 bytes\_sent 的变化。几条同时出现时优先看：同一外部 IP 的连接持续几分钟；bytes\_received 涨得很快；服务器发出的 bytes\_sent 远小于接收量；同一 IP 还开了很多短命的 TLS 连接。Xint 测试的攻击就是一条长连接上发大量 WINDOW\_UPDATE，nginx 回得很少，同时同一 IP 开很多短连接。连续几分钟都是这样又没有合理解释（比如大文件上传），封掉来源再排查。

按连接看请求：默认日志不记录请求属于哪条连接。在 http 块里加一个 log\_format，记录连接 ID、连接上的请求数、请求长度等字段，不需要 debug 版本：

```
log_format h2_hunt '$time_iso8601 src=$remote_addr conn=$connection '
                   'requests=$connection_requests proto=$server_protocol '
                   'status=$status request_length=$request_length '
                   'bytes_sent=$bytes_sent request_time=$request_time';

access_log /var/log/nginx/h2-hunt.log h2_hunt;
```

nginx -t 和 nginx -s reload 之后，只看 HTTP/2 请求：

```
sudo grep 'proto=HTTP/2.0' /var/log/nginx/h2-hunt.log | tail -n 200
```

从连接统计里挑一个可疑 IP，把它的 request\_length 按 conn 加起来，和 ss 里同一 IP 的 bytes\_received 对比。bytes\_received 一直涨、日志里的请求长度很小，说明客户端发了很多没有形成请求的数据，符合控制帧洪水的特征。同一时间段 request\_time 很长也是信号。

worker 启动的程序：Xint 的利用用 execve() 启动 shell 或其他程序，正常 worker 不会这么做。先找 worker 账号的 UID：

```
ps -eo uid,user,pid,ppid,args | grep '[n]ginx: worker process'
```

系统装了 auditd 的话，把 NGINX\_UID 换成上一条输出里的数字 UID，加一条规则：

```
sudo auditctl -a always,exit -F arch=b64 -S execve,execveat \
  -F euid=NGINX_UID -k nginx_worker_exec
```

规则只记录安装之后的事件，结果为空不能排除之前的入侵。同一个 UID 的其他进程也会命中，要看进程号和父进程号确认是不是 nginx 起的。查看记录：

```
sudo ausearch -k nginx_worker_exec -ts recent -i
```

看有没有 /bin/sh、/bin/bash 或其他由 nginx worker 启动的程序。

worker 异常退出：利用失败可能让 worker 崩溃，查 error.log 和 core dump：

```
sudo grep -Ei 'worker process.*exited|signal 11|segfault' /var/log/nginx/error.log
sudo coredumpctl list nginx
```

worker 崩溃可能有和攻击无关的原因，要和其他信号一起判断。

几类证据里，worker 启动程序这一条最明确，看到就立即处理。其余几类单独出现都可能有正常原因，同时出现又解释不了时，封掉来源再排查：持续的大量入站流量、同一来源的很多连接、实际接收字节与日志请求长度差距很大、worker 反复异常退出。

## 时间线

时间均为韩国标准时间（KST）。

| 日期 | 事件 |
| --- | --- |
| 2026 年 10 月 11 日 | Xint 研究团队发现漏洞 |
| 2026 年 10 月 16 日 | 通过 HackerOne 报告给 F5 |
| 2026 年 10 月 20 日 | HackerOne 完成验证 |
| 2026 年 10 月 27 日 | 报告交给 F5 的 nginx 开发团队 |
| 2026 年 11 月 10 日 | nginx 团队请求验证补丁 |
| 2026 年 11 月 10 日 | Xint 完成补丁验证 |
| 2026 年 11 月 19 日 | 计划发布补丁 |

CVE-2026-123007 是 Xint 的研究人员在准备 ZeroDay Cloud 2026 时发现的。几天后，Xint 的一次全自动扫描在没有人工干预的情况下找到了另外四个。漏洞由 Xint 研究团队的 @imssm99、@cdor1、@tjbecker、@yves 报告。

一次找到五个远程代码执行漏洞，在 nginx 上并不常见。二十多年里 nginx 的未认证 [rce](https://mrxn.net/tag/rce "标签：rce") 很少，CVE-2013-2028 是一个例子，由构造的 HTTP 请求触发栈缓冲区溢出。2025 年 nginx 安全通告列表记录了两个新漏洞；2026 年到 11 月 17 日为止记录了 26 个（不含 nginx2root），其中好几个是缓冲区溢出、释放后使用这类内存破坏问题。AI 辅助的研究正在更快地发现漏洞，即使是被反复研究过的 nginx 代码也一样。

## 参考

- nginx2root 项目页与演示：<https://nginx2root.com/>
- 完整分析：<https://xint.io/blog/nginx2root-remote-code-execution>
- F5 公告 K000164058（补丁状态确认）：<https://my.f5.com/manage/s/article/K000164058>
- nginx 安全通告列表：<https://nginx.org/en/security_advisories.html>
