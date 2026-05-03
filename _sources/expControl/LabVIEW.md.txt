# LabVIEW 实验控制

## 命令

此命令用于构建 LabVIEW 实验控制对象。LabVIEW 是用于控制伊利诺伊大学厄巴纳-香槟分校（UIUC）MTS MiniMost 和 LBCB 的软件。LabVIEW 使用 LabVIEW NTCP 插件通信协议通过单一持久 TCP 连接进行通信。NEESit 文档 TR-2004-58 包含了 LabVIEW NTCP 插件的具体规范。此命令必须与 expControlPoint 命令配合使用。

<div class="definition">

<span id="def:LabVIEW" label="def:LabVIEW"></span> expControl LabVIEW tag ipAddr ipPort -trialCP cpTags -outCP cpTags \<-ctrlFilters (5 \$filterTag)\> \<-daqFilters (5 \$filterTag)\>

</div>

|             |                                                                                                                             |
|:------------|:----------------------------------------------------------------------------------------------------------------------------|
| \$tag       | 唯一控制标签                                                                                                                |
| ipAddr      | LabVIEW 计算机的 IP 地址                                                                                                    |
| \$ipPort    | LabVIEW 计算机的 IP 端口号（可选，默认值为 44000）                                                                          |
| \$cpTags    | 先前定义的控制点标签                                                                                                        |
| \$filterTag | 先前定义的滤波器标签标识；滤波器标签标识大小为 5（条目：\[位移, 速度, 加速度, 力, 时间\]\[disp, vel, accel, force, time\]） |

## 示例

    # 定义实验控制点
    expControlPoint 1 ux disp -fact 0.003 -lim -0.01 0.01
    expControlPoint 2 ux disp -fact 0.003 ux force -fact [expr 18.0/7.0]

    # 定义实验控制
    expControl LabVIEW 1 "130.126.242.175" 44000 -trialCP 1 -outCP 2

上述示例命令使用 IP 地址 "130.126.242.175"，端口号为 44000。-trialCP 和 -outCP 字段使用先前定义的实验控制点。有关 expControlPoint 命令的详细说明，请参阅本手册第 7 章。

## 记录Recorder

在创建 ExpControlRecorder 对象时，对 LabVIEW 实验控制的有效查询包括（代码setResponse部分）：

- 控制（命令）位移：ctrlDisp, ctrlDisplacement, ctrlDisplacements

- 控制（命令）力：ctrlForce, ctrlForces

- 数据采集（反馈）位移：daqDisp, daqDisplacement, daqDisplacements

- 数据采集（反馈）力：daqForce, daqForces

## 参考

Hubbard, P., Calderon, J., Gose, S. (2004). “Protocol Specification for the LabView NTCP plugin.” NEESit Technical Report (TR-2004-58).