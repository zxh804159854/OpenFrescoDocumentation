# beamColumn 实验单元

## 命令

此命令用于构建梁-柱实验单元对象。该单元由两个节点定义。

<div class="definition">

expElement beamColumn eleTag iNode jNode transTag -site siteTag -initStif Kij \<-iMod\> \<-noRayleigh\> \<-rho rho\> \<-cMass\>

</div>

注：从源代码看貌似支持\<-tangStif tangStifTag\>或者\<-tangStiff tangStifTag\>，在实验过程中使用切线刚度可以替换初始刚度。从其他代码看，这个参数一般在-initStif Kij后面。

<div class="definition">

expElement beamColumn eleTag iNode jNode transTag -server ipPort \<ipAddr\> \<-ssl\> \<-udp\> \<-dataSize size\> -initStif Kij \<-iMod\> \<-noRayleigh\> \<-rho rho\> \<-cMass\>

</div>

|                 |                                                                |
|:----------------|:---------------------------------------------------------------|
| \$eletag        | 唯一单元标签                                                   |
| \$iNode,\$jNode | 端节点标签                                                     |
| \$transTag      | 先前定义的坐标变换对象的标签                                   |
| \$siteTag       | 先前定义的站点对象的标签                                       |
| \$Kij           | 单元的初始刚度矩阵分量（按行排列）                             |
| -iMod           | 使用Nakashima初始刚度修正法进行误差校正（可选，默认值为false） |
| -noRayleigh     | 不考虑瑞雷阻尼（可选，默认值为考虑）                           |
| \$rho           | 单位长度质量（可选，默认值为0.0）                              |
| -cMass          | 用于形成一致质量矩阵（可选）                                   |
| \$ipPort        | 中间层服务器的IP端口                                           |
| ipAddr          | 中间层服务器的IP地址（可选）                                   |
| -ssl            | 使用OpenSSL进行安全传输（可选）                                |
| -udp            | 使用udp进行数据传输（默认是tcp/ip）                            |
| \$size          | 发送的数据大小（可选）                                         |

## 示例

    # 定义模型几何
    # 
    set mass 0.12
    # node $tag $xCrd $yCrd $mass
    node 1 0.0 0.00
    node 2 108.0 -54.00
    node 3 216.0 -42.00
    node 4 324.0 0.00
    node 5 0.0 0.00 -mass $mass $mass 116.6
    node 6 108.0 0.00 -mass $mass $mass 116.6
    node 7 216.0 0.00 -mass $mass $mass 116.6
    node 8 324.0 0.00 -mass $mass $mass 116.6
    node 9 108.0 0.00 -mass $mass $mass 116.6
    node 10 216.0 0.00 -mass $mass $mass 116.6 

    # 定义实验站点
    # -
    # expSite RemoteSite $tag <-setup $setupTag> $ipAddr $ipPort <$dataSize>
    expSite RemoteSite 1 "127.0.0.1" 8090
    expSite RemoteSite 2 "127.0.0.1" 8091

    # 定义几何变换
    #  
    # geomTransf type $tag  
    geomTransf Linear 1  
    geomTransf Corotational 2

    # 定义实验单元
    #  
    expElement beamColumn 2 2 9 1 -site 1 -initStif1213 0 0 0 11.2 -302.4 0 -302.4 10886.4

节点2和9连接上述二维梁-柱实验单元。使用线性坐标变换。该单元定义为远程实验站点，IP地址为"127.0.0.1"，端口号为8090。该单元的初始刚度矩阵为$\mathbf{K}_i$：

$$\mathbf{K}_{i} = \left[ \begin{array}{ccc} 
1213 & 0 & 0 \\ 
0 & 11.2 & -302.4 \\ 
0 & -302.4 & 10886.4 
\end{array} \right]$$

## 记录Recorder

在创建 ElementRecorder 对象时（参见 OpenSees 手册），对梁-柱实验单元的有效查询包括：

- 全局力：force, forces, globalForce, globalForces

- 局部力：localForce, localForces

- 基本力：basicForce, basicForces, daqForce, daqForces

- 控制（命令）位移：defo, deformation, deformations, basicDefo, basicDeformation, basicDeformations, ctrlDisp, ctrlDisplacement, ctrlDisplacements

- 控制（命令）速度：ctrlVel, ctrlVelocity, ctrlVelocities

- 控制（命令）加速度：ctrlAccel, ctrlAcceleration, ctrlAccelerations

- 控制（命令）力：ctrlForce, ctrlForces

- 控制（命令）时间：ctrlTime, ctrlTimes

- 数据采集位移：daqDisp, daqDisplacement, daqDisplacements

- 数据采集（反馈）速度：daqVel, daqVelocity, daqVelocities

- 数据采集（反馈）加速度：daqAccel, daqAcceleration, daqAccelerations

- 数据采集（反馈）力：daqForce, daqForces

- 数据采集（反馈）时间：daqTime, daqTimes

说明：除了全局力局部力，其他的变量都是在基本坐标系（basic system B）下。

## 初始刚度矩阵Kij

1、2D（对应ux，uy，rz）与有限元教材一致 $$K_{init} = \begin{bmatrix}
\dfrac{EA}{L} & 0 & 0 \\[15pt]
0 & \dfrac{12EI}{L^{3}} & -\dfrac{6EI}{L^{2}} \\[15pt]
0 & -\dfrac{6EI}{L^{2}} & \dfrac{4EI}{L}
\end{bmatrix}
\quad \text{对应分量：} \begin{bmatrix} u_{x} \\ u_{y} \\ R_{z} \end{bmatrix}$$ 2、 3D（对应ux，uy，rz，uz，ry，rx） 与有限元教材（ux，uy，uz，rx，ry，rz）不一致 $$\mathbf{K}_{init} = \begin{bmatrix}
\dfrac{EA}{L} & 0 & 0 & 0 & 0 & 0 \\[15pt]
0 & \dfrac{12EI_{z}}{L^{3}} & -\dfrac{6EI_{z}}{L^{2}} & 0 & 0 & 0 \\[15pt]
0 & -\dfrac{6EI_{z}}{L^{2}} & \dfrac{4EI_{z}}{L} & 0 & 0 & 0 \\[15pt]
0 & 0 & 0 & \dfrac{12EI_{y}}{L^{3}} & \dfrac{6EI_{y}}{L^{2}} & 0 \\[15pt]
0 & 0 & 0 & \dfrac{6EI_{y}}{L^{2}} & \dfrac{4EI_{y}}{L} & 0 \\[15pt]
0 & 0 & 0 & 0 & 0 & \dfrac{GJ}{L}
\end{bmatrix}
\quad \text{对应分量：} \begin{bmatrix} u_{x} \\ u_{y} \\ R_{z} \\ u_{z} \\ R_{y} \\ R_{x} \end{bmatrix}$$

## 参考

初始刚度修正参考文献 \[1\] Nakashima, M. and Kato, H. (1987). "Experimental error growth behavior and error growth controlling on-line computer test control method," Building Research Institute, BRI-Report No. 123, Ministry of Construction, Tsukuba, Japan.