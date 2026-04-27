# MTSCsi 实验控制

## 命令

此命令用于构建 MTSCsi 实验控制对象。MTSCsi（MTS 计算机仿真接口）实验控制对象用于通过 CSI API 与 MTS 硬件进行通信。

<div class="definition">

expControl MTSCsi tag configFileName rampTime -trialCP cpTags -outCP cpTags \<-ctrlFilters (5 \$filterTag)\> \<-daqFilters (5 \$filterTag)\>

</div>

|                |                                                                                                                             |
|:---------------|:----------------------------------------------------------------------------------------------------------------------------|
| \$tag          | 唯一控制标签                                                                                                                |
| configFileName | Csi 配置文件的路径，包括带 .mtscs 扩展名的文件名                                                                            |
| \$rampTime     | 斜坡时间 \[秒\]                                                                                                             |
| \$cpTags       | 先前定义的控制点标签                                                                                                        |
| \$filterTag    | 先前定义的滤波器标签标识；滤波器标签标识大小为 5（条目：\[位移, 速度, 加速度, 力, 时间\]\[disp, vel, accel, force, time\]） |

## 示例

    expControl MTSCsi 1 "C:/MTSCsi/Example/OpenFresco_uNEES.mtscs" 0.1 -trialCP 1 -outCP 2

上述示例命令使用路径`C:/MTSCsi/Example/OpenFresco_uNEES.mtscs`，斜坡时间为 0.1 秒。

<figure>
<img src="image/ch01/MTSCsi.jpg" style="width:80.0%" />
<figcaption>MTSCsi 实验控制</figcaption>
</figure>

## 记录Recorder

在创建 ExpControlRecorder 对象时，对 MTSCsi 实验控制的有效查询包括（代码setResponse部分）：

- 控制（命令）信号：ctrlSig, ctrlSignal, ctrlSignals

- 数据采集（反馈）信号：daqSig, daqSignal, daqSignals

## 参考

<http://www.dspaceinc.com/ww/en/inc/home/products/hw/singbord.cfm>
