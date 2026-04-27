# Speedgoat 实验控制

## 命令

此命令用于构建 Speedgoat 实验控制对象，模型运行在 Speedgoat 实时机上。貌似是xpc的升级版。资料太少，待补充。

<div class="definition">

expControl Speedgoat tag ipAddr ipPort \<-udp\> -trialCP cpTags -outCP cpTags \<-timeOut t\> \<-ctrlFilters (5 \$filterTag)\> \<-daqFilters (5 \$filterTag)\>

</div>

|             |                                                                                                                             |
|:------------|:----------------------------------------------------------------------------------------------------------------------------|
| \$tag       | 唯一控制标签                                                                                                                |
| ipAddr      | Speedgoat 的 IP 地址                                                                                                        |
| \$ipPort    | Speedgoat 的 IP 端口                                                                                                        |
| \$cpTags    | 先前定义的控制点标签                                                                                                        |
| \$filterTag | 先前定义的滤波器标签标识；滤波器标签标识大小为 5（条目：\[位移, 速度, 加速度, 力, 时间\]\[disp, vel, accel, force, time\]） |

## 示例

    expControl 

解析

## 记录Recorder

在创建 ExpControlRecorder 对象时，对 Speedgoat 实验控制的有效查询包括（代码setResponse部分）：

- 控制（命令）信号：ctrlSig, ctrlSignal, ctrlSignals

- 数据采集（反馈）信号：daqSig, daqSignal, daqSignals

## 参考

<http://nees.berkeley.edu/Facilities/network-computers.shtml>