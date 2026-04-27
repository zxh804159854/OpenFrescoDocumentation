# SCRAMNet 实验控制

## 命令

此命令用于构建 SCRAMNet 实验控制对象。SCRAMNet（共享公共内存网络）是一种实时通信网络，基于复制的共享内存概念。每台计算机拥有一个 2 MB 的内存模块，该模块被镜像到网络中的所有其他计算机。写入一台计算机本地内存的数据会被复制到网络中的其他计算机。图 4 展示了 SCRAMNet 在 nees@berkeley 的实现方式。

<div class="definition">

expControl SCRAMNet tag -nodeID id memOffset -trialCP cpTags -outCP cpTags \<-ctrlFilters (5 \$filterTag)\> \<-daqFilters (5 \$filterTag)\>

</div>

|             |                                                                                                                             |
|:------------|:----------------------------------------------------------------------------------------------------------------------------|
| \$tag       | 唯一控制标签                                                                                                                |
| \$memOffset | SCRAMNet 基内存地址的内存偏移量 \[字节\]                                                                                    |
| \$id        | OpenFresco SCRAMNet 节点 ID                                                                                                 |
| \$cpTags    | 先前定义的控制点标签                                                                                                        |
| \$filterTag | 先前定义的滤波器标签标识；滤波器标签标识大小为 5（条目：\[位移, 速度, 加速度, 力, 时间\]\[disp, vel, accel, force, time\]） |

## 示例

    expControl SCRAMNet 1 381020 8 -trialCP 1 -outCP 2

上述示例命令使用内存偏移量 381020 字节。

<figure>
<img src="image/ch01/SCRAMNet .jpg" style="width:80.0%" />
<figcaption>SCRAMNet 实验控制</figcaption>
</figure>

## 记录Recorder

在创建 ExpControlRecorder 对象时，对 SCRAMNet 实验控制的有效查询包括（代码setResponse部分）：

- 控制（命令）信号：ctrlSig, ctrlSignal, ctrlSignals

- 数据采集（反馈）信号：daqSig, daqSignal, daqSignals

## 参考

<http://nees.berkeley.edu/Facilities/network-computers.shtml> 。

