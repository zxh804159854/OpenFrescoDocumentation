# SimDomain 实验控制

## 命令

此命令用于构建仿真域（Simulation Domain）实验控制对象。SimDomain 命令在 OpenFresco 中提供完整的 OpenSees 域，包括材料、截面和单元库。

这使得使用 OpenSees 模拟实际实验试件成为可能。它可用于测试计算模型、实验设置和网络通信，以确保在进行实际实验之前，混合仿真的所有非实验方面都能正常运行。此命令必须与 expControlPoint 命令配合使用。

<div class="definition">

expControl SimDomain tag -trialCP cpTags -outCP cpTags \<-ctrlFilters (5 \$filterTag)\> \<-daqFilters (5 \$filterTag)\>

</div>

|             |                                                                                                                             |
|:------------|:----------------------------------------------------------------------------------------------------------------------------|
| \$tag       | 唯一控制标签                                                                                                                |
| \$cpTags    | 先前定义的控制点标签                                                                                                        |
| \$filterTag | 先前定义的滤波器标签标识；滤波器标签标识大小为 5（条目：\[位移, 速度, 加速度, 力, 时间\]\[disp, vel, accel, force, time\]） |

## 示例

    # 定义材料
    # _____________
    # uniaxialMaterial Steel02 $matTag $Fy $E $b $R0 $cR1 $cR2 $a1 $a2 $a3 $a4
    uniaxialMaterial Elastic 1 [expr 2.26*29000]
    uniaxialMaterial Steel02 2 [expr 1.5*54] 146966.4 0.01 18.5 0.925 0.15 0.0 1.0 0.0 1.0

    # 定义截面
    # _____________
    # section Aggregator $secTag $matTag1 $string1 $matTag2 $string2
    section Aggregator 2 1 P 2 Mz

    # 定义坐标变换
    # _____________
    # geomTransf Linear $transfTag
    geomTransf Linear 1

    # 定义单元
    # _____________
    # element nonlinearBeamColumn $eleTag $iNode $jNode $numIntgrPts $secTag $transfTag
    element nonlinearBeamColumn 1 1 2 5 2 1

    # 定义控制点
    # _____________
    # expControlPoint tag nodeTag dir resp <-fact f> <-lim 1 u> ...
    expControlPoint 1 2 ux disp uy disp rz disp
    expControlPoint 2 2 ux disp ux force uy disp uy force rz disp rz force

    # 定义实验控制
    # _____________
    # expControl SimDomain $tag -trialCP cpTags -outCP cpTags
    expControl SimDomain 1 -trialCP 1 -outCP 2

上述示例使用标签为 1 的试件控制点和标签为 2 的输出控制点。试件控制点发送 OpenSees 中定义的非线性梁柱单元节点 2 在 ux、uy 和 rz 方向的位移。控制点 2 在同一节点测量 ux、uy 和 rz 方向的位移和力。有关 expControlPoint 命令的详细说明，请参阅本手册第 7 章。

<figure>
<img src="image/ch01/SimDomain.jpg" style="width:80.0%" />
<figcaption>SimDomain 实验控制</figcaption>
</figure>

## 记录Recorder

在创建 ExpControlRecorder 对象时，对 SimDomain 实验控制的有效查询包括（代码setResponse部分）：

- 控制（命令）位移：ctrlDisp, ctrlDisplacement, ctrlDisplacements

- 控制（命令）速度：ctrlVel, ctrlVelocity, ctrlVelocities

- 控制（命令）加速度：ctrlAccel, ctrlAcceleration, ctrlAccelerations

- 控制（命令）力：ctrlForce, ctrlForces

- 数据采集位移：daqDisp, daqDisplacement, daqDisplacements

- 数据采集（反馈）速度：daqVel, daqVelocity, daqVelocities

- 数据采集（反馈）加速度：daqAccel, daqAcceleration, daqAccelerations

- 数据采集（反馈）力：daqForce, daqForces

## 参考

<https://openfresco.berkeley.edu/>