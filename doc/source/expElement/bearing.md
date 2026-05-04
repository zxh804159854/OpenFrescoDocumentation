# bearing 支承实验单元
## 命令
此命令用于支座实验单元对象。

**bearing 2d（site）**
```tcl
expElement bearing eleTag iNode jNode pFrcCtrl -P matTag -Mz matTag -site siteTag -initStif Kij <-orient x1 x2 x3 y1 y2 y3> <-pDelta Mratios> <-shearDist sDratio> <-iMod> <-doRayleigh> <-mass m>
```

**bearing 2d（server）**
```tcl
expElement bearing eleTag iNode jNode pFrcCtrl -P matTag -Mz matTag -server ipPort <ipAddr> <-ssl> <-udp> <-dataSize size> -initStif Kij <-orient x1 x2 x3 y1 y2 y3> <-pDelta Mratios> <-shearDist sDratio> <-iMod> <-doRayleigh> <-mass m>
```

**bearing 3d（site）**
```tcl
expElement bearing eleTag iNode jNode pFrcCtrl -P matTag -T matTag -My matTag -Mz matTag -site siteTag -initStif Kij <-orient <x1 x2 x3> y1 y2 y3> <-pDelta Mratios> <-shearDist sDratio> <-iMod> <-doRayleigh> <-mass m>
```

**bearing 3d（server）**
```tcl
expElement bearing eleTag iNode jNode pFrcCtrl -P matTag -T matTag -My matTag -Mz matTag -server ipPort <ipAddr> <-ssl> <-udp> <-dataSize size> -initStif Kij <-orient <x1 x2 x3> y1 y2 y3> <-pDelta Mratios> <-shearDist sDratio> <-iMod> <-doRayleigh> <-mass m>
```

| 参数 | 说明 |
|:--- |:--- |
| $eleTag | 唯一单元标签 |
| $iNode, $jNode | 端节点标签 |
| $siteTag | 先前定义的站点对象的标签 |
| $Kij | 单元的初始刚度矩阵分量（按行排列） |
| -iMod | 使用Nakashima初始刚度修正法进行误差校正（可选，默认值为false） |
| -noRayleigh | 不考虑瑞雷阻尼（可选，默认值为考虑） |
| $rho1, $rho2 | 支撑腿的单位长度质量（可选，默认值为0.0） |
| $ipPort | 中间层服务器的IP端口 |
| ipAddr | 中间层服务器的IP地址（可选） |
| -ssl | 使用OpenSSL进行安全传输（可选） |
| $size | 发送的数据大小（可选） |
| -udp | 使用udp进行数据传输（默认是tcp/ip） |

## 示例

## 记录Recorder
在创建 ElementRecorder 对象时（参见 OpenSees 手册），对bearing实验单元的有效查询包括：
- 全局力：force, forces, globalForce, globalForces
  - 2d顺序：Px_1，Py_1，Mz_1，Px_2，Py_2，Mz_2
  - 3d顺序：Px_1，Py_1，Pz_1，Mx_1，My_1，Mz_1，Px_2，Py_2，Pz_2，Mx_2，My_2，Mz_2
- 局部力：localForce, localForces
  - 2d顺序：N_1，V_1，q_1，M_1，N_2，V_2，M_2
  - 3d顺序：N_1，Vy_1，Vz_1，T_1，My_1，Mz_1，N_2，Vy_2，Vz_2，T_2，My_2，Mz_2
- 基本力：basicForce, basicForces, daqForce, daqForces
  - 2d顺序：qb1，qb2，qb3
  - 3d顺序：qb1，qb2，qb3，qb4，qb5，qb6
- 局部位移：localDisp, localDisplacement,localDisplacements
  - 2d顺序：ux_1，uy_1，rz_1，ux_2，uy_2，rz_2
- 控制（命令）位移：defo, deformation, deformations, basicDefo, basicDeformation, basicDeformations, ctrlDisp, ctrlDisplacement, ctrlDisplacements
  - 2d顺序：db1，db2,db3
- 控制（命令）速度：ctrlVel, ctrlVelocity, ctrlVelocities
  - 2d顺序：vb1，vb2,vb3
- 控制（命令）加速度：ctrlAccel, ctrlAcceleration, ctrlAccelerations
  - 2d顺序：ab1，ab2,ab3
- 数据采集位移：daqDisp, daqDisplacement, daqDisplacements
  - 2d顺序：dbDaq1，dbDaq2,dbDaq3
- 数据采集（反馈）速度：daqVel, daqVelocity, daqVelocities
  - 2d顺序：vbDaq1，vbDaq2,vbDaq3
- 数据采集（反馈）加速度：daqAccel, daqAcceleration, daqAccelerations
  - 2d顺序：abDaq1，abDaq2,abDaq3
- 材料输出：material

## 参考