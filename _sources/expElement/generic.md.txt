# generic 实验单元

## 命令

此命令用于构建通用实验单元对象。该单元由任意数量的节点及这些节点的自由度定义。

<div class="definition">

expElement generic eleTag -node Ndi -dof dofNdi -dof dofNdj ... -site siteTag -initStif Kij \<-iMod\> \<-noRayleigh\> \<-mass Mij\> \<-checkTime\>

</div>

<div class="definition">

expElement generic eleTag -node Ndi -dof dofNdi -dof dofNdj ... -server ipPort \<ipAddr\> \<-ssl\> \<-udp\> \<-dataSize size\> -initStif Kij \<-iMod\> \<-noRayleigh\> \<-mass Mij\> \<-checkTime\>

</div>

|                    |                                                                |
|:-------------------|:---------------------------------------------------------------|
| \$eletag           | 唯一单元标签                                                   |
| \$Ndi              | n个端节点标签（n = 节点数量）                                  |
| \$dofNdi, \$dofNdj | n个端节点的自由度                                              |
| \$siteTag          | 先前定义的站点对象的标签                                       |
| \$Kij              | 单元的初始刚度矩阵分量（按行排列）                             |
| -iMod              | 使用Nakashima初始刚度修正法进行误差校正（可选，默认值为false） |
| -noRayleigh        | 不考虑瑞雷阻尼（可选，默认值为考虑）                           |
| \$Mij              | 质量矩阵（可选，默认值为0.0）                                  |
| \$ipPort           | 中间层服务器的IP端口                                           |
| ipAddr             | 中间层服务器的IP地址（可选）                                   |
| -ssl               | 使用OpenSSL进行安全传输（可选）                                |
| -udp               | 使用udp进行数据传输（默认是tcp/ip）                            |

## 示例

    # 定义模型几何
    # 
    set mass3 0.04
    set mass4 0.02
    # node $tag $xCrd $yCrd $mass
    node 1 0.0 0.00
    node 2 100.0 0.00
    node 3 0.0 54.00 -mass $mass3 $mass3
    node 4 100.0 54.00 -mass $mass4 $mass4
    # 定义实验站点
    # 
    # expSite LocalSite $tag $setupTag
    expSite LocalSite 2 2 

    # 定义实验单元
    # expElement generic 1 -node 1 3 -dof 1 2 -dof 1 2 -site 2 
    #   -initStif 130 150 110 100 150 200 220 180 100 110 180 150 125 100 100 125 200 

节点1和3连接上述二维通用实验单元。每个节点使用平动自由度1和2。该单元使用本地实验站点定义。该单元的初始刚度矩阵为$\mathbf{K}_I$：

    130 150 110 100   
    150 220 180 100   
    110 180 150 125   
    100 100 125 200 

## 记录Recorder

在创建 ElementRecorder 对象时（参见 OpenSees 手册），对generic实验单元的有效查询包括：

- 全局力：force, forces, globalForce, globalForces

- 局部力（=goal）：localForce, localForces

- 基本力：basicForce, basicForces, daqForce, daqForces

- 控制（命令）位移：defo, deformation, deformations, basicDefo, basicDeformation, basicDeformations, ctrlDisp, ctrlDisplacement, ctrlDisplacements

- 控制（命令）速度：ctrlVel, ctrlVelocity, ctrlVelocities

- 控制（命令）加速度：ctrlAccel, ctrlAcceleration, ctrlAccelerations

- 控制（命令）力：ctrlForce, ctrlForces

- 控制（命令）时间：ctrlTime, ctrlTimes

- 数据采集（反馈）位移：daqDisp, daqDisplacement, daqDisplacements

- 数据采集（反馈）速度：daqVel, daqVelocity, daqVelocities

- 数据采集（反馈）加速度：daqAccel, daqAcceleration, daqAccelerations