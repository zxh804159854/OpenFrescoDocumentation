# SimSimulink 实验控制

用来将实验单元的信号发送到simulink，可以只是普通主机上的 Simulink 通信模型，不一定是专用实时硬件。和simulink的S-function的SFun_OPF_TCPServer和SFun_OPF_UDPServer一起使用（老版是SFun_OPFConnect），即将信号传到这个sfunction里面，这个是通过tcp或者udp进行通信。

## 命令

<div class="definition">

expControl SimSimulink tag ipAddr ipPort \<-udp\> -trialCP cpTags -outCP cpTags \<-ctrlFilters (5 \$filterTag)\> \<-daqFilters (5 \$filterTag)\>

</div>

|             |                                                                                                                             |
|:------------|:----------------------------------------------------------------------------------------------------------------------------|
| \$tag       | 唯一控制标签                                                                                                                |
| ipAddr      | SimSimulink 的 IP 地址                                                                                                      |
| \$ipPort    | SimSimulink 的 IP 端口                                                                                                      |
| \$cpTags    | 先前定义的控制点标签                                                                                                        |
| \$filterTag | 先前定义的滤波器标签标识；滤波器标签标识大小为 5（条目：\[位移, 速度, 加速度, 力, 时间\]\[disp, vel, accel, force, time\]） |

## 示例

    expControl SimSimulink 1 "127.0.0.1" 8090 -trialCP 1 -outCP 2 

案例在EXAMPLES/OneBayFrame/ControlSystem

<figure>
<img src="image/ch01/SimSimulink.png" style="width:80.0%" />
<figcaption>SimSimulink 实验控制</figcaption>
</figure>

## 记录Recorder

在创建 ExpControlRecorder 对象时，对 SimSimulink 实验控制的有效查询包括（代码setResponse部分）：

- 控制（命令）信号：ctrlSig, ctrlSignal, ctrlSignals

- 数据采集（反馈）信号：daqSig, daqSignal, daqSignals

## 参考

MTSPEER (2018) – Hybrid Simulation Technologies & Methods for Civil Engineering