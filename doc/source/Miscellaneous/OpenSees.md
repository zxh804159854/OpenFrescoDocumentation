# OpenSees建模命令
这部分命令用于基础建模，这与 OpenSees 中可用的命令相同。源代码位置SRC/interpreter/tcl/TclWrapper.cpp

包括下面命令
* model
* logFile
* metaData
* defaultUnits
* start
* stop
* node
* fix
* fixX
* fixY
* fixZ
* uniaxialMaterial
* geomTransf
* rayleigh
* setElementRayleighDampingFactors

## Basic Model Builder
此命令用于构造 BasicBuilder 对象。这与 OpenSees 中可用的命令相同。

```tcl
model BasicBuilder -ndm $ndm <-ndf $ndf>
```

| 参数 | 说明 |
|:----|:-----|
| $ndm | 模型维度（1、2 或 3） |
| $ndf | 节点的自由度数（可选）（默认值取决于 ndm 的值：ndm=1 -> ndf=1；ndm=2 -> ndf=3；ndm=3 -> ndf=6） |

## Basic Model Builder
此命令用于构造 BasicBuilder 对象。这与 OpenSees 中可用的命令相同。

```tcl
model BasicBuilder -ndm $ndm <-ndf $ndf>
```

| 参数 | 说明 |
|:----|:-----|
| $ndm | 模型维度（1、2 或 3） |
| $ndf | 节点的自由度数（可选）（默认值取决于 ndm 的值：ndm=1 -> ndf=1；ndm=2 -> ndf=3；ndm=3 -> ndf=6） |

### 示例：
```tcl
model BasicBuilder -ndm 2 -ndf 2
```

此示例创建一个具有两个维度和每个节点 2 个自由度的模型。

## Node 命令
此命令用于构造 Node 对象。它为 Node 对象分配坐标。这与 OpenSees 中可用的命令相同。

```tcl
node $nodeTag (ndm $coords)
```

| 参数 | 说明 |
|:----|:-----|
| $nodeTag | 标识节点的整数标签 |
| $coords | 节点坐标（ndm 个参数） |

**示例：**
```tcl
node 1 0.0 0.0
```

此示例在二维原点上创建标签为 1 的节点。
```tcl
model BasicBuilder -ndm 2 -ndf 2
```

此示例创建一个具有两个维度和每个节点 2 个自由度的模型。

## Node 命令
此命令用于构造 Node 对象。它为 Node 对象分配坐标。这与 OpenSees 中可用的命令相同。

```tcl
node $nodeTag (ndm $coords)
```

| 参数 | 说明 |
|:----|:-----|
| $nodeTag | 标识节点的整数标签 |
| $coords | 节点坐标（ndm 个参数） |

**示例：**
```tcl
node 1 0.0 0.0
```

此示例在二维原点上创建标签为 1 的节点。