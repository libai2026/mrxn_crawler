---
title: "一段会迅速耗尽你机器内存的Java 代码"
source: https://mrxn.net/jswz/java-OutOfMemoryError-code-to-dos.html
asset_dir: assets/一段会迅速耗尽你机器内存的java-代码
---

# 一段会迅速耗尽你机器内存的Java 代码

[Mrxn](https://mrxn.net/author/1)- 发表于2025/3/17 18:35
- 540浏览
- [0评论](#comment)
- 36分钟阅读

深入探索

Web安全书籍

安全

网络安全会议

---

# 前言

这个是在对某个jar包进行代码审计时，发现的，当时还比较懵逼为啥断不下来，IDEA老是崩。后来才发现是这个代码有问题！

# 正文

直接上代码，看下是何方神圣写的如此牛逼的代码

```
public class Main {
    private static final String i(String paramString) {
    int i;
    if ((i = paramString.length()) % 2 != 0)
      return "-1"; 
    String str = "";
    for (byte b = 0; b < i / 2; b++)
      str = str + str; 
    return str;
  }
    private static final String j(String paramString) {
    if (paramString == null)
      return null; 
    int i;
    if ((i = (paramString = paramString.toLowerCase()).length()) == 0)
      return ""; 
    String str1 = "";
    String str2 = "";
    if ((paramString = paramString).length() % 3 != 0)
      return "-1"; 
    byte b;
    for (b = 0; b < paramString.length() / 3; b++) {
      if (b % 3 == 0) {
        str1 = str1 + str1;
      } else if (b % 3 == 1) {
        str1 = str1 + str1 + paramString.substring(b * 3, b * 3 + 1);
      } else {
        str1 = str1 + str1;
      } 
    } 
    for (b = 0; b < str1.length() / 2; b++)
      str2 = str2 + str2; 
    return str2 = i(str2);
  }
    public static void main(String[] args) {
        System.out.println(j("30024f00127307062050067900306e0002f060062900256605063690061f00366e03066140066900476706020270021d004261"));
    }
}
```

代码一运行就会报错

```
Exception in thread "main" ERROR!
java.lang.OutOfMemoryError: Java heap space
    at java.base/jdk.internal.misc.Unsafe.allocateUninitializedArray0(Unsafe.java:1387)
    at java.base/jdk.internal.misc.Unsafe.allocateUninitializedArray(Unsafe.java:1380)
    at java.base/java.lang.StringConcatHelper.newArray(StringConcatHelper.java:511)
    at java.base/java.lang.invoke.DirectMethodHandle$Holder.invokeStatic(DirectMethodHandle$Holder)
    at java.base/java.lang.invoke.LambdaForm$MH/0x00007e596c149000.invoke(LambdaForm$MH)
    at java.base/java.lang.invoke.Invokers$Holder.linkToTargetMethod(Invokers$Holder)
    at Main.j(Main.java:29)
    at Main.main(Main.java:39)
    at java.base/java.lang.invoke.LambdaForm$DMH/0x00007e596c030c00.invokeStatic(LambdaForm$DMH)
    at java.base/java.lang.invoke.LambdaForm$MH/0x00007e596c144800.invoke(LambdaForm$MH)
    at java.base/java.lang.invoke.Invokers$Holder.invokeExact_MT(Invokers$Holder)
    at java.base/jdk.internal.reflect.DirectMethodHandleAccessor.invokeImpl(DirectMethodHandleAccessor.java:154)
```

非常醒目的 `OutOfMemoryError` ！！直接内存耗尽！

代码浅析

> 根本原因是代码中涉及到的字符串操作逻辑会导致字符串长度呈指数级增长，从而耗尽了 JVM 的堆内存（Heap Space），最终抛出 OutOfMemoryError。

在方法 j 中，str1 的增长逻辑如下：

```
for (b = 0; b < paramString.length() / 3; b++) {
    if (b % 3 == 0) {
        str1 = str1 + str1;
    } else if (b % 3 == 1) {
        str1 = str1 + str1 + paramString.substring(b * 3, b * 3 + 1);
    } else {
        str1 = str1 + str1;
    }
}
```

- 每次循环，str1 的长度会翻倍，甚至在某些情况下还会额外增加一个字符。
- 假设 paramString.length() = 102，那么循环次数为 34 次。
- 在第 0 次循环后，str1 的长度为 0。
- 在第 1 次循环后，str1 的长度为 1。
- 在第 2 次循环后，str1 的长度为 2。
- 在第 3 次循环后，str1 的长度为 4。
- 在第 4 次循环后，str1 的长度为 8。
- ...
- 在第 34 次循环后，str1 的长度会达到一个天文数字。  
  这种指数级增长会迅速耗尽内存，导致 OutOfMemoryError。

在方法 j 中，str2 的增长逻辑如下：

```
for (b = 0; b < str1.length() / 2; b++) {
    str2 = str2 + str2;
}
```

- 假设 str1 的长度已经非常大（例如，超过 1GB），那么 str2 的长度会增长得更快。
- 由于 str2 的增长也是指数级的，内存会被迅速耗尽。

方法 i 的逻辑如下：

```
private static final String i(String paramString) {
    int i;
    if ((i = paramString.length()) % 2 != 0)
        return "-1"; 
    String str = "";
    for (byte b = 0; b < i / 2; b++)
        str = str + str; 
    return str;
}
```

- 如果 str2 的长度已经非常大，传递给方法 i 后，str 的增长会进一步加剧。
- 这会导致更快的内存耗尽。

好了，代码浅析完毕，写这篇文章的目的并不是来分析它，而是通过这个代码，我想到了用它在免杀方面的作用，如果某些EDR或者AV对代码进行分析时，如果走入这个逻辑中，是不是有可能也直接崩溃？这个代码也算是[漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E "漏洞")的一种？逻辑DOS？

- 标签：
- [#代码](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81)
- [#漏洞](https://mrxn.net/tag/%E6%BC%8F%E6%B4%9E)
- [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
- [#Java](https://mrxn.net/tag/Java)

---

文章目录

- [1.前言](#toc-1-)
- [2.正文](#toc-2-)

  
  

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAALcElEQVR4Aezci3LjuA4E0Jz9/3/eGxjTEkU94s3Nw1WjVJAGGg2QIcSN7anaf97e3v79rP07fY19ptTlGtGO9bMfTTD5xIXhZqzcbLMm8ayr+CwXvrB0ZeX/P1YDea+/v1/lBJaBvE/37Vk72/xY/4wmerxhKQk/Ih4aGpNbit6dcDO+px7fdC2W3/WR+OBH+kVG9wlfmFywuGctNYXLQCq47fdPYDcQevrs8aPtsq+huTwtRz2SC35Wkzp6zcRXmDWDV9rP5Oi9sMejfruBHIlu7udO4EsHkqdsxPwq7J8Qtly0QdZ8uBl5XjPWstax+qPmI5/P1V31/dKBXC105547gS8ZCP2kjEuy58Z8+blJ5X9kdD+2ONbRuXB0fLVOckG6hnNM/+/ALxnId2zsb+35PQP5W0/zC37v3UBydY/wbL1oWa95uGBqExfS+vLL6JjG4mKpD4Y/wlmT+AjptWgcNUe9z7ixbvTP9MWPuvi7gSRx4++cwDIQ+gnhY5y3StfU1GM0N2ufiecenH/UQa+D09Z4fOySvoURl182x8XRdclxHCOSBfFYk49xKXp3loG8+/f3C5zAP/UkfNbm/bM+DcnRXNYIXzhzc1yaGN0ncTA1heH+C9J9q76MjllvJc3NfUsfSy7xZ/G+ITnJF8HdQOingcajfdI5Go804fKkJB6RrmeLo+bMZ1vDGs812QN7zZxLXHjWJzxrP7b+kSbcFe4GciW+c99/AstA6AnXk1GWpWmeFSs/WrQjFz851nrajyY4a8MfYbRjbuYSc7xe1dK5WYtQO8TjFdSYqF6jjbn4bOvomBWXgaTohfGv2No9kBcb8z/0dcl1u9pfNHTNrKV5zKklTo9CbK5+cWWL+MCha0pXRsc4UG8pPNZjxepRtlVuo8qX0XXll21Vx1HpZjtWNnvfkD6Hl/m5vDGkp5+dzVOtmNaUX8Y2Li5G5+Z+NM/Hb7xSW0jXlV/GNi4ua5c/WvgjpPtc5WjN2LP8sYathm1cerbcWB//viF1Ui9kpwOhp8mK2TfNJQ7SPEKd/je7nohF9MfBQ/8n3EDpj2wUcV4/6sqntelJx6yYXLDqRmOvTf6oZubo+tQUng6kkrf9/AmcvsqapzluLbngmIs/5xLTTwUrJpfaI6T1ydFxakekc5xj+gRTn3hEus+sSVxIa3geq65sXOu+IeNpvIB/D+QFhjBuYRkIfdWSZBsXX9erjG2OjisXK/2RJT/ikW7mome71qijc+FSM8fhC5Oja4uL0Vw0M9J51pfwsya9jpCuH2uWgYzk7f/eCSwDyQTZT23e3qxNPOrY9mEbH2mP+kTHeX00qQ+GD9I9EOrxMpvzJ7yE6YdFj0othkcuxFkNrUOkG1wGsmHv4NdOYDeQTDZ4tDNsnoZoaJ7rJ27WJw5mbdZ+yV0hrY+GjtMv/BHSWlaMjubSJ5j8iMlxXFP56Msvo7V42w3k7f761RM4/XDxalc11bJo6AknLmTPjTznt4h9ba1XVj3KONfQudKXsY2Lqx7/1eg+NFaf2eaetJYVo6G5xIX3DalTeCE7HQg9vfEJoDka83tEk/g7kF4zawXHtWjNyJV/pC2+bM4lLqz8fzV6D1X/kaX3qDsdSMQ3fuoEPl10D+TTR/c9hcunvXP7XCP6CmKRJBdcEk84qSmc5di8nC5N7ExL12CWPHrhECOm81mHjjl/0ZHaEem6kSuf5lHhxrLmSN43ZDyNF/B3A8HjibraG61hi5l4YerLL0vMtoaveRLTf8Rat2zk4tP7SBwsfSxcMHyQ7oFIFsTpObLN0THuN4ZvL/a1vDHM1IP01Mb9JjfjqIkfDd0ncfKFM5c4SNei5BuL5gg3wvfgSpMcdk80zUXz3urxTfOP4M+PaGb8k34AXRfNg5x+7P6TNeXv8IdPYHmVRU/vmfV5Xpunga5JXJi16NwclyaW3Ix0LebUZTz3neOjYuxu0azjXDOvwV5735D5RH85vgfyywOYl9/9UY+grldZ4hGLLxu5M5/ttaRjVpxrq3fZzB/FpYvNedY1uPZTy6pLX5pLHEzNiFc5us+oLz81hfcNqRN5IVsGQk+PxqM90jm2eKWtqZdFU34sXJBtX9Y4miBrjq0fzYxZtzC58svoHuELaa7yZcWdGa1li6O+epTRmuToGPcbw7cX+1puSE1utKt9jrrRZ510+Gf6RJOaYPjCcMHiziyaGUd9cvSeEx8hrRnryz/SFl92lKP7HOXCLQOpJrf9/gns3hjSU6QxkyvMdukcjeGvsOrLRg3bejqm8UjLPhdd9S9LTGtpDH+E7DU0Vz3LUkfzrJhc6coSs2qKL2PlEOkD7xvyOIbX+bEbSE1wNDw+LsCy6zFfPh6aRfDu0ByN79Tuu2rLkih/tPBHOOris10rfPCoT7hnNJz3T58Z07eQbX20NI/7Vdbbi33tbsj37+9e4eoETj86oa9RXbXZ6ByNRwvMNUeacNEmZt83muCsRagF8fhPKY1L4t1hy7GN3yXLN+e5RfTHobXscd77n5Ll/0Nf+fuG5FReBJeBsJ1oTauMLc/+38BLV/ZVv1P1mu2Z3qmh95yamWf/O0Q7YupGrvwjnu2apZuN1hzVR7sMJMSNv3sCpwNhO82aarbKNhf+CGkt55g6tprwR0hra1+x6OZ45isfbka6L+bUEmPzt4n1xlXvsojLn42uj2bE04GMotv/uRNYBpIpZunE9DTZPwWsOaT0gXg8RY/g/Uf6vbu7bz7WstXsmgwEH2tpTfZ1hGmZ3Fkc/lmc+9F7wf3G8O3FvpYb8mL7+mu3s/u0NydBX6Ncr0KaozHaK6y6siNN8aNFw75/dNHMcfF0XXJBmi9NLLnE7DXJBeea8CPycR/ONfcNGU/zBfzlo5N5L3ka6Gmy/6MeTWoTj5hc8ChHrxHNEbLV0DErpjfNpc/MI6nHCw/W3w0LFxHNJQ6mb2G4YHFliQvZ9ql8WeVi9w3JSbwILgOpSY12tT+2k46W5lkxuSvMurOGtc+sSTwirQ9HxzTO/ceYc83cb6yLz7aejlkx2qt+y0AivvF3T2AZCOskWf2j7c0TTnyER/UzR68382NMa2hMjo4RavkbMO9nEbw7eOje3dNvWkNjhHTMisnNOO5hzh3Fy0COkjf38yewvA8ZJ1n+1VboJyMatnHxbDk6ZsXSldV6ZeWfWeXLkqf7JD5CWkNj1c92VBdu1s5xdFdIr41T2dj3viGnx/Q7iXsgl+f+88kP3xiO1ynbG7nyw+PxhxKhlrh0s0WEh27Oj3G0wTE3+7MmMb0OQm3+Pbv6LInBwWN/A7Vzq/bIRmHy4ea4+PuG1Cm8kC1/1OmngOfx6vc4mn7p2fePls6VroyOWbH40TjPRZf+IyY346ihe4eLluYTj8jzOfba+4aMp/kC/jKQPAXP4Lzvo5pokpvj4sPNSD85pYnNmsTJF4YL0n1oDH+EtIYVj3QfcbWPsisdvUbpyugY978Yvr3Y13JDsi/WabH1o3kGeb6W1l71rSepLBq6hj1GU/rRWLXR0Fx04a/wSEv3YYtjn7mO1oYv3A1kbHD7P38C90B+/swvV/ySgdBXb1yprl/ZyJVPa1n/la50R1b6GF13pAsXbWK6JvwRztrEI9J92OJVv7E+Pl2fupnH/Uf97cW+vuSGPPM7sX06qobmaCxuNJrHSG98PD7WYL1xG8FJwFqHRYWlH+0vySccPq7JzUi7xIU/NpAsfuP1CewGUlM6s7NW0dNPBysmFxx7hAuOufLDj0j3rnzZmKt4tOTCJS4MN2PlYnPuKj6roffL+Q1m1ewGcrXonfv+E1gGwjolrv2zbeUpGZHudVbzX/n0fqaOXps9ps+MrNo5lzXDJ34WWXtjKUu/wmUgS/Z2fvUE7oH86vHvF/8fAAAA///wX83QAAAABklEQVQDAKZUxoDFz1gzAAAAAElFTkSuQmCC)

手机扫码阅读
