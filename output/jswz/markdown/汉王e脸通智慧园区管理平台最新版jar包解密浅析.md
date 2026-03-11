---
title: "汉王e脸通智慧园区管理平台最新版jar包解密浅析"
source: https://mrxn.net/jswz/efacego-dencrypt-jar.html
asset_dir: assets/汉王e脸通智慧园区管理平台最新版jar包解密浅析
---

# 汉王e脸通智慧园区管理平台最新版jar包解密浅析

[Mrxn](https://mrxn.net/author/1)* 发表于2025/9/27 08:46
* 1171浏览
* [4评论](#comment)
* 2小时阅读

深入探索

恶意软件分析工具

漏洞扫描服务

网络安全培训


(adsbygoogle = window.adsbygoogle || []).push({});

---

# 简介

目前最新版本为 V2.1.0.3 版本的 iface.server-1.0.jar 和 iface.common-1.0.jar 这两个核心jar包已经是加密过的了(其实从v2.0.1.2就加密了，本文也是在v2.0.1.2就已经完成分析)，想要代码审计就必须获取解密后的jar包或者解密后的class文件，众所周知，Java代码最终都是运行在jvm里，且在jvm里是明文的，最简单获取代码就是直接dump jvm 里与 iface 相关的class文件即可。对于没有加密版本之前的相关漏洞汇总：[e脸通智慧园区管理平台漏洞汇总](https://mrxn.net/?keyword=%E6%B1%89%E7%8E%8B)

漏洞预警服务

# 正文

默认使用反编译工具如IDEA、JD-GUI 等显示 `// INTERNAL ERROR //` 表明，jar包不是常规class文件打包

[![汉王e脸通智慧园区管理平台最新版jar包解密浅析](images/img-001-6fb2bbbddf4a.webp)](https://image.mrxn.net/ce71b9e650244f3eb06fc1a9877b4a56.webp)

使用 hexdump 查看加密的jar包 class 文件如下

深入探索

SQL注入防护

网络安全课程

SQL注入检测工具

[![汉王e脸通智慧园区管理平台最新版jar包解密浅析](images/img-002-17e087dbddd0.webp)](https://image.mrxn.net/d580554b3b864da58effc3aeb6bac9f9.webp)

```
➜  iface.common-1.0 file AppConst.class 
AppConst.class: RAR archive data
➜  iface.common-1.0 hexdump -C AppConst.class
00000000  52 61 72 21 1a 07 00 cf  90 73 00 00 0d 00 00 00  |Rar!.....s......|
00000010  aa bb cc dd ee ff c3 d3  4e 3f be d5 7e bc 5b ac  |........N?..~.[.|
00000020  4c c6 b7 99 f2 70 f0 2b  0c d3 38 f8 d2 a7 3f e5  |L....p.+..8...?.|
00000030  42 1b 74 2d 4a 5c 02 60  f5 78 62 92 ee fa 00 00  |B.t-J\.`.xb.....|
00000040  02 dc 00 00 02 e0 6c 07  51 e2 09 cc 3d df 60 46  |......l.Q...=.`F|
00000050  35 81 c9 2c d1 32 15 f8  68 f0 2e ac 93 65 5c c2  |5..,.2..h....e\.|
00000060  14 72 e0 90 cd 0c fe 95  d4 49 6a eb 3d 38 24 76  |.r.......Ij.=8$v|
00000070  34 82 93 6d 51 2f 95 03  52 e0 68 9b 13 00 57 9e  |4..mQ/..R.h...W.|
00000080  24 aa 04 d9 e0 f3 3d 4a  ba 57 59 d9 e5 37 7f dc  |$.....=J.WY..7..|
00000090  85 45 0e ef c5 7f 9d 69  f0 b0 4b 73 fe 9c aa ae  |.E.....i..Ks....|
000000a0  96 49 19 4f 5c 82 3b 63  a2 12 97 99 68 08 22 f9  |.I.O\.;c....h.".|
000000b0  03 ab a2 e2 1e 79 25 c0  5b 3f df 92 d0 20 63 db  |.....y%.[?... c.|
000000c0  f2 09 85 e4 25 16 eb 5a  98 f8 49 d1 aa 66 e2 33  |....%..Z..I..f.3|
```

深入探索

网页浏览器

安全研究工具

安全研究报告

file 命令识别到的 AppConst.class 表示是rar压缩文件，且通过hexdump 得到的 6152 2172 即 rar! 字节码文件幻数 `52 61 72 21 1a 07 00` （RAR 版本 1.5 到 4.x 的字节码文件幻数（RAR 4 及之前版本）），RAR 版本 5.x 的字节码文件幻数是 `52 61 72 21 1A 07 01 00` 比旧版本多了一个字节（第7字节变成了0x01）。

但是此文件实际不是rar文件！不能解压的，我比较懒，不喜欢去分析如何加载如何解密后在jvm运行的，直接dump！一步到位！

# dump class

dump jvm的calss文件，对于老鸟来说很简单，有很多工具如

* jcmd：JDK 自带的命令行工具，功能丰富
* jmap：可以dump堆快照，间接分析 class 信息（通过工具（如 Eclipse MAT）分析堆快照，找到 class 对象并导出。）
* BTrace：动态追踪工具，可以在运行时hook类加载器，dump加载的class字节码，自定义脚本，拦截类加载过程，写出对应的字节码文件
* Bytecode Outline（IDE 插件）：直接查看并导出 class 文件，但需要加载 class 文件或者 jar，不是动态 dump
* 使用JVMTI agent（自定义native agent）：编写 JVMTI (Java Virtual Machine Tool Interface) agent，hook类加载事件，保存字节码，比较复杂但灵活，适合深入调试
* VisualVM + Profiler 插件：VisualVM 自带一些内存和类分析插件，有些插件支持保存加载的class字节码
* Byteman：用于动态插桩，也可以dump类字节码
* Java Instrumentation API：用 Java agent 方式，在类加载时拦截并保存字节码
* 使用 `arthas` 等 attach 工具

我这里直接使用 Java agent 直接 hook ！

dump 指定 className 为 `com/hanvon/iface` 的jvm calss，代码如下

```
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.lang.instrument.ClassFileTransformer;
import java.lang.instrument.Instrumentation;
import java.security.ProtectionDomain;

public class DumpAgent {
    public static void premain(String agentArgs, Instrumentation inst) {
        System.out.println("[*] DumpAgent started...");
        inst.addTransformer(new ClassFileTransformer() {
            @Override
            public byte[] transform(ClassLoader loader,
                                    String className,
                                    Class<?> classBeingRedefined,
                                    ProtectionDomain protectionDomain,
                                    byte[] classfileBuffer) {
                if (className != null && classfileBuffer != null) {
                    try {
                        // 避免 dump JVM 内部或代理类（如 sun/, java/, javax/, etc）
                        if (className.startsWith("com/hanvon/iface")) {
                            String filePath = "C:\\\\temp\\\\dump_classes\\\\" + className + ".class";
                            File f = new File(filePath);
                            f.getParentFile().mkdirs();
                            try (FileOutputStream fos = new FileOutputStream(f)) {
                                fos.write(classfileBuffer);
                                System.out.println("[+] Dumped: " + className);
                            }
                        }
                    } catch (Throwable t) {
                        System.err.println("[-] Error dumping class: " + className);
                        t.printStackTrace();
                    }
                }
                return classfileBuffer;
            }
        });
    }
}
Manifest-Version: 1.0
Premain-Class: DumpAgent
Can-Redefine-Classes: true
Can-Retransform-Classes: true
```

使用如下命令编译成jar文件

> 因为 `EFaceGo` 的Java运行版本是1.8版本
>
> 所以你的java -version 以及 javac -version 命令的结果需要是1.8版本，不然加载会报错

```
javac -source 1.8 -target 1.8 DumpAgent.java && jar cfm dumpagent.jar META-INF/MANIFEST.MF *.class
```

编译后目录结构如下

```
├── DumpAgent$1.class
├── DumpAgent.class
├── DumpAgent.java
├── META-INF
│   └── MANIFEST.MF
└── dumpagent.jar

2 directories, 5 files
```

然后将 dumpagent.jar 复制到`EFaceGo`的安装目录 `C:\EFaceGo\Tomcat8\webapps\manage\WEB-INF\lib` ，根据你的安装目录修改路径。

# 设置jvm参数

打开 `C:\EFaceGo\Tomcat8\bin\tomcat8w.exe` ，找到 【Java】 选项卡

在 【Java Options】 部分添加如下内容

```
-javaagent:C:\EFaceGo\Tomcat8\webapps\manage\WEB-INF\lib\dumpagent.jar
-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5005
```

[![汉王e脸通智慧园区管理平台最新版jar包解密浅析](images/img-003-7775b3eac152.webp)](https://image.mrxn.net/99696296ca7440c9a324cdc9947fa888.webp)

如果dump出的class还是加密的，尝试切换位置，放置在最后

[![汉王e脸通智慧园区管理平台最新版jar包解密浅析](images/img-004-700e6411df09.webp)](https://image.mrxn.net/387fe1e61fdc4f0fa9d841714cf84a7a.webp)

然后点击 【应用】

然后在服务里重启 `Apache Tomcat 8.5 Tomcat8` 服务

[![汉王e脸通智慧园区管理平台最新版jar包解密浅析](images/img-005-edee5403c8e4.webp)](https://image.mrxn.net/3e9611ee55634ab4aef9b52412daa08b.webp)

或者你在命令行里使用 `net stop tomcat8 && net start tomcat8` 命令进行重启。

注意观察 `C:\EFaceGo\Tomcat8\logs` 下面的 `tomcat8-stdout.2025-xx-xx.log` 日志，出现如下内容

```
2025-xx-xx xx:xx:xx Apache Commons Daemon procrun stdout initialized.
[*] DumpAgent started...
Listening for transport dt_socket at address: 5005
[+] Dumped: com/hanvon/iface/web/listener/WebAppEventListener
[+] Dumped: com/hanvon/iface/web/filter/HttpServletRequestReplacedFilter
[+] Dumped: com/hanvon/iface/utils/TheApp
[+] Dumped: com/hanvon/iface/utils/RecordProcessor
[+] Dumped: com/hanvon/iface/utils/Utils
[+] Dumped: com/hanvon/iface/types/HistoryTableInfo
[+] Dumped: com/hanvon/iface/web/controller/utils/operationLog/OperationLog
[+] Dumped: com/hanvon/iface/utils/Encrypter
[+] Dumped: com/hanvon/iface/utils/SM4Utils
[+] Dumped: com/hanvon/iface/utils/StrUtil
```

就代表 agent hook成功，进入 `C:\TEMP\dump_classes` 目录查看dump 的class文件即可

[![汉王e脸通智慧园区管理平台最新版jar包解密浅析](images/img-006-4fdd37b7f34d.webp)](https://image.mrxn.net/a8895c3e6a014c628e75a98c7e2af9d5.webp)

压缩后将其解压到 `EFaceGo` 的 manage class目录下即可开始审计啦！

注：采用这种方式可能dump不全！建议加载agent后等两分钟等全部加载了，刷新页面后再去保存calss文件。

后面有空了再讲讲如何解密这种jar文件。

加上 `-verbose:class` 启动参数，在日志文件 tomcat8-stdout.2025-xx-xx.log 看哪些类是由哪个路径加载

```
[Opened C:\EFaceGo\Java\jre1.8.0_181\lib\rt.jar]
[Loaded java.lang.Object from C:\EFaceGo\Java\jre1.8.0_181\lib\rt.jar]
[Loaded java.io.Serializable from C:\EFaceGo\Java\jre1.8.0_181\lib\rt.jar]
[Loaded java.lang.Comparable from C:\EFaceGo\Java\jre1.8.0_181\lib\rt.jar]
[Loaded java.lang.CharSequence from C:\EFaceGo\Java\jre1.8.0_181\lib\rt.jar]
[Loaded java.lang.String from C:\EFaceGo\Java\jre1.8.0_181\lib\rt.jar]
[Loaded java.lang.reflect.AnnotatedElement from C:\EFaceGo\Java\jre1.8.0_181\lib\rt.jar]
[Loaded java.lang.reflect.GenericDeclaration from C:\EFaceGo\Java\jre1.8.0_181\lib\rt.jar]
[Loaded java.lang.reflect.Type from C:\EFaceGo\Java\jre1.8.0_181\lib\rt.jar]
[Loaded java.lang.Class from C:\EFaceGo\Java\jre1.8.0_181\lib\rt.jar]
[Loaded java.lang.Cloneable from C:\EFaceGo\Java\jre1.8.0_181\lib\rt.jar]
[Loaded java.lang.ClassLoader from C:\EFaceGo\Java\jre1.8.0_181\lib\rt.jar]
[Loaded java.lang.System from C:\EFaceGo\Java\jre1.8.0_181\lib\rt.jar]
[Loaded java.lang.Throwable from C:\EFaceGo\Java\jre1.8.0_181\lib\rt.jar]
[Loaded java.lang.Error from C:\EFaceGo\Java\jre1.8.0_181\lib\rt.jar]
[Loaded java.lang.ThreadDeath from C:\EFaceGo\Java\jre1.8.0_181\lib\rt.jar]
......
```

上述 dump 下面的class 文件还是加密的(加载顺序有关,调整后正常dumpclass文件，或者是因为在web页面尝试了导入授权，激活了解密class，之前只是刷新，没有触发加载这些类即没有解密,或者多等待一段时间后，写入解密后的class，反正会覆写),放在最后，特别是放在 **-agentpath 后面**

[![汉王e脸通智慧园区管理平台最新版jar包解密浅析](images/img-007-54152a1996e9.webp)](https://image.mrxn.net/7670167200cd487399ee6c96594f8aba.webp)

还在jvm参数里发现了

`-agentpath:C:\EFaceGo\Tomcat8\bin\libhwcheck.dll`

是一个 native agent，可能被用来控制或加密/解密 JVM 类的加载过程。

二者区别如下

| 项目 | -javaagent | -agentpath |
| --- | --- | --- |
| 类型 | Java 语言写的 agent（.jar） | Native C/C++ 写的 JVMTI agent（.dll / .so） |
| 接口 | 使用 java.lang.instrument.Instrumentation | 使用 JVMTI（Java Virtual Machine Tool Interface） |
| 常见文件类型 | .jar | .dll, .so, .dylib |
| 启动调用 | premain(String args, Instrumentation inst)（或 agentmain） | Agent\_OnLoad(JavaVM *vm, char* options, void \*reserved) |
| 功能能力 | 插桩类、方法字节码修改 | JVM 更底层能力：类加载 hook、线程监控、加解密控制、反调试等 |
| 加载时机 | 启动时、attach 后 | 通常只能启动时加载（attach 支持但更复杂） |

[![汉王e脸通智慧园区管理平台最新版jar包解密浅析](images/img-008-ce3fb4bf2461.webp)](https://image.mrxn.net/fec7f17009a34d868c3545edc33e022d.webp)

但是 `libhwcheck.dll` 大概率是**硬件加密狗检测或硬件绑定校验**的Agent，并非class加解密

[![汉王e脸通智慧园区管理平台最新版jar包解密浅析](images/img-009-840bf5c19175.webp)](https://image.mrxn.net/07b2a8235bc54cea9a3e297af791c743.webp)

通过进入后台，各个功能点点 dump 的class更完整（不点也没事，大部分主要class都还是能dump下来的

[![汉王e脸通智慧园区管理平台最新版jar包解密浅析](images/img-010-2c47342ce113.webp)](https://image.mrxn.net/3a1c082c50224fa2882a79bc5927dd23.webp)

# 编写解密工具

通过翻找观察tomcat目录文件时间戳变化，发现tomcat的lib目录下的一个jar包 `tomcat-coyote.jar` 时间明显和其他不一样：

[![汉王e脸通智慧园区管理平台最新版jar包解密浅析](images/img-011-84f35bb21773.webp)](https://image.mrxn.net/180200af12624e579fdb1bf1156c86dc.webp)

其他jar包都是 2023年11月10号的，唯独它是2024年3月6号的，多半有猫腻！

直接下载一个官方版本的 `tomcat-coyote.jar` 和其进行对比

tomcat版本信息在启动时会打印在控制台，也会写入 logs/catalina.日期.log 里

[![汉王e脸通智慧园区管理平台最新版jar包解密浅析](images/img-012-39a16a802f99.webp)](https://image.mrxn.net/adf2f7bd247b473f8a30deb7db70ff5b.webp)

直接去 <https://mvnrepository.com/artifact/org.apache.tomcat/tomcat-coyote/8.5.96> 下载一个 `tomcat-coyote-8.5.96.jar` 文件，对比如下

[![汉王e脸通智慧园区管理平台最新版jar包解密浅析](images/img-013-ad8fe0cded46.webp)](https://image.mrxn.net/4720623f8dc94bc28a3b70b035ee9119.webp)

两个jar包就一处不一样 `org/apache/tomcat/util/bcel/classfile/ClassParser.class`

这个 `ClassParser.class` 文件是 Tomcat 中用于**解析** **`.class`** **字节码文件结构**的类，属于 BCEL（Byte Code Engineering Library）的一部分，主要用于读取和分析 Java 字节码。

然后将这两个jar里的这个 `ClassParser.class` 直接用解压软件提取出来，尝试查看这个不同的class

[![汉王e脸通智慧园区管理平台最新版jar包解密浅析](images/img-014-5f93e1ad2e2a.webp)](https://image.mrxn.net/2b0c1305ee3e4a7f85e4a0d8542bbc77.webp)

可以看到 EFACEGO 里面自带的这个 tomcat-coyote.jar 文件幻数明显不是常见Java calss 文件的幻数 ca fe ba be

那我们修改下前面的agent 来 dump 这个class，dump后的class用 jd-gui 查看下有啥猫腻

[![汉王e脸通智慧园区管理平台最新版jar包解密浅析](images/img-015-b8f000fb22a7.webp)](https://image.mrxn.net/0e389fb25d304db9b817c06666eeb8a8.webp)

魔改版本增加的 decode 方法，顾名思义 那就是解码！

看下魔改的主要变动内容如下

```
private InputStream decode(InputStream is) throws Exception {
    int size = is.available();
    is.mark(size + 1);
    if (size < ENCRYPT_HEAD.length + ENCRYPT_TAIL.length + 24 + 16 + 8)
      return is; 
    byte[] head = new byte[ENCRYPT_HEAD.length];
    if (is.read(head) != ENCRYPT_HEAD.length) {
      is.reset();
      return is;
    } 
    for (int i = 0; i < ENCRYPT_HEAD.length; i++) {
      if (head[i] != ENCRYPT_HEAD[i]) {
        is.reset();
        return is;
      } 
    } 
    byte[] key = new byte[24];
    if (is.read(key) != 24)
      throw new IOException("Tomcat ClassParser failed parse file[0]"); 
    byte[] iv = new byte[16];
    if (is.read(iv) != 16)
      throw new IOException("Tomcat ClassParser failed parse file[1]"); 
    byte[] buffer = new byte[8];
    if (is.read(buffer) != 8)
      throw new IOException("Tomcat ClassParser failed parse file[2]"); 
    int sourceLen = buffer[0] << 24 & 0xFF000000 | buffer[1] << 16 & 0xFF0000 | buffer[2] << 8 & 0xFF00 | buffer[3] & 0xFF;
    int dataLen = buffer[4] << 24 & 0xFF000000 | buffer[5] << 16 & 0xFF0000 | buffer[6] << 8 & 0xFF00 | buffer[7] & 0xFF;
    if (sourceLen <= 0 || dataLen <= 0 || size != ENCRYPT_HEAD.length + ENCRYPT_TAIL.length + 24 + 16 + 8 + dataLen)
      throw new IOException("Tomcat ClassParser failed parse file[3]"); 
    byte[] data = new byte[dataLen];
    if (is.read(data) != dataLen)
      throw new IOException("Tomcat ClassParser failed parse file[4]"); 
    SecretKeySpec keySpec = new SecretKeySpec(key, "AES");
    IvParameterSpec ivSpec = new IvParameterSpec(iv);
    Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
    cipher.init(2, keySpec, ivSpec);
    byte[] decrypted = cipher.doFinal(data);
    if (decrypted == null || decrypted.length != sourceLen)
      throw new IOException("Tomcat ClassParser failed parse file[5]"); 
    byte code = (byte)(sourceLen & 0xFF);
    for (int j = 0; j < sourceLen; j++)
      decrypted[j] = (byte)(decrypted[j] ^ code); 
    return new ByteArrayInputStream(decrypted);
  }

  private static final byte[] ENCRYPT_HEAD = new byte[] { 
      82, 97, 114, 33, 26, 7, 0, -49, -112, 115, 
      0, 0, 13, 0, 0, 0, -86, -69, -52, -35, 
      -18, -1 };

  private static final byte[] ENCRYPT_TAIL = new byte[] { -105, -60, 61, 123, 0, 64, 7, 0 };
```

这不就是我们心心念念的解密逻辑吗！其主要处理逻辑如下

* 如果不满足加密数据结构长度，否则直接放回。
* 读取头部标记，与 `ENCRYPT_HEAD` 比较，若不匹配，也说明不是加密格式，返回原始流。
* 读取密钥、IV 和长度信息，若读取失败，抛出 `IOException`，如果数据长度不对，也抛出异常。
* 读取密文数据
* 执行 AES 解密（AES 使用 CBC 模式，带填充，key 和 iv 是前面读取的，`2` 表示 `Cipher.DECRYPT_MODE`）
* 验证长度并异或还原（使用 `(sourceLen & 0xFF)` 得到一个字节做异或）
* 返回解密结果

加密格式结构如下

| 顺序 | 字节数 | 说明 |
| --- | --- | --- |
| 1 | 22 | `ENCRYPT_HEAD` 魔术头 |
| 2 | 24 | AES 密钥 |
| 3 | 16 | AES IV 向量 |
| 4 | 8 | 解密后长度 + 加密数据长度 |
| 5 | N | 加密数据 |
| 6 | 8 | `ENCRYPT_TAIL` 魔术尾（**未验证！此段代码未读取尾部，只通过 size 检查存在**） |

知道了加密方式后，就可以写一个解密工具直接将整个jar包进行解密，下载方式在最后

[![汉王e脸通智慧园区管理平台最新版jar包解密浅析](images/img-016-4e11a7a57d31.webp)](https://image.mrxn.net/d9f95570d661461a927cccbb0c46b0ad.webp)

成功解密

[![汉王e脸通智慧园区管理平台最新版jar包解密浅析](images/img-017-d1cf1f5c370a.webp)](https://image.mrxn.net/dcba592b2b2b42e68b17ac33891f7268.webp)

[![汉王e脸通智慧园区管理平台最新版jar包解密浅析](images/img-018-978fd4046560.webp)](https://image.mrxn.net/c307622967e74130a4c638b3fc0496a2.webp)

# 参考

* `https://github.com/accessmodifier364/Dumper`
* [为了方便动态dump自定义class类，魔改了 accessmodifier364/Dumper 项目](https://github.com/Mr-xn/Dumper)
* [解密工具下载](https://image.mrxn.net/2e6722d49cf54395bd90dc8424537542.jar)

* 标签：
* [#代码审计](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81%E5%AE%A1%E8%AE%A1)
* [#Java](https://mrxn.net/tag/Java)

---


// 获取当前脚本所在的父容器
const parentContainer = document.currentScript.parentElement;
let searchContainer = parentContainer.querySelector('article') || parentContainer;
if (searchContainer) {
// 优先在 class 名为 prose 或 markdown 的容器内搜索 img 图片
let images = [];
const containers = searchContainer.querySelectorAll('.prose, .markdown');
containers.forEach(function(container) {
images = images.concat(Array.from(container.querySelectorAll('img')));
});
if (images.length === 0) {
images = searchContainer.querySelectorAll('img');
}
images.forEach(function(img) {
if (img.getAttribute('data-action') === 'zoom') {
const parentLink = img.parentNode;
if (parentLink.tagName === 'A') {
parentLink.setAttribute('data-fancybox', 'gallery');
}
} else {
const link = document.createElement('a');
link.setAttribute('data-fancybox', 'gallery');
link.setAttribute('href', img.getAttribute('src'));
img.parentNode.insertBefore(link, img);
link.appendChild(img);
}
});
// 初始化 Fancybox
Fancybox.bind("[data-fancybox]", {
// 您的自定义选项
});
}

文章目录
×

* [1.简介](#toc-1-)
* [2.正文](#toc-2-)
* [3.dump class](#toc-3-)
* [4.设置jvm参数](#toc-4-)
* [5.编写解密工具](#toc-5-)
* [6.参考](#toc-6-)



.x\_nav\_toc {
position: fixed;
top: 0;
right: -300px;
width: 280px;
height: 100%;
background-color: white;
box-shadow: -2px 0 15px rgba(0, 0, 0, 0.1);
z-index: 1000;
transition: right 0.3s ease;
display: flex;
flex-direction: column;
overflow: hidden;
padding-top: 10px;
}
.x\_nav\_toc.active {
right: 0;
}
.x\_toc\_header {
display: flex;
justify-content: space-between;
align-items: center;
padding: 15px 20px;
height: 48px;
border-bottom: 1px solid #eee;
}
.x\_toc\_title {
font-size: 18px;
font-weight: bold;
color: #333;
}
.x\_toc\_close {
background: none;
border: none;
font-size: 24px;
cursor: pointer;
color: #777;
transition: color 0.2s;
}
.x\_toc\_close:hover {
color: #333;
}
.x\_toc\_content {
flex: 1;
overflow-y: auto;
padding: 15px 20px;
padding-right: 10px;
}
.x\_anchor-list {
list-style-type: none;
padding: 0;
margin: 0;
}
/\* 减小目录项间距 \*/
.x\_anchor-list li {
margin-bottom: 4px; /\* 间距从8px减小到4px \*/
}
.x\_anchor-list a {
text-decoration: none;
color: #555;
display: block;
padding: 6px 10px; /\* 减少内边距 \*/
transition: all 0.2s;
font-size: 14px;
border-radius: 4px;
line-height: 1.4; /\* 减小行高 \*/
}
.x\_anchor-list a:hover,
.x\_anchor-list a:focus {
background-color: #f8f9fa;
color: #0068d6;
}
.toc-number {
font-weight: 600;
margin-right: 8px;
color: #495057;
display: inline-block;
min-width: 25px;
}
/\* 减小各级标题间距 \*/
.toc-h1 {
font-weight: 600;
font-size: 15px;
margin-top: 10px; /\* 上边距从15px减小到10px \*/
padding-left: 5px !important;
}
.toc-h2 {
font-size: 14px;
padding-left: 15px !important; /\* 缩进从20px减小到15px \*/
}
.toc-h3 {
font-size: 13px;
padding-left: 25px !important; /\* 缩进从30px减小到25px \*/
}
.toc-h4 {
font-size: 12px;
padding-left: 35px !important; /\* 缩进从40px减小到35px \*/
}
/\* 修改后的切换按钮样式 - 使用图标且位置下移 \*/
.x\_toc\_toggle {
position: fixed;
bottom:120px; right: 17px;width:40px;height:40px;background-color:white;
border-radius: 50%;
border: none;
cursor: pointer;
box-shadow: 0 4px 12px rgba(0,0,0,0.15);
z-index: 999;
transition: all 0.3s ease;
display: flex;
align-items: center;
justify-content: center;
padding: 0;
}
.x\_toc\_toggle svg {
width:24px;height:24px;stroke:#3d9bff;
}
.x\_toc\_toggle:hover {
#background-color: #0081f8;
transform: translateY(-3px);
box-shadow: 0 6px 15px rgba(0,0,0,0.2);
}
@media (max-width: 768px) {
.x\_nav\_toc {
width: 280px;
}
.x\_toc\_toggle {
bottom: 100px; /\* 手机端也下移位置 \*/
right: 30px;
width: 40px;
height: 40px;
}
.x\_toc\_toggle svg {
width: 20px;
height: 20px;
}
}

document.addEventListener('DOMContentLoaded', function() {
// 获取所有标题元素
var className = ".line-numbers";
var selectors = [];
for (var i = 1; i <= 6; i++) {
selectors.push(className + ' h' + i);
}
var headings = document.querySelectorAll(selectors.join(', '));
// 获取DOM元素
var tocContainer = document.querySelector('.x\_nav\_toc');
var toggleButton = document.querySelector('.x\_toc\_toggle');
var tocList = document.querySelector('.x\_anchor-list');
var closeButton = document.querySelector('.x\_toc\_close');
var currentHighlight = null;
// 检测是否为移动设备
const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
// 如果没有标题，隐藏所有元素
if (headings.length === 0) {
tocContainer.style.display = 'none';
toggleButton.style.display = 'none';
return;
}
// 初始化层级计数器
var counters = [0, 0, 0, 0, 0, 0]; // h1-h6
var currentLevel = 0;
// 生成带数字编号的目录
headings.forEach(function(heading, index) {
var level = parseInt(heading.tagName[1]);
// 更新计数器
counters[level - 1] += 1; // 增加当前级别计数器
// 重置更低级计数器
for (var i = level; i < 6; i++) {
counters[i] = 0;
}
// 生成编号字符串（如"1.2.3"）
var numberParts = [];
for (var i = 0; i < level; i++) {
if (counters[i] > 0) {
numberParts.push(counters[i]);
}
}
var numberText = numberParts.join('.')+'.';
// 创建唯一ID
var id = 'toc-' + numberText.replace(/\./g, '-');
heading.id = id;
var listItem = document.createElement('li');
var anchor = document.createElement('a');
var numberSpan = document.createElement('span');
numberSpan.className = 'toc-number';
numberSpan.textContent = numberText;
anchor.appendChild(numberSpan);
anchor.innerHTML += heading.textContent;
anchor.href = '#' + id;
anchor.classList.add('toc-h' + level);
listItem.appendChild(anchor);
tocList.appendChild(listItem);
// 添加点击事件（不关闭目录）
anchor.addEventListener('click', function(e) {
e.preventDefault();
// 更新高亮状态
if (currentHighlight) {
currentHighlight.classList.remove('active');
}
this.classList.add('active');
currentHighlight = this;
// 滚动到对应位置
var targetId = this.getAttribute('href').substring(1);
var targetElement = document.getElementById(targetId);
if (targetElement) {
var header = document.querySelector("header");
var headerHeight = header ? header.offsetHeight : 0;
var elementPosition = targetElement.getBoundingClientRect().top + window.pageYOffset;
var offsetPosition = elementPosition - headerHeight - 20;
window.scrollTo({
top: offsetPosition,
behavior: 'smooth'
});
// 滚动到目录项的可视区域
this.scrollIntoView({behavior: 'smooth', block: 'nearest'});
// 点击事件中
if (isMobile) {
closeToc(); // 移动端点击后关闭目录
}
}
});
});
// 切换按钮点击事件
toggleButton.addEventListener('click', function() {
tocContainer.classList.add('active');
});
// 关闭按钮点击事件
closeButton.addEventListener('click', function(e) {
e.stopPropagation();
closeToc();
});
// 滚动时更新高亮状态
window.addEventListener('scroll', function() {
var fromTop = window.scrollY;
var header = document.querySelector("header");
var headerHeight = header ? header.getBoundingClientRect().height : 0; // 更精确的header高度
//console.log(headerHeight);
// 精准计算标题文档位置
var activeSection = null;
headings.forEach(function(heading) {
var section = document.getElementById(heading.id);
if (!section) return;
// 使用getBoundingClientRect获取精确位置
var rect = section.getBoundingClientRect();
var sectionTop = rect.top + fromTop; // 转换为文档顶部绝对位置
var sectionBottom = rect.bottom + fromTop + headerHeight;
// 增加20px激活区域缓冲
if (fromTop + headerHeight + 20 >= sectionTop && fromTop < sectionBottom) {
activeSection = heading;
}
});
// 更新高亮状态（新增精确边界判断）
if (activeSection) {
var tocLink = tocList.querySelector('a[href="#' + activeSection.id + '"]');
if (tocLink && currentHighlight !== tocLink) {
if (currentHighlight) {
currentHighlight.blur();
currentHighlight.classList.remove('active');
}
tocLink.classList.add('active');
tocLink.focus();
currentHighlight = tocLink;
// 平滑滚动到可视区域（改进触发条件）
var tocRect = tocLink.getBoundingClientRect();
var tocContainerRect = tocContainer.getBoundingClientRect();
if (tocRect.bottom > tocContainerRect.bottom || tocRect.top < tocContainerRect.top) {
tocLink.scrollIntoView({behavior: 'auto', block: 'nearest'});
}
}
}
});
// 关闭目录面板
function closeToc() {
tocContainer.classList.remove('active');
}
});

/\* 超小屏幕隐藏 \*/
@media (max-width: 768px) {
#qrcode-right {
display: none;
}
}

版权所有：[Mrxn's Blog](https://mrxn.net/)  
文章标题：[汉王e脸通智慧园区管理平台最新版jar包解密浅析](https://mrxn.net/jswz/efacego-dencrypt-jar.html)  
文章链接：<https://mrxn.net/jswz/efacego-dencrypt-jar.html>  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

![](data:image/png;base64,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)

设备上扫码阅读


var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/efacego-dencrypt-jar.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});

  

### 📚 推荐阅读

* [深信服运维安全管理系统 install\_patch 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-system-concentration_management-install_patch-rce.html)
* [深信服运维安全管理系统 del\_patch 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-system-concentration_management-del_patch-rce.html)
* [深信服运维安全管理系统 upload\_file 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-cssp-app-upload_file-rce.html)
* [深信服运维安全管理系统 csspost/update 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-csspost-update-rce.html)
* [深信服运维安全管理系统 save\_SNMP 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-SNMP-save_SNMP-rce.html)
* [深信服运维安全管理系统 getLdap 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-getLdap-rce.html)
* [深信服运维安全管理系统 Jwt 密钥硬编码](https://mrxn.net/jswz/sangfor_osm-login-search_login-token-leak.html)
* [深信服运维安全管理系统 del\_route 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-netConfig-del_route-rce.html)
* [深信服运维安全管理系统 del\_net 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-netConfig-del_net-rce.html)
* [深信服运维安全管理系统 change\_net 远程命令执行漏洞](https://mrxn.net/jswz/sangfor_osm-netConfig-change_net-rce.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 updateLoginName SQL注入漏洞](https://mrxn.net/jswz/bigant-user-updateLoginName-sqli.html)
* [九佳易管理系统 PrivilegedCodeDestroy.asmx SQL注入漏洞](https://mrxn.net/jswz/a8erp-Interface-licx-PrivilegedCodeDestroy-sqli.html)
* [九佳易管理系统 Ajax\_XT.ashx SQL 注入漏洞](https://mrxn.net/jswz/a8erp-Ajax_XT-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 moveDept SQL注入漏洞](https://mrxn.net/jswz/bigant-dept-moveDept-sqli.html)
* [青龙面板最新版v2.20.1 鉴权绕过致RCE漏洞](https://mrxn.net/jswz/qinglong-auth-bypass-rce.html)
* [九佳易管理系统 picHY.ashx SQL 注入漏洞](https://mrxn.net/jswz/a8erp-HuiYuanDangAn-picHY-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 安装程序二次注入致远程代码执行漏洞](https://mrxn.net/jswz/bigant-install-config-rce.html)
* [东胜物流软件 MsChDuiController 多个SQL注入漏洞](https://mrxn.net/jswz/dongsheng-MsChDuiController-sqli.html)
* [大蚂蚁 (BigAnt) 即时通讯系统 PublicController 任意文件读取漏洞](https://mrxn.net/jswz/bigant-Public-download.html)
* [东胜物流软件 MsAnnounceController SQL注入漏洞](https://mrxn.net/jswz/dongsheng-MsAnnounce-GetData-sqli.html)

  

/\* 底部展示样式 \*/
.qrcode-bottom-box {
margin: 40px auto;
text-align: center;
}
.qrcode-title {
font-size: 16px;
color: #666;
margin-bottom: 0px;
font-weight: bold;
text-align: center;
}
.qrcode-bottom-box img {
display: inline-block;
padding: 10px;
background: #fff;
border-radius: 8px;
margin: 10px auto;
}
/\* 悬浮展示样式 \*/
.qrcode-float {
position: fixed;
z-index: 9999;
background: rgba(255,255,255,0.98);
padding: 20px;
border-radius: 12px;
}
.qrcode-float:hover {
transform: scale(1.05);
}
/\* 移动端适配 \*/
@media (max-width: 1440px) {
.qrcode-float {
right: 2%;
transform: none;
}
}
/\* 超小屏幕隐藏 \*/
@media (max-width: 768px) {
.qrcode-float {
display: none;
}
}

![](data:image/png;base64,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)

手机扫码阅读


var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/efacego-dencrypt-jar.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});
 