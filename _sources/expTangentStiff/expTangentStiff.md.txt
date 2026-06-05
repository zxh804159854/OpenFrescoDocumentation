# expTangentStiff 简介

这些命令用于构建实验expTangentStiff对象。主要由Hong Kim 实现。

下面内容来自于附录2的3.3.1 兼容性方法的实现

估计切线刚度矩阵的方法被实现为 ExperimentalTangentStiff 类的具体类。ETBroyden、ETBfgs、ETTranspose 和 ETIntrinisic 类分别在 OpenFresco 中部署了 Broyden、BFGS、Transpose 和 Intrinsic 方法。使 ExperimentalTangentStiff 成为一个单独的类而不是 ESFTangForceConverter 的子类，使 ExperimentalTangentStiff 更加通用。**这种解耦架构允许 ExperimentalElement 类使用切线刚度估计来估计实验单元的切线刚度矩阵。在 OpenFresco 的原始版本中，ExperimentalElement 类总是返回初始刚度矩阵（由用户提供），即使调用获取切线刚度矩阵的方法也是如此。使用切线刚度矩阵而不是初始刚度矩阵可以获得更好的结果。**

主要原理参考Kim, H.K., (2011). Development and implementation of advanced control methods for hybrid simulation. Ph.D. Dissertation, University of California, Berkeley, California.