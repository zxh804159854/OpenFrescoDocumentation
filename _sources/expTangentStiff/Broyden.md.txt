# Broyden

使用 Broyden 方法来估计切线刚度矩阵。

## 命令

```tcl
expTangentStiff Broyden tag
```

下面内容来自于附录2的3.3.1 兼容性方法的实现:

**全局坐标系的更新公式：**[2]

$\Delta r_n$是增量力向量，$\Delta u_n$是增量位移向量。

$$
K_n=K_{n-1}+\frac{(\Delta r_n-K_{n-1}\Delta u_n)\Delta u_n^T}{\Delta u_n^T\Delta u_n}
$$


**在 actuator system：**

$\Delta \bar{u}_n$ 和 $\Delta \bar{f}_n$ 是系统在时间步 $n$ 时，实际坐标下的增量实测位移向量与力向量。

$$
K_n^{Act}=K_{n-1}^{Act}+\frac{(\Delta \bar f_n-K_{n-1}^{Act}\Delta \bar u_n)\Delta \bar u_n^T}{\Delta \bar u_n^T\Delta \bar u_n}
$$

## 示例

这个示例来自于OpenFresco/EXAMPLES/TrussModel
/Truss_Local.tcl

```tcl
# create ModelBuilder (with two-dimensions and 2 DOF/node)
model BasicBuilder -ndm 2 -ndf 2

# Load OpenFresco package
# -----------------------
# (make sure all dlls are in the same folder as openSees.exe)
loadPackage OpenFresco

# Define geometry for model
# -------------------------
# node $tag $xCrd $yCrd $mass
node 1   0.0  0.0
node 2 144.0  0.0
node 3 168.0  0.0
node 4  72.0 96.0

# set the boundary conditions
# fix $tag $DX $DY
fix 1 1 1 
fix 2 1 1
fix 3 1 1

# Define materials
# ----------------
set E 3000.0
set A3 5.0
set L3 [expr sqrt(pow(168.0-72.0,2.0) + pow(96.0,2.0))]
set kInit [expr $E*$A3/$L3]
# uniaxialMaterial Elastic $matTag $E
uniaxialMaterial Elastic 1 $E
#uniaxialMaterial Elastic 2 $kInit
uniaxialMaterial Steel01 2 50.0 $kInit 0.1

# Define experimental control
# ---------------------------
# expControl SimUniaxialMaterials $tag $matTags
expControl SimUniaxialMaterials 1 2

# Define experimental setup
# -------------------------
# expSetup OneActuator $tag <-control $ctrlTag> $dir -sizeTrialOut $t $o <-trialDispFact $f> ...
expSetup OneActuator 1 -control 1 1 -sizeTrialOut 1 1

# Define experimental site
# ------------------------
# expSite LocalSite $tag $setupTag
expSite LocalSite 1 1

# Define experimental tangent stiffness
# -------------------------------------
# expTangentStiff Broyden $tag
expTangentStiff Broyden 1
# expTangentStiff BFGS $tag <-eps $value>
#expTangentStiff BFGS 1
# expTangentStiff Transpose $tag $numCols
#expTangentStiff Transpose 1 1

# Define numerical elements
# -------------------------
# element truss $eleTag $iNode $jNode $A $matTag
element truss 1 1 4 10.0 1
element truss 2 2 4  5.0 1
#element corotTruss 1 1 4 10.0 1
#element corotTruss 2 2 4  5.0 1

# Define experimental element
# ---------------------------
# expElement truss $eleTag $iNode $jNode -site $siteTag -initStif $Kij <-tangStif tangStifTag> <-iMod> <-rho $rho> 
expElement truss 3 3 4 -site 1 -initStif $kInit -tangStif 1
#expElement corotTruss 3 3 4 -site 1 -initStif $kInit -tangStif 1
```

## 参考

[1]Kim, H.K., (2011). Development and implementation of advanced control methods for hybrid simulation. Ph.D. Dissertation, University of California, Berkeley, California.

[2] J.E. Carrion and B.F. Spencer. Model-based strategies for real-time hybrid testing. In ASCE  Structure Congress, Seattle, WA, 2003.