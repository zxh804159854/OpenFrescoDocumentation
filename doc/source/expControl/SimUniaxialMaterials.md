# SimUniaxialMaterials 实验控制

## 命令

此命令用于构建 SimUniaxialMaterials 实验控制对象。它可用于使用 1 至 n 个 OpenSees 单轴材料模型模拟具有 1 至 n 个非耦合自由度的试件。由于材料模型模拟的是给定作动器位移下 1 至 n 个作动器载荷传感器将测量的力，因此指定材料值的单位为力和位移，而非应力和应变。

<div class="definition">

expControl SimUniaxialMaterials tag matTags \<-ctrlFilters (5 \$filterTag)\> \<-daqFilters (5 \$filterTag)\>

</div>

|             |                                                                                                                             |
|:------------|:----------------------------------------------------------------------------------------------------------------------------|
| \$tag       | 唯一控制标签                                                                                                                |
| \$matTag    | 先前定义的单轴材料标签                                                                                                      |
| \$filterTag | 先前定义的滤波器标签标识；滤波器标签标识大小为 5（条目：\[位移, 速度, 加速度, 力, 时间\]\[disp, vel, accel, force, time\]） |

## 示例

    uniaxialMaterial Elastic 2 5.6
    expControl SimUniaxialMaterials 1 2

上述示例命令使用标签为 2、刚度为 5.6 的 OpenSees 单轴弹性材料模型。OpenSees 命令语言手册包含所有可用单轴材料模型的完整列表。

<figure>
<img src="image/ch01/SimUniaxialMaterials.jpg" style="width:80.0%" />
<figcaption>SimUniaxialMaterials 实验控制</figcaption>
</figure>

## 记录Recorder

在创建 ExpControlRecorder 对象时，对 SimUniaxialMaterials 实验控制的有效查询包括（代码setResponse部分）：

- 控制（命令）信号：ctrlSig, ctrlSignal, ctrlSignals

- 数据采集（反馈）信号：daqSig, daqSignal, daqSignals

## 参考

<http://www.dspaceinc.com/ww/en/inc/home/products/hw/singbord.cfm>