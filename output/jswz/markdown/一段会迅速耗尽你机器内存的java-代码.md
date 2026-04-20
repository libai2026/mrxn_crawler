---
title: "一段会迅速耗尽你机器内存的Java 代码"
source: https://mrxn.net/jswz/java-OutOfMemoryError-code-to-dos.html
asset_dir: embedded-base64
---

# 前言

这个是在对某个jar包进行[代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1 "标签：代码审计")时，发现的，当时还比较懵逼为啥断不下来，IDEA老是崩。后来才发现是这个[代码](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81 "标签：代码")有问题！

计算机内存

# 正文

直接上[代码](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81 "标签：代码")，看下是何方神圣写的如此牛逼的代码

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

深入探索

脚本语言

计算机科学

计算机安全

代码一运行就会报错

软件实用程序

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

深入探索

开放源代码

编程

软件

非常醒目的 `OutOfMemoryError` ！！直接[内存](#)耗尽！

计算机内存

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

Java（编程语言）

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

计算机内存
