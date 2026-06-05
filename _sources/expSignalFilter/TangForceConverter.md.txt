# TangentForceConverter 实验信号滤波器

新增命令，是用于Force控制使用。

下面内容来自于附录2的3.3.1 兼容性方法的实现

ESFTangForceConverter 类使用切线刚度矩阵将位移转换为力。ESFTangForceConverter 构造函数以 int tag（唯一标签）、Matrix& initStif（对初始切线刚度矩阵的引用）和 ExperimentalTangentStiff $^ *$ tangStif（指向 ExperimentalTangentStiff 的指针）作为参数。int tag 和 Matrix& initStif 由用户提供。它使用 ExperimentalTangentStiff 类来估计试件的切线刚度矩阵。ESFTangForceConverter 对象必须有一个 ExperimentalTangentStiff 对象。ESFTangForceConverter 的 converting (Vector∗ td , Vector $^ *$ df) 方法在将 $\bar {  { \mathbf { u } } } _ { n }$ 转换为 ${ \bar { \pmb f } } _ { n }$ 之前调用 updateTangentStiff 方法，使用测量的位移-力对更新切线刚度矩阵。ESFTangForceConverter 类使用方程 3.11 将变形转换为力。

ESFTangForceConverter 和 ESFKrylovForceConverter 具有防止噪声引起虚假更新的过滤器。增量测量位移和力向量在 ESFTangConverter 的 updateIncreMat 方法中被过滤，防止对切线刚度矩阵进行不必要的更新。在 ESFKrylovForceConverter 中，增量测量位移和力向量的过滤确保来自控制系统的噪声不会填充 Krylov 子空间。这些过滤器采用测量对向量的 1-范数或 2-范数。如果这些范数都大于用户定义的限值，则进行更新。

## 命令
```tcl
expSignalFilter TangentForceConverter tag -initStif Kij -tangStif tangStifTag
```

| 参数 | 说明 |
|:----|:-----|
| $tag | 唯一实验信号滤波器标签 |

## 参考

[1]Kim, H.K., (2011). Development and implementation of advanced control methods for hybrid simulation. Ph.D. Dissertation, University of California, Berkeley, California.