---
title: "sqlmap 最新版系统自带 tamper 解释中文翻译"
source: https://mrxn.net/jswz/sqlmap-tamper.html
asset_dir: embedded-base64
---

# 前言

截止目前最新版本为 `1.7.10.1#dev` 版本.系统自带 tamper 共计 69个.相较笔者早期的文章 [SQLMAP tamper WAF 绕过脚本列表注释](https://mrxn.net/netsafe/492.html),变化还是较大,因此记录下,下面分别是英文和中文翻译.

# 英文

使用如下命令获取 [sqlmap](//mrxn.net/tag/sqlmap "sqlmap") 自带所有的 tamper 列表

```
python3 sqlmap.py --list-tampers
```

```
* 0eunion.py - Replaces instances of <int> UNION with <int>e0UNION
* apostrophemask.py - Replaces apostrophe character (') with its UTF-8 full width counterpart (e.g. ' -> %EF%BC%87)
* apostrophenullencode.py - Replaces apostrophe character (') with its illegal double unicode counterpart (e.g. ' -> %00%27)
* appendnullbyte.py - Appends (Access) NULL byte character (%00) at the end of payload
* base64encode.py - Base64-encodes all characters in a given payload
* between.py - Replaces greater than operator ('>') with 'NOT BETWEEN 0 AND #' and equals operator ('=') with 'BETWEEN # AND #'
* binary.py - Injects keyword binary where possible
* bluecoat.py - Replaces space character after SQL statement with a valid random blank character. Afterwards replace character '=' with operator LIKE
* chardoubleencode.py - Double URL-encodes all characters in a given payload (not processing already encoded) (e.g. SELECT -> %2553%2545%254C%2545%2543%2554)
* charencode.py - URL-encodes all characters in a given payload (not processing already encoded) (e.g. SELECT -> %53%45%4C%45%43%54)
* charunicodeencode.py - Unicode-URL-encodes all characters in a given payload (not processing already encoded) (e.g. SELECT -> %u0053%u0045%u004C%u0045%u0043%u0054)
* charunicodeescape.py - Unicode-escapes non-encoded characters in a given payload (not processing already encoded) (e.g. SELECT -> \u0053\u0045\u004C\u0045\u0043\u0054)
* commalesslimit.py - Replaces (MySQL) instances like 'LIMIT M, N' with 'LIMIT N OFFSET M' counterpart
* commalessmid.py - Replaces (MySQL) instances like 'MID(A, B, C)' with 'MID(A FROM B FOR C)' counterpart
* commentbeforeparentheses.py - Prepends (inline) comment before parentheses (e.g. ( -> /**/()
* concat2concatws.py - Replaces (MySQL) instances like 'CONCAT(A, B)' with 'CONCAT_WS(MID(CHAR(0), 0, 0), A, B)' counterpart
* decentities.py - HTML encode in decimal (using code points) all characters (e.g. ' -> &#39;)
* dunion.py - Replaces instances of <int> UNION with <int>DUNION
* equaltolike.py - Replaces all occurrences of operator equal ('=') with 'LIKE' counterpart
* equaltorlike.py - Replaces all occurrences of operator equal ('=') with 'RLIKE' counterpart
* escapequotes.py - Slash escape single and double quotes (e.g. ' -> \')
* greatest.py - Replaces greater than operator ('>') with 'GREATEST' counterpart
* halfversionedmorekeywords.py - Adds (MySQL) versioned comment before each keyword
* hex2char.py - Replaces each (MySQL) 0x<hex> encoded string with equivalent CONCAT(CHAR(),...) counterpart
* hexentities.py - HTML encode in hexadecimal (using code points) all characters (e.g. ' -> &#x31;)
* htmlencode.py - HTML encode (using code points) all non-alphanumeric characters (e.g. ' -> &#39;)
* if2case.py - Replaces instances like 'IF(A, B, C)' with 'CASE WHEN (A) THEN (B) ELSE (C) END' counterpart
* ifnull2casewhenisnull.py - Replaces instances like 'IFNULL(A, B)' with 'CASE WHEN ISNULL(A) THEN (B) ELSE (A) END' counterpart
* ifnull2ifisnull.py - Replaces instances like 'IFNULL(A, B)' with 'IF(ISNULL(A), B, A)' counterpart
* informationschemacomment.py - Add an inline comment (/**/) to the end of all occurrences of (MySQL) "information_schema" identifier
* least.py - Replaces greater than operator ('>') with 'LEAST' counterpart
* lowercase.py - Replaces each keyword character with lower case value (e.g. SELECT -> select)
* luanginx.py - LUA-Nginx WAFs Bypass (e.g. Cloudflare)
* misunion.py - Replaces instances of UNION with -.1UNION
* modsecurityversioned.py - Embraces complete query with (MySQL) versioned comment
* modsecurityzeroversioned.py - Embraces complete query with (MySQL) zero-versioned comment
* multiplespaces.py - Adds multiple spaces (' ') around SQL keywords
* ord2ascii.py - Replaces ORD() occurences with equivalent ASCII() calls
* overlongutf8.py - Converts all (non-alphanum) characters in a given payload to overlong UTF8 (not processing already encoded) (e.g. ' -> %C0%A7)
* overlongutf8more.py - Converts all characters in a given payload to overlong UTF8 (not processing already encoded) (e.g. SELECT -> %C1%93%C1%85%C1%8C%C1%85%C1%83%C1%94)
* percentage.py - Adds a percentage sign ('%') infront of each character (e.g. SELECT -> %S%E%L%E%C%T)
* plus2concat.py - Replaces plus operator ('+') with (MsSQL) function CONCAT() counterpart
* plus2fnconcat.py - Replaces plus operator ('+') with (MsSQL) ODBC function {fn CONCAT()} counterpart
* randomcase.py - Replaces each keyword character with random case value (e.g. SELECT -> SEleCt)
* randomcomments.py - Add random inline comments inside SQL keywords (e.g. SELECT -> S/**/E/**/LECT)
* schemasplit.py - Splits FROM schema identifiers (e.g. 'testdb.users') with whitespace (e.g. 'testdb 9.e.users')
* scientific.py - Abuses MySQL scientific notation
* sleep2getlock.py - Replaces instances like 'SLEEP(5)' with (e.g.) "GET_LOCK('ETgP',5)"
* sp_password.py - Appends (MsSQL) function 'sp_password' to the end of the payload for automatic obfuscation from DBMS logs
* space2comment.py - Replaces space character (' ') with comments '/**/'
* space2dash.py - Replaces space character (' ') with a dash comment ('--') followed by a random string and a new line ('\n')
* space2hash.py - Replaces (MySQL) instances of space character (' ') with a pound character ('#') followed by a random string and a new line ('\n')
* space2morecomment.py - Replaces (MySQL) instances of space character (' ') with comments '/**_**/'
* space2morehash.py - Replaces (MySQL) instances of space character (' ') with a pound character ('#') followed by a random string and a new line ('\n')
* space2mssqlblank.py - Replaces (MsSQL) instances of space character (' ') with a random blank character from a valid set of alternate characters
* space2mssqlhash.py - Replaces space character (' ') with a pound character ('#') followed by a new line ('\n')
* space2mysqlblank.py - Replaces (MySQL) instances of space character (' ') with a random blank character from a valid set of alternate characters
* space2mysqldash.py - Replaces space character (' ') with a dash comment ('--') followed by a new line ('\n')
* space2plus.py - Replaces space character (' ') with plus ('+')
* space2randomblank.py - Replaces space character (' ') with a random blank character from a valid set of alternate characters
* substring2leftright.py - Replaces PostgreSQL SUBSTRING with LEFT and RIGHT
* symboliclogical.py - Replaces AND and OR logical operators with their symbolic counterparts (&& and ||)
* unionalltounion.py - Replaces instances of UNION ALL SELECT with UNION SELECT counterpart
* unmagicquotes.py - Replaces quote character (') with a multi-byte combo %BF%27 together with generic comment at the end (to make it work)
* uppercase.py - Replaces each keyword character with upper case value (e.g. select -> SELECT)
* varnish.py - Appends a HTTP header 'X-originating-IP' to bypass Varnish Firewall
* versionedkeywords.py - Encloses each non-function keyword with (MySQL) versioned comment
* versionedmorekeywords.py - Encloses each keyword with (MySQL) versioned comment
* xforwardedfor.py - Append a fake HTTP header 'X-Forwarded-For' (and alike)
```

深入探索

网络安全培训

漏洞预警服务

安全研究报告

# 中文

```
0eunion.py - 将 <int> UNION 替换为 <int>e0UNION
apostrophemask.py - 将单引号字符（'）替换为其UTF-8全角对应字符（例如 ' -> %EF%BC%87）
apostrophenullencode.py - 将单引号字符（'）替换为其非法的双Unicode对应字符（例如 ' -> %00%27）
appendnullbyte.py - 在Payload末尾添加（Access）NULL字节字符（%00）
base64encode.py - 对给定Payload中的所有字符进行Base64编码
between.py - 将大于运算符（'>'）替换为 'NOT BETWEEN 0 AND #'，将等于运算符（'='）替换为 'BETWEEN # AND #'。
binary.py - 在可能的情况下注入关键字binary
bluecoat.py - 将SQL语句后的空格字符替换为有效的随机空白字符。然后将字符“=”替换为操作符LIKE。
chardoubleencode.py - 对给定Payload中的所有字符进行双URL编码（不处理已经编码的内容）（例如SELECT -> %2553%2545%254C%2545%2543%2554）
charencode.py - 对给定Payload中的所有字符进行URL编码（不处理已经编码的内容）（例如SELECT -> %53%45%4C%45%43%54）
charunicodeencode.py - 对给定Payload中的所有字符进行Unicode-URL编码（不处理已经编码的内容）（例如SELECT -> %u0053%u0045%u004C%u0045%u0043%u0054）
charunicodeescape.py - 在给定的负载中Unicode转义非编码字符（不处理已经编码的内容）（例如SELECT -> \u0053\u0045\u004C\u0045\u0043\u0054）
commalesslimit.py - 将（MySQL）实例如'LIMIT M，N'替换为'LIMIT N OFFSET M'对应项
commalessmid.py - 将（MySQL）实例如'MID（A，B，C）'替换为'MID（A FROM B FOR C）'对应项
commentbeforeparentheses.py - 在括号（例如（））前添加（内联）注释（例如（-> / ** /（））
concat2concatws.py - 将（MySQL）实例如'CONCAT（A，B）'替换为'CONCAT_WS（MID（CHAR（0），0，0），A，B）'对应项
decentities.py - 使用代码点将所有字符进行HTML十进制编码（例如'-> '）
dunion.py - 将<int> UNION替换为<int>DUNION
equaltolike.py - 将等于运算符（'='）的所有出现替换为LIKE对应项
equaltorlike.py - 将等于运算符（'='）的所有出现替换为RLIKE对应项
escapequotes.py - 反斜杠转义单引号和双引号（例如'->\ '）
greatest.py - 将大于运算符（'>'）替换为GREATEST对应项
halfversionedmorekeywords.py - 在每个关键字之前添加（MySQL）有版本的注释
hex2char.py - 将每个（MySQL）0x <hex>编码的字符串替换为等效的CONCAT（CHAR（），...）对应项
hexentities.py - 使用代码点将所有字符进行HTML十六进制编码（例如'-> 1）
htmlencode.py - 使用代码点将所有非字母数字字符进行HTML编码（例如'-> '）
if2case.py - 将实例如'IF（A，B，C）'替换为'CASE WHEN（A）THEN（B）ELSE（C）END'对应项
ifnull2casewhenisnull.py - 将实例如'IFNULL（A，B）'替换为'CASE WHEN ISNULL（A）THEN（B）ELSE（A）END'对应项
ifnull2ifisnull.py - 将实例如'IFNULL（A，B）'替换为'IF（ISNULL（A），B，A）'对应项
informationschemacomment.py - 在（MySQL）“information_schema”标识符的所有出现之后添加内联注释（/ ** /）
least.py - 将大于运算符（'>'）替换为LEAST对应项
lowercase.py - 将每个关键字字符替换为小写值（例如SELECT-> select）
luanginx.py - LUA-Nginx WAFs绕过（例如Cloudflare）
misunion.py - 将UNION实例替换为-.1UNION
modsecurityversioned.py - 使用（MySQL）有版本的注释括起来完整的查询
modsecurityzeroversioned.py - 使用（MySQL）零版本的注释括起来完整的查询
multiplespaces.py - 在SQL关键字周围添加多个空格（' '）
ord2ascii.py - 将ORD（）出现替换为等效的ASCII（）调用
overlongutf8.py - 将给定负载中的所有（非字母数字）字符转换为过长的UTF8（不处理已经编码的内容）（例如'->%C0%A7）
overlongutf8more.py - 将给定负载中的所有字符转换为过长的UTF8（不处理已经编码的内容）（例如SELECT->%C1%93%C1%85%C1%8C%C1%85%C1%83%C1%94）
percentage.py - 在每个字符（例如SELECT->%S%E%L%E%C%T）前面添加一个百分比符号（'％'）
plus2concat.py - 将加号运算符（'+'）替换为（MsSQL）函数CONCAT（）对应项
plus2fnconcat.py - 将加号运算符（'+'）替换为（MsSQL）ODBC函数{fn CONCAT（）}对应项
randomcase.py - 将每个关键字字符替换为随机情况值（例如SELECT->SEleCt）
randomcomments.py - 在SQL关键字中添加随机内联注释（例如SELECT->S / ** / E / ** / LECT）
schemasplit.py - 将FROM模式标识符（例如'testdb.users'）与空格（例如'testdb 9.e.users'）拆分
scientific.py - 滥用MySQL的科学计数法
sleep2getlock.py - 将实例如'SLEEP（5）'替换为“GET_LOCK（'ETgP'，5）”之类的内容
sp_password.py - 将（MsSQL）函数'sp_password'附加到有效负载的末尾，以自动混淆来自DBMS日志的内容
space2comment.py - 将空格字符（' '）替换为注释'/ ** /'
space2dash.py - 将空格字符（' '）替换为破折号注释（'--'）后跟随一个随机字符串和一个新行（'\n'）
space2hash.py - 将（MySQL）空格字符（' '）的实例替换为井字符（'#'），后跟随一个随机字符串和一个新行（'\n'）
space2morecomment.py - 将（MySQL）空格字符（' '）的实例替换为注释'/ _ /'
space2morehash.py - 将（MySQL）空格字符（' '）的实例替换为井字符（'#'），后跟随一个随机字符串和一个新行（'\n'）
space2mssqlblank.py - 将（MsSQL）空格字符（' '）的实例替换为来自有效备选字符集的随机空白字符
space2mssqlhash.py - 将空格字符（' '）替换为井字符（'#'），后跟随一个新行（'\n'）
space2mysqlblank.py - 将（MySQL）空格字符（' '）的实例替换为来自有效备选字符集的随机空白字符
space2mysqldash.py - 将空格字符（' '）替换为破折号注释（'--'）后跟随一个新行（'\n'）
space2plus.py - 将空格字符（' '）替换为加号（'+'）
space2randomblank.py - 将空格字符（' '）替换为来自有效备选字符集的随机空白字符
substring2leftright.py - 将PostgreSQL SUBSTRING替换为LEFT和RIGHT
symboliclogical.py - 将AND和OR逻辑运算符替换为其符号对应项（&&和||）
unionalltounion.py - 将UNION ALL SELECT实例替换为UNION SELECT对应项
unmagicquotes.py - 将引号字符（'）替换为多字节组合%BF%27，同时在末尾添加通用注释（使其起作用）
uppercase.py - 将每个关键字字符替换为大写值（例如select->SELECT）
varnish.py - 添加HTTP头'X-originating-IP'以绕过Varnish防火墙
versionedkeywords.py - 使用（MySQL）有版本的注释括起来每个非函数关键字
versionedmorekeywords.py - 使用（MySQL）有版本的注释括起来每个关键字
xforwardedfor.py - 添加假HTTP头'X-Forwarded-For'（等等）
```

# 后记

小 Tips : 在对 mssql 数据时,不要使用 randomcomments !  
有时候合理组合使用这些 tamper 可以大大提高我们发现 [SQL 注入](//mrxn.net/tag/sql注入 "SQL 注入")的机率.本文为笔记系列.  
如有不妥之处或不错的 tamper ,欢迎指出交流.
