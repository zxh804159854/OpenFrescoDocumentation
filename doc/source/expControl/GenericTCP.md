# GenericTCP 实验控制

### 命令

此命令用于构建 GenericTCP 实验控制对象。通用tcp传输，用于给实验设备发送命令。

<div class="definition">

expControl GenericTCP tag ipAddr ipPort -ctrlModes (5 mode) -daqModes (5 mode) \<-initFile fileName\> \<-ssl\> \<-udp\> \<-ctrlFilters (5 filterTag)\> \<-daqFilters (5 filterTag)\>

</div>

|             |                                                                                                                             |
|:------------|:----------------------------------------------------------------------------------------------------------------------------|
| \$tag       | 唯一控制标签                                                                                                                |
| ipAddr      | 控制器程序的 IP 地址                                                                                                        |
| \$ipPort    | 控制器程序的 IP 端口                                                                                                        |
| \$mode      | 控制和数据采集模式标志数组，对应（位移, 速度, 加速度, 力, 时间） (disp, vel, accel, force, time)                            |
| fileName    | 用于初始化控制器的附加参数 ASCII 文本文件（可选）                                                                           |
| \$filterTag | 先前定义的滤波器标签标识；滤波器标签标识大小为 5（条目：\[位移, 速度, 加速度, 力, 时间\]\[disp, vel, accel, force, time\]） |

### 示例

    expControlPoint 1  1 disp
    expControlPoint 2  1 disp 1 force
    #expControl SCRAMNetGT 1 4096 -trialCP 1 -outCP 2
    expControl GenericTCP 1 "127.0.0.1" 44000 -ctrlModes 1 0 0 0 0 -daqModes 1 0 0 1 0

说明

### 记录Recorder

在创建 ExpControlRecorder 对象时，对 GenericTCP 实验控制的有效查询包括（代码setResponse部分）：

- 控制（命令）位移：ctrlDisp, ctrlDisplacement, ctrlDisplacements

- 控制（命令）速度：ctrlVel, ctrlVelocity, ctrlVelocities

- 控制（命令）加速度：ctrlAccel, ctrlAcceleration, ctrlAccelerations

- 控制（命令）力：ctrlForce, ctrlForces

- 控制（命令）时间：ctrlTime, ctrlTimes

- 数据采集位移：daqDisp, daqDisplacement, daqDisplacements

- 数据采集（反馈）速度：daqVel, daqVelocity, daqVelocities

- 数据采集（反馈）加速度：daqAccel, daqAcceleration, daqAccelerations

- 数据采集（反馈）力：daqForce, daqForces

- 数据采集（反馈）时间：daqTime, daqTimes

### 参考

\[1\] Moustafa MA, Mosalam KM. Development of hybrid simulation system for multi-degree- of-freedom large-scale testing n.d. 6th International Conference on Advances in Experimental Structural Engineering 11th International Workshop on Advanced Smart Materials and Smart Structures Technology August 1-2, 2015, University of Illinois, Urbana-Champaign, United States

<http://www.dspaceinc.com/ww/en/inc/home/products/hw/singbord.cfm>
