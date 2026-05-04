# generic 实验单元
## 命令
构建通用实验单元，支持任意节点数与自由度。

**site模式**
```tcl
expElement generic eleTag -node Ndi -dof dofNdi -dof dofNdj ... -site siteTag -initStif Kij <-iMod> <-noRayleigh> <-mass Mij> <-checkTime>
```

**server模式**
```tcl
expElement generic eleTag -node Ndi -dof dofNdi -dof dofNdj ... -server ipPort <ipAddr> <-ssl> <-udp> <-dataSize size> -initStif Kij <-iMod> <-noRayleigh> <-mass Mij> <-checkTime>
```

| 参数 | 说明 |
|:--- |:--- |
| $eleTag | 唯一单元标签 |
| $Ndi | 端节点标签 |
| $dofNdi,$dofNdj | 节点自由度 |
| $siteTag | 站点标签 |
| $Kij | 初始刚度矩阵（按行） |
| -iMod | Nakashima修正（可选） |
| -noRayleigh | 关闭瑞雷阻尼（可选） |
| $Mij | 质量矩阵（可选） |
| 其余 | 同beamColumn |

## 示例
```tcl
# 定义模型几何
set mass3 0.04
set mass4 0.02
# node $tag $xCrd $yCrd $mass
node 1 0.0 0.00
node 2 100.0 0.00
node 3 0.0 54.00 -mass $mass3 $mass3
node 4 100.0 54.00 -mass $mass4 $mass4
# 定义实验站点
expSite LocalSite 2 2 
# 定义实验单元
expElement generic 1 -node 1 3 -dof 1 2 -dof 1 2 -site 2 -initStif 130 150 110 100 150 220 180 100 110 180 150 125 100 100 125 200
```

初始刚度矩阵：
$$
\mathbf{K}_{i} = \left[ \begin{array}{cccc}
130 &150 &110 &100\\   
150 &220 &180 &100 \\  
110 &180 &150 &125\\   
100 &100 &125 &200 \\
\end{array} \right]
$$

![通用实验单元](fig/generic.jpg)

## 记录Recorder
- 全局力：force, forces, globalForce, globalForces
- 局部力：localForce, localForces
- 基本力：basicForce, basicForces, daqForce, daqForces
- 控制位移/速度/加速度
- 数据采集位移/速度/加速度
