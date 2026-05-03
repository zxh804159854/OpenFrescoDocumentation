# SCRAMNetGT 实验控制

## 命令

此命令用于构建 SCRAMNetGT 实验控制对象。SCRAMNet的升级版。

<div class="definition">

expControl SCRAMNetGT tag -nodeID id memOffset -trialCP cpTags -outCP cpTags \<-ctrlFilters (5 \$filterTag)\> \<-daqFilters (5 \$filterTag)\>

</div>

|             |                                                                                                                             |
|:------------|:----------------------------------------------------------------------------------------------------------------------------|
| \$tag       | 唯一控制标签                                                                                                                |
| \$memOffset | SCRAMNetGT 基内存地址的内存偏移量 \[字节\]                                                                                  |
| \$id        | OpenFresco SCRAMNetGT 节点 ID                                                                                               |
| \$cpTags    | 先前定义的控制点标签                                                                                                        |
| \$filterTag | 先前定义的滤波器标签标识；滤波器标签标识大小为 5（条目：\[位移, 速度, 加速度, 力, 时间\]\[disp, vel, accel, force, time\]） |

## 示例

    expControl SCRAMNetGT 1 4096 -trialCP 1 -outCP 2

上述示例命令使用内存偏移量 4096 字节。

## 记录Recorder

在创建 ExpControlRecorder 对象时，对 SCRAMNetGT 实验控制的有效查询包括（代码setResponse部分）：

- 控制（命令）信号：ctrlSig, ctrlSignal, ctrlSignals

- 数据采集（反馈）信号：daqSig, daqSignal, daqSignals

## 参考

<http://nees.berkeley.edu/Facilities/network-computers.shtml> 。