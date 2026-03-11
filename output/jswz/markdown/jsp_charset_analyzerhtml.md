---
title: "JSP Charset Analyzer"
source: https://mrxn.net/jswz/jsp_charset_analyzer.html
---

# JSP Charset Analyzer

[Mrxn](https://mrxn.net/author/1)* 发表于2025/8/3 12:46
* 531浏览
* [0评论](#comment)
* 4小时
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

# jsp\_charset\_analyzer

JSP Charset Analyzer JSP字符集支持分析

> 有的目标环境有杀软，静态都不能过谈何动态，先过了静态再说！
>   
> 此脚本方便获得目标环境支持的所有编码字符集，然后针对性的进行组合，从而达到 Bypass AV 的效果。

# 获取目标环境支持字符集列表

新建一个jsp页面

```
<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%@ page isELIgnored="true" %> <%-- Good practice to avoid EL conflicts --%>
<%@ page import="java.nio.charset.Charset" %>
<%@ page import="java.util.Map" %>
<%@ page import="java.util.SortedMap" %>
<%@ page import="java.util.List" %>
<%@ page import="java.util.ArrayList" %>
<%@ page import="java.util.LinkedHashMap" %>
<!DOCTYPE html>
<html>
<head>
    <title>JSP 字符集支持分析</title>
    <meta charset="UTF-8">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; margin: 20px; background-color: #f9f9f9; color: #333; }
        h1, h3 { color: #1a1a1a; }
        table { border-collapse: collapse; width: 100%; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; font-family: 'Menlo', 'Courier New', Courier, monospace; }
        th { background-color: #f2f2f2; cursor: pointer; user-select: none; position: relative; }
        th:hover { background-color: #e8e8e8; }
        .sort-arrow { position: absolute; right: 8px; top: 50%; transform: translateY(-50%); color: #888; font-size: 12px; }
        .payload { background-color: #eef; padding: 10px; border-left: 5px solid #66f; margin-bottom: 20px; word-wrap: break-word; font-family: 'Menlo', 'Courier New', Courier, monospace; }
        .problematic { background-color: #ffdddd !important; }
        .clean { background-color: #ddffdd !important; }
        .controls { margin-bottom: 20px; }
        .controls button { background-color: #007bff; color: white; border: none; padding: 10px 15px; border-radius: 4px; cursor: pointer; font-size: 14px; margin-right: 10px; }
        .controls button:hover { background-color: #0056b3; }
        .controls button.secondary { background-color: #c82333; }
        .controls button.secondary:hover { background-color: #a21b29; }
        td:first-child { word-break: break-word; } /* Allow long lists of charsets to wrap */
    </style>
</head>
<body>

    <h1>JSP 编码字符集支持分析</h1>
    <p><b>新功能：</b>如果多个字符集产生完全相同的编码字节，它们将被合并到同一行中进行展示。</p>
    <p><b>功能：</b>动态排序（点击表头）和导出为CSV文件。</p>

    <h3>测试载荷 (Payload):</h3>
    <div class="payload"><%
        String payload = "<%out.println(java.util.UUID.randomUUID().toString());new java.io.File(application.getRealPath(request.getServletPath())).delete();%" + ">";
        out.print(payload.replace("<", "&lt;").replace(">", "&gt;"));
    %></div>

    <div class="controls">
        <button onclick="exportToCSV('all_charsets_grouped.csv', false)">导出所有为 CSV</button>
        <button onclick="exportToCSV('problematic_charsets_grouped.csv', true)" class="secondary">仅导出有问题项为 CSV</button>
    </div>

    <table id="charsetTable">
        <thead>
            <tr>
                <th onclick="sortTable(0)">字符集名称 (合并显示) <span class="sort-arrow"></span></th>
                <th onclick="sortTable(1)">是否有问题? <span class="sort-arrow"></span></th>
                <th>编码后的字节 (Hex Representation)</th>
            </tr>
        </thead>
        <tbody>
        <%
            // =========================================================================
            //  START OF MODIFIED LOGIC
            // =========================================================================

            // Step 1: Group charsets by their resulting byte sequence.
            // We use LinkedHashMap to maintain a somewhat predictable insertion order.
            Map<String, List<String>> groupedCharsets = new LinkedHashMap<>();
            Map<String, Boolean> problematicFlags = new LinkedHashMap<>();

            SortedMap<String, Charset> availableCharsets = Charset.availableCharsets();
            for (Map.Entry<String, Charset> entry : availableCharsets.entrySet()) {
                String charsetName = entry.getKey();
                String hexString = "";
                boolean isProblematic = false;
                try {
                    byte[] encodedBytes = payload.getBytes(charsetName);
                    StringBuilder sb = new StringBuilder();
                    for (byte b : encodedBytes) {
                        if (b < 32 || b > 126) {
                            isProblematic = true;
                        }
                        sb.append(String.format("%02X ", b));
                    }
                    hexString = sb.toString().trim();
                } catch (Exception e) {
                    hexString = "Encoding Error: " + e.getMessage();
                    isProblematic = true;
                }

                // Add the charset name to the list for this specific hex output.
                groupedCharsets.computeIfAbsent(hexString, k -> new ArrayList<>()).add(charsetName);

                // Store the problematic status for this group (only needs to be set once).
                problematicFlags.putIfAbsent(hexString, isProblematic);
            }

            // Step 2: Render the grouped results into the table.
            for (Map.Entry<String, List<String>> groupEntry : groupedCharsets.entrySet()) {
                String hexString = groupEntry.getKey();
                List<String> charsetsInGroup = groupEntry.getValue();
                boolean isProblematic = problematicFlags.get(hexString);

                // Join the list of charset names with a comma for display.
                String combinedCharsetNames = String.join(", ", charsetsInGroup);
                String rowClass = isProblematic ? "problematic" : "clean";
        %>
            <tr class="<%= rowClass %>">
                <td><%= combinedCharsetNames %></td>
                <td><%= isProblematic ? "是" : "否" %></td>
                <td><%= hexString %></td>
            </tr>
        <%
            } // End of the rendering loop
            // =========================================================================
            //  END OF MODIFIED LOGIC
            // =========================================================================
        %>
        </tbody>
    </table>

<script>
    // --- NO CHANGES NEEDED FOR JAVASCRIPT ---
    // The sorting and exporting functions work on the final rendered HTML table.

    // --- 排序功能 ---
    let sortDirection = {}; 
    function sortTable(columnIndex) {
        const table = document.getElementById("charsetTable");
        const tbody = table.tBodies[0];
        const rows = Array.from(tbody.rows);
        const headers = table.tHead.rows[0].cells;
        const direction = sortDirection[columnIndex] === 'asc' ? 'desc' : 'asc';
        sortDirection = { [columnIndex]: direction };
        for (let i = 0; i < headers.length; i++) {
            const arrow = headers[i].querySelector('.sort-arrow');
            if (arrow) {
                if (i === columnIndex) {
                    arrow.textContent = direction === 'asc' ? ' ▲' : ' ▼';
                } else {
                    arrow.textContent = '';
                }
            }
        }
        rows.sort((a, b) => {
            const cellA = a.cells[columnIndex].innerText.toLowerCase();
            const cellB = b.cells[columnIndex].innerText.toLowerCase();
            if (cellA < cellB) return direction === 'asc' ? -1 : 1;
            if (cellA > cellB) return direction === 'asc' ? 1 : -1;
            return 0;
        });
        tbody.innerHTML = '';
        rows.forEach(row => tbody.appendChild(row));
    }

    // --- 导出CSV功能 ---
    function exportToCSV(filename, problematicOnly) {
        const table = document.getElementById("charsetTable");
        let csv = [];
        const headers = Array.from(table.tHead.rows[0].cells).map(header => `"${header.innerText.replace(/"/g, '""').trim()}"`);
        csv.push(headers.join(','));
        const rows = table.tBodies[0].rows;
        for (let i = 0; i < rows.length; i++) {
            const row = rows[i];
            if (problematicOnly && !row.classList.contains('problematic')) {
                continue;
            }
            const rowData = Array.from(row.cells).map(cell => `"${cell.innerText.replace(/"/g, '""')}"`);
            csv.push(rowData.join(','));
        }
        const csvContent = csv.join('\n');
        const blob = new Blob(["\uFEFF" + csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement("a");
        if (link.download !== undefined) {
            const url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", filename);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    }
</script>

</body>
</html>
```

放到 Tomcat 目录下，浏览器访问即可得到当前jdk下jsp支持的字符集

![JSP Charset Analyzer](https://image.mrxn.net/ee26c1b0c96c49d9ad6cbfdc4cc78d6e.webp)

可以根据结果进行排序互尊导出结果。
  
结果显示支持的字符集中，可以用来编码绕过AV静态扫描的字符集如下

```
"IBM-Thai","IBM01140","IBM01141","IBM01142","IBM01143",
"IBM01144","IBM01145","IBM01146","IBM01147","IBM01148",
"IBM01149","IBM037","IBM1026","IBM1047","IBM273","IBM277",
"IBM278","IBM280","IBM284","IBM285","IBM297","IBM420","IBM424","IBM500",
"IBM870","IBM871","IBM918","x-IBM1025","x-IBM1097","x-IBM1112","x-IBM1122","x-IBM1123",
"x-IBM1166","x-IBM1364","x-IBM833","x-IBM875","x-IBM933","x-IBM935","x-IBM937","x-IBM939","IBM290","x-IBM930"
```

当然，其中一部分字符集编码后的结果是一样的。

# jar 生成指定编码字符集jsp文件

批量生成指定字符集或全部设定字符集jsp文件实现Java代码如下

```
import java.io.*;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.charset.UnsupportedCharsetException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.text.SimpleDateFormat;
import java.util.Base64;
import java.util.Date;

public class GenerateCp290Jsp {
    // 定义所有支持的编码列表
    private static final String[] SUPPORTED_ENCODINGS = {
        "IBM-Thai","IBM01140","IBM01141","IBM01142","IBM01143",
        "IBM01144","IBM01145","IBM01146","IBM01147","IBM01148",
        "IBM01149","IBM037","IBM1026","IBM1047","IBM273","IBM277",
        "IBM278","IBM280","IBM284","IBM285","IBM297","IBM420","IBM424","IBM500",
        "IBM870","IBM871","IBM918","x-IBM1025","x-IBM1097","x-IBM1112","x-IBM1122","x-IBM1123",
        "x-IBM1166","x-IBM1364","x-IBM833","x-IBM875","x-IBM933","x-IBM935","x-IBM937","x-IBM939","IBM290","x-IBM930"
    };

    public static void main(String[] args) {
        boolean allMode = false;
        if (args.length < 1) {
            printUsage();
            System.exit(1);
        }

        String inputFile = args[0];
        String outputFile = null;
        String inputEncoding = StandardCharsets.UTF_8.name();
        String outputEncoding = "cp290";
        boolean outputHex = false;
        boolean outputBase64 = false;

        // 解析命令行参数
        for (int i = 1; i < args.length; i++) {
            if (args[i].equalsIgnoreCase("-all")) {
                allMode = true;
            } else if (args[i].equalsIgnoreCase("-ie") && i + 1 < args.length) {
                inputEncoding = args[++i];
            } else if (args[i].equalsIgnoreCase("-oe") && i + 1 < args.length) {
                outputEncoding = args[++i];
            } else if (args[i].equalsIgnoreCase("-o") && i + 1 < args.length) {
                outputFile = args[++i];
            } else if (args[i].equalsIgnoreCase("-hex")) {
                outputHex = true;
            } else if (args[i].equalsIgnoreCase("-base64")) {
                outputBase64 = true;
            } else {
                System.err.println("警告: 忽略未知参数: " + args[i]);
            }
        }

        // 如果启用了 -all 模式
        if (allMode) {
            System.out.println("启用全编码模式，将生成所有支持的编码版本");
            System.out.println("支持的编码数量: " + SUPPORTED_ENCODINGS.length);

            String baseOutputPath = outputFile;
            if (baseOutputPath != null) {
                // 如果指定了输出路径，检查是否是目录
                Path outputPath = Paths.get(baseOutputPath);
                if (!Files.isDirectory(outputPath) && !baseOutputPath.endsWith(File.separator)) {
                    // 如果指定的是文件路径，则使用其父目录
                    baseOutputPath = (outputPath.getParent() != null) ? 
                        outputPath.getParent().toString() : "";
                }
            }

            for (String enc : SUPPORTED_ENCODINGS) {
                try {
                    // 为每个编码生成输出文件名
                    String encOutputFile;
                    if (baseOutputPath == null) {
                        encOutputFile = generateOutputFileName(inputFile, enc);
                    } else {
                        String fileName = Paths.get(generateOutputFileName(inputFile, enc)).getFileName().toString();
                        encOutputFile = Paths.get(baseOutputPath, fileName).toString();
                    }

                    // 转换并写入文件
                    convertAndWriteFile(
                        inputFile, 
                        inputEncoding, 
                        enc, 
                        encOutputFile, 
                        outputHex, 
                        outputBase64
                    );

                    System.out.println("成功生成: " + enc);
                } catch (Exception e) {
                    System.err.println("编码 " + enc + " 处理失败: " + e.getMessage());
                }
            }

            System.out.println("全编码模式完成，共尝试生成 " + SUPPORTED_ENCODINGS.length + " 个文件");
        } else {
            // 单编码模式（原始逻辑）
            try {
                convertAndWriteFile(
                    inputFile, 
                    inputEncoding, 
                    outputEncoding, 
                    outputFile, 
                    outputHex, 
                    outputBase64
                );
            } catch (UnsupportedCharsetException e) {
                System.err.println("错误: 不支持的编码 - " + e.getCharsetName());
                System.err.println("请确认您的JVM支持此编码");
            } catch (IOException e) {
                System.err.println("处理文件时发生错误: " + e.getMessage());
                e.printStackTrace();
            }
        }
    }

    // 文件转换逻辑
    private static void convertAndWriteFile(
        String inputFile, 
        String inputEncoding, 
        String outputEncoding, 
        String outputFile, 
        boolean outputHex, 
        boolean outputBase64
    ) throws IOException {
        // 自动生成输出文件名（如果需要）
        if (outputFile == null) {
            outputFile = generateOutputFileName(inputFile, outputEncoding);
        } else {
            // 检查输出路径是否是目录
            Path outputPath = Paths.get(outputFile);
            if (Files.isDirectory(outputPath) || outputFile.endsWith(File.separator)) {
                // 如果输出路径是目录或结尾有分隔符，生成文件名并添加到路径中
                String fileName = Paths.get(generateOutputFileName(inputFile, outputEncoding)).getFileName().toString();
                outputFile = outputPath.resolve(fileName).toString();
            }
        }

        System.out.println("正在读取文件: " + inputFile + " (输入编码: " + inputEncoding + ")");
        byte[] fileContent = Files.readAllBytes(Paths.get(inputFile));

        // 添加JSP编码指令（使用ASCII编码）
        String jspDirective = "<%@ page pageEncoding=\"" + outputEncoding + "\"%>\n";
        byte[] directiveBytes = jspDirective.getBytes(StandardCharsets.US_ASCII);

        // 转换文件内容到目标编码
        String content = new String(fileContent, Charset.forName(inputEncoding));
        byte[] contentBytes;
        try {
            contentBytes = content.getBytes(Charset.forName(outputEncoding));
        } catch (UnsupportedCharsetException e) {
            System.err.println("错误: 不支持的输出编码 - " + outputEncoding);
            throw e;
        }

        // 合并指令和内容
        byte[] finalBytes = new byte[directiveBytes.length + contentBytes.length];
        System.arraycopy(directiveBytes, 0, finalBytes, 0, directiveBytes.length);
        System.arraycopy(contentBytes, 0, finalBytes, directiveBytes.length, contentBytes.length);

        // 确保输出文件的父目录存在
        Path finalPath = Paths.get(outputFile);
        if (finalPath.getParent() != null) {
            Files.createDirectories(finalPath.getParent());
        }

        // 写入主要输出文件
        System.out.println("正在写入文件: " + outputFile + " (输出编码: " + outputEncoding + ")");
        try (FileOutputStream fos = new FileOutputStream(outputFile)) {
            fos.write(finalBytes);
            System.out.println("文件转换成功!");
            System.out.println("输入文件: " + inputFile + " (" + inputEncoding + ")");
            System.out.println("输出文件: " + outputFile + " (" + outputEncoding + ")");
            System.out.println("已添加JSP编码指令: " + jspDirective.trim());
        }

        // 如果需要，生成十六进制编码文件
        if (outputHex) {
            String hexFile = outputFile + ".hex";
            writeHexFile(hexFile, finalBytes);
            System.out.println("已生成十六进制编码文件: " + hexFile);
        }

        // 如果需要，生成Base64编码文件
        if (outputBase64) {
            String base64File = outputFile + ".base64";
            writeBase64File(base64File, finalBytes);
            System.out.println("已生成Base64编码文件: " + base64File);
        }
    }

    // 生成十六进制编码文件
    private static void writeHexFile(String filename, byte[] data) throws IOException {
        StringBuilder hex = new StringBuilder(data.length * 2);
        for (byte b : data) {
            hex.append(String.format("%02X", b));
        }
        Files.write(Paths.get(filename), hex.toString().getBytes(StandardCharsets.UTF_8));
    }

    // 生成Base64编码文件
    private static void writeBase64File(String filename, byte[] data) throws IOException {
        String base64 = Base64.getEncoder().encodeToString(data);
        Files.write(Paths.get(filename), base64.getBytes(StandardCharsets.UTF_8));
    }

    // 生成输出文件名：输入文件名_输出编码_时间戳
    private static String generateOutputFileName(String inputFile, String outputEncoding) {
        Path path = Paths.get(inputFile);
        String fileName = path.getFileName().toString();

        int dotIndex = fileName.lastIndexOf('.');
        String baseName = (dotIndex > 0) ? fileName.substring(0, dotIndex) : fileName;
        String extension = (dotIndex > 0) ? fileName.substring(dotIndex) : "";

        String timeStamp = new SimpleDateFormat("yyyyMMddHHmmss").format(new Date());
        String newFileName = baseName + "_" + outputEncoding + "_" + timeStamp + extension;

        if (path.getParent() != null) {
            return path.getParent().resolve(newFileName).toString();
        }
        return newFileName;
    }

    // 动态获取JAR文件名
    private static String getJarName() {
        try {
            return new File(GenerateCp290Jsp.class
                .getProtectionDomain()
                .getCodeSource()
                .getLocation()
                .toURI())
                .getName();
        } catch (Exception e) {
            return "GenerateCp290Jsp.jar";
        }
    }

    private static void printUsage() {
        String jarName = getJarName();

        System.out.println("用法: java -jar " + jarName + " <输入文件> [选项]");
        System.out.println("选项:");
        System.out.println("  -ie <编码>     输入文件编码 (默认: UTF-8)");
        System.out.println("  -oe <编码>     输出文件编码 (默认: cp290)");
        System.out.println("  -o <输出路径>   输出文件或目录路径 (默认: 自动生成)");
        System.out.println("  -hex           额外生成十六进制编码文件");
        System.out.println("  -base64        额外生成Base64编码文件");
        System.out.println("  -all           生成所有支持的编码版本");
        System.out.println("\n支持的编码 (" + SUPPORTED_ENCODINGS.length + " 种):");
        System.out.println("  " + String.join(", ", SUPPORTED_ENCODINGS));

        System.out.println("\n示例:");
        System.out.println("  1. 基本用法:");
        System.out.println("     java -jar " + jarName + " input.jsp");
        System.out.println("     输出: input_cp290_20231020123456.jsp");

        System.out.println("\n  2. 生成所有编码版本:");
        System.out.println("     java -jar " + jarName + " input.jsp -all");
        System.out.println("     在输入文件同目录下生成多个文件: ");
        System.out.println("        input_cp037_20231020123456.jsp");
        System.out.println("        input_cp290_20231020123456.jsp");
        System.out.println("        ...");

        System.out.println("\n  3. 指定输出目录并生成所有编码版本:");
        System.out.println("     java -jar " + jarName + " input.jsp -all -o output/");
        System.out.println("     在output目录下生成多个文件");

        System.out.println("\n  4. 生成所有编码版本并附加十六进制和Base64:");
        System.out.println("     java -jar " + jarName + " input.jsp -all -hex -base64");
        System.out.println("     为每个编码版本生成三个文件: .jsp, .hex, .base64");
    }
}
```

然后使用如下命令进行编译成jar包，方便调用

```
javac GenerateCp290Jsp.java && jar cfm GenerateCp290Jsp.jar MANIFEST.MF GenerateCp290Jsp.class
```

使用说明

```
用法: java -jar GenerateCp290Jsp.jar <输入文件> [选项]
选项:
  -ie <编码>     输入文件编码 (默认: UTF-8)
  -oe <编码>     输出文件编码 (默认: cp290)
  -o <输出路径>   输出文件或目录路径 (默认: 自动生成)
  -hex           额外生成十六进制编码文件
  -base64        额外生成Base64编码文件
  -all           生成所有支持的编码版本

支持的编码 (42 种):
  IBM-Thai, IBM01140, IBM01141, IBM01142, IBM01143, IBM01144, IBM01145, IBM01146, IBM01147, IBM01148, IBM01149, IBM037, IBM1026, IBM1047, IBM273, IBM277, IBM278, IBM280, IBM284, IBM285, IBM297, IBM420, IBM424, IBM500, IBM870, IBM871, IBM918, x-IBM1025, x-IBM1097, x-IBM1112, x-IBM1122, x-IBM1123, x-IBM1166, x-IBM1364, x-IBM833, x-IBM875, x-IBM933, x-IBM935, x-IBM937, x-IBM939, IBM290, x-IBM930

示例:
  1. 基本用法:
     java -jar GenerateCp290Jsp.jar input.jsp
     输出: input_cp290_20231020123456.jsp

  2. 生成所有编码版本:
     java -jar GenerateCp290Jsp.jar input.jsp -all
     在输入文件同目录下生成多个文件: 
        input_cp037_20231020123456.jsp
        input_cp290_20231020123456.jsp
        ...

  3. 指定输出目录并生成所有编码版本:
     java -jar GenerateCp290Jsp.jar input.jsp -all -o output/
     在output目录下生成多个文件

  4. 生成所有编码版本并附加十六进制和Base64:
     java -jar GenerateCp290Jsp.jar input.jsp -all -hex -base64
     为每个编码版本生成三个文件: .jsp, .hex, .base64
```

# 注意

所有代码均为现实牛马鞭策赛博牛马实现！现实牛马不负任何责任哈！

* 标签：
* [#
  代码](https://mrxn.net/tag/%E4%BB%A3%E7%A0%81)
* [#
  黑客工具](https://mrxn.net/tag/%E9%BB%91%E5%AE%A2%E5%B7%A5%E5%85%B7)
* [#
  Java](https://mrxn.net/tag/Java)

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

版权所有：
[Mrxn's Blog](https://mrxn.net/)
  
文章标题：
[JSP Charset Analyzer](https://mrxn.net/jswz/jsp_charset_analyzer.html)
  
文章链接：
<https://mrxn.net/jswz/jsp_charset_analyzer.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jsp\_charset\_analyzer.html"),
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

手机扫码阅读



var qrcode = new QRCode(document.getElementById("posts-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/jsp\_charset\_analyzer.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});